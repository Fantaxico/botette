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
nameCoordinates = (927, 299, 1015, 310)
pinCoordinates = (921, 500, 955, 510)

def hunt(shared_variables, general_options, hunting_options, notification_options, targets):
    monImagePath = f"{workingDir}/mon_cropped.png"
    pinImagePath = f"{workingDir}/pin_cropped.png"
    ballImagePath = f"{workingDir}/ball_cropped.png"
    debugMode = shared_variables["debugMode"].value 
    moveToUse = hunting_options["moveToUse"]
    doHunt = hunting_options["doHunt"]
    autoBlazeRadar = hunting_options["autoBlazeRadar"]
    fleeFromFights = hunting_options["fleeFromFights"]
    discordUserId = general_options["discordUserId"]

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
                    helper.takeGameScreenshot(monImagePath, nameCoordinates, greyscaleOptions={
                        'use': True
                    })
                    encounter = helper.getTextFromImage(monImagePath + '.jpeg')
                    encounter = encounter.strip()
                    printx("Encounter is: " + encounter)
                    for target in targets:
                        if encounter == target["Name"]:
                            printx("Encounter is a target")
                            tryCatch(shared_variables, notification_options, discordUserId, ballImagePath, moveToUse, target)
                    else:
                        if autoBlazeRadar:
                            pinSolver = helper.isImageVisableOnScreen(f'{assetsDir}/general/pin.png', 0.9)
                            if pinSolver:
                                time.sleep(0.5)
                                printx("Pin solver detected")
                                x, y, width, height = pinSolver
                                pin = helper.solvePin(pinImagePath, pinCoordinates)
                                if notification_options["OnBlazeRadar"]: helper.sendDiscordNotification("Your blaze radar triggered. My guess is `{pin}`", discordUserId)
                                if pin: 
                                    printx(f"Pin is {pin}") 
                                    helper.clickAt(x, y)
                                    helper.sendMessage(pin)
                                    button_x, button_y = locator.coordinatesRelativeTo(pinSolver, diff_y=40)
                                    helper.clickAt(button_x, button_y)
                                    tryCatch(shared_variables, notification_options, discordUserId, ballImagePath, moveToUse,  {"Name": encounter, "PriorityBall": { "Name" : "Ultra Ball"}})
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

def tryCatch(shared_variables, notification_options, discordUserId, ballImagePath, moveToUse, target):
    ballName = target["PriorityBall"]["Name"]
    if notification_options["OnCatchAttempt"]: 
        if notification_options["IsAnonymous"]:
            helper.sendDiscordNotification(f"Trying to catch a target", discordUserId)
        else:
            helper.sendDiscordNotification(f"Trying to catch target `{target["Name"]}` with an `{ballName}`", discordUserId)
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
                ballImage = f'{assetsDir}/general/balls/{ballName.lower()}.png'
                hasBall = helper.isImageVisableOnScreen(ballImage, 0.9)
                if hasBall:
                    time.sleep(3)
                    x, y, width, height = hasBall
                    ballCoordinates = (x+20, y+25, x+41, y+39)
                    helper.takeGameScreenshot(ballImagePath, ballCoordinates, greyscaleOptions={
                        'use': True,
                        'basewidth': 90
                    }, 
                    extendOptions={
                        'use': True,
                        'size': 50
                    })
                    ballCountText = helper.getTextFromImage(ballImagePath + '.jpeg')
                    count = int(ballCountText.split('x')[1])
                    if count == 10 or count == 5:
                        if notification_options["OnBallCount"]: 
                            if notification_options["IsAnonymous"]:
                                helper.sendDiscordNotification(f"Careful, there are only a few of your Pokeball left", discordUserId)
                            else:
                                helper.sendDiscordNotification(f"Careful, there are only `{count}` `{ballName}s` left", discordUserId)
                    printx(f"Using a {ballName} ({count - 1} left)")
                    helper.clickAt(x, y)
                else:
                    if notification_options["OnCatchAttempt"]: 
                        if notification_options["IsAnonymous"]:
                            helper.sendDiscordNotification(f"Damn, no balls left.. I'll kill the target", discordUserId)
                        else:
                            helper.sendDiscordNotification(f"Damn, no more `{ballName}`s left to catch `{target["Name"]}`.. I'm killing it", discordUserId)
                    fight(moveToUse)
                    rand = helper.numberRandomize(0, 1)
                    if rand <= (5 / 10):
                        x,y = locator.chat
                        helper.clickAt(x,y)
                        helper.sendMessage("f")

                    time.sleep(120)
                    helper.exitBot()

        else:
            return

def selfSet(value, shared):
    shared["isFighting"].value = value
    return value

def printx(str):
    print(f"(Hunter): {str}")
