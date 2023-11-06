import pygetwindow as gw
import random
import time
import pyautogui
import pytesseract
import re
from PIL import ImageGrab, Image

game_window_title = "Pokemon Blaze Online"

# Game Window

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
    print(f"{game_window.width, game_window.height}")
    new_x = (obj_x / 1936) * game_window.width
    new_y = (obj_y / 1048) * game_window.height
    return int(new_x), int(new_y)

# Images

def isImageVisableOnScreen(pathToImage, confidence_level=0.7):
    return pyautogui.locateOnScreen(pathToImage, confidence=confidence_level)

def getTextFromImage(image):
    screenshot = Image.open(image)
    text = pytesseract.image_to_string(screenshot)
    return text

def takeGameScreenshotCropped(coordinates):
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = getGameWindow()
    screenshot = ImageGrab.grab(
        bbox=(
            game_window.left, 
            game_window.top, 
            game_window.left + game_window.width, 
            game_window.top + game_window.height
        )
    )
    #(left, upper, right, lower)
    cropped_screenshot = screenshot.crop(coordinates)
    cropped_screenshot.save("game_cropped.png")

# Controls
    
def clickAt(x, y, mouseButton='left'):
    pyautogui.moveTo(x, y)
    pyautogui.click(button=mouseButton)
    time.sleep(0.5)

def pressKey(key, min_seconds=0.01, max_seconds=0.06):
    sleep_time = numberRandomize(min_seconds, max_seconds)
    pyautogui.keyDown(key)
    time.sleep(sleep_time)
    pyautogui.keyUp(key)

# Etc

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
    printx(f"(ERROR): {str}")

