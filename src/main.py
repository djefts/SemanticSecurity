"""
Running Experiment on Facebook Account John Keck

Username: TimElvResearch@gmail.com
Password: keckW2323#
"""
from fb_scraper_api import *
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
from dateutil.parser import parse
import datetime

john_permalink = "https://www.facebook.com/john.keck.125"
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
        scroll_down_v2(firefox, 2.0)  # default delay of 0.5 rarely works- extended to support variable environments
        user_info = get_user_information(firefox)
        get_methods(user_info[0])
        get_variables(user_info[0])
        print('\n\n')
        
        john = User(john_name)
        
        # print(user_info)
        for span_text in user_info:
            print(span_text.replace('\n', ' '))
            if "Lives in" in span_text:
                john.lives_in = span_text.split("Lives in ")[1]
            if "From" in span_text:
                john.hometown = span_text.split("From ")[1]
            if "Pronounces name" in span_text:
                john.pronunciation = span_text.split("Pronounces name ")[1]
            if "Born on" in span_text:
                john.birthday = parse(span_text.split("Born on ")[1])
        print("\n\n" + str(john))
    finally:
        # post-run cleanup
        sleep(5)
        firefox.quit()
