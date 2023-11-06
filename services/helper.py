import pygetwindow as gw
import random
import time
import pyautogui
import pytesseract
import re
from PIL import ImageGrab, Image

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
    
def isImageVisable(pathToImage, confidence_level=0.7):
    return pyautogui.locateOnScreen(pathToImage, confidence=confidence_level)

def clickAt(x, y, mouseButton='left'):
    pyautogui.moveTo(x, y)
    pyautogui.click(button=mouseButton)
    

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

def textFromImage(image):
    screenshot = Image.open(image)
    text = pytesseract.image_to_string(screenshot)
    return text

def printx(x, str):
    print(f"({x}): {str}")

def numberRandomize(min_value, max_value, isInt = False):
    if isInt:
        res = random.randint(min_value, max_value)
    else:
        res = random.uniform(min_value, max_value)
    return res

def press(key, min_seconds, max_seconds, debug = False):
    sleep_time = numberRandomize(min_seconds, max_seconds)
    if debug:
        print("Pressing {key} for {sleep_time}")
    pyautogui.keyDown(key)
    time.sleep(sleep_time)
    pyautogui.keyUp(key)


def sliceTextPlusCharacters(text, characters):
    from_index = text.find("[From]")
    
    # Slice the text at "[From]" + the next 50 characters
    sliced_text = text[from_index + 6:from_index + characters]
    print(sliced_text)
    
    next_chat_entry = sliced_text.find("[")
    print(next_chat_entry)
    sliced_text2 = sliced_text[0:next_chat_entry]
    print(sliced_text2)
    return sliced_text2

def calcTime(steps):
    if steps == 1:
        return 0.01, 0.06
    elif steps == 2:
        return 0.09, 0.21
    elif steps == 3:
        return 0.24, 0.37
    elif steps == 4:
        return 0.44, 0.49