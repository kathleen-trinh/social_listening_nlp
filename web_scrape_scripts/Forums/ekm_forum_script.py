#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# ekm_forum_script.py
#
# Script for scraping sub-forums/threads on EKM Forum using...
# Homepage URL: https://forum.ekmmetering.com/
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 03/12/2019
# Last Modified: 03/12/2019
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import math
import pandas as pd
import os
import string
import time


# In[267]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the thread you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the first page in the thread
#       and that the string ends with a slash "/"
myURL = "https://forum.ekmmetering.com/viewtopic.php?f=10&t=3215"

# Timeout for __ seconds (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in driver.set_page_load_timeout(timeout_for)
# where the page will timeout after timeout_for seconds.
timeout_for = 60

# Time to sleep for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in function: time.sleep(time_to_sleep)
#       where the code will pause for time_to_sleep seconds, allowing page to load.
#       You may insert this function where needed if script does not run well as is.
time_to_sleep_for = 5

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/MeterProject/EKM_Forum/"

# File name you want to save the file as (CHANGE FIELDS AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name_date = "190313"
forum_code = "f-10_t-3215"
forum_title = "Gas-measurement-conversion-info"
file_name = file_name_date + "_EKM-Forum_" + forum_code + "_" + forum_title + ".csv"

#####################################################################################


# In[4]:


##### FUNCTIONS FOR GENERAL USE #####################################################
# NOTE: Each page appears to display a maximum of 10 posts on the page.

def get_num_posts():
    """
    This function takes in no parameters,
    finds the element that says "x posts" on the page,
    and returns the total number of posts "x" as an integer.
    """
    num_posts = 1
    try:
        num_posts_element = driver.find_element_by_xpath('//*[@id="page-body"]/div[2]/div[3]')
        num_posts_text = num_posts_element.text
        num_posts_text_split = num_posts_text.split()
        num_posts = int(num_posts_text_split[0])
    except NoSuchElementException:
        pass
    return num_posts

def calc_num_pages(num_posts):
    num_pages = math.ceil(num_posts / 10)
    return num_pages


# In[5]:


##### FUNCTIONS FOR DATA EXTRACTION #################################################

# Get post IDs
def get_post_ids():
    """
    This function takes in no parameters,
    finds all elements containing an id with "post_content" on the current page,
    and returns a list of strings of all found elements.
    This function is used to obtain a list:
    ["post_content####", "post_content####", ...]
    """
    id_elements = driver.find_elements_by_xpath("//*[contains(@id, 'post_content')]")
    ids_as_str = []
    for element in id_elements:
        id_str = element.get_attribute("id")
        if id_str.startswith("post_content"):
            ids_as_str.append(id_str)
        else:
            pass
    return ids_as_str

# Get userName
def get_userName(id):
    """
    This function takes in a string (id) in the form of "post_content####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the username of the post's author,
    and returns a string (userName), which is the username.
    """
    userName_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/p/span/strong/a')
    userName = userName_element.text
    return userName

# Get userTimestamp
def get_userTimestamp(id):
    """
    This function takes in a string (id) in the form of "post-#######",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the timestamp (e.g. "Feb 2, 2011") of the post,
    and returns a string (userTimestamp), which is the timestamp of when the post was made.
    Example: "Feb 2, 2011 at 5:15 PM"
    """
    userTimestamp_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/p')
    userTimestamp_text = userTimestamp_element.text
    userTimestamp_split = userTimestamp_text.split()[-6:]
    userTimestamp = " ".join(userTimestamp_split)
    return userTimestamp

# Get userPostTitle
def get_userPostTitle(id):
    userPostTitle_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/h3/a')
    userPostTitle = userPostTitle_element.text
    return userPostTitle

