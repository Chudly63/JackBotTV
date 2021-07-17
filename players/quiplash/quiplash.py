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

    def details():
        return {
            "name": "Quiplash XL",
            "pack": "JackBox Party Pack 2"
        }

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


class Quiplash2(QuiplashPlayer):

    def details():
        return {
            "name": "Quiplash 2",
            "pack": "JackBox Party Pack 3"
        }

    def checkForQuestion(self):
        coinFlip = random.randint(0,1)
        if(coinFlip):
            self.checkForSafetyQuip()
        else:
            super().checkForQuestion()
    
    def checkForSafetyQuip(self):
        try:
            safetyQuip = self.getDisplayedElements(id="quiplash-submit-safetyquip")
            if(len(safetyQuip) == 1):
                safetyQuip[0].click()
                return True
        except: 
            pass

        return False
    
    def checkForVote(self):
        try:
            votes = self.getDisplayedElements(className="quiplash2-vote-button")
            if(len(votes) == 2):
                random.choice(votes).click()
                return True
        except:
            pass

        return False

    def play(self):
        gameOn = True
        gameStarted = False
        while(gameOn):
            if not gameStarted:
                self.checkForEveryoneIn("quiplash-startgame")
            
            if self.checkForQuestion() or self.checkForVote():
                gameStarted = True
                continue

            if gameStarted:
                super().checkForQuestion()

            if self.checkForDisconnected() or self.checkForPlayAgain():
                gameOn = False
                self.driver.quit()

            sleep(5)


class Quiplash3(QuiplashPlayer):

    def details():
        return {
            "name": "Quiplash 3",
            "pack": "JackBox Party Pack 7"
        }

    def checkForEveryoneIn(self, elementClass):
        if(len(self.getDisplayedElements(className=elementClass)) == 1):
        #if(len(self.getActiveButtonsByClass(elementClass)) == 1):
            input("=== Press enter to start the game! ===\n")
            self.getDisplayedElements(className=elementClass)[0].click()
            #self.getActiveButtonsByClass(elementClass)[0].click()
            return True
        
        return False

    def checkForQuestion(self):
        try:
            choices = self.getDisplayedElements(className="choice-button", attributes=[("data-action", "choose")])
            #choices = self.getDisplayedElementsByClassNameAndAttributeValue("choice-button", "data-action", "choose")
            if(len(choices) == 2):
                random.choice(choices).click()
                return True
        except:
            pass

        return False

    def checkForSafetyQuip(self):
        try:
            safetyQuip = self.getDisplayedElements(className="choice-button", attributes=[("data-index", "safetyQuip")])
            #safetyQuip = self.getDisplayedElementsByClassNameAndAttributeValue("choice-button", "data-index", "safetyQuip")
            if(len(safetyQuip) == 1):
                safetyQuip[0].click()
                return True
        except:
            pass

        return False

    def checkForPlayAgain(self):
        try:
            samePlayers = self.getDisplayedElements(className="choice-button", attributes=[("data-action", "PostGame_Continue")])
            #samePlayers = self.getDisplayedElementsByClassNameAndAttributeValue("choice-button", "data-action", "PostGame_Continue")
            if(len(samePlayers) == 1):
                if ("Y" in input("Play again?").upper()):
                    samePlayers[0].click()
                    return False
                else:
                    newPlayers = self.getDisplayedElements(className="choice-button", attributes=[("data-action", "PostGame_NewGame")])
                    #newPlayers = self.getDisplayedElementsByClassNameAndAttributeValue("choice-button", "data-action", "PostGame_NewGame")
                    if(len(newPlayers) > 0):
                        newPlayers[0].click()
                        return True
        except:
            pass

        return False


    def isCharacterSelected(self):
        try:
            return len(self.getDisplayedElements(id="playericon")) > 0
            #return self.driver.find_element_by_id("playericon").is_displayed()
        except:
            return False

    def selectCharacter(self):
        while(not self.isCharacterSelected()):
            try:
                random.choice(self.getDisplayedElements(className="characters")).click()
                #random.choice(self.getActiveButtonsByClass("characters")).click()
            except:
                continue

    def checkForThripLash(self):
        try:
            textAreas = self.getDisplayedElements(id="input-text-textarea")
            if(len(textAreas) == 3):
                for textArea in textAreas:
                    textArea.clear()
                    response = None
                    while(response == None or len(response) > 30):
                        response = random.choice(ANSWERS)
                    textArea.send_keys(response)
                
                self.getDisplayedElements(className="choice-button", attributes=[("data-action","submit")])[0].click()
                return True
        except:
            pass

        return False


    def play(self):
        self.selectCharacter()
        gameOn = True
        gameStarted = False
        while(gameOn):
            if not gameStarted: 
                self.checkForEveryoneIn("vipStart")

            if self.checkForQuestion() or self.checkForSafetyQuip():
                gameStarted = True
                continue
            
            if gameStarted:
                self.checkForThripLash()

            if self.checkForDisconnected() or self.checkForPlayAgain():
                gameOn = False
                self.driver.quit()

            sleep(5)