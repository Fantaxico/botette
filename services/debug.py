import pyautogui
import time
import helper
import locator 

def game_window_coordinates():
    time.sleep(2)
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = helper.getGameWindow()
    print(f"Coordinates: left={game_window.left}, top={game_window.top}, width={game_window.width}, height={game_window.height}")

def get_mouse_position():
    time.sleep(2)
    x, y = pyautogui.position()
    print(f"Mouse position: x={x}, y={y}")

def test():
    while True:
        time.sleep(2)
        whisper = helper.isImageVisableOnScreen("assets/chat/whisper_button.png", 0.9)
        if whisper:
            x, y, w, h = whisper
            print(f"Found at {x}/{y}")
            helper.clickAt(x,y)
            time.sleep(1)
            button_x, button_y = locator.whisper_button_x(y)
            pyautogui.moveTo(button_x,button_y)
            helper.clickAt(button_x,button_y)

test()