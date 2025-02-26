#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# instagram_script.py
#
# Script for scraping comments off posts on an Instagram page / account.
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 04/25/2019
# Last Modified: 04/29/2019
#####################################################################################


# In[2]:


##### READ ME #######################################################################
#
# This script is able to scrape comments off posts on an Instagram page / account.
#
# This script's code should only be executed at portions at a time due to
# ChromeDriver being unable to open the given webpage all the time.
# Please do not run this script as an executable / as a whole.
#
##### WARNINGS ######################################################################
#
# 1. This script is prone to errors when Instagram pages fail to load on the first
#    attempt to go to a URL.
# 2. Please do not scroll or click anywhere on the browser window where ChromeDriver
#    is operating while the script is trying to click buttons or extract data.
#
##### READ ME (continued) ###########################################################
#
# Before running this script:
# 1. Change the values of the global variables in the "GLOBAL VARIABLES" section
#    as necessary. Please read the notes attached to each when changing the value.
# 2. Reminder: If you change the value of any of the global variables, please
#    re-run the "GLOBAL VARIABLES" section before executing any code that uses
#    the global variable you changed or updated.
#
# When running this script:
# 1. Messages will print out to the terminal to indicate where the code is
#    currently at during execution.
# 2. If the webpage does not load when ChromeDriver starts, please manually
#    reload the page in the same window until the webpage loads. If the webpage
#    is appearing to take a long time to load, please try manually refreshing the
#    page until it loads.
#
#####################################################################################


# In[3]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import re
import string
import time
#####################################################################################


# In[40]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of Instagram's home page / domain (CHANGE AS NEEDED)
# Type: string
IG_URL = "https://www.instagram.com/"

# Timeout for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in driver.set_page_load_timeout(timeout_for)
# where the page will timeout after timeout_for seconds.
# The timeout is needed to move on with the script, as the page will take
# a long time to load, and we only need the text on the page to load.
timeout_for = 60

# Time to sleep for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in function: time.sleep(time_to_sleep)
# where the code will pause for time_to_sleep seconds, allowing page to load.
# You may insert this function where needed if script does not run well as is.
time_to_sleep_for = 3

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/Nissan/Instagram/"

# The first few words you want each output file to include in the beginning in its filename (CHANGE AS NEEDED)
# Type: string
# Note: The full filename is generated later through the use of the function make_filename().
filename_timestamp = "190429"
account_name = "nissanusa"

# URL of the Instagram account whose posts you want to scrape
# Type: string
IG_account_URL = IG_URL + account_name + "/"

# Flag used to indicate whether or not comments made by the account should be included in the output
# Type: Boolean
get_account_comments = True

#####################################################################################


# In[41]:


##### FUNCTIONS FOR PAGE NAVIGATION, SCROLLING, CLICKING ############################

def go_to_URL(URL):
    try:
        print("[IG SCRIPT] Attempting to open URL:", URL, "...")
        driver.set_page_load_timeout(timeout_for)
        driver.get(URL)
        return 0
    except TimeoutException as ex:
        print("[IG SCRIPT] TimeoutException has been thrown. " + str(ex))
        return -1

def scroll_to_bottom(scroll_inc, scroll_count):
    print("[IG SCRIPT] Scrolling to bottom of page " + str(scroll_inc) + " times...")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(0, scroll_inc):
        print("[IG SCRIPT]\t" + str(i+1) + ". Scrolling...")
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        # Wait to load page
        time.sleep(time_to_sleep_for)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if last_height == new_height:
            print("[IG SCRIPT] Bottom of page detected. If content is not loading, please wait and try again or reload page.")
        else:
            scroll_count += 1
    print("[IG SCRIPT] Finished scrolling to bottom of page")
    print("[IG SCRIPT] --------------------------------------------------------------------------")
    return scroll_count

# Add function that calls above function repeatedly depending on user input
def scroll_to_bottom_wInput():
    scroll_count = 0
    scroll = True
    while scroll == True:
        user_command = input("[IG SCRIPT] Scroll down page? y/n > ")
        if user_command == "y":
            print("[IG SCRIPT]\tYou entered:'" + user_command + "'")
            scroll_inc = input("[FB SCRIPT] Scroll down how many times? (Please enter a positive integer.) > ")
            # Add while and try/except blocks for input error handling
            print("[IG SCRIPT]\tYou entered:'" + scroll_inc + "'")
            print("[IG SCRIPT] --------------------------------------------------------------------------")
            scroll_count = scroll_to_bottom(int(scroll_inc), scroll_count)
            print("[IG SCRIPT] Total scroll count: ", scroll_count)
        elif user_command == "n":
            print("[IG SCRIPT]\tYou entered:'" + user_command + "'. Proceeding with rest of script...")
            print("[IG SCRIPT] --------------------------------------------------------------------------")
            scroll = False
        else:
            print("[IG SCRIPT]\tInput not recognized.")
            
def click_LoadMoreComments_btn(comment_section_element, counter):
    try:
        LoadMoreComments_btn = comment_section_element.find_element_by_class_name("Z4IfV")
        driver.execute_script("arguments[0].scrollIntoView();", LoadMoreComments_btn)
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(0.5)
        print("[IG SCRIPT]\t" + str(counter) + ". Clicking 'Load more comments' / 'View all comments' button on post...")
        LoadMoreComments_btn.click()
        time.sleep(0.5)
        return 0
    except NoSuchElementException:
        print("[IG SCRIPT]\tDid not detect 'View all comments' button on post")
        return -1

