import time
import random
import pyautogui
from services.helper import helper
from services.locator import locator

def hunt(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            isWatching = shared_variables["isWatching"].value 
            hasBattleScreen = helper.isImageVisableOnScreen('assets/general/battle.png', 0.9)
            if hasBattleScreen:
                x, y, width, height = hasBattleScreen
                printx(f"Battle detected")
                isFighting = selfSet(True, shared_variables)
            elif not hasBattleScreen and isFighting:
                printx("Battle ended")
                isFighting = selfSet(False, shared_variables)

            if not isChatting and not isWatching and isFighting:
                pinSolver = helper.isImageVisableOnScreen('assets/general/pin.png', 0.9)
                if pinSolver:
                    time.sleep(0.5)
                    printx("Pin solver detected")
                    x, y, width, height = pinSolver
                    pin = helper.solvePin()
                    if pin: 
                        printx(f"Pin is {pin}")
                        helper.clickAt(x, y)
                        helper.sendMessage(pin)
                        button_x, button_y = locator.coordinatesRelativeTo(pinSolver, diff_y=40)
                        helper.clickAt(button_x, button_y)
                        tryCatch()
                else:
                    printx("Hunting..")
                    move_location = helper.isImageVisableOnScreen('assets/moves/shockwave.png')
                    if move_location:
                        x, y, width, height = move_location
                        pyautogui.moveTo(x, y)
                        pyautogui.click()
                        


def tryCatch(shared_variables):
    while True:
        # We need battle check to know when its captured
        hasBattleScreen = helper.isImageVisableOnScreen('assets/general/battle.png', 0.9)
        if hasBattleScreen:
            isChatting = shared_variables["isChatting"].value
            isWatching = shared_variables["isWatching"].value 
            printx(f"Catching..")
            time.sleep(3)
            if not isChatting and not isWatching:
                bag_x, bag_y = locator.bag
                helper.clickAt(bag_x, bag_y)
                bag = [
                    ('Ultra Ball', 'assets/general/ultra.png'),
                    ('Master Ball', 'assets/general/master.png'),
                    ('Great Ball', 'assets/general/great.png'),
                    ('Starter Ball', 'assets/general/starter.png'),
                    ('Poke Ball', 'assets/general/regular.png'),
                ]
                for ball, image in bag:
                    hasBall = helper.isImageVisableOnScreen(image, 0.9)
                    if hasBall:
                        printx(f"Using a {ball}")
                        x, y, width, height = hasBall
                        helper.clickAt(x, y)
                        break
                    else:
                        return
        else:
            return

def selfSet(value, shared):
    shared["isFighting"].value = value
    return value

def printx(str):
    print(f"(Hunter): {str}")
