# Version 3: Interactive Chat Interface with Goose

This version provides a chat-like interface for interacting with the Goose AI agent. It includes a Flask server and a client script for sending messages.

Key files:

*   `Dockerfile`: Defines the steps to build the Docker image, including installing Python, Flask, and Goose.  It also sets the API key (replace the placeholder with your actual key).
*   `config.yaml`: Contains the configuration for Goose.
*   `server.py`: Implements the Flask server with a `/chat` endpoint that manages a Goose session, receives user input, sends it to Goose, and returns the response. It uses subprocesses and queues for handling the Goose process.
*   `client.py`: A simple Python client that sends messages to the server and displays the responses.

To run this version:

1.  Build the Docker image: `docker build -t goose-v3 .`
2.  Run the Docker container, mapping port 8000: `docker run -p 8000:8000 goose-v3`
3.  Run the client: `python client.py` (This assumes the server is running on localhost:8000)

**Important:**

*   Replace `REPLACE_WITH_YOUR_API_KEY` in the `Dockerfile` with your actual Google API key.
*   The server runs on port 8000.
*   The client connects to the server at `http://localhost:8000/chat`.
*   The server manages a persistent Goose session, improving efficiency for multiple interactions.
