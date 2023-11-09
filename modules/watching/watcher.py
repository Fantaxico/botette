import time
import random
import pyautogui
from services.helper import helper
from services.locator import locator

def watch(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            isWatching = shared_variables["isWatching"].value 
            time.sleep(5)
            
            if not isChatting:
                friendRequest = helper.isImageVisableOnScreen('assets/general/friend.png', 0.9)
                if friendRequest:
                    printx("Friend request detected")
                    isWatching = selfSet(True, shared_variables)
                    x, y, width, height = friendRequest
                    helper.clickAt(x, y)
                    isWatching = selfSet(False, shared_variables)

                no = helper.isImageVisableOnScreen('assets/general/no.png', 0.9)
                yes = helper.isImageVisableOnScreen('assets/general/yes.png', 0.9)
                if no:
                    printx("Popup(no) detected")
                    isWatching = selfSet(True, shared_variables)
                    x, y, width, height = no
                    helper.clickAt(x, y)
                    isWatching = selfSet(False, shared_variables)
                # Only if no is not visable
                elif yes:
                    printx("Popup(yes) detected")
                    isWatching = selfSet(True, shared_variables)
                    x, y, width, height = yes
                    helper.clickAt(x, y)
                    isWatching = selfSet(False, shared_variables)

                # Case if it is not a fighting pin
                pinSolver = helper.isImageVisableOnScreen('assets/general/pin.png', 0.9)
                if pinSolver and not isFighting:
                    printx("Pin solver detected")
                    isWatching = selfSet(True, shared_variables)
                    x, y, width, height = pinSolver
                    pin = helper.solvePin()
                    if pin: 
                        printx(f"Pin is {pin}")
                        helper.clickAt(x, y)
                        helper.sendMessage(pin)
                        button_x, button_y = locator.coordinatesRelativeTo(pinSolver, diff_y=40)
                        helper.clickAt(button_x, button_y)
                        isWatching = selfSet(False, shared_variables)

def selfSet(value, shared):
    shared["isWatching"].value = value
    return value

def printx(str):
    print(f"(Watcher): {str}")


