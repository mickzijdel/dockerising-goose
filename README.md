# Goose Docker App with Chat Interface

This repository contains a Dockerized application that allows you to interact with the Goose AI agent, using the Gemini LLM. It includes several versions, demonstrating different approaches to setting up and interacting with Goose.

## Project Overview

This project evolved through the following stages:

*   **Version 1 (v1): Goose in Docker**
    *   Demonstrates running the Goose AI agent within a Docker container.
    *   Key files:
        *   `Dockerfile`: Defines the steps to build the Docker image, including installing dependencies, configuring Goose, and setting the API key (replace the placeholder with your actual key).
        *   `config.yaml`: Contains the configuration for Goose, specifying the provider (Google), the model (gemini-2.0-flash-exp), and enabling the developer extension.
    *   To run this version:
        1.  Build the Docker image: `docker build -t goose-v1 .`
        2.  Run the Docker container: `docker run -it goose-v1`
    *   **Important:** Replace `REPLACE_WITH_YOUR_API_KEY` in the `Dockerfile` with your actual Google API key.

*   **Version 2 (v2): Chatting with Goose via Curl Requests**
    *   Sets up a Flask server that allows you to interact with the Goose AI agent using curl requests.
    *   Key files:
        *   `Dockerfile`: Defines the steps to build the Docker image, including installing Python, Flask, and Goose. It also sets the API key (replace the placeholder with your actual key).
        *   `config.yaml`: Contains the configuration for Goose.
        *   `server.py`: Implements the Flask server with a `/chat` endpoint that receives user input via POST requests, sends it to Goose, and returns the response.
        *   `test.py`: (Likely) Contains tests for the server.
    *   To run this version:
        1.  Build the Docker image: `docker build -t goose-v2 .`
        2.  Run the Docker container, mapping port 8000: `docker run -p 8000:8000 goose-v2`
        3.  Send a curl request to the server: `curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, Goose!"}' http://localhost:8000/chat`
    *   **Important:**
        *   Replace `REPLACE_WITH_YOUR_API_KEY` in the `Dockerfile` with your actual Google API key.
        *   The server runs on port 8000.

*   **Version 3 (v3): Interactive Chat Interface with Goose**
    *   Provides a chat-like interface for interacting with the Goose AI agent. It includes a Flask server and a client script for sending messages.
    *   Key files:
        *   `Dockerfile`: Defines the steps to build the Docker image, including installing Python, Flask, and Goose.  It also sets the API key (replace the placeholder with your actual key).
        *   `config.yaml`: Contains the configuration for Goose.
        *   `server.py`: Implements the Flask server with a `/chat` endpoint that manages a Goose session, receives user input, sends it to Goose, and returns the response. It uses subprocesses and queues for handling the Goose process.
        *   `client.py`: A simple Python client that sends messages to the server and displays the responses.
    *   To run this version:
        1.  Build the Docker image: `docker build -t goose-v3 .`
        2.  Run the Docker container, mapping port 8000: `docker run -p 8000:8000 goose-v3`
        3.  Run the client: `python client.py` (This assumes the server is running on localhost:8000)
    *   **Important:**
        *   Replace `REPLACE_WITH_YOUR_API_KEY` in the `Dockerfile` with your actual Google API key.
        *   The server runs on port 8000.
        *   The client connects to the server at `http://localhost:8000/chat`.
        *   The server manages a persistent Goose session, improving efficiency for multiple interactions.

## Configuration and Setup

*   **LLM:** This project uses the Gemini LLM (Language Model) with the Goose AI agent.
*   **API Key:** You need a Google API key to use the Gemini LLM. Replace the `REPLACE_WITH_YOUR_API_KEY` placeholder in the `Dockerfile` of each version with your actual API key.
*   **Goose Configuration Trick:** Goose doesn't natively support silent configuration. To work around this, the Dockerfiles in this project use a trick where Goose is installed silently, and then an existing `config.yaml` file is copied over to configure Goose. This allows for a fully automated setup within the Docker container.

## .gitignore

A `.gitignore` file has been added to the repository to exclude unnecessary files from being committed, such as:

*   Python bytecode files (`*.pyc`, `*.pyd`, `__pycache__/`)
*   Virtual environment directories (`.venv/`, `venv/`, `env/`)
*   Docker logs (`*.log`)
*   Operating system-specific files (`.DS_Store`, `Thumbs.db`)
*   Temporary files (`*.swp`, `*.swo`, `*~`, `*.bak`, `*.orig`, `tmp/`, `temp/`)

## Next Steps

*   Implement proper logging using a library like `logging` in Python.
*   Implement comprehensive error handling.
*   Consider using asynchronous tasks in v3 to improve server responsiveness.
*   Implement authentication and authorization for the chat interface.
*   Explore using WebSockets for a real-time chat experience.