'''
Jackbox Player Class

High-Level class that game-specific classes inherit from.

Contains logic for creating a webdriver, logging into a game,
and other common player functions
'''

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep
import random


class Player():
    
    def login(self, code, name):
        self.name = name
        options = Options()
        options.headless = True
        self.driver = Firefox(options=options)
        self.driver.get("https://jackbox.tv/")
        while(not self.enterDetails(code, name)):
            continue
        while(not self.submitDetails()):
            continue
        print(f"Player {name} has connected!")
        sleep(2)

    def enterDetails(self, code, name):
        try:
            roomcode = self.driver.find_element_by_id('roomcode')
            if not roomcode.get_attribute('value').upper() == code.upper():
                roomcode.clear()
                roomcode.send_keys(code)
            username = self.driver.find_element_by_id("username")
            if not username.get_attribute('value').upper() == name.upper():
                username.clear()
                username.send_keys(name)
            return (roomcode.get_attribute('value').upper() == code.upper() and username.get_attribute('value').upper() == name.upper())
        except Exception as e:
            print(f"Enter Details {e}")

        return False

    def submitDetails(self):
        try:
            join = self.driver.find_element_by_id("button-join")
            if not join.is_enabled():
                return False
            join.click()
            return True
        except Exception as e:
            print(f"Submit details {e}")

        return False

    def filterElementsByAttributeValue(self, elements, attributeName, attributeValue):
        filteredElements = []
        for element in elements:
            if element.get_attribute(attributeName) == attributeValue:
                filteredElements.append(element)

        return filteredElements

    def getDisplayedElements(self, id=None, className=None, attributes=None):
        try:
            displayedElements = []
            elements = []
            if(id):
                elements = self.driver.find_elements_by_id(id)
            if(className):
                elements.extend(self.driver.find_elements_by_class_name(className))
            for element in elements:
                if element.is_displayed():
                    displayedElements.append(element)

            if(attributes):
                for attribute in attributes:
                    if isinstance(attribute, tuple):
                        displayedElements = self.filterElementsByAttributeValue(displayedElements, attribute[0], attribute[1])

            return displayedElements
        except:
            pass

        return []

    #Gets a list of buttons with the class name `buttonClass`
    #If the list is not empty, and the buttons are enabled/displayed, click a random one
    def clickRandom(self, buttonClass):
        try:
            buttons = self.getDisplayedElements(className=buttonClass)
            if(len(buttons) > 0):
                random.choice(buttons).click()
                return True
        except Exception as e:
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
            print(f"Check for disconnected {e}")
            pass


        return False

    #Check to see if the "Everyone's In" button appears on the bot's UI
    #If it does, then the bot will wait for confirmation from the user before starting the game
    def checkForEveryoneIn(self, elementId):
        try:
            everyoneIn = self.driver.find_element_by_id(elementId)
            if(everyoneIn.is_enabled() and everyoneIn.is_displayed()):
                input("=== Press enter to start the game! ===\n")
                everyoneIn.click()
                return True
        except Exception as e:
            print(f"Check for everyone in {e}")
            pass

        return False