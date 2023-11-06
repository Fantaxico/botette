import time
import random
import pyautogui
from services import helper

def fight(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.is_game_active():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value 
            time.sleep(1)
            #printx("Screening for battle..")
            hasBattleScreen = pyautogui.locateOnScreen('assets/general/battle.png', confidence=0.9)
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
    print(f"(Fighter): {str}")
