"""
Running Experiment on Facebook Account John Keck

Username: TimElvResearch@gmail.com
Password: keckW2323#
"""

import calendar
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
        self.gender = 'Apache Attack Helicopter'
        self.birthday = '01-01'  # MM-DD-YYYY
        self.lives_in = ''
        self.hometown = ''
        self.hobbies = []  # list of nouns
        self.friends = []  # list of tuples
        self.degrees = []  # list of strings, index matches schools
        self.schools = []  # list of strings, index matches degrees
        self.fb_posts = []  # list of strings
        
        # Facebook Information:
        self.fb_email = ''
        self.fb_password = ''
        self.fb_username = ''
    
    def set_information(self, information):
        self.pronunciation = information['pronunciation']
        self.gender = information['gender']
        self.birthday = self.parse_birthday(information['birthday'], information['birthyear'])
        self.lives_in = information['lives_in']
        self.hometown = information['hometown']
        self.hobbies = information['hobbies']
        self.friends = information['friends']
    
    def parse_birthday(self, birthday_str, year_str):
        """
        Converts birthday string form "Month_Name 00" to "00-00"
        :param birthday_str: string in the form "Month_Name 00"
        :return: string in the form "MM-DD"
        """
        months_dict = {month: index for index, month in enumerate(calendar.month_name) if month}  # 'August': 9
        month, day = birthday_str.split(' ')
        month_num = str(months_dict[month]).zfill(2)  # left-pad the string with 0's if necessary
        return str(month_num) + '-' + day.zfill(2) + '-' + str(year_str)
    
    def __str__(self):
        string = ("{} ({}) is from '{}', "
                  "currently lives in '{}', "
                  "and has [{}] hobbies and [{}] friends. "
                  ).format(self.name, self.pronunciation, self.hometown,
                           self.lives_in,
                           len(self.hobbies), len(self.friends))
        if len(self.degrees) > 1:
            string += "They have degrees in {} from {}".format(self.degrees, self.schools)
        elif len(self.degrees) > 0:
            string += "They have a degree in {} from {}.".format(self.degrees, self.schools)
        
        return string


def fb_scraper_main(fb_user_information):
    name = fb_user_information['name']
    user = User(name)
    email = user.fb_email = fb_user_information['email']
    password = user.fb_password = fb_user_information['password']
    username = user.fb_username = fb_user_information['username']
    permalink = 'https://facebook.com/' + user.fb_username
    print(permalink, fb_user_information['permalink'])
    try:
        assert permalink == fb_user_information['permalink']
    except AssertionError:
        permalink = 'https://www.facebook.com/' + user.fb_username
        assert permalink == fb_user_information['permalink']
    
    posts = []
    try:
        firefox, wait = get_driver()
        
        friends_permalink = permalink + '/friends'
        
        facebook_login(firefox, wait, email, password, name, username, permalink)
        
        print("Cleared popup:", check_clear_popups(firefox, wait))
        
        # collect basic user information from page
        user_info = get_user_information(firefox, permalink, friends_permalink)
        user.set_information(user_info)
        
        # collect facebook posts text
        user.posts = get_posts(firefox, permalink)
        print("\n\nPOSTS:")
        print('\n'.join(posts))
        
        print("\n\n" + str(user))
    finally:
        # posts-run cleanup
        sleep(5)
        firefox.quit()
    
    return user


if __name__ == '__main__':
    john_fb_login = {'email': 'TimElvResearch@gmail.com',
                     'password': 'keckW2323#',
                     'name': 'John Keck',
                     'username': 'john.keck.125',
                     'permalink': 'https://www.facebook.com/john.keck.125'}
    david_fb_login = {'email': 'dvdjefts27@gmail.com',
                      'password': 'i love maria 2',
                      'name': 'David Jefts',
                      'username': 'david.jefts',
                      'permalink': 'https://www.facebook.com/david.jefts'}
    fb_scraper_main(john_fb_login)
