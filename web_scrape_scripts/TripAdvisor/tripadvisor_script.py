#!/usr/bin/env python
# coding: utf-8

# In[120]:


#####################################################################################
# tripadvisor_script.py.py
#
# Script for scraping reviews / comments on a TripAdvisor page.
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 04/24/2019
# Last Modified: 04/24/2019
#####################################################################################


# In[121]:


##### READ ME #######################################################################
#
# This script is able to scrape comments on Facebook posts on a Facebook page's
# "Posts" page where "Facebook page" refers to a company's page on Facebook and
# NOT a user's page/wall, newsfeed, or any other type of Facebook webpage.
#
# This script's code should only be executed at portions at a time due to
# ChromeDriver being unable to open the given webpage all the time.
# Please do not run this script as an executable / as a whole.
#
##### WARNINGS ######################################################################
#
# 1. This script is prone to errors when scraping videos with 2,000+ comments.
#    Videos with 1,500+ comments are iffy...
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
# 3. Please allow the webpage to fully load before moving on.
# 4. Suggestion: After the page loads, please manually pause the video if you do
#    not want it to play while the script runs the next pieces of code.
# 5. Reminder: Please manually scroll down the page past the description to get the
#    first few comments to load before executing the piece of code to scroll to
#    the very bottom of the page.
#
#####################################################################################


# In[122]:


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


# In[154]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the Facebook Page you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the Posts section of the page.
#       Should end with "posts/".
myURL = "https://www.tripadvisor.com/Attraction_Review-g274887-d298971-Reviews-or3000-Danube_River-Budapest_Central_Hungary.html"

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
path_to_folder = "C://Users/kathleen.trinh/Documents/RiverCruiseProject/TripAdvisor/Locations/"

# The first few words you want each output file to include in the beginning in its filename (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
filename_timestamp = "190424"
page_title = "Danube-River"
filename = filename_timestamp + "_TripAdvisor_" + page_title + ".csv"

# Name of Location (CHANGE AS NEEDED)
TripAdvisorLocation = "Danube River"

#####################################################################################


# In[124]:


##### FUNCTIONS FOR PAGE NAVIGATION #################################################

def click_NextPage():
    pagination_element = driver.find_element_by_class_name("unified")
    NextPage_btn = pagination_element.find_elements_by_class_name("nav")[1]
    driver.execute_script("arguments[0].scrollIntoView();", NextPage_btn)
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, -100);")
    time.sleep(0.5)
    NextPage_btn.click()
    
def go_to_next_page(page_num):
    URL_part1 = "https://www.tripadvisor.com/Attraction_Review-g274887-d298971-Reviews-or"
    URL_part2 = str(page_num) + "0"
    URL_part3 = "-Danube_River-Budapest_Central_Hungary.html"
    newURL = URL_part1 + URL_part2 + URL_part3
    # Open URL with a timeout
    try:
        print("[TripAdvisor SCRIPT] Attempting to open URL:", newURL, " ...")
        driver.set_page_load_timeout(timeout_for)
        driver.get(newURL)
        return 0
    except TimeoutException as ex:
        print("[TripAdvisor SCRIPT] TimeoutException has been thrown. " + str(ex))
        return -2
    if driver.current_url == myURL:
        print("[TripAdvisor SCRIPT] Detected that next page redirected to first page")
        return -1

#####################################################################################


# In[125]:


##### FUNCTIONS FOR DATA EXTRACTION #################################################

def click_SeeMore(entry_element):
    try:
        SeeMore_btn = entry_element.find_element_by_class_name("taLnk")
        driver.execute_script("arguments[0].scrollIntoView();", SeeMore_btn)
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(0.5)
        SeeMore_btn.click()
    except NoSuchElementException:
        pass

def get_review_elements():
    review_elements = driver.find_elements_by_class_name("review-container")
    return review_elements

# Username
def get_userName(review_element):
    username_element = review_element.find_element_by_class_name("info_text")
    username = username_element.text
    return username

# Location (optional)
def get_userLocation(review_element):
    location = ""
    try:
        location_element = review_element.find_element_by_class_name("userLoc")
        location = location_element.text
    except NoSuchElementException:
        pass
    return location

# Timestamp
def get_timestamp(review_element):
    timestamp_element = review_element.find_element_by_class_name("ratingDate")
    timestamp = timestamp_element.get_attribute("title")
    return timestamp

