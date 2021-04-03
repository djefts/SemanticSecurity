"""
Running Experiment on Facebook Account John Keck

Username: TimElvResearch@gmail.com
Password: keckW2323#
"""
from fb_scraper_api import *
from time import sleep

user_permalink = "https://www.facebook.com/john.keck.125"
user_page = 'john.keck.125'


class User:
    def __init__(self):
        self.lives_in = ''
        self.location_from = ''
        self.hobbies = []
        self.friends = []


if __name__ == '__main__':
    firefox = get_driver()
    user_info = get_user_information(firefox)
    print(user_info)
    
    sleep(3)
    
    firefox.quit()
