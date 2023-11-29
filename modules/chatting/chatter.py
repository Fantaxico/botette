import time
import random
import pyautogui
import os
from services.helper import helper
from modules.chatting import ai
from dotenv import load_dotenv
load_dotenv()

assetsDir = os.getenv("ASSET_DIR")
workingDir = os.getenv("WORKING_DIR")

#(left, upper, right, lower)
chatCoordinates = (1520, 830, 1920, 1030)


def chat(shared_variables):
    chatImagePath = f"{workingDir}/chat_cropped.png"
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            time.sleep(1)
            printx("Screen monitoring..")
            hasBeenWhispered = helper.isImageVisableOnScreen(f'{assetsDir}/chat/whisper_from.png', 0.9)                
            if hasBeenWhispered:
                printx("Whisper detected..")
                isChatting = selfSet(True, shared_variables)
                # Answer
                x, y, width, height = hasBeenWhispered

                # Text recognition
                helper.takeGameScreenshot(chatImagePath, (x+50, y+7, x+400, y+20), greyscaleOptions={
                    "use": True, 
                    "basewidth": 900
                })
                
                chatText = helper.getTextFromImage(chatImagePath)
                print("Chat:" + chatText)

                # AI
                response = ai.chatgptRequest(chatText)

                helper.clickAt(x, y, mouseButton='right')
                whisperTo = helper.isImageVisableOnScreen(f'{assetsDir}/chat/whisper_button.png', 0.9)
                if whisperTo:
                    x, y, width, height = whisperTo
                    helper.clickAt(x, y)
                    x = helper.isImageVisableOnScreen(f'{assetsDir}/chat/whisper_button_x.png', 0.9)
                    if x:
                        x, y, width, height = x
                        helper.clickAt(x+5, y+5)
                        chatField = helper.isImageVisableOnScreen(f'{assetsDir}/chat/chat_entry.png', 0.9)
                        if chatField:
                            time.sleep(1)
                            x, y, width, height = chatField
                            printx("Sending Message..")
                            helper.clickAt(x, y)
                            helper.sendMessage(response)
                            time.sleep(1)
                            helper.clickAt(x, y)

                            helper.sendMessage("/clear")
                            time.sleep(1)
                        
                            # Clear chat input
                            pyautogui.moveTo(x, y - 30)
                            pyautogui.click()

                            printx("Message sent")
                            helper.sendDiscordNotification(f'Booo! Someone whispered to you: "{chatText}". My Answer was: "{response}"')
                            isChatting = selfSet(False, shared_variables)


def selfSet(value, shared):
    shared["isChatting"].value = value
    return value

def printx(str):
    print(f"(Chatter): {str}")

