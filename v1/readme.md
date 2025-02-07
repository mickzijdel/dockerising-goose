# Version 1: Goose in Docker

This version demonstrates running the Goose AI agent within a Docker container.

Key files:

*   `Dockerfile`: Defines the steps to build the Docker image, including installing dependencies, configuring Goose, and setting the API key (replace the placeholder with your actual key).
*   `config.yaml`: Contains the configuration for Goose, specifying the provider (Google), the model (gemini-2.0-flash-exp), and enabling the developer extension.

To run this version:

1.  Build the Docker image: `docker build -t goose-v1 .`
2.  Run the Docker container: `docker run -it goose-v1`

**Important:** Replace `REPLACE_WITH_YOUR_API_KEY` in the `Dockerfile` with your actual Google API key.
