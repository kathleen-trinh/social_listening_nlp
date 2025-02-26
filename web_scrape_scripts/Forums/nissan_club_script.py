#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# nissan_club_script.py
#
# Script for scraping sub-forums on https://www.nissanclub.com/ using...
# Homepage URL: https://www.nissanclub.com/
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 2.1
# Date Created: 01/30/2019
# Last Modified: 02/26/2019
#####################################################################################

#####################################################################################
#
# V2.0 Notes:
#
# 1. Separated a) opening Chrome Driver and b) attempt to open URL
#    into two sections to allow faster URL change.
# 2. Added column "Thread Title" to output, which is a string  
#    containing the title of the thread the post belongs to.
#
# V2.1 Notes:
#
# 1. Added lines that will add a custom comment ID for each Reddit comment scraped
#    for a project. It will be contained in the "My Comment ID" column of the
#    Pandas data frame.
#
#####################################################################################

#####################################################################################
#
# READ ME
#
# This script is able to scrape sub-forums on https://www.nissanclub.com/,
# using Selenium and ChromeDriver to navigate through multiple pages on the sub-forum
# and the Pandas package to organize the data to output a .csv file.
#
# YOU NEED THESE INSTALLED:
# 1. Python ver. 3.x
# 2. Selenium
# 3. Chromedriver
# 4. Pandas (a Python package)
#
#####################################################################################
#
# CODE OVERVIEW -- This script...
#
# 1. Sets up the ChromeDriver to open a new Chrome browser window.
# 2. Navigates to the given URL, which should be the 1st page of a sub-forum on
#    https://www.nissanclub.com/
# 3. Obtains each post data on the 1st page and adds the data to a global list.
# 4. Clicks on an arrow to open a "Go to Page" pop-up box.
# 5. Inputs the next page number into the text box and hits ENTER as a key.
# 6. Loads the next page and obtains each post data on that page.
# 7. Steps 4-6 are repeated for all consequent pages.
# 8. Makes a data frame using Pandas with the obtained post data.
# 9. Outputs a .csv file containing the post data.
#
#####################################################################################
#
# A FEW WARNINGS...
#
# Once chromedriver starts, please put the window on another desktop monitor or
# such that your mouse will NOT hover over the page. It is important to NOT let
# your mouse hover over the page while the script is navigating to the other pages
# on the sub-forum, as the "Go to Page" pop-up dialog box may disappear if you
# hover over something else, interfering with page number input into the text box.
# If your mouse DOES hover over the page and the next page does not load as
# expected, please restart the script from the beginning to obtain accurate results.
#
# This site contains many ads and may have trouble fully loading the page within
# a considerable amount of time, thus, a timeout is in place to allow the code to
# move on without waiting for the page to load all of its contents.
# As a result, the terminal will print error messages regarding the timeout, but
# please disregard them, as it is simply a sign that the code is moving on
# in this script.
#
# This script may not work as expected on every try due to Internet connectivity
# and other loading errors, so it is vital that the user pays attention to the
# chromedriver window and terminal outputs (print statements) as the code is running.
#
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
import re
import os
import time
#####################################################################################


# In[80]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the sub-forum you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the very first page in the sub-forum
myURL = "https://www.nissanclub.com/forums/new-2019-nissan-altima-discussion/516779-altima-reverses-while-neutral.html"

# Timeout for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in driver.set_page_load_timeout(timeout_for)
# where the page will timeout after timeout_for seconds.
# The timeout is needed to move on with the script, as the page will take
# a long time to load, and we only need the text on the page to load.
timeout_for = 120

# Time to sleep for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in function: time.sleep(time_to_sleep)
# where the code will pause for time_to_sleep seconds, allowing page to load.
# You may insert this function where needed if script does not run well as is.
time_to_sleep_for = 5

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/Nissan/NissanAltimaGapAnalysis/NissanClub/"