# Get userComment
def get_userComment(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the user's message on the post,
    and returns a string (userComment), which is the main text of the user's message.
    NOTE: This function does not extract any quotes / replies to previous posts.
    """
    userComment_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div')
    userComment = userComment_element.text
    return userComment

# Get data for a single post
def get_post_data(id, URL, userPostNum):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    extracts the data from the different fields on the post,
    and returns a list with the post's data (9 items), such that:
    [postID, userName, userTitle, userBanners, userTimestamp, userEditTimestamp, userPostTitle, userComment, userPostNum]
    Please note that userBanners is a list.
    """
    userName = get_userName(id)
    userTimestamp = get_userTimestamp(id)
    userPostTitle = get_userPostTitle(id)
    userComment = get_userComment(id)
    MyCommentID = "EKMF_" + forum_code + "_Com" + str(userPostNum)
    #post_data = [MyCommentID, id, userName, userTimestamp, userPostTitle, userComment, userPostNum, URL]
    post_data = [MyCommentID, id, userName, userTimestamp, userPostTitle, userComment, URL]
    #print("post_data =", post_data)
    #print()
    return post_data

# Get data for all posts on a single page
def get_post_data_on_page(URL, userPostNum):
    """
    This function takes in no parameters,
    finds all Post IDs on the current page,
    and for each Post ID,
    extracts the data fields for each post corresponding to the Post ID,
    and returns a list of lists (post_data_on_page)
    containing all post data on the current page, such that:
    [[postID, userName, ... userPostNum], ...]
    """
    post_data_on_page = []
    post_ids = get_post_ids()
    counter = 1
    for id in post_ids:
        print(counter, ". Getting post data for Post #" + id[12:] + " ...")
        post_data = get_post_data(id, URL, userPostNum)
        post_data_on_page.append(post_data)
        userPostNum += 1
        counter += 1
    return post_data_on_page


# In[6]:


##### FUNCTIONS TO CHECK DATA #######################################################

def check_num_posts(all_post_data):
    print("---------------------------------------------------------------------------\n")
    print("Checking number of posts...")
    print("\tLength of all_post_data =", len(all_post_data), "   |   Detected num_posts =", num_posts)
    if len(all_post_data) == num_posts:
        return True
    else:
        return False


# In[7]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("---------------------------------------------------------------------------\n")
print("Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[268]:


# Open URL with a timeout, so you don't wait for ads to load
try:
    print("Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("TimeoutException has been thrown. " + str(ex))


# In[269]:


# Get number of posts & calculate number of pages in the forum
print("---------------------------------------------------------------------------\n")
num_posts = get_num_posts()
print("Number of Posts:", num_posts)
num_pages = calc_num_pages(num_posts)
print("Number of Pages:", num_pages, "\n")


# In[270]:


# Get post data on the first page
print("---------------------------------------------------------------------------\n")
print("Getting post data on page 1...")
all_post_data = []
page1_result = get_post_data_on_page(myURL, 1)
for post in page1_result:
    all_post_data.append(post)
print("Finished getting post data on page 1")
print("Length of all_post_data =", len(all_post_data), "\n")


# In[271]:


# If there is more than 1 page in the sub-forum,
# go through each page and extract the post data for each post on each page.
# Else, if there is only 1 page in the sub-forum,
# do nothing.
print("---------------------------------------------------------------------------\n")
print("Checking if there is more than 1 page...")
if num_pages > 1:
    print("More than 1 page detected\n")
    pageNav = 10
    for page in range(2, (num_pages + 1)):
        try:
            print("---------------------------------------------------------------------------\n")
            print("Attempting to open page:", page, "...")
            driver.set_page_load_timeout(timeout_for)
            nextPageURL = myURL + "&start=" + str(pageNav)
            driver.get(nextPageURL)
            print("Waiting for", time_to_sleep_for, "seconds to allow page to load.")
            print("Please manually reload page, if necessary.")
            time.sleep(time_to_sleep_for)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
        finally:
            print("Getting post data on page", page, "...")
            result = get_post_data_on_page(nextPageURL, pageNav + 1)
            for post in result:
                all_post_data.append(post)
            pageNav += 10
            print("Finished getting post data on page", page)
            print("Length of all_post_data =", len(all_post_data), "\n")
else:
    print("Only 1 page detected\n")
    pass


# In[272]:


# Check number of posts
check_num_posts_result = check_num_posts(all_post_data)
print("Length of all_posts_data equals Last post #? --", check_num_posts_result, "\n")
if check_num_posts_result == False:
    print("\tPlease re-run script from the beginning.")
print("---------------------------------------------------------------------------\n")


# In[273]:


##### MAKE PANDAS DATA FRAME OBJECT #################################################
col_names = ['My Comment ID', 'Post ID', 'Username', 'Timestamp', 'Post Title', 'Comment', 'URL']
df = pd.DataFrame(all_post_data, columns = col_names)

print(df)


# In[274]:


df


# In[275]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + file_name), index = None, header=True, encoding='utf-8-sig')

#####################################################################################

