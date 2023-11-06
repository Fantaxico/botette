import pyautogui
import time
import helper

def game_window_coordinates():
    time.sleep(2)
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = helper.getGameWindow()
    print(f"Coordinates: left={game_window.left}, top={game_window.top}, width={game_window.width}, height={game_window.height}")

def get_mouse_position():
    time.sleep(2)
    x, y = pyautogui.position()
    print(f"Mouse position: x={x}, y={y}")

game_window_coordinates()