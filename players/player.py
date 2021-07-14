'''
Jackbox Player Class

High-Level class that game-specific classes inherit from.

Contains logic for creating a webdriver, logging into a game,
and other common player functions
'''

from selenium import webdriver
from time import sleep
import random


class Player():
    
    def login(self, code, name):
        self.name = name
        self.driver = webdriver.Firefox()
        self.driver.get("https://jackbox.tv/")
        sleep(1)
        self.driver.find_element_by_id('roomcode').send_keys(code)
        self.driver.find_element_by_id("username").send_keys(name)
        self.driver.find_element_by_id("button-join").click()
        print(f"Player {name} has connected!")
        sleep(2)

    def getActiveButtonsByClass(self, buttonClass):
        try:
            activeButtons = []
            buttons = self.driver.find_elements_by_class_name(buttonClass)
            for button in buttons:
                if button.is_enabled() and button.is_displayed():
                    activeButtons.append(button)
            return activeButtons
        except Exception as e:
            print(e)
            pass

    #Gets a list of buttons with the class name `buttonClass`
    #If the list is not empty, and the buttons are enabled/displayed, click a random one
    def clickRandom(self, buttonClass):
        try:
            buttons = self.getActiveButtonsByClass(buttonClass)
            if(len(buttons) > 0):
                random.choice(buttons).click()
                return True
        except Exception as e:
            print(e)
            pass

        return False

    #Check to see if the "Disconnected" popup appears
    #If so, the game is over
    def checkForDisconnected(self):
        try:
            titles = self.driver.find_elements_by_id("swal2-title")
            for title in titles:
                if "DISCONNECTED" in title.text.upper() and title.is_displayed():
                    print(f"Player {self.name} has disconnected!")
                    return True
        except Exception as e:
            print(e)
            pass


        return False

    #Check to see if the "Everyone's In" button appears on the bot's UI
    #If it does, then the bot will wait for confirmation from the user before starting the game
    def checkForEveryoneIn(self, elementId):
        try:
            everyoneIn = self.driver.find_element_by_id(elementId)
            if(everyoneIn.is_enabled() and everyoneIn.is_displayed()):
                input("Press enter to start the game!")
                everyoneIn.click()
                return True
        except Exception as e:
            print(e)
            pass

        return False