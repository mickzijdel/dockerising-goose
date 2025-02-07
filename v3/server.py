from flask import Flask, request, jsonify
import subprocess
import logging
import sys
import re
import atexit
import time
import threading
import queue

# Set up logging to output to both file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('server.log')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables
goose_process = None
response_queue = queue.Queue()

def read_output(pipe, queue):
    """Read output from pipe and put it in queue"""
    for line in pipe:
        queue.put(line.strip())

def initialize_goose_session():
    """Initialize a new Goose session and return the process object"""
    global goose_process
    logger.info("Initializing new Goose session...")
    try:
        goose_process = subprocess.Popen(
            ["goose", "session"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Start threads to read stdout and stderr
        threading.Thread(target=read_output, args=(goose_process.stdout, response_queue), daemon=True).start()
        threading.Thread(target=read_output, args=(goose_process.stderr, response_queue), daemon=True).start()
        
        # Clear initial startup messages
        time.sleep(2)
        while not response_queue.empty():
            response_queue.get()
        
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Goose session: {str(e)}", exc_info=True)
        return False

def cleanup_goose_session():
    """Cleanup function to properly terminate the Goose session"""
    global goose_process
    if goose_process:
        logger.info("Cleaning up Goose session...")
        try:
            goose_process.terminate()
            goose_process.wait(timeout=5)
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
            goose_process.kill()
        finally:
            goose_process = None

# Register cleanup function to run on server shutdown
atexit.register(cleanup_goose_session)

def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

@app.route("/", methods=["GET"])
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    global goose_process
    logger.info("Chat endpoint called")
    
    try:
        # Initialize session if not already running
        if not goose_process or goose_process.poll() is not None:
            if not initialize_goose_session():
                return jsonify({"error": "Failed to initialize Goose session"}), 500

        user_input = request.json.get("message")
        if not user_input:
            logger.warning("No message provided in request")
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Sending message to Goose: {user_input}")
        
        # Clear any existing messages in the queue
        while not response_queue.empty():
            response_queue.get()
        
        # Send input to Goose
        goose_process.stdin.write(f"{user_input}\n")
        goose_process.stdin.flush()
        
        # Wait for and collect response
        time.sleep(2)  # Give time for response to generate
        
        response_lines = []
        timeout = time.time() + 10  # 10 second timeout
        
        while time.time() < timeout:
            try:
                line = response_queue.get_nowait()
                if line and not any(x in line for x in ["starting session", "logging to", "Goose is running"]):
                    response_lines.append(line)
                if "Closing session" in line:
                    break
            except queue.Empty:
                if response_lines:  # If we have some response, consider it complete
                    break
                time.sleep(0.1)  # Small delay before next check
        
        response_text = "\n".join(response_lines)
        logger.info(f"Received response from Goose: {response_text}")
        
        if not response_text:
            return jsonify({"error": "No response received from Goose"}), 500
            
        return jsonify({"response": clean_ansi_codes(response_text)})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        cleanup_goose_session()  # Cleanup on error
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    if initialize_goose_session():
        logger.info("Server will be available at http://0.0.0.0:8000")
        app.run(debug=False, host="0.0.0.0", port=8000)
    else:
        logger.error("Failed to start Goose session, server startup aborted")
        sys.exit(1)