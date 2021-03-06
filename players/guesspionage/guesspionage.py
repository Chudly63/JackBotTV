'''
Jackbox Guesspionage Player Class

Player class for the game Guesspionage
Each GuesspionagePlayer will choose a random guessing and voting strategy

Strategies:
    Guessing Strategies (Choosing a percentage)
        1. SafeGuesser - Choose a percentage near 50%
        2. RandomGuesser - Choose a random percentage
        3. WildGuesser - Choose a percentage > 75% or < 25%
        4. IndecisiveGuesser - Keep choosing random percentages until time runs out
    Voting Strategies   (Much Higher, Higher, Lower, or Much Lower)
        1. MajorityVoter - Choose the option with the greatest probability of being correct
        2. RandomVoter - Choose a random option
        3. RiskyVoter - Like the MajorityVoter, but will always pick Much Higher or Much Lower if available
        4. EvenStevenVoter - Votes Higher on even guesses and Lower on odd guesses
        5. RouletteVoter - Makes a random guess of their own, and then votes for it
    Final Round - Choose three random options
'''
from players.player import Player
from players.guesspionage.strategies import *
from time import sleep
import random

GUESSING_STRAGEIES = [
    SafeGuesser,
    RandomGuesser,
    WildGuesser,
    IndecisiveGuesser
]

VOTING_STRAGETIES = [
    MajorityVoter,
    RandomVoter,
    RiskyVoter,
    EvenStevenVoter,
    RouletteVoter
]

class GuesspionagePlayer(Player):

    def __init__(self, code, name):
        self.login(code, name)
        self.checkForCharacterSelect("robot")
        while(not self.isCharacterSelected()):
            self.checkForCharacterSelect()
        self.guessingStrategy = random.choice(GUESSING_STRAGEIES)(self.driver)
        self.votingStrategy = random.choice(VOTING_STRAGETIES)(self.driver)

        print(f"{name} {self.guessingStrategy.describe()} and {self.votingStrategy.describe()}")

    def isCharacterSelected(self):
        try:
            character = self.driver.find_element_by_id("pollposition-character")
            return character.is_displayed()
        except:
            pass
        return False
    
    def checkForCharacterSelect(self, preference=None):
        if preference:
            try:
                characterButtons = self.getDisplayedElements(className="pollposition-character-button", attributes=[("aria-label", preference.lower())])
                if(len(characterButtons > 0)):
                    characterButtons[0].click()
                    return True
            except Exception as e:
                pass
        else:
            return self.clickRandom("pollposition-character-button")
        
        return False

    def checkForFinalRound(self):
        try:
            choices = self.getDisplayedElements(className="pollposition-choice-button")
            if(len(choices) > 4):
                random.choice(choices).click()
                return True
        except Exception as e:
            print(f"Check for final round {e}")
            pass

        return False

    #Check to see if the options for Play Again / New Players appears
    #If so, prompt the user to either restart the game, or go back to the menu
    def checkForPlayAgain(self):
        try:
            samePlayers = self.driver.find_element_by_id("pollposition-sameplayers")
            if (samePlayers.is_enabled() and samePlayers.is_displayed()):
                if ("Y" in input("Play again?").upper()):
                    samePlayers.click()
                    return False
                else:
                    self.driver.find_element_by_id("pollposition-newplayers").click()

                return True
        except Exception as e:
            print(f"Check for play again {e}")
            pass


        return False

class Guesspionage(GuesspionagePlayer):

    def details():
        return {
            "name": "Guesspionage",
            "pack": "JackBox Party Pack 3"
        }

    def play(self):
        gameStarted = False
        gameOn = True
        while(gameOn):
            if not gameStarted:
                if self.checkForEveryoneIn("pollposition-character-startgame"):
                    gameStarted = True

            if self.guessingStrategy.makeGuess() or self.votingStrategy.makeVote():
                gameStarted = True
                sleep(10)

            if gameStarted:
                if self.checkForFinalRound():
                    continue

            if self.checkForDisconnected() or self.checkForPlayAgain():
                gameOn = False
                self.driver.quit()
                
            sleep(5)

