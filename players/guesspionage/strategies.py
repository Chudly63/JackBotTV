import random
from players.player import Player
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from re import findall, match


#Guesses a random percentage
class RandomGuesser(Player):

    def __init__(self, driver):
        self.driver = driver

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
                    if(random.randint(0,2) == 1):
                        self.driver.find_element_by_id("pollposition-submitpercentage").click()
                        return True

        except Exception as e:
            print(e)
            pass

        return False


#Always hovers around the 50% mark
class SafeGuesser(Player):

    def __init__(self, driver):
        self.driver = driver

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
class WildGuesser(Player):

    def __init__(self, driver):
        self.driver = driver

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
            print(e)
            pass

        return False



# VOTING STRATEGIES


#Votes for a random option
class RandomVoter(Player):

    def __init__(self, driver):
        self.driver = driver

    def makeVote(self):
        self.clickRandom("pollposition-high-low-button")

#Votes for the option with the highest probability of being correct
class MajorityVoter(Player):

    def __init__(self, driver):
        self.driver = driver

    def makeVote(self):
        try:
            elements = self.driver.find_elements_by_class_name("pollposition-text.question-text")
            question = ""
            for element in elements:
                if match("^.*said \d+%.*$", element.text):
                    question = element.text
                    break
            if(len(question) > 0):
                numbers = [int(s) for s in findall(r'\b\d+\b', question)]
                if(len(numbers) > 0):
                    percentage = numbers[-1]
                    if(percentage <= 50):
                        self.voteFor("Higher")
                    else:
                        self.voteFor("Lower")

        except Exception as e:
            print(e)
            pass

        return False

    def voteFor(self, vote):
        try:
            buttons = self.getActiveButtonsByClass("pollposition-high-low-button")
            for button in buttons:
                if button.get_attribute("data-choice")==vote:
                    button.click()
        except Exception as e:
            print(e)
            pass

        return False