def click_LoadMoreComments():
    print("[IG SCRIPT] Finding and clicking 'Load more comments' / 'View all comments' buttons...")
    comment_section_element = driver.find_element_by_class_name("KlCQn")
    counter = 1
    click_btn_result = click_LoadMoreComments_btn(comment_section_element, counter)
    while click_btn_result == 0:
        counter += 1
        click_btn_result = click_LoadMoreComments_btn(comment_section_element, counter)
    print("[IG SCRIPT] Finished attempt to find and click 'Load more comments' / 'View all comments' buttons")
    
#####################################################################################


# In[42]:


##### FUNCTIONS FOR DATA EXTRACTION #################################################

def get_post_elements():
    print("[IG SCRIPT] Getting post elements...")
    post_elements = driver.find_elements_by_class_name("v1Nh3")
    print("[IG SCRIPT]\tDetected " + str(len(post_elements)) + " post elements on page")
    return post_elements

# NOTE: In HTML, links appear as relative paths, but
#       when retrieved using Selenium, they appear as absolute paths.

def get_post_links(post_elements):
    print("[IG SCRIPT] Retrieving post links from post elements...")
    post_links = []
    for post_element in post_elements:
        post_link = post_element.find_element_by_xpath(".//a[@href]").get_attribute("href")
        post_links.append(post_link)
    return post_links

def get_comment_elements():
    print("[IG SCRIPT] Getting comment elements...")
    comment_elements = []
    try:
        comment_elements = driver.find_elements_by_class_name("C4VMK")
        print("[IG SCRIPT]\tDetected " + str(len(comment_elements)) + " comment elements")
    except NoSuchElementException:
        print("[IG SCRIPT]\tDetected NO comment elements")
    return comment_elements

def get_username(comment_element):
    username_element = comment_element.find_element_by_class_name("_6lAjh")
    username = username_element.text
    return username

def get_comment(comment_element):
    comment_element = comment_element.find_element_by_tag_name("span")
    comment = comment_element.text
    return comment

def get_comment_data(comment_element, post_URL):
    post_code = post_URL.split("/")[-2]
    username = get_username(comment_element)
    comment = get_comment(comment_element)
    return [post_code,
            username,
            comment,
            post_URL]

def get_comment_data_on_post(post_URL):
    go_to_URL_result = go_to_URL(post_URL)
    if go_to_URL_result < 0:
        print("[IG SCRIPT] Error occurred trying to load:", IG_URL, "-- Please try again")
        return -1
    click_LoadMoreComments()
    time.sleep(time_to_sleep_for)
    ALL_comment_data = []
    comment_elements = get_comment_elements()
    counter = 1
    for comment_element in comment_elements:
        print("[IG SCRIPT]\t" + str(counter) + ". Getting comment data for comment #" + str(counter) + " ...")
        comment_data = get_comment_data(comment_element, post_URL)
        ALL_comment_data.append(comment_data)
        counter += 1
    make_output_file(ALL_comment_data, post_URL)
    return 0

def get_comment_data_on_ALL_posts(post_links):
    counter = 1
    for post_link in post_links:
        print("[IG SCRIPT] " + str(counter) + ". Getting comment data for post: " + post_link + " ...")
        result = get_comment_data_on_post(post_link)
        print()
        if result < 0:
            print("[IG SCRIPT] " + str(counter) + ". Error occurred trying to get comment data for post: " + post_link + " -- Stopping data extraction process")
            break
        counter += 1

#####################################################################################


# In[43]:


##### FUNCTIONS FOR DATA OUTPUT #####################################################

def make_filename(post_URL):
    post_code = post_URL.split("/")[-2]
    filename = filename_timestamp + "_Instagram_" + account_name + "_" + post_code + ".csv"
    return filename

def make_dataframe(data):
    # Set up column names for output file
    col_names = ["Post Code",
                "Username",
                "Comment",
                "URL"]
    # Make Pandas Data Frame object
    df = pd.DataFrame(data, columns = col_names)
    return df

def make_output_file(data, post_URL):
    filename = make_filename(post_URL)
    df = make_dataframe(data)
    # Export Pandas Data Frame object to a .csv file
    df.to_csv((path_to_folder + filename), index=None, header=True, encoding="utf-8-sig")

#####################################################################################


# In[33]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("[IG SCRIPT] Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[44]:


go_to_URL_result = go_to_URL(IG_account_URL)
if go_to_URL_result < 0:
    print("[IG SCRIPT] Error occurred trying to load:", IG_URL, "-- Please try again")


# In[45]:


scroll_to_bottom_wInput()


# In[46]:


post_elements = get_post_elements()
post_links = get_post_links(post_elements)


# In[47]:


get_comment_data_on_ALL_posts(post_links)


# In[37]:


go_to_URL("https://www.instagram.com/p/BwK1BMbnYnR/")


# In[38]:


comment_section = driver.find_element_by_class_name("KlCQn")


# In[39]:


click_LoadMoreComments()


# In[22]:


go_to_URL_result = go_to_URL(post_links[2])


# In[ ]:


comment_elements = get_comment_elements()


# In[ ]:


for CE in comment_elements:
    username = get_username(CE)
    print("username =", username)
    comment = get_comment(CE)
    print("comment =", comment)
    print()

