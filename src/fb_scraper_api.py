"""
This file contains all the methods and structures necessary to scrape information from an input Facebook page
"""
import random
import regex

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
from time import sleep
from dateutil import parser


def get_name(mystery_object):
    print(type(mystery_object).__name__)


def get_methods(mystery_object, spacing = 40):
    """
    Prints the details for all the methods associated with the Class of the input object
    :param mystery_object: input object
    :param spacing: Space between the method and its description
    :return: None
    """
    print(type(mystery_object).__name__)
    method_list = []
    for method_name in dir(mystery_object):
        try:
            if callable(getattr(mystery_object, method_name)):
                method_list.append(str(method_name))
        except:
            method_list.append(str(method_name))
    process_func = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in method_list:
        try:
            print(str(method.ljust(spacing)) + ' ' + process_func(str(getattr(mystery_object, method).__doc__))[:200])
        except:
            print(method.ljust(spacing) + '\t' + ' getattr() failed')


def get_variables(mystery_object):
    """
    Prints out all the attributes associated with the Class of the input object
    :param mystery_object: input object
    :return: None
    """
    variable_list = []
    for variable_name in dir(mystery_object):
        try:
            if not callable(getattr(mystery_object, variable_name)):
                variable_list.append(str(variable_name))
        except:
            variable_list.append(str(variable_name))
    print(*variable_list, sep = ", ")


def get_user_information(driver, user_link, user_friends_link):
    span_tags = driver.find_elements_by_tag_name('span')
    sleep(1)
    
    span_texts = []
    for span in span_tags:
        try:
            # grab all the text and put it into a list for easy comprehension
            text = span.text
        except StaleElementReferenceException:
            # element can apparently disappear for as-of-yet unknown reasons
            text = ''
        if text is not None and text != '':
            # print("Span:", "{} - '{}'".format(span, text))
            span_texts.append(span.text.replace('\n', ' '))
    
    user_info = {'degrees': [], 'schools': []}
    for span in span_texts:
        # print(span)
        if "Lives in " in span:
            user_info['lives_in'] = span.split("Lives in ")[1]
        if "From " in span:
            user_info['hometown'] = span.split("From ")[1]
        if "Pronounces name " in span:
            user_info['pronunciation'] = span.split("Pronounces name ")[1]
        if "Studies " in span:  # current degree
            user_info['degrees'].append(span.split("Studies ")[1].split(" at")[0])
            user_info['schools'].append(span.split(" at ")[1])
        if "Studied " in span:  # completed degree
            user_info['degrees'].append(span.split("Studied ")[1].split(" at")[0])
            user_info['schools'].append(span.split(" at ")[1])
        if "Went to " in span:  # non-degree education
            user_info['degrees'].append("No degree")
            user_info['schools'].append(span.split("Went to ")[1])
    
    # Get hobbies
    hobbies = get_hobbies(driver)
    print("\n\nHOBBIES:", hobbies)
    user_info['hobbies'] = hobbies
    
    # Get friends
    friends = get_friends(driver, user_friends_link)
    print("\n\nFRIENDS:", friends)
    user_info['friends'] = friends
    
    # Get birthday/year
    driver.get('https://www.facebook.com/john.keck.125/about_contact_and_basic_info')
    about_profile = driver.find_element_by_css_selector("""div[data-pagelet="ProfileAppSection_0"]""")
    basic_info_section = about_profile.find_element_by_css_selector("""div[class=""]""")
    info_list = basic_info_section.text.splitlines()
    gender = -1
    birthday = -1
    birthyear = -1
    for i in range(len(info_list)):
        # go through the info, the label is in the list one index after the data
        element_text = info_list[i]
        if element_text == "Gender":
            gender = i - 1
        if element_text == "Birth date":
            birthday = i - 1
        if element_text == "Birth year":
            birthyear = i - 1
    
    user_info['gender'] = info_list[gender]
    user_info['birthday'] = info_list[birthday]
    user_info['birthyear'] = info_list[birthyear]
    
    print("\nCollected basic information.")
    return user_info


def get_friends(driver, friends_link):
    """
    Navigates to the user's friends page, then searches for spans with the "dir=auto" tag and grabs the list of friends
    
    :param driver: WebDriver object
    :param friends_link: hyperlink to the user's friends page
    :return: list of friends
    """
    sleep(4)
    driver.get(friends_link)
    scroll_down(driver, 5)
    
    friends_element = driver.find_element_by_css_selector("""div[data-pagelet="ProfileAppSection_0"]""")
    links = friends_element.find_elements_by_css_selector("""a[role="link"]""")
    
    # the text elements that are not names
    invalid_names = ['', 'Friends', 'Friend Requests', 'Find Friends']
    friends = []
    for link in links:
        try:
            friend_link = link.get_attribute('href')
            # the first check limits search to just text elements
            # the second check removes those that are not names
            if link.text not in invalid_names:
                if link.text not in friends and 'mutual friend' not in link.text:
                    friend_name = link.text
                    # print((friend_username, friend_link))
                    friends.append((friend_name, friend_link))
        except StaleElementReferenceException:
            pass
    
    return friends


