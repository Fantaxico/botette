import time
import random
import pyautogui
from services import helper

# Overwrite this with window size
chat_coordinates = (1040, 720, 1450, 900)

def hunt(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value 
            time.sleep(1)
            printx("Screen monitoring..")
            #printx("Screening for battle..")
            hasBattleScreen = helper.isImageVisable('assets/general/battle.png', 0.9)
            if hasBattleScreen:
                x, y, width, height = hasBattleScreen
                printx(f"Battle detected")
                isFighting = selfSet(True, shared_variables)
            elif not hasBattleScreen and isFighting:
                printx("Battle ended")
                isFighting = selfSet(False, shared_variables)

            if not isChatting and isFighting:
                printx(f"Fighting..")
                move_location = helper.isImageVisable('assets/moves/bugbuzz.png')
                if move_location:
                    x, y, width, height = move_location
                else:
                    return
                pyautogui.moveTo(x, y)
                pyautogui.click()

def selfSet(value, shared):
    shared["isFighting"].value = value
    return value


def printx(str):
    print(f"(Hunter): {str}")
