import time
import random
import requests
import json
import os
import pyautogui
from services.helper import helper
from services.locator import locator
from dotenv import load_dotenv
load_dotenv()

assetsDir = os.getenv("ASSET_DIR")
workingDir = os.getenv("WORKING_DIR")
#(left, upper, right, lower)
nameCoordinates = (927, 299, 1015, 315)

def hunt(shared_variables, targets, moveToUse, doHunt, fleeFromFights):
    monImagePath = f"{workingDir}/mon_cropped.png"
    pinImagePath = f"{workingDir}/pin_cropped.png"
    debugMode = shared_variables["debugMode"].value 

    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            isWatching = shared_variables["isWatching"].value 
            hasBattleScreen = helper.isImageVisableOnScreen(f'{assetsDir}/general/battle.png', 0.9)
            if hasBattleScreen:
                x, y, width, height = hasBattleScreen
                printx(f"Battle detected")
                isFighting = selfSet(True, shared_variables)
            elif not hasBattleScreen and isFighting:
                printx("Battle ended")
                isFighting = selfSet(False, shared_variables)

            if not isChatting and not isWatching and isFighting:
                if doHunt:
                    printx("Hunting..")
                    helper.takeGameScreenshotCropped(monImagePath, nameCoordinates, greyscale=True)
                    encounter = helper.getTextFromImage(monImagePath + '.jpeg')
                    encounter = encounter.strip()
                    printx("Encounter is: " + encounter)
                    pinSolver = helper.isImageVisableOnScreen(f'{assetsDir}/general/pin.png', 0.9)
                    if pinSolver:
                        time.sleep(0.5)
                        printx("Pin solver detected")
                        x, y, width, height = pinSolver
                        pin = helper.solvePin(pinImagePath)
                        if pin: 
                            printx(f"Pin is {pin}") 
                            helper.clickAt(x, y)
                            helper.sendMessage(pin)
                            button_x, button_y = locator.coordinatesRelativeTo(pinSolver, diff_y=40)
                            helper.clickAt(button_x, button_y)
                            tryCatch(shared_variables, {"Name": encounter, "PriorityBall": { "Name" : "Ultra Ball"}})
                    else:
                        for target in targets:
                            if encounter == target["Name"]:
                                printx("Encounter is a target")
                                tryCatch(shared_variables, target)
                        else:
                            if fleeFromFights:
                                flee()
                            else:
                                fight(moveToUse)
                else:
                    if fleeFromFights:
                        flee()
                    else:
                        fight(moveToUse)

def flee():
    printx("Fleeing..")
    x, y = locator.run
    helper.clickAt(x, y)

def fight(moveToUse):
    printx(f"Fighting.. ({moveToUse})")
    x, y = getattr(locator, f"move_{moveToUse}", locator.move_1)
    pyautogui.moveTo(x, y)
    pyautogui.click()

def tryCatch(shared_variables, target):
    helper.sendDiscordNotification(f"Booo! Trying to catch {target["Name"]} with a {target["PriorityBall"]["Name"]}")
    while True:
        # We need battle check to know when its captured
        hasBattleScreen = helper.isImageVisableOnScreen(f'{assetsDir}/general/battle.png', 0.9)
        if hasBattleScreen:
            isChatting = shared_variables["isChatting"].value
            isWatching = shared_variables["isWatching"].value 
            printx(f"Catching {target["Name"]}..")
            if not isChatting and not isWatching:
                bag_x, bag_y = locator.bag
                helper.clickAt(bag_x, bag_y)
                bag = [
                    (target["PriorityBall"]["Name"],f'{assetsDir}/general/balls/{target["PriorityBall"]["Name"].lower()}.png'),
                    ('Ultra Ball', f'{assetsDir}/general/balls/ultra ball.png'),
                    ('Master Ball', f'{assetsDir}/general/balls/master ball.png'),
                    ('Great Ball', f'{assetsDir}/general/balls/great ball.png')
                ]
                for ball, image in bag:
                    hasBall = helper.isImageVisableOnScreen(image, 0.9)
                    if hasBall:
                        time.sleep(3)
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
