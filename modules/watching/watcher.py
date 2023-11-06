import time
import random
import pyautogui
from services import helper

def watch(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            time.sleep(5) 
            if not isChatting:
                friendRequest = helper.isImageVisableOnScreen('assets/general/friend.png', 0.9)
                if friendRequest:
                    printx("Friend request detected")
                    x, y, width, height = friendRequest
                    helper.clickAt(x, y)

                no = helper.isImageVisableOnScreen('assets/general/no.png', 0.9)
                yes = helper.isImageVisableOnScreen('assets/general/yes.png', 0.9)
                if no:
                    printx("Popup(no) detected")
                    x, y, width, height = no
                    helper.clickAt(x, y)
                # Only if no is not visable
                elif yes:
                    printx("Popup(yes) detected")
                    x, y, width, height = yes
                    helper.clickAt(x, y)
def printx(str):
    print(f"(Watcher): {str}")
