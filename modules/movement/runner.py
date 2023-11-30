import time
from services.helper import helper

def run(shared_variables, general_options, running_options):
    randomness = running_options["runningRandomness"]
    invert = running_options["runningInvert"]
    directions = running_options["runningDirection"].split("/")
    discordUserId = general_options["discordUserId"]
    
    if invert: directions = helper.swapIndex(directions, 0, 1)
    debugMode = shared_variables["debugMode"].value 
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
                rand = helper.numberRandomize(0, 1)
                holdTimes = (0.44, 0.49)
                # x% chance to occur
                if rand <= (randomness / 10):
                     # Randomize less steps to go
                     rand = helper.numberRandomize(1, 3, isInt=True)
                     if debugMode: printx(f"Randomness edited steps to {rand}")
                     min, max = helper.calcStepTime(rand)
                     # Edid hold times to be earlier
                     holdTimes = (min, max)

                printx(f"Running..")
                # Keep holding to go 4 steps(clean) be sure to be in a spot with walls
                helper.pressKey(directions[0], holdTimes[0], holdTimes[1])
                helper.pressKey(directions[1], holdTimes[0], holdTimes[1])
                

def selfSet(value, shared):
    shared["isRunning"].value = value
    return value

def printx(str):
    print(f"(Runner): {str}")
