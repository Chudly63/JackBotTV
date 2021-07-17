import random
from players.player import Player
from selenium.webdriver.common.action_chains import ActionChains
from time import perf_counter, sleep
from re import findall, match


class Guesser(Player):

    def __init__(self, driver):
        self.driver = driver

    def makeGuess(self):
        pass

    def describe(self):
        return "has no identity"

#Guesses a random percentage
class RandomGuesser(Guesser):

    def describe(self):
        return "guesses as the winds guide them"

    def makeGuess(self):
        try:
            wheel = self.driver.find_element_by_id("pollposition-percentage-picker")

            if(wheel.is_displayed()):
                while(True):
                    offset1 = random.randint(0,int(wheel.size["width"]))
                    offset2 = random.randint(0,int(wheel.size["height"]))
                    action = ActionChains(self.driver)
                    action.move_to_element_with_offset(wheel, offset1, offset2)
                    action.click()
                    action.perform()
                    sleep(3)
                    if(random.randint(0,2) < 2):
                        self.driver.find_element_by_id("pollposition-submitpercentage").click()
                        return True

        except Exception as e:
            print(e)
            pass

        return False


#Always hovers around the 50% mark
class SafeGuesser(Guesser):

    def describe(self):
        return "runs it down the middle"

    def makeGuess(self):
        try:
            wheel = self.driver.find_element_by_id("pollposition-percentage-picker")

            if(wheel.is_displayed()):
                nudge = int(wheel.size["width"] / 40)
                offset1 = int(wheel.size["width"] / 2 + random.randint(nudge * -1, nudge))
                offset2 = int(wheel.size["height"] * 2 / 3)
                action = ActionChains(self.driver)
                action.move_to_element_with_offset(wheel, offset1, offset2)
                action.click()
                action.perform()
                sleep(3)
                self.driver.find_element_by_id("pollposition-submitpercentage").click()
                return True

        except Exception as e:
            print(e)
            pass

        return False


#Always guesses > 75% or < 25%
class WildGuesser(Guesser):

    def describe(self):
        return "loves chaos"

    def makeGuess(self):
        try:
            wheel = self.driver.find_element_by_id("pollposition-percentage-picker")

            if(wheel.is_displayed()):
                offset1 = random.randint(0,int(wheel.size["width"]))
                offset2 = random.randint(0,int(wheel.size["height"] / 2))
                action = ActionChains(self.driver)
                action.move_to_element_with_offset(wheel, offset1, offset2)
                action.click()
                action.perform()
                sleep(3)
                self.driver.find_element_by_id("pollposition-submitpercentage").click()
                return True

        except Exception as e:
            print(f"Wild guess {e}")
            pass

        return False


#Keeps changing their guess and never locks in
class IndecisiveGuesser(Guesser):

    def describe(self):
        return "hates commitment"

    def makeGuess(self):
        try:
            wheel = self.driver.find_element_by_id("pollposition-percentage-picker")

            if(wheel.is_displayed()):
                while(True):
                    offset1 = random.randint(0,int(wheel.size["width"]))
                    offset2 = random.randint(0,int(wheel.size["height"]))
                    action = ActionChains(self.driver)
                    action.move_to_element_with_offset(wheel, offset1, offset2)
                    action.click()
                    action.perform()
                    sleep(2)

        except Exception as e:
            print(e)
            return 

        return False



# VOTING STRATEGIES

class Voter(Player):

    def __init__(self, driver):
        self.driver = driver
    
    def makeVote(self):
        pass

    def describe(self):
        return "doesn't partake in politics"

    def getGuessPercentage(self):
        try:
            elements = self.getDisplayedElements(className="pollposition-text.question-text")
            for element in elements:
                if match("^.*said \d+%.*$", element.text):
                    numbers = [int(s) for s in findall(r'\b\d+\b', element.text)]
                    if(len(numbers) > 0):
                        return numbers[-1]
        except Exception as e:
            print(f"Get Guess Percentage {e}")
            pass

        return None

    def voteFor(self, vote):
        try:
            buttons = self.getDisplayedElements(className="pollposition-high-low-button", attributes=[("data-choice", vote)])
            if(len(buttons) == 1):
                buttons[0].click()
                return True
        except Exception as e:
            print(f"Vote For {e}")
            pass

        return False

    def areMuchOptionsAvailable(self):
        try:
            return len(self.getDisplayedElements(className="pollposition-choice-button")) == 4
        except:
            return False

#Votes for a random option
class RandomVoter(Voter):

    def describe(self):
        return "clicks the first button they see"

    def makeVote(self):
        return self.clickRandom("pollposition-high-low-button")


#Votes for the option with the highest probability of being correct
class MajorityVoter(Voter):

    def describe(self):
        return "likes to play it safe"

    def makeVote(self):
        try:
            percentage = self.getGuessPercentage()
            if(percentage == None):
                return False
            elif(percentage <= 50):
                self.voteFor("Higher")
            else:
                self.voteFor("Lower")
            return True

        except Exception as e:
            print(f"Majority Vote {e}")
            pass

        return False


#Always votes much higher or much lower if those options are available
class RiskyVoter(Voter):

    def describe(self):
        return "ain't afraid to double-down"

    def makeVote(self):
        percentage = self.getGuessPercentage()
        if(percentage == None):
            return False
        elif(percentage <= 50):
            if(self.areMuchOptionsAvailable()):
                self.voteFor("Much_Higher")
            else:
                self.voteFor("Higher")
        else:
            if(self.areMuchOptionsAvailable()):
                self.voteFor("Much_Lower")
            else:
                self.voteFor("Lower")
        return True

#Votes up on even responses and down on odd responses
class EvenStevenVoter(Voter):

    def describe(self):
        return "doesn't like your odds"

    def makeVote(self):
        percentage = self.getGuessPercentage()
        if(percentage == None):
            return False
        elif(percentage % 2 == 0):
            self.voteFor("Higher")
        else:
            self.voteFor("Lower")
        return True

#Picks a random percentage, and then votes for whatever option matches it
class RouletteVoter(Voter):

    def describe(self):
        return "is ready to SPIN. THAT. WHEEL!"

    def makeVote(self):
        spin = random.randint(0,100)
        percentage = self.getGuessPercentage()
        if(percentage == None):
            return False
        elif(spin + 15 < percentage and self.areMuchOptionsAvailable()):
            self.voteFor("Much_Lower")
        elif(spin - 15 > percentage and self.areMuchOptionsAvailable()):
            self.voteFor("Mush_Higher")
        elif(spin < percentage):
            self.voteFor("Lower")
        else:
            self.voteFor("Higher")
        return True