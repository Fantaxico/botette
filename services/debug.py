import pyautogui
import time
import helper
import locator 
import re

def game_window_coordinates():
    time.sleep(2)
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = helper.getGameWindow()
    print(f"Coordinates: left={game_window.left}, top={game_window.top}, width={game_window.width}, height={game_window.height}")

def get_mouse_position():
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"Mouse position: x={x}, y={y}")

#(left, upper, right, lower) (x, y, x + width, y + height)
def test():
    time.sleep(3)
    helper.takeGameScreenshotCropped("pin_cropped.png", (800, 490, 1100, 530))
    pin_text = helper.getTextFromImage("pin_cropped.png")
    pin = re.findall(r"\[(.*?)\]", pin_text)
    if pin:
        return pin[0]
    else:
        return None

test()