# File name you want to save the file as (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name = "190226_nissanclub_Nissan-Altima-Forums_Altima-Reverses-While-in-Neutral.csv"

# Title of the thread (CHANGE AS NEEDED)
# Type: string
threadTitle = "Altima Reverses While in Neutral"

#####################################################################################


# In[4]:


##### FUNCTIONS FOR GENERAL USE #####################################################

def get_num_results(id):
    """
    This function takes in a string (id),
    gets the Post Number ("post #x of y") of the post,
    and returns the total number of posts "y" as an integer.
    """
    postNum_element = driver.find_elements_by_xpath('//*[@id="postcount' + id + '"]')[0]
    postNum = postNum_element.text
    num_results = postNum.split()[-1]
    return int(num_results)

def check_num_results(results, num_results):
    """
    This function takes in a list (results) and an integer (num_results)
    and returns True if the length of the list is equal to the given integer.
    It returns False otherwise.
    This function is used to check if the length of the list containing all post data
    is equal to the total number of posts the sub-forum claims to have.
    """
    if len(results) == num_results:
        return True
    else:
        return False


# In[5]:


def get_num_pages():
    """
    This function takes in no parameters,
    finds the element that says "Page x of y" on the page,
    and returns the total number of pages "y" as an integer.
    NOTE: The line of code containing the XPath runs into an error
    when the sub-forum consists of only 1 page.
    """
    pages_element = driver.find_elements_by_xpath('//*[@id="fixed-controls"]/div/span[1]/div/table/tbody/tr/td[1]')[0]
    pages_text = pages_element.text
    pages_text_split = pages_text.split()
    num_pages = pages_text_split[-1]
    return int(num_pages)


# In[6]:


##### FUNCTIONS FOR PART 1: FIND ALL POST IDs #######################################

# XPath REFERENCES for each data field we want to extract for each post
# NOTE: It appears that each post has its own ID as "postmenu_#######"
# Poster's userID XPath: //*[@id="postmenu_4748554"]/a
# Poster's post date XPath: //*[@id="post4748554"]/div[1]/span[2]
# Poster's comment XPath: //*[@id="post_message_4748554"]
# Poster's Post # XPath: //*[@id="postcount4748554"]/strong


# In[7]:


# Step 1 in order to find ALL post IDs:
# Get ALL id tags on page
def get_all_ids_on_page():
    """
    This function takes in no parameters,
    finds all elements containing an id with "postmenu" on the current page,
    and returns a list of strings of all found elements.
    This function is used to obtain a list:
    ["postmenu_#######", "postmenu_#######", ...]
    """
    ids_on_page = driver.find_elements_by_xpath("//*[contains(@id, 'postmenu')]")
    ids_as_str = []
    for i in ids_on_page:
        ids_as_str.append(i.get_attribute('id'))
    return ids_as_str


# In[8]:


# Step 2 in order to find ALL post IDs:
# Find ONLY post IDs ("postmenu_#######") using regular expression
# NOTE: Don't really need this function because it appears that ALL id tags on the page
# that contain "postmenu" are associated with a user's post and not anything else on the page.
def get_all_postmenu_ids(ids_list):
    """
    This function takes in a list of strings (ids_list),
    iterates through each string in the list and
    uses a regular expression to find the number in the string.
    It returns a list of strings (post_ids_as_str)
    in which each string is a unique number corresponding to a post on the page.
    """
    post_ids_as_str = []
    for id in ids_list:
        matchObj = re.match( '^(postmenu_[0-9]*)$', id, flags=0)
        #print("Checking: ", id)
        if matchObj:
            #print("Found match: ", id)
            post_ids_as_str.append(id)
        else:
            #print("Doesn't match: ", id)
            pass
    return post_ids_as_str


# In[9]:


# Step 3 in order to find ALL post IDS:
# Find ONLY the post number in the id tag
# Then convert results (list of str) to int (list of int)

