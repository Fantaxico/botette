import pygetwindow as gw
import random
import time
import pyautogui

game_window_title = "Pokemon Blaze Online"

def bring_game_to_front():
    try:
        game_window = gw.getWindowsWithTitle(game_window_title)[0]
        game_window.minimize()
        game_window.restore()
        game_window.activate()
        return game_window.left, game_window.top, game_window.width, game_window.height
    except IndexError:
        printx("Bot", "Error: Game window not found.")
        exit()

def is_game_active():
    active_window = gw.getActiveWindow()
    if active_window:
        return active_window.title == game_window_title
    else:
        False
    

def isImageVisable(pathToImage, confidence_level=0.7):
    return pyautogui.locateOnScreen(pathToImage, confidence=confidence_level)

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

def calcTime(steps):
    if steps == 1:
        return 0.01, 0.06
    elif steps == 2:
        return 0.09, 0.21
    elif steps == 3:
        return 0.24, 0.37
    elif steps == 4:
        return 0.44, 0.49