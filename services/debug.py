import pyautogui
import time
from helper import helper
import locator 
import cv2
from PIL import ImageGrab, Image
import re
import json
import os
from dotenv import load_dotenv
load_dotenv()

assetsDir = os.getenv("ASSET_DIR")
workingDir = os.getenv("WORKING_DIR")

def game_window_coordinates():
    time.sleep(2)
    game_window, game_window.left, game_window.top, game_window.width, game_window.height = helper.getGameWindow()
    print(f"Coordinates: left={game_window.left}, top={game_window.top}, width={game_window.width}, height={game_window.height}")

def get_mouse_position():
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"""Mouse position: x={x}, y={y}""")


#(left, upper, right, lower) (x, y, x + width, y + height)
def test():
    time.sleep(1)
    ballImage = f'{assetsDir}/general/balls/ultra ball.png'
    ballImagePath = f"{workingDir}/ball_cropped.png"
    hasBall = helper.isImageVisableOnScreen(ballImage, 0.9)
    if hasBall:
        x, y, width, height = hasBall
        ballCoordinates = (x+20, y+25, x+41, y+39)
        helper.takeGameScreenshot(ballImagePath, ballCoordinates, greyscaleOptions={
            'use': True,
            'basewidth': 100
        }, 
        extendOptions={
            'use': True
        })
        ballCountText = helper.getTextFromImage(ballImagePath + '.jpeg')
        count = int(ballCountText.split('x')[1])
        time.sleep(1)
        print(f"Using a Ultra ball ({count - 1})")

get_mouse_position()
