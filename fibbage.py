'''
Jackbox Fibbage Player Class

Player class for the game Fibbage

Strategy:
    When submitting a lie, choose the "Lie for me" option
    When guessing the truth, pick randomly
    When selecting a category, pick randomly
    When liking other responses, pick lies that contain terms that robots like
'''
from time import sleep
from player import Player


termsRobotsLike = [
    "robot",
    "oil",
    "computer",
    "circuit",
    "python",
    "alex",
    "bender"
]

class FibbagePlayer(Player):

    def __init__(self, code, name):
        self.login(code, name)

    def checkForSoundSelect(self):
        return self.clickRandom("fibbage-bloop-button")

    #Check to see if the "Everyone's In" button appears on the bot's UI
    #If it does, then the bot will wait for confirmation from the user before starting the game
    def checkForEveryoneIn(self):
        try:
            everyoneIn = self.driver.find_element_by_id("fibbage-startgame")
            if(everyoneIn.is_enabled() and everyoneIn.is_displayed()):
                input("Press enter to start the game!")
                everyoneIn.click()
                return True
        except Exception as e:
            print(e)
            pass

        return False

    def checkForCategorySelect(self):
        return self.clickRandom("fibbage-category-button")

    def checkForLikes(self):
        try:
            likes = self.driver.find_elements_by_class_name("fibbage-like-button")
            if(len(likes) > 0 and likes[0].is_enabled() and likes[0].is_displayed()):
                for option in likes:
                    for termRobotsLike in termsRobotsLike:
                        if termRobotsLike.lower() in option.text.lower():
                            option.click()
        except Exception as e:
            print(e)
            pass

        return False


    #Check to see if a question is present on the bot's UI
    #If so, the bot writes an answer and submits
    def checkForLie(self):
        try:
            lieForMe = self.driver.find_element_by_id("fibbage-lieforme")
            if (lieForMe.is_enabled() and lieForMe.is_displayed()):
                lieForMe.click()
                sleep(1)
                return self.clickRandom("fibbage-suggestion-button")
        except Exception as e:
            print(e)
            pass

        return False

    #Check to see if a prompt for a vote is present on the bot's UI
    #If so, pick a random option to vote for
    def checkForVote(self):
        if self.clickRandom("fibbage-lie-button"):
            self.checkForLikes()
            return True

        return False


    #Check to see if the options for Play Again / New Players appears
    #If so, prompt the user to either restart the game, or go back to the menu
    def checkForPlayAgain(self):
        try:
            samePlayers = self.driver.find_element_by_id("fibbage-sameplayers")
            if (samePlayers.is_enabled() and samePlayers.is_displayed()):
                if ("Y" in input("Play again?").upper()):
                    samePlayers.click()
                    return False
                else:
                    self.driver.find_element_by_id("fibbage-newplayers").click()

                return True
        except Exception as e:
            print(e)
            pass


        return False


class FibbageXL(FibbagePlayer):
    def play(self):
        gameOn = True
        while(gameOn):
            if self.checkForLie() or self.checkForVote():
                sleep(10)
                continue

            self.checkForCategorySelect()

            if self.checkForDisconnected():
                gameOn = False
                self.driver.quit()

            sleep(5)


class Fibbage2(FibbagePlayer):
    def play(self):
        gameOn = True
        gameStarted = False
        while(gameOn):
            if not gameStarted:
                self.checkForSoundSelect()
                self.checkForEveryoneIn()
            
            if self.checkForLie() or self.checkForVote():
                gameStarted = True
                sleep(10)
                continue

            self.checkForCategorySelect()

            if self.checkForDisconnected() or self.checkForPlayAgain():
                gameOn = False
                self.driver.quit()

            sleep(5)   