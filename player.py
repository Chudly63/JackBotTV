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
        self.driver = webdriver.Firefox()
        self.driver.get("https://jackbox.tv/")
        sleep(1)
        self.driver.find_element_by_id('roomcode').send_keys(code)
        self.driver.find_element_by_id("username").send_keys(name)
        self.driver.find_element_by_id("button-join").click()
        sleep(5)

    #Gets a list of buttons with the class name `buttonClass`
    #If the list is not empty, and the buttons are enabled/displayed, click a random one
    def clickRandom(self, buttonClass):
        try:
            buttons = self.driver.find_elements_by_class_name(buttonClass)
            if(len(buttons) > 0 and buttons[0].is_enabled() and buttons[0].is_displayed()):
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
                    print("Disconnected - Game Over")
                    return True
        except Exception as e:
            print(e)
            pass


        return False