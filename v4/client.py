import requests

def main():
    url = "http://localhost:8000/chat"
    headers = {"Content-Type": "application/json"}

    while True:
        user_input = input("Enter your message (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        payload = {"message": user_input}

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"Response: {response.json().get('response')}")
            else:
                print(f"Error: {response.json().get('error')}")
        except requests.exceptions.ConnectionError:
            print("Could not connect to server. Is it running?")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 