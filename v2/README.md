# Version 2: Chatting with Goose via Curl Requests

This version sets up a Flask server that allows you to interact with the Goose AI agent using curl requests.

Key files:

*   `Dockerfile`: Defines the steps to build the Docker image, including installing Python, Flask, and Goose. It also sets the API key (replace the placeholder with your actual key).
*   `config.yaml`: Contains the configuration for Goose.
*   `server.py`: Implements the Flask server with a `/chat` endpoint that receives user input via POST requests, sends it to Goose, and returns the response.
*   `test.py`: (Likely) Contains tests for the server.

To run this version:

1.  Build the Docker image: `docker build -t goose-v2 .`
2.  Run the Docker container, mapping port 8000: `docker run -p 8000:8000 goose-v2`
3.  Send a curl request to the server: `curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, Goose!"}' http://localhost:8000/chat`

**Important:**

*   Replace `REPLACE_WITH_YOUR_API_KEY` in the `Dockerfile` with your actual Google API key.
*   The server runs on port 8000.
