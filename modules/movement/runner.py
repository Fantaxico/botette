import time
from services import helper

def run(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.is_game_active():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            isRunning = shared_variables["isRunning"].value

            if isFighting or isChatting:
                isRunning = selfSet(False, shared_variables)
            else:
                isRunning = selfSet(True, shared_variables)
            
            if isRunning:
                printx("Running..")
                helper.press("A", 0.01, 0.05)
                helper.press("D", 0.01, 0.05)

def selfSet(value, shared):
    shared["isRunning"].value = value
    return value

def printx(str):
    print(f"(Runner): {str}")
