from multiprocessing import Process, Value
from services.helper import helper
from modules.movement import runner
from modules.chatting import chatter
from modules.fighting import fighter
from modules.fighting import hunter
from modules.watching import watcher
import time
import json
import os

thisDir = os.path.dirname(os.path.abspath(__file__))
config_path = thisDir + '/config.json'

if __name__ == '__main__':
    with open(config_path, 'r') as file:
        data = json.load(file)
    
    doHunt = data["Hunt"]
    runFromFights = data["RunFromFights"]
    targets = data["Targets"]
    moveToUse = data["Move"]
    debugMode = data["Debug"]

    helper.printx("Bot", "Starting..")

    if debugMode:
         helper.printx("Debug", "-------------------------------")
         helper.printx("Debug",f"Bot directory: {thisDir}")
         helper.printx("Debug",f"Hunt: {doHunt}")
         helper.printx("Debug",f"Catching targets: {targets}")
         helper.printx("Debug",f"Run from fights: {runFromFights}")
         helper.printx("Debug",f"Fighting move: {moveToUse}")
         helper.printx("Debug", "-------------------------------")
            
    shared_variables = {
        "isRunning": Value('b', True),
        "isFighting": Value('b', False),
        "isChatting": Value('b', False),
        "isWatching": Value('b', False),
        "debugMode": Value('b', debugMode)
    }
    
    time.sleep(2)
    helper.bringGameToFront()
    running_process = Process(target=runner.run, args=(shared_variables,))
    fighting_process = Process(target=hunter.hunt, args=(thisDir, shared_variables, targets, moveToUse, doHunt, runFromFights))
    #chatting_process = Process(target=chatter.chat, args=(shared_variables,))
    #watching_process = Process(target=watcher.watch, args=(shared_variables,))

    # Start all processes
    running_process.start()
    fighting_process.start()
    #chatting_process.start()
    #watching_process.start()
