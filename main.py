from multiprocessing import Process, Value
from services.helper import helper
from modules.movement import runner
from modules.chatting import chatter
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

    # General 
    debugMode = data["Debug"]
    discordUserId = data["DiscordUserId"]
    tickChatter = data["TickChatter"]
    tickWatcher = data["TickWatcher"]
    general_options = {
        "debugMode": debugMode,
        "discordUserId": discordUserId,
        "tickChatter": tickChatter,
        "tickWatcher": tickWatcher
    }

    # Running
    runningDirection = data["RunningDirection"]
    runningInvert = data["RunningInvert"]
    runningRandomness = data["RunningRandomness"]
    running_options = {
        "runningDirection": runningDirection,
        "runningInvert": runningInvert,
        "runningRandomness": runningRandomness,
    }
    
    # Hunting
    doHunt = data["HuntingMode"]
    moveToUse = data["MoveToUse"]
    targets = [target['Name'] for target in data["Targets"]]
    fleeFromFights = data["FleeFromFights"]
    autoBlazeRadar = False
    hunting_options = {
        "doHunt": doHunt,
        "moveToUse": moveToUse,
        "fleeFromFights": fleeFromFights,
        "autoBlazeRadar": autoBlazeRadar
    }

    # Notifications
    notification_options = data["UserNotifications"]
    notifyIsAnonymous = notification_options["IsAnonymous"]
    notifyOnDisconnect = notification_options["OnDisconnect"]
    notifyOnBlazeRadar = notification_options["OnBlazeRadar"]
    notifyOnCatchAttempt = notification_options["OnCatchAttempt"]
    notifyOnWisperMessage = notification_options["OnWisperMessage"]
    notifyOnFriendRequest = notification_options["OnFriendRequest"]
    notifyOnAdminPin = notification_options["OnAdminPin"]
    notifyOnBallCount = notification_options["OnBallCount"]

    helper.printx("Bot", "Starting..")
    if debugMode:
         helper.printx("Debug", "--------------- GENERAL ---------------")
         helper.printx("Debug",f"Bot directory: {thisDir}")
         helper.printx("Debug",f"Discord User ID: {discordUserId}")
         helper.printx("Debug", "--------------- RUNNING ---------------")
         helper.printx("Debug",f"Direction: {runningDirection}")
         helper.printx("Debug",f"Invert: {runningInvert}")
         helper.printx("Debug",f"Randomness: {runningRandomness}")
         helper.printx("Debug", "--------------- HUNTING ---------------")
         helper.printx("Debug",f"Hunting: {doHunt}")
         helper.printx("Debug",f"Targets: {targets}")
         helper.printx("Debug",f"AutoBlazeRadar: {autoBlazeRadar}")
         helper.printx("Debug",f"Flee: {fleeFromFights}") if fleeFromFights else helper.printx("Debug",f"Fighting move: {moveToUse}")
         helper.printx("Debug", "------------- NOTIFICATION ------------")
         helper.printx("Debug",f"IsAnonymous: {notifyIsAnonymous}")
         helper.printx("Debug",f"OnDisconnect: {notifyOnDisconnect}")
         helper.printx("Debug",f"OnBlazeRadar: {notifyOnBlazeRadar}")
         helper.printx("Debug",f"OnCatchAttempt: {notifyOnCatchAttempt}")
         helper.printx("Debug",f"OnWisperMessage: {notifyOnWisperMessage}")
         helper.printx("Debug",f"OnFriendRequest: {notifyOnFriendRequest}")
         helper.printx("Debug",f"OnAdminPin: {notifyOnAdminPin}")
         helper.printx("Debug",f"OnBallCount: {notifyOnBallCount}")
         helper.printx("Debug", "---------------------------------------")
            
    shared_variables = {
        "isRunning": Value('b', True),
        "isFighting": Value('b', False),
        "isChatting": Value('b', False),
        "isWatching": Value('b', False),
        "debugMode": Value('b', debugMode)
    }
    
    time.sleep(2)
    helper.bringGameToFront()
    running_process = Process(target=runner.run, args=(shared_variables, general_options, running_options))
    fighting_process = Process(target=hunter.hunt, args=(shared_variables, general_options, hunting_options, notification_options, data["Targets"]))
    chatting_process = Process(target=chatter.chat, args=(shared_variables, general_options, notification_options, running_options, data["Targets"]))
    watching_process = Process(target=watcher.watch, args=(shared_variables, general_options, notification_options))

    # Start all processes
    running_process.start()
    fighting_process.start()
    chatting_process.start()
    watching_process.start()
