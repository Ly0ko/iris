import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

headers = {"Authorization": f"Bearer {api_key}"}


def count_tokens(text):
    return len(text.split())


def get_gpt3_response(messages):
    current_token_count = sum(count_tokens(
        message["content"]) for message in messages)

    if current_token_count >= 4000:
        print("Token limit reached. Popping the second message.")
        messages.pop(1)
        current_token_count = sum(count_tokens(
            message["content"]) for message in messages)

    if current_token_count >= 4000:
        raise ValueError(
            "Token count still too high after removing the second message.")

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=data,
        headers=headers,
    )

    response.raise_for_status()
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"].strip()
