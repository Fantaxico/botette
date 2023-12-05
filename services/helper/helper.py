from PIL import ImageGrab, Image
from dotenv import load_dotenv
import pygetwindow as gw
import random
import time
import pyautogui
import pytesseract
import cv2
import json
import requests
import os
import psutil
import os

load_dotenv()

workingDir = os.getenv("WORKING_DIR")
webhookUrl = os.getenv("DISCORD_WEBHOOK")

# Game Window
gameWindowTitle = "Pokemon Blaze Online"

def getGameWindow():
    try:
        gameWindow = gw.getWindowsWithTitle(gameWindowTitle)[0]
        return gameWindow, gameWindow.left, gameWindow.top, gameWindow.width, gameWindow.height
    except IndexError:
        printx("Bot", "Error: Game window not found.")
        exit()

def bringGameToFront():
    gameWindow, gameWindow.left, gameWindow.top, gameWindow.width, gameWindow.height = getGameWindow()
    gameWindow.minimize()
    gameWindow.restore()
    gameWindow.activate()

def isGameActive():
    activeWindow = gw.getActiveWindow()
    if activeWindow:
        return activeWindow.title == gameWindowTitle
    else:
        False

def calculateObjCoordinates(obj_x, obj_y):
    gameWindow, gameWindow.left, gameWindow.top, gameWindow.width, gameWindow.height = getGameWindow()
    #printx("Debug", f"calculateObjCoordinates: {game_window.width, game_window.height}")
    new_x = (obj_x / 1936) * gameWindow.width
    new_y = (obj_y / 1048) * gameWindow.height
    return int(new_x), int(new_y)

# Images

def isImageVisableOnScreen(pathToImage, confidence_level=0.7):
    return pyautogui.locateOnScreen(pathToImage, confidence=confidence_level)

def getTextFromImage(imagePath):
    screenshot = Image.open(imagePath)
    text = pytesseract.image_to_string(screenshot)
    text = text.strip()
    return text

def solvePin(imagePath, pinCoordinates):
    takeGameScreenshot(imagePath, pinCoordinates, full=False, greyscaleOptions= {
        'use': True,
        'basewidth': 100
    },
    extendOptions= {
        'use': True
    })
    pin_text = getTextFromImage(imagePath + '.jpeg')
    return pin_text

def takeGameScreenshot(imagePath, coordinates, full=False ,greyscaleOptions=None, extendOptions=None):
    # Options
    if greyscaleOptions is None:
        greyscaleOptions = {'use': False, 'basewidth': 300, 'baseheight': 0}
    greyscale = greyscaleOptions.get('use', False)
    basewidth = greyscaleOptions.get('basewidth', 300)
    baseheight = greyscaleOptions.get('baseheight', 0)

    if extendOptions is None:
        extendOptions = {'use': False, 'size': 20}
    extend = extendOptions.get('use', False)
    size = extendOptions.get('size', 20)

    #Logic
    screenshot = getScreenshot()
    if full:
        screenshot.save(imagePath)
        return
    
    croppedScreenshot = screenshot.crop(coordinates)
    croppedScreenshot.save(imagePath)

    optOutputPath = imagePath + '.jpeg'
    if greyscale:
        greyScaleImage(imagePath, optOutputPath ,basewidth, baseheight)
    if extend:
        extendImageBlack(optOutputPath, optOutputPath, size)

def greyScaleImage(imagePath, outputPath, basewidth=300, baseHeight=0):
    img = Image.open(imagePath)
    wpercent = (basewidth/float(img.size[0]))
    hsize = baseHeight if baseHeight != 0 else int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize))
    img.save(imagePath)

    img = cv2.imread(imagePath)
    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    retval, threshold2 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(outputPath,threshold2)

def extendImageBlack(imagePath, outputPath, size):
    image = Image.open(imagePath)
    newWidth = image.width + 2 * size
    newHeight = image.height + 2 * size
    extImage = Image.new("RGB", (newWidth, newHeight), "black")
    extImage.paste(image, (size, size))
    extImage.save(outputPath)

def getScreenshot():
    gameWindow, gameWindow.left, gameWindow.top, gameWindow.width, gameWindow.height = getGameWindow()
    screenshot = ImageGrab.grab(
        bbox=(
            gameWindow.left, 
            gameWindow.top, 
            gameWindow.left + gameWindow.width, 
            gameWindow.top + gameWindow.height
        )
    )
    return screenshot

# Controls
    
def clickAt(x, y, mouseButton='left'):
    pyautogui.moveTo(x, y)
    pyautogui.click(button=mouseButton)
    time.sleep(0.3)

def pressKey(key, minSeconds=0.01, maxSeconds=0.06):
    sleep_time = numberRandomize(minSeconds, maxSeconds)
    pyautogui.keyDown(key)
    time.sleep(sleep_time)
    pyautogui.keyUp(key)

def sendMessage(text):
    pyautogui.write(text)
    pressKey("ENTER", 0.1, 0.5)

# Notifications

def sendDiscordNotification(message, userId=None, withScreenshot=False):   
    if userId is None or userId == "":
        printx("Bot", f"Failed to send notification. No userId given.")
        return 

    preset = f"Booo! <@{userId}>"
    webhook_url = webhookUrl
    data = {
        'content': f'{preset} {message}'
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
def containsConsecutiveChars(text1, text2):
    for i in range(len(text2) - 2):
        if text2[i:i+3] in text1:
            return True
    return False

def exitBot():
    terminateProcess("python.exe")
    terminateProcess("BotetteUI.exe")

def terminateProcess(name):
    try:
        pid = getPIDName(name)
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Terminate the parent process
        parent.terminate()
        parent.wait(timeout=5)

        # Terminate the child processes
        for child in children:
            child.terminate()
            child.wait(timeout=5)
        print(f"Process {pid} and its children terminated successfully.")

    except psutil.NoSuchProcess as e:
        print(f"Error: {e}")
    except psutil.AccessDenied as e:
        print(f"Error: {e}")

def getPIDName(name):
    for process in psutil.process_iter(['pid', 'name']):
        printx("Debug", process.info['name'])
        if process.info['name'] == name:
            return process.info['pid']

def swapIndex(array, index1, index2):
    temp1 = array[index1]
    temp2 = array[index2]
    array[index1] = temp2
    array[index2] = temp1
    return array


def numberRandomize(minValue, maxValue, isInt = False):
    if isInt:
        res = random.randint(minValue, maxValue)
    else:
        res = random.uniform(minValue, maxValue)
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

