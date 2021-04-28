"""
This file contains all the methods and structures necessary to scrape information from an input Facebook page
"""

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
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


def get_user_information(driver):
    span_tags = driver.find_elements_by_tag_name('span')
    sleep(1)
    
    span_texts = []
    for span in span_tags:
        while True:
            try:
                # grab all the text and put it into a list for easy comprehension
                text = span.text
            except StaleElementReferenceException:
                # element can apparently disappear for as-of-yet unknown reasons
                text = ''
            except NoSuchElementException:
                # element is on a part of the page that hasn't been loaded yet
                # TODO this may cause infinite-looping behaviours
                scroll_down_v2(driver)
                continue
            break
        if text is not None and text != '':
            print("Span:", "{} - '{}'".format(span, text))
            span_texts.append(span.text)

    user_info = {}
    for span in span_texts:
        print(span.replace('\n', ' '))
        if "Lives in " in span:
            user_info['lives_in'] = span.split("Lives in ")[1]
        if "From " in span:
            user_info['hometown'] = span.split("From ")[1]
        if "Pronounces name " in span:
            user_info['pronunciation'] = span.split("Pronounces name ")[1]
        if "Born on " in span:
            user_info['birthday'] = parser.parse(span.split("Born on ")[1])
        # TODO hobbies
        user_info['hobbies'] = []
        # TODO friends
        user_info['friends'] = []
    return user_info


def get_driver(email = 'TimElvResearch@gmail.com', password = 'keckW2323#', username = 'John Keck',
               permalink = 'https://www.facebook.com/john.keck.125'):
    """
    Starts up the Firefox driver and navigates to the input user's Facebook Homepage
    Default parameters are the email/password/website for the Semantic Security test user "John Keck"
    :param username: The name of the user
    :param email: Facebook login email
    :param password: Facebook login password
    :param permalink: https://www.facebook.com/[facebook username]
    :return: Selenium Firefox WebDriver object
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
    wait.until(EC.title_contains("{} | Facebook".format(username)))
    
    return driver, wait


def get_element_children(element):
    element.find_elements_by_xpath(".//*")
    
    
def get_button_elements(driver, css_selector):
    buttons = driver.find_elements_by_css_selector(css_selector)
    print(buttons)


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_down_v2(driver, scroll_pause_time = 0.5):
    """Courtesy of https://stackoverflow.com/a/27760083/8705841"""
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
