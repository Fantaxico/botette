import pygetwindow as gw
import random
import time
import pyautogui
import pytesseract
import re
from PIL import ImageGrab, Image
import cv2
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

workingDir = os.getenv("WORKING_DIR")

# Game Window
game_window_title = "Pokemon Blaze Online"

def getGameWindow():
    try:
        game_window = gw.getWindowsWithTitle(game_window_title)[0]
        return game_window, game_window.left, game_window.top, game_window.width, game_window.height
    except IndexError:
        printx("Bot", "Error: Game window not found.")
        exit()

def bringGameToFront():
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = getGameWindow()
    game_window.minimize()
    game_window.restore()
    game_window.activate()

def isGameActive():
    active_window = gw.getActiveWindow()
    if active_window:
        return active_window.title == game_window_title
    else:
        False

def calculateObjCoordinates(obj_x, obj_y):
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = getGameWindow()
    #printx("Debug", f"calculateObjCoordinates: {game_window.width, game_window.height}")
    new_x = (obj_x / 1936) * game_window.width
    new_y = (obj_y / 1048) * game_window.height
    return int(new_x), int(new_y)

# Images

def isImageVisableOnScreen(pathToImage, confidence_level=0.7):
    return pyautogui.locateOnScreen(pathToImage, confidence=confidence_level)

def getTextFromImage(imagePath):
    screenshot = Image.open(imagePath)
    text = pytesseract.image_to_string(screenshot)
    text = text.strip()
    return text

def solvePin(image_path):
    takeGameScreenshotCropped(image_path, (800, 490, 1100, 530))
    pin_text = getTextFromImage(image_path)
    pin = re.findall(r"\[(.*?)\]", pin_text)
    if pin:
        return pin[0]
    else:
        return None

def takeGameScreenshotCropped(imagePath, coordinates, greyscale = False, basewidth=300):
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = getGameWindow()
    screenshot = ImageGrab.grab(
        bbox=(
            game_window.left, 
            game_window.top, 
            game_window.left + game_window.width, 
            game_window.top + game_window.height
        )
    )
    cropped_screenshot = screenshot.crop(coordinates)
    cropped_screenshot.save(imagePath)
    if greyscale:
        greyScaleImage(imagePath, basewidth)

def takeGameScreenshot(imagePath):
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = getGameWindow()
    screenshot = ImageGrab.grab(
        bbox=(
            game_window.left, 
            game_window.top, 
            game_window.left + game_window.width, 
            game_window.top + game_window.height
        )
    )
    screenshot.save(imagePath)

# Controls
    
def clickAt(x, y, mouseButton='left'):
    pyautogui.moveTo(x, y)
    pyautogui.click(button=mouseButton)
    time.sleep(0.3)

def pressKey(key, min_seconds=0.01, max_seconds=0.06):
    sleep_time = numberRandomize(min_seconds, max_seconds)
    pyautogui.keyDown(key)
    time.sleep(sleep_time)
    pyautogui.keyUp(key)

def sendMessage(text):
    pyautogui.write(text)
    pressKey("ENTER", 0.1, 0.5)

# Notifications

def sendDiscordNotification(message, withScreenshot=False):
    webhook_url = 'https://discord.com/api/webhooks/1176979268119576576/-KdIk8HJDBgy-452JQBW4o6IOssV8FNWHCZUW5yb6xw1Uxj5HKGK2jZcZ9ybTA_vm9On'
    data = {
        'content': message
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        printx("Bot", "Notification sent successfully!")
    else:
        printx("Bot", f"Failed to send notification. Status code: {response.status_code}")


# Etc

def swapIndex(array, index1, index2):
    temp1 = array[index1]
    temp2 = array[index2]
    array[index1] = temp2
    array[index2] = temp1
    return array

def greyScaleImage(imagePath, basewidth=300):
    img = Image.open(imagePath)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize))
    img.save(imagePath)

    img = cv2.imread(imagePath)
    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    retval, threshold2 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(imagePath + '.jpeg',threshold2)

def numberRandomize(min_value, max_value, isInt = False):
    if isInt:
        res = random.randint(min_value, max_value)
    else:
        res = random.uniform(min_value, max_value)
    return res

def calcStepTime(steps):
    if steps == 1:
        return 0.01, 0.06
    elif steps == 2:
        return 0.09, 0.21
    elif steps == 3:
        return 0.24, 0.37
    elif steps == 4:
        return 0.44, 0.49
            
def printx(x, str):
    print(f"({x}): {str}")

def printe(str):
    printx("Bot",f"(ERROR): {str}")