def get_num(mystr):
    """
    This function takes in a string (mystr)
    and uses a regular expression to find the number in the string.
    It returns a string (number_str[0]),
    which should only be the number found in the string.
    """
    number_str = re.findall('\d+', mystr)
    return number_str[0]

def get_post_ids_as_num(ids_to_convert):
    """
    This function takes in a list of strings (ids_to_convert),
    iterates through each string in the list to find the number in each string,
    and returns a list of string (result),
    which should only contain strings that are numbers.
    """
    result = []
    for id in ids_to_convert:
        result.append(get_num(id))
    return result


# In[10]:


# Function to combine Steps 1, 2, and 3 above
def get_all_post_ids():
    """
    This function takes in no parameters
    and simply calls the 3 functions needed for Steps 1, 2, and 3
    to obtain all Post IDs on the current page.
    """
    ids_as_str = get_all_ids_on_page()
    post_ids_as_str = get_all_postmenu_ids(ids_as_str)
    post_ids = get_post_ids_as_num(post_ids_as_str)
    return post_ids


# In[11]:


##### FUNCTIONS FOR PART 2: EXTRACTING POST DATA ####################################

# Get userID
def get_userID(id):
    """
    This function takes in a string (id),
    which should be the Post ID of a post on the page,
    finds the element corresponding to the username of the post's author,
    and returns a string (userID), which is the username.
    """
    userID_element = driver.find_elements_by_xpath('//*[@id="postmenu_' + id + '"]/a')[0]
    userID = userID_element.text
    return userID


# In[12]:


# Get userDate
def get_userDate(id):
    """
    This function takes in a string (id),
    which should be the Post ID of a post on the page,
    finds the element corresponding to the timestamp of the post,
    and returns a string (userDate), which is the post's timestamp.
    Example: "11-17-2013, 03:19 PM"
    """
    userDate_element = driver.find_elements_by_xpath('//*[@id="post' + id + '"]/div[1]/span[2]')[0]
    userDate = userDate_element.text
    return userDate


# In[13]:


# Get userComment
def get_userComment(id):
    """
    This function takes in a string (id),
    which should be the Post ID of a post on the page,
    finds the element corresponding to the user's message on the post,
    and returns a string (userComment), which is the main text of the user's message.
    NOTE: This function does not extract any quotes / replies to previous posts.
    """
    userComment_element = driver.find_elements_by_xpath('//*[@id="post_message_' + id + '"]')[0]
    userComment = userComment_element.text
    return userComment


# In[14]:


# Get userPostNum (post # in sub-forum)
def get_userPostNum(id):
    """
    This function takes in a string (id),
    which should be the Post ID of a post on the page,
    finds the element corresponding to the Post # ("post #x of y"),
    and returns a string (userPostNum) in the format "post #x of y".
    """
    userPostNum_element = driver.find_elements_by_xpath('//*[@id="postcount' + id + '"]/strong')[0]
    userPostNum = userPostNum_element.text
    return userPostNum


# In[24]:


# Get data for all posts on a single page and add them to the list
def get_post_data_on_page():
    """
    This function takes in no parameters,
    finds all Post IDs on the current page,
    and for each Post ID,
    extracts the data fields for each post corresponding to the Post ID,
    and returns a list of lists (post_data_on_page)
    containing all post data on the current page, such that:
    [[postID, userID, userDate, userComment, userPostNum], ...]
    """
    post_data_on_page = []
    post_ids = get_all_post_ids()
    i = 0
    for postID in post_ids:
        MyCommentID = "NC_" + postID + "_Com" + str(i)
        userID = get_userID(postID)
        userDate = get_userDate(postID)
        userComment = get_userComment(postID)
        userPostNum = get_userPostNum(postID)
        post_data = [MyCommentID, postID, threadTitle, userID, userDate, userComment, userPostNum]
        post_data_on_page.append(post_data)
        i += 1
    return post_data_on_page


# In[16]:


##### FUNCTIONS FOR CHECKING DATA AFTER EXTRACTION ##################################

