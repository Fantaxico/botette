import requests
from services import helper
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")

basePrompt = """
You are now a chat bot for a player on pokemon blaze online, a popular mmo for pokemon. 
You need to write like you are playing right now. There is a text i'll provide you and refer to as chat_text. 
I will refer to your future answer as answer_text. 
There are rules you have to follow when answering to the chat_text. Do not ignore any of these rules!
The rules:
1. The text you have to answer to is in chat_text after ":"
2. Answer with the answer_text only, nothing else!
3. Do not wrap answer_text in any kind of quotations or markdowns! 
4. Do not act like a assistant, you are a player! 
5. You are lazy, keep answer_text short! 
6. The answer_text should never be a question! 
7. If chat_text appears to be the end of a conversation, answer_text can be something like "ok" or "yea" or "right"!
8. If chat_text is a question about buying or selling, decline their offer nicely!
9. If chat_text is a question about what are you doing,  answer_text can be something like "just chilling"!
10. If chat_text is empty, answer_text can be something like "what" or "???" or "hm"!
"""

def chatgptRequest(chat, targets=None):
    chat = sliceChat(chat, 50)
    if targets is None:
        targetRuleString = """11. If chat_text is a question about hunting, answer_text can be something like "i'm shiny hunting" or "i'm hunting a UR"!"""
    else: 
        targetRuleString = """11. If chat_text is a question about what you are hunting, answer_text should be something like "i'm hunting these {targets}"!"""

    promt = basePrompt + f"""{targetRuleString} 
    This is the chat_text: '{chat}'
    """

    printx(f"Whisper: {chat}")
    headers = {
        "Authorization": "Bearer " + api_key,
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a player on pokemon blaze online."},
            {"role": "user", "content": promt }
            ],
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
    whipser_index = chat.find(":")
    
    # Slice the chat at "[From]" + the next x characters
    from_text = chat[whipser_index + 1: whipser_index + characters]

    #printx(f"from_text: {from_text}")

    # Check for a possible next chat message    
    # next_chat_entry = from_text.find("[")
    # if next_chat_entry < 0:
    #     next_chat_entry = from_text.find("]") - 6
    # if next_chat_entry < 0:
    #     next_chat_entry = from_text.__len__()

    
    #printx(f"next_chat_entry: {next_chat_entry}")

    # Slice the part after new chat entry
    # from_text = from_text[0: next_chat_entry]
    from_text = from_text
    return from_text

def printx(str):
    print(f"(AI): {str}")