import time
import random
import pyautogui
from services.helper import helper
from modules.chatting import ai

# Overwrite this with window size
chatCoordinates = (1040, 720, 1450, 900)
chatName = "chat_cropped.png"

def chat(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            time.sleep(5)
            printx("Screen monitoring..")
            hasBeenWhispered = helper.isImageVisableOnScreen('assets/chat/whisper_from.png', 0.9)                
            if hasBeenWhispered:
                printx("Whisper detected..")
                isChatting = selfSet(True, shared_variables)

                # Text recognition
                helper.takeGameScreenshotCropped(chatName, chatCoordinates)
                chatText = helper.getTextFromImage(chatName)

                # AI
                response = ai.chatgptRequest(chatText)

                # Answer
                x, y, width, height = hasBeenWhispered
                helper.clickAt(x, y, mouseButton='right')
                whisperTo = helper.isImageVisableOnScreen('assets/chat/whisper_button.png', 0.9)
                if whisperTo:
                    x, y, width, height = whisperTo
                    helper.clickAt(x, y)
                    x = helper.isImageVisableOnScreen('assets/chat/whisper_button_x.png', 0.9)
                    if x:
                        x, y, width, height = x
                        helper.clickAt(x+5, y+5)
                        chatField = helper.isImageVisableOnScreen('assets/chat/chat_entry.png', 0.9)
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
                else:
                    helper.printe("")


def selfSet(value, shared):
    shared["isChatting"].value = value
    return value

def printx(str):
    print(f"(Chatter): {str}")

