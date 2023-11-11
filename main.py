from multiprocessing import Process, Value
from services.helper import helper
from modules.movement import runner
from modules.chatting import chatter
from modules.fighting import fighter
from modules.fighting import hunter
from modules.watching import watcher
import time

shared_variables = {
    "isRunning": Value('b', True),
    "isFighting": Value('b', False),
    "isChatting": Value('b', False),
    "isWatching": Value('b', False)
}

if __name__ == '__main__':
    helper.printx("Bot", "Starting..")
    huntOption = input("Do you want to hunt ? (y/_)")

    helper.bringGameToFront()
    time.sleep(2)

    running_process = Process(target=runner.run, args=(shared_variables,))
    fighting_process = Process(target=hunter.hunt if huntOption == "y" else fighter.fight, args=(shared_variables,))
    chatting_process = Process(target=chatter.chat, args=(shared_variables,))
    watching_process = Process(target=watcher.watch, args=(shared_variables,))

    # Start all processes
    running_process.start()
    fighting_process.start()
    chatting_process.start()
    watching_process.start()
