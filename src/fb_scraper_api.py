"""
Running Experiment on Facebook Account John Keck

Username: TimElvResearch@gmail.com
Password: keckW2323#

This file contains all the methods and structures necessary to scrape information from an input Facebook page
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import wget
from time import sleep


def get_methods(object, spacing = 40):
    methodList = []
    for method_name in dir(object):
        try:
            if callable(getattr(object, method_name)):
                methodList.append(str(method_name))
        except:
            methodList.append(str(method_name))
    processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in methodList:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                  processFunc(str(getattr(object, method).__doc__)))
        except:
            print(method.ljust(spacing) + '' + ' getattr() failed')
    print('\n\n')


def get_user_information(driver):
    lives_in = ''
    location_from = ''
    hobbies = []
    friends = []
    information = driver.find_elements_by_tag_name('span')
    get_methods(information[0])
    return information


def get_driver(email = 'TimElvResearch@gmail.com', password = 'keckW2323#',
               permalink = 'https://www.facebook.com/john.keck.125'):
    """
    Starts up the Firefox driver and navigates to the input user's Facebook Homepage
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
    print("Firefox driver load success!")
    
    driver.get('https://www.facebook.com/')
    
    username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    
    username_input.clear()
    username_input.send_keys(str(email))
    password_input.clear()
    password_input.send_keys(str(password))
    
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login']")))
    button.send_keys(Keys.RETURN)
    
    sleep(10)
    
    driver.get(permalink)
    
    return driver
