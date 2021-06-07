"""
Running Experiment on Facebook Account John Keck

Username: TimElvResearch@gmail.com
Password: keckW2323#
"""
from fb_scraper_api import *
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
import datetime

john_permalink = "https://www.facebook.com/john.keck.125"
john_friends_link = "https://www.facebook.com/john.keck.125/friends"
john_username = 'john.keck.125'
john_name = "John Keck"


class User:
    def __init__(self, name):
        self.name = str(name)
        self.pronunciation = ''
        self.lives_in = ''
        self.hometown = ''
        self.birthday = None
        self.hobbies = []
        self.friends = []
    
    def set_information(self, information):
        self.pronunciation = information['pronunciation']
        self.lives_in = information['lives_in']
        self.hometown = information['hometown']
        self.birthday = information['birthday']
        self.hobbies = information['hobbies']
        self.friends = information['friends']
    
    def __str__(self):
        return ("{} ({}) is from '{}', "
                "currently lives in '{}', "
                "and has [{}] hobbies and [{}] friends. "
                "They were born on {}."
                ).format(self.name, self.pronunciation, self.lives_in,
                         self.hometown,
                         len(self.hobbies), len(self.friends),
                         self.birthday.strftime("%x"))


if __name__ == '__main__':
    try:
        firefox, wait = get_driver()
        facebook_login(firefox, wait)
        
        # get_methods(user_info[0])
        # get_variables(user_info[0])
        
        print("Cleared popup:", check_clear_popups(firefox, wait))
        
        # collect basic user information from page
        john = User(john_name)
        user_info = get_user_information(firefox, john_permalink, john_friends_link)
        john.set_information(user_info)
        
        print("\n\n" + str(john))
    
    finally:
        # post-run cleanup
        sleep(5)
        firefox.quit()
