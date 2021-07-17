'''
Jackbox Partypack Bot
Alex M Brown
Started: 7/11/2021

Python bot that can play a game of Jackbox using Selenium
'''


from players.guesspionage.guesspionage import Guesspionage
from players.quiplash.quiplash import Quiplash2, Quiplash3, QuiplashXL
from players.fibbage.fibbage import FibbageXL, Fibbage2
from threading import Thread
import random


ROBOT_NAMES = [
    "JackBot",
    "BitLash",
    "QuipHash",
    "WordSpudFan",
    "J.A.C.K.",
    "AimBot",
    "BeepBorp",
    "PythonGuy",
    "Gene",
    "Rando",
    "g00seMoo$e",
    "ZipZapZorp",
    "Krunk",
    "Bebeaked"
]

PLAYER_CLASSES = [
    QuiplashXL,
    Quiplash2,
    Quiplash3,
    FibbageXL,
    Fibbage2,
    Guesspionage
]

def playBall(code, name, playerClass):
    player = playerClass(code, name)
    player.play()

PLAYER_THREADS = []

gameSelectPrompt = "Options:"
for i in range(1, len(PLAYER_CLASSES)+1):
    gameSelectPrompt += f"\n{i}. {PLAYER_CLASSES[i-1].details()['name']}\t\t{PLAYER_CLASSES[i-1].details()['pack']}"
gameSelectPrompt += "\nWhat game are we playing? "

gameSelect = int(input(gameSelectPrompt))
playerCount = int(input("How many bots would you like? "))
roomCode = input("Enter room code: ")

random.shuffle(ROBOT_NAMES)

print(f"Starting {playerCount} bots...")
for i in range(0, playerCount):
    newThread = Thread(target=playBall, args=(roomCode,ROBOT_NAMES[i], PLAYER_CLASSES[gameSelect-1]))
    PLAYER_THREADS.append(newThread)
    newThread.start()


for player in PLAYER_THREADS:
    player.join()