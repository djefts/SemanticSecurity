"""
Running Experiment on Facebook Account John Keck

Username: TimElvResearch@gmail.com
Password: keckW2323#
"""
from fb_scraper_api import *
from time import sleep

john_permalink = "https://www.facebook.com/john.keck.125"
john_username = 'john.keck.125'
john_name = "John Keck "


class User:
    def __init__(self):
        self.lives_in = ''
        self.location_from = ''
        self.hobbies = []
        self.friends = []


if __name__ == '__main__':
    firefox, wait = get_driver()
    scroll_down(firefox)
    user_info = get_user_information(firefox)
    get_methods(user_info[0])
    get_variables(user_info[0])
    print('\n\n')
    
    # print(user_info)
    for span_tag in user_info:
        if span_tag.text is not None and span_tag.text != '':
            print("Span:", "{} - '{}'".format(span_tag, span_tag.text))
            children = get_element_children(span_tag)
            try:
                for child in children:
                    print("\t{}".format(child.text))
            except TypeError:
                print("\t<No children>")
    
    sleep(5)
    firefox.quit()