# Rating
def get_rating(review_element):
    rating_element = review_element.find_element_by_class_name("ui_bubble_rating")
    rating = "" # rating is after the space after the span class name
    return rating

# Review title
def get_reviewTitle(review_element):
    title_element = review_element.find_element_by_class_name("noQuotes")
    title = title_element.text
    return title

# Review body
def get_reviewBody(review_element):
    body_element = review_element.find_element_by_class_name("partial_entry")
    body_text = body_element.text
    if body_text.endswith("More"):
        click_SeeMore(body_element)
        time.sleep(1)
        body_element = review_element.find_element_by_class_name("partial_entry")
        body_text = body_element.text
        attempts = 3
        while attempts != 0:
            if body_text.endswith("More"):
                time.sleep(attempts)
                body_text = body_element.text
                attempts -= 1
            else:
                attempts = 0
    return body_text

# Date of Experience
def get_DateOfExperience(review_element):
    #DOE_element = review_element.find_element_by_class_name("stay_date_label")
    #DOE = DOE_element.text
    DOE_element = review_element.find_elements_by_class_name("prw_rup")[4]
    DOE_split = DOE_element.text.split()
    DOE = " ".join(DOE_split[3:])
    return DOE

# Number of Helpful Votes on review
def get_reviewNumHelpfulVotes(review_element):
    numHV_element = review_element.find_element_by_class_name("numHelp")
    numHV = numHV_element.text
    if numHV == "":
        return "0"
    return numHV

# Remove Location from Username (if applicable)
def rem_loc_from_username(username, location):
    if username.endswith(location):
        username = username[:-(len(location) + 1)]
    return username

#####################################################################################


# In[155]:


##### FUNCTIONS TO PUT IT ALL TOGETHER ##############################################

def get_reviewData(review_element):
    username = get_userName(review_element)
    location = get_userLocation(review_element)
    if location != "":
        username = rem_loc_from_username(username, location)
    timestamp = get_timestamp(review_element)
    reviewTitle = get_reviewTitle(review_element)
    reviewBody = get_reviewBody(review_element)
    DateOfExperience = get_DateOfExperience(review_element)
    reviewNumHV = get_reviewNumHelpfulVotes(review_element)
    URL = driver.current_url
    reviewData = [TripAdvisorLocation,
                 username,
                 location,
                 timestamp,
                 reviewTitle,
                 reviewBody,
                 DateOfExperience,
                 reviewNumHV,
                 URL]
    return reviewData

def get_reviewDataOnPage(ALL_reviews):
    r_counter = 1
    review_elements = get_review_elements()
    for review_element in review_elements:
        print("[TripAdvisor SCRIPT]\t\t" + str(r_counter) + ". Extracting data for review #" + str(r_counter) + "...")
        reviewData = get_reviewData(review_element)
        ALL_reviews.append(reviewData)
        r_counter += 1
    return ALL_reviews
        
def get_ALL_reviewData():
    ALL_reviews = []
    p_counter = 301
    scraping = True
    while scraping == True:
        print("[TripAdvisor SCRIPT]\t" + str(p_counter) + ". Extracting data for reviews on page #" + str(p_counter) + "...")
        ALL_reviews = get_reviewDataOnPage(ALL_reviews)
        next_result = go_to_next_page(p_counter)
        if next_result < 0:
            scraping = False
        elif p_counter == 400:
            scraping = False
        else:
            p_counter += 1
    print("[TripAdvisor SCRIPT] Stopping scraping")
    return ALL_reviews

#####################################################################################


# In[127]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("[FB SCRIPT] Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[156]:


# NOTE: If you want to get more than just the first few posts:
# 1. Manually log into Facebook in the window Chrome Driver is operating.
# 2. Reload the Facebook page you want to scrape (while logged in).
# This will allow you to view more posts than a user that is not logged in.

# Open URL with a timeout
try:
    print("[TripAdvisor SCRIPT] Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("[TripAdvisor SCRIPT] TimeoutException has been thrown. " + str(ex))


# In[150]:


ALL_reviews = get_ALL_reviewData()


# In[151]:


# Set up column names for output file
col_names = ["Destination",
             "Username",
             "User's Location",
             "Timestamp",
             "Title",
             "Comment",
             "Date of Experience",
             "Helpful Votes",
             "URL"]

# Make Pandas Data Frame object
df = pd.DataFrame(ALL_reviews, columns = col_names)


# In[152]:


print(df)


# In[153]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + filename), index=None, header=True, encoding="utf-8-sig")

