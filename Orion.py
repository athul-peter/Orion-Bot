import openai
import requests
import logging
import os

# Replace the placeholder with your own OpenAI API Key
openai.api_key = "Place_Your_open_API_Key_here"

# Set up a logger to help debug any issues with the API requests
logging.basicConfig(level=logging.DEBUG)

def generate_response(prompt):
            completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
    )

    message = completions.choices[0].text
    return message

# Replace the placeholder with your own Telegram bot API Key
BOT_TOKEN = "Place_your_Telegram_BOT_Token"

# Set up the base URL for sending messages and receiving updates
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    if offset:
        url += f"?offset={offset}"
    result = requests.get(url).json()
    return result

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    result = requests.post(url, json=data).json()
    return result

def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            response = generate_response(prompt=text)
            send_message(chat_id=chat_id, text=response)
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(offset=last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = updates["result"][-1]["update_id"] + 1
            handle_updates(updates)

if __name__ == '__main__':
    main()