def print_post_data(post_data):
    """
    This function takes in a list of lists (post_data),
    iterates through each list (data for a single post) in the list,
    and prints out the contents to the terminal.
    This function may be used for searching for errors in the data retrieval process.
    """
    print("\n\n\n-------------------------------- POST DATA --------------------------------")
    for post in all_post_data:
        print(post)
        print("---------------------------------------------------------------------------")

def print_check_num_posts(post_data, num_results):
    """
    This function takes in a list of lists (post_data) and an int (num_results)
    where post_data should be the global list containing all post data
    and num_results is the number of posts in the sub-forum,
    checks if the length of the given list is equal to the number of posts in the sub-forum,
    prints the result to the terminal,
    and returns a Boolean True or False.
    """
    result = check_num_results(post_data, num_results)
    print("Length of posts is correct? --", result)
    return result

#####################################################################################


# In[17]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[81]:


# Open URL with a timeout, so you don't wait for ads to load
try:
    print("Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("TimeoutException has been thrown. " + str(ex))
    


# In[82]:


# Global variable to hold each post data on all pages
# Type: list of lists such that: [[postID, userID, userDate, userComment, userPostNum], ...]
all_post_data = []

# Get page 1's posts
print("Getting post data on page 1...")
page1_result = get_post_data_on_page()
for post in page1_result:
    all_post_data.append(post)
print("Finished getting post data on page 1\n")


# In[83]:


print("---------------------------------------------------------------------------\n")
# Get number of all posts in sub-forum and print the result to the terminal
num_results = get_num_results(all_post_data[0][0])
print("Number of Results:", num_results)

# Get number of pages in sub-forum and print the result to the terminal
# MAX number of posts on 1 page = 15
num_pages = 1
if num_results > 15:
    num_pages = get_num_pages()
print("Number of Pages:", num_pages)
print("\n---------------------------------------------------------------------------\n")


# In[84]:


# XPath REFERENCES for elements needed to go to Next Page
# XPath to open "Go to Page..." pop-up: //*[@id="pagenav.16"]
# XPath to text input box: //*[@id="pagenav_itxt"]

# If there is more than 1 page in the sub-forum,
# go through each page and extract the post data for each post on each page.
# Else, if there is only 1 page in the sub, forum,
# do nothing.
print("Checking if there is more than 1 page...")
if num_pages > 1:
    print("More than 1 page detected")
    print("---------------------------------------------------------------------------")
    for page in range(1, num_pages):
        try:
            print("Attempting to open page:", (page + 1), "...")
            GoToPage_element = driver.find_elements_by_xpath("//*[contains(@id, 'pagenav.')]")[0]
            GoToPage_element.click()
            time.sleep(time_to_sleep_for)
            input_element = driver.find_element_by_id("pagenav_itxt")
            input_element.send_keys(str(page + 1))
            input_element.send_keys(Keys.ENTER)
        except TimeoutException as ex:
            isLoading = 0
            print("Exception has been thrown. " + str(ex))
        finally:
            print("Getting post data on page", (page + 1), "...")
            result = get_post_data_on_page()
            for post in result:
                all_post_data.append(post)
            print("Finished getting post data on page", (page + 1))
            print("---------------------------------------------------------------------------")
else:
    print("Only 1 page detected")
    print("---------------------------------------------------------------------------\n")
    pass
    


# In[85]:


print_check_num_posts(all_post_data, num_results)
print("Note: If False, please re-run the script from the beginning (starting the ChromeDriver).")

#####################################################################################


# In[86]:


##### MAKE PANDAS DATA FRAME OBJECT #################################################
col_names = ['My Comment ID', 'Post ID', 'Thread Title', 'User ID', 'Timestamp', 'Post', 'Post #']
df = pd.DataFrame(all_post_data, columns = col_names)

print(df)


# In[87]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + file_name), index = None, header=True)

#####################################################################################


# In[64]:


# Close ChromeDriver
driver.close()

