'''
Jackbox Quiplash Player Class

Player class for the game Quiplash

Strategy:
    When answering a question, choose a random answer from a list in a text file
    When voting on the best answer to another question, pick randomly
'''

import random
from time import sleep
from players.player import Player
from os.path import realpath

ANSWERS = []

#Reads a list of potential submissions from a text file 
#in a resources directory found within the same directory as jackbot.py
FILE_PATH = realpath(__file__)
with open(f"{FILE_PATH}/../../../resources/quips.txt", "r") as quips:
    ANSWERS = quips.read().splitlines()

print(ANSWERS[0])

class QuiplashPlayer(Player):

    def __init__(self, code, name):
        self.login(code, name)

    #Check to see if a question is present on the bot's UI
    #If so, the bot writes an answer and submits
    def checkForQuestion(self):
        try:
            question = self.driver.find_element_by_id("question-text").text
            if len(question) > 0:
                self.driver.find_element_by_id("quiplash-answer-input").send_keys(random.choice(ANSWERS))
                self.driver.find_element_by_id("quiplash-submit-answer").click()
                return True
        except Exception as e:
            print(e)
            pass


        return False

    #Check to see if a prompt for a vote is present on the bot's UI
    #If so, pick a random option to vote for
    def checkForVote(self):
        self.clickRandom("quiplash-vote-button")


    #Check to see if the options for Play Again / New Players appears
    #If so, prompt the user to either restart the game, or go back to the menu
    def checkForPlayAgain(self):
        try:
            samePlayers = self.driver.find_element_by_id("quiplash-sameplayers")
            if (samePlayers.is_enabled() and samePlayers.is_displayed()):
                if ("Y" in input("Play again?").upper()):
                    samePlayers.click()
                    return False
                else:
                    self.driver.find_element_by_id("quiplash-newplayers").click()

                return True
        except Exception as e:
            print(e)
            pass


        return False


class QuiplashXL(QuiplashPlayer):
    def play(self):
        gameOn = True
        gameStarted = False
        while(gameOn):
            if not gameStarted:
                self.checkForEveryoneIn("quiplash-startgame")
            
            if self.checkForQuestion() or self.checkForVote():
                gameStarted = True
                continue

            if self.checkForDisconnected() or self.checkForPlayAgain():
                gameOn = False
                self.driver.quit()

            sleep(5)