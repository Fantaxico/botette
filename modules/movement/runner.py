import time
from services import helper

def run(shared_variables):
    # We want it to run indefinitly
    while True:
        if helper.isGameActive():
            isChatting = shared_variables["isChatting"].value
            isFighting = shared_variables["isFighting"].value
            isRunning = shared_variables["isRunning"].value

            if isFighting or isChatting:
                isRunning = selfSet(False, shared_variables)
            else:
                isRunning = selfSet(True, shared_variables)
            
            if isRunning:
                printx(f"Running.. ({isChatting}/{isFighting}/{isRunning})")
                key = "A"
                rand = helper.numberRandomize(0,1,True)
                if rand == 0:
                    key = "D"
                helper.pressKey(key, 0.01, 0.05)

def selfSet(value, shared):
    shared["isRunning"].value = value
    return value

def printx(str):
    print(f"(Runner): {str}")
