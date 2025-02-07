import requests
import logging

logging.basicConfig(level=logging.DEBUG)

def test_endpoint():
    url = "http://localhost:5000/chat"
    payload = {"message": "test message"}
    headers = {"Content-Type": "application/json"}
    
    try:
        # First try the health check
        health_response = requests.get("http://localhost:5000/")
        print(f"Health check response: {health_response.text}")
        
        # Then try the chat endpoint
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Is it running?")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_endpoint()