def get_hobbies(driver):
    # load some of the page
    scroll_page_down(driver)
    scroll_page_up(driver)
    sleep(1)
    try:
        # if there are more than ~7 hobbies then there is a "See All" button
        # find the popup button, scroll it into view, then click on it
        hobbies_button = search_css_elements(driver, """div[aria-pressed]""")[0]
        driver.execute_script("window.scrollTo(0, {});".format(hobbies_button.location['y'] - 100))
        hobbies_button.click()
        # there are issues if this doesn't get time to load
        sleep(2)
    except IndexError:
        # no "See All" Hobbies button
        print("Less than 7 hobbies.")
    
    # All hobbies have an emoji right before the hobby in the aria-label's text
    hobbies_elements = search_css_elements(driver, """a[aria-label]""")
    hobbies = []
    for element in hobbies_elements:
        try:
            hobby = element.text.replace('\n', ' ')
            # I hope this never breaks in the future with later Unicode emoji updates
            count = len(regex.findall('[😀-🙏🌀-🗿🚀-🛿☀-➿︀-︀️]', hobby))
            if count > 0:
                hobby = hobby.split(' ', 1)[1]
                if hobby not in hobbies:
                    hobbies.append(hobby)
        except StaleElementReferenceException:
            # we dont usually need to worry about elements that get unloaded...?
            pass
    
    return hobbies


def get_posts(driver, permalink):
    driver.get(permalink)
    scroll_down(driver)
    post_elements = search_css_elements(driver, """div[class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]""")
    # print_elements(post_elements)
    
    posts_text = []
    for element in post_elements:
        if element.text != '':
            posts_text.append(element.text)
    return posts_text


def get_driver():
    """
    Starts up the Firefox driver
    :return: Selenium Firefox WebDriver object and a Selenium Wait object
    """
    # Setup Firefox environment
    rel_dir = os.path.dirname(__file__)
    options = webdriver.FirefoxOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--incognito")
    
    driver = webdriver.Firefox(options = options,
                               executable_path = rel_dir + '/Firefox_Drivers/geckodriver.exe',
                               service_log_path = rel_dir + '/Firefox_Drivers/geckodriver.log')
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(10)
    print("Firefox driver load success!\n\n")
    
    return driver, wait


def facebook_login(driver, wait, email, password, name, username, permalink):
    """
    Logs into Facebook and navigates to the input user's Facebook Page
    
    :param driver: Firefox WebDriver object
    :param wait: Selenium Firefox Wait object
    :param email: Facebook login email
    :param password: Facebook login password
    :param name: The name of the user
    :param username: Facebook-assigned username, found in the user's page link
    :param permalink: Facebook link to the user's page: 'https://www.facebook.com/[facebook username]'
    :return:
    """
    # Log in to Facebook
    driver.get('https://www.facebook.com/')
    email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    
    email_input.clear()
    email_input.send_keys(str(email))
    password_input.clear()
    password_input.send_keys(str(password))
    
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login']")))
    button.send_keys(Keys.RETURN)
    
    wait.until_not(EC.title_contains("Log In or Sign Up"))
    driver.get(permalink)
    wait.until(EC.title_contains("{} | Facebook".format(name)))


def print_elements(elements):
    for element in elements:
        try:
            print("{} ||| '{}'".format(element.get_attribute('innerHTML'), element.text.replace('\n', ' ')))
        except StaleElementReferenceException:
            pass


def get_element_children(element):
    element.find_elements_by_xpath(".//*")


def search_css_elements(driver, css_selector):
    # print("Searching for '{}' elements...".format(css_selector))
    elements = driver.find_elements_by_css_selector(css_selector)
    return elements


def check_clear_popups(driver, wait):
    sleep(2)
    buttons = search_css_elements(driver, """div[role="button"]""")
    for button in buttons:
        if button.text == "Done":
            wait.until(EC.element_to_be_clickable(button)).click()
            return button


def scroll_page_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_page_up(driver):
    driver.execute_script("window.scrollTo(0, 0);")


def scroll_down(driver, scroll_pause_time = 2):
    """Courtesy of https://stackoverflow.com/a/27760083/8705841"""
    sleep(scroll_pause_time)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    sleep(scroll_pause_time / 2.0)
    scroll_page_down(driver)
    sleep(scroll_pause_time / 2.0)
    scroll_page_up(driver)
    sleep(scroll_pause_time / 2.0)
    
    while True:
        try:
            # the presence of this element indicates the user's timeline is not completely loaded
            search_css_elements(driver, """div[class="suspended-feed"]""")[0]
        except IndexError:
            # error means the element was not found. Timeline is loaded
            break
        # print(loading_element)
        # Scroll down to bottom
        scroll_page_down(driver)
        
        # Wait to load page
        # Randomness might help with Facebook bot detection algorithms?
        sleep(random.random() * scroll_pause_time + 2)
        
        # Randomly scroll up
        # This behaviour is necessary because Facebook will shadow-block you if it thinks you are not human
        if random.random() >= .4:
            scroll_page_up(driver)
            sleep(scroll_pause_time / 2.0)
            scroll_page_down(driver)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
