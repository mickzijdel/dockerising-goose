from flask import Flask, request, jsonify
import subprocess
import logging
import sys

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

@app.route("/", methods=["GET"])
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    logger.info("Chat endpoint called")
    try:
        user_input = request.json.get("message")
        if not user_input:
            logger.warning("No message provided in request")
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Received message: {user_input}")

        process = subprocess.Popen(
            ["goose", "session"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=user_input + "\n")
        
        if process.returncode != 0:
            logger.error(f"Goose process error: {stderr}")
            return jsonify({"error": "Internal process error", "details": stderr}), 500

        logger.info(f"Successfully processed message, response: {stdout.strip()}")
        return jsonify({"response": stdout.strip()})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    logger.info("Server will be available at http://0.0.0.0:8000")
    app.run(debug=True, host="0.0.0.0", port=8000)