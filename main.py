from multiprocessing import Process, Value
from services import helper
from modules.movement import runner
from modules.chatting import chatter
from modules.fighting import fighter
import time

shared_variables = {
    "isRunning": Value('b', True),
    "isFighting": Value('b', False),
    "isChatting": Value('b', False) 
}

if __name__ == '__main__':
    helper.printx("Bot", "Starting..")
    helper.bringGameToFront()
    time.sleep(2)

    running_process = Process(target=runner.run, args=(shared_variables,))
    fighting_process = Process(target=fighter.fight, args=(shared_variables,))
    chatting_process = Process(target=chatter.chat, args=(shared_variables,))

    # Start all processes
    running_process.start()
    fighting_process.start()
    chatting_process.start()
