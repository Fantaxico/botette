import time
import random
import pyautogui
from services import helper
from modules.chatting import ai

# Overwrite this with window size
chat_coordinates = (1040, 720, 1450, 900)

def chat(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            time.sleep(5)
            printx("Screen monitoring..")
            hasBeenWhispered = helper.isImageVisable('assets/chat/whisper_from.png', 0.9)
            friendRequest = helper.isImageVisable('assets/general/friend.png', 0.9)
            if friendRequest:
                x, y, width, height = friendRequest
                helper.clickAt(x, y)
                time.sleep(0.5)
                
            if hasBeenWhispered:
                printx("Whisper detected..")
                isChatting = selfSet(True, shared_variables)

                # Text recognition
                helper.takeGameScreenshotCropped(chat_coordinates)
                chatText = helper.textFromImage("game_cropped.png")

                # AI
                response = ai.chatgptRequest(chatText)

                # Answer
                x, y, width, height = hasBeenWhispered
                helper.clickAt(x, y, mouseButton='right')
                whisperTo = helper.isImageVisable('assets/chat/whisper_text.png', 0.9)
                if whisperTo:
                    x, y, width, height = whisperTo
                    helper.clickAt(x, y)
                    time.sleep(0.5)
                    x = helper.isImageVisable('assets/general/x.png', 0.9)
                    if x:
                        x, y, width, height = x
                        helper.clickAt(x+5, y+5)
                        chatField = helper.isImageVisable('assets/chat/chat_entry.png', 0.9)
                        if chatField:
                            time.sleep(1)
                            x, y, width, height = chatField
                            printx("Sending Message..")
                            helper.clickAt(x, y)
                            sendMessage(response)
                            time.sleep(1)
                            helper.clickAt(x, y)
                            sendMessage("/clear")
                            time.sleep(1)
                        
                            # Clear chat input
                            pyautogui.moveTo(x, y - 30)
                            pyautogui.click()

                            printx("Message sent")
                            isChatting = selfSet(False, shared_variables)


def selfSet(value, shared):
    shared["isChatting"].value = value
    return value

def sendMessage(text):
    pyautogui.write(text)
    helper.press("ENTER", 0.1, 0.5)

def printx(str):
    print(f"(Chatter): {str}")

