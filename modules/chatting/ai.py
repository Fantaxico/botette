import requests
from services import helper
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")

basePrompt = 'I have a text. I will refer to this text as chat_text. I will refer to your answer as answer_text. There are rules you have to follow. Do not ignore any of these rules. The rules: 1. Answer to message_text like a conversation!  2. Do not wrap answer_text in any kind of quotations, markdowns or other text! 3. Answer with the answer_text only nothing else! 4. The text you have to answer to is after in the chat_text after ":" 5. Act like a Pokemon Player on Pokemon Blaze Online never like a chat assistant! 6. You are lazy, answer_text should be short but modern! 7. answer_text should never be a question! 8. If chat_text does not contain a question, answer with something simple like "ok" or "yea"! Here are some examples:  chat_text: " Player1: how are you ?" answer_text: "good" or  chat_text: "Luciaeex: hi" answer_text: "hey" or chat_text: " Fantaxxxx: what nature is the pokemon ?" answer_text: "mature" or chat_text: " IDana: you sell shards ?" answer_text: "no" or chat_text: "Kaptr: are you shiny tracking ?" answer_text: "no just chilling" or chat_text: "Cappe: ok" answer_text: "yea". This is the chat_text: '
def chatgptRequest(chat):
    chat = sliceChat(chat, 50)
    printx(f"Whisper: {chat}")
    headers = {
        "Authorization": "Bearer " + api_key,
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": basePrompt + chat}],
        "temperature": 0.7,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    if response.status_code != 200:
        raise Exception(f"ChatGPT request failed with status code {response.status_code}")

    #printx(response.json())
    printx(f"Answer: {response.json()["choices"][0]["message"]["content"]}")


    return response.json()["choices"][0]["message"]["content"]

def sliceChat(chat, characters):
    # Find the Whisper
    whipser_index = chat.find("[From]")
    
    # Slice the chat at "[From]" + the next x characters
    from_text = chat[whipser_index + 6: whipser_index + characters]

    #printx(f"from_text: {from_text}")

    # Check for a possible next chat message    
    next_chat_entry = from_text.find("[")
    if next_chat_entry < 0:
        next_chat_entry = from_text.find("]") - 6
    if next_chat_entry < 0:
        next_chat_entry = from_text.__len__()

    
    #printx(f"next_chat_entry: {next_chat_entry}")

    # Slice the part after new chat entry
    from_text = from_text[0: next_chat_entry]
    return from_text

def printx(str):
    print(f"(AI): {str}")