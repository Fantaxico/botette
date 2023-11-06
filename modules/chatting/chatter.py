import time
import random
import pyautogui
from services import helper

def chat(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.is_game_active():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            time.sleep(1)
            hasBeenWhispered = pyautogui.locateOnScreen('assets/chat/whisper_from.png', confidence=0.7)
            if hasBeenWhispered:
                printx("Whisper detected..")
                isChatting = selfSet(True, shared_variables)
       
            if isChatting:
                chatEntry = pyautogui.locateOnScreen('assets/chat/chat_entry.png', confidence=0.9)
                if chatEntry:
                    printx("Sending Message..")
                    x, y, width, height = chatEntry
                    pyautogui.moveTo(x, y)
                    pyautogui.click()
                    sendMessage("hey m8")
                    sendMessage("/clear")
                    pyautogui.moveTo(x, y - 20)
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


