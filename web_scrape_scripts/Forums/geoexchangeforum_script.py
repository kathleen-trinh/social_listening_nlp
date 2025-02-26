#!/usr/bin/env python
# coding: utf-8

# In[196]:


#####################################################################################
# geoexchangeforum_script.py
#
# Script for scraping a thread on GeoExchangeForum on...
# GeoExchange Forum URL: https://www.geoexchange.org/forum/
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 02/07/2019
# Last Modified: 02/08/2019
#####################################################################################


# In[197]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import re
import string
import time
#####################################################################################


# In[431]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the thread you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the first page in the thread.
myURL = "https://www.geoexchange.org/forum/threads/geothermal-costs.501/"

# Timeout for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in driver.set_page_load_timeout(timeout_for)
# where the page will timeout after timeout_for seconds.
# The timeout is needed to move on with the script, as the page may take
# a long time to load, and we only need the text on the page to load.
timeout_for = 120

# Time to sleep for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in function: time.sleep(time_to_sleep)
# where the code will pause for time_to_sleep seconds, allowing page to load.
# You may insert this function where needed if script does not run well as is.
time_to_sleep_for = 45

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/GeothermalProject/GeoExchangeForum/"

# File name you want to save the file as (CHANGE FIELDS AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name_date = "190208"
sub_forum = "General-Discussions"
forum_code = "501"
forum_title = "Geothermal-Costs___TEST"
file_name = file_name_date + "_" + sub_forum + "_" + forum_code + "_" + forum_title + ".csv"

#####################################################################################


# In[329]:


##### FUNCTIONS FOR GENERAL USE #####################################################
# NOTE: Each page appears to display a maximum of 20 posts on the page.

def get_num_pages():
    """
    This function takes in no parameters,
    finds the element that says "Page x of y" on the page,
    and returns the total number of pages "y" as an integer.
    """
    num_pages = 1
    try:
        pages_element = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[3]/div[2]/span')[0]
        pages_text = pages_element.text
        pages_text_split = pages_text.split()
        num_pages = int(pages_text_split[-1])
    except IndexError:
        pass
    return num_pages


# In[213]:


##### FUNCTIONS FOR DATA EXTRACTION #################################################

# XPath REFERENCES for each data field we want to extract for each post
# NOTES:
# 1. It appears that each post has its own ID as "post-#####"
# 2. Because each post's data field has an id tag with "post-#####", we can just
#    get all "post-#####", rather than just the 5-digit number.
# Poster's username XPath: //*[@id="post-36160"]/div[1]/div/h3/a
# Poster's user title: //*[@id="post-36160"]/div[1]/div/h3/em[1]
# Poster's user banner: //*[@id="post-36160"]/div[1]/div/h3/em[2]/strong
# Poster's post date XPath: //*[@id="post-36160"]/div[2]/div[3]/div[1]/span/a/span
# Poster's last edited date XPath: //*[@id="post-36160"]/div[2]/div[2]/span
# 2nd post's title XPath: //*[@id="post-36171"]/div[2]/div[1]/article/blockquote/b
# Poster's comment XPath: //*[@id="post-36160"]/div[2]/div[1]/article/blockquote
# Poster's Post # XPath: //*[@id="post-36160"]/div[2]/div[3]/div[2]/a


# In[214]:


#####################################################################################

# Get ALL id tags on page with "post-#####"
def get_post_ids():
    """
    This function takes in no parameters,
    finds all elements containing an id with "post-" on the current page,
    and returns a list of strings of all found elements.
    This function is used to obtain a list:
    ["post-#####", "post-#####", ...]
    """
    id_elements = driver.find_elements_by_xpath("//*[contains(@id, 'post-')]")
    ids_as_str = []
    for element in id_elements:
        id_str = element.get_attribute("id")
        if id_str.startswith("post-"):
            ids_as_str.append(id_str)
        else:
            pass
    return ids_as_str

# Get userName
def get_userName(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the username of the post's author,
    and returns a string (userName), which is the username.
    """
    userName_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div/h3/a')[0]
    userName = userName_element.text
    return userName

# Get userTitle
# NOTE: It appears that the original poster of a thread does not have a title for
#       their initial post.
def get_userTitle(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the title of the user (e.g. "Member", "Active Member"),
    and returns a string (userTitle), which is the user's title.
    """
    userTitle_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div/h3/em[1]')[0]
    userTitle = userTitle_element.text
    return userTitle

# Get userBanner (OPTIONAL FIELD)
# NOTES:
# 1. Not every user has a banner.
# 2. Some users have more than 1 banner.

def get_userBanners(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the banners of the user (e.g. "Forum Leader", "Industry Professional"),
    and returns a list of string (userBanners), which is a list containing
    the user's banners as strings.
    """
    userBanners = []
    getting_banners = True
    div_num = 2
    while getting_banners == True:
        try:
            userBanner_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div/h3/em[' + str(div_num) + ']/strong')[0]
            userBanner = userBanner_element.text
            userBanners.append(userBanner)
            div_num += 1
        except:
            getting_banners = False
            #print("\tError: No more user banners detected for user of Post #" + id[5:] + ".")
    return userBanners

# Get userTimestamp
def get_userTimestamp(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the timestamp (e.g. "Feb 2, 2011") of the post,
    and returns a string (userTimestamp), which is the timestamp of when the post was made.
    Example: "Feb 2, 2011 at 5:15 PM"
    """
    userTimestamp = ""
    try:
        userTimestamp_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[2]/div[1]/span/a/span')[0]
        userTimestamp = userTimestamp_element.get_attribute("title")
    except IndexError:
        try:
            userTimestamp_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[3]/div[1]/span/a/span')[0]
            userTimestamp = userTimestamp_element.get_attribute("title")
        except:
            print("\tUnknown error occurred trying to get Timestamp of Post #" + id[5:] + ".")
    return userTimestamp

# Get userEditTimestamp
def get_userEditTimestamp(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the edited timestamp (after "Last edited:"),
    and returns a string (userEditTimestamp), which is the timestamp of when the post was last edited.
    Example: "Feb 2, 2011 at 5:15 PM"
    """
    userEditTimestamp = ""
    try:
        userEditTimestamp_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[2]/span')[0]
        userEditTimestamp = userEditTimestamp_element.get_attribute("title")
    except IndexError:
        print("\tIndexError: Post #" + id[5:] + " was not edited.")
    return userEditTimestamp

# Get userPostTitle (OPTIONAL FIELD)
# NOTE: Not every user puts a title on their post.
def get_userPostTitle(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the title of the user's post,
    and returns a string (userPostTitle), which is the post's title.
    """
    userPostTitle = ""
    try:
        userPostTitle_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[1]/article/blockquote/b')[0]
        userPostTitle = userPostTitle_element.text
    except IndexError:
        print("\tIndexError: Post #" + id[5:] + " did not include a title on their post.")
    finally:
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
    userComment_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[1]/article/blockquote')[0]
    userComment = userComment_element.text
    return userComment

# Get userPostNum (post # in sub-forum)
def get_userPostNum(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the Post #,
    and returns a string (userPostNum) in the format "#[number]".
    """
    userPostNum = ""
    try:
        userPostNum_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[2]/div[2]/a')[0]
        userPostNum = userPostNum_element.text
    except IndexError:
        try:
            userPostNum_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[2]/div[3]/div[2]/a')[0]
            userPostNum = userPostNum_element.text
        except:
            print("\tUnknown error occurred trying to get Post Number of Post #" + id[5:] + ".")
    return userPostNum

# Get dat a for a single post
def get_post_data(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    extracts the data from the different fields on the post,
    and returns a list with the post's data (9 items), such that:
    [postID, userName, userTitle, userBanners, userTimestamp, userEditTimestamp, userPostTitle, userComment, userPostNum]
    Please note that userBanners is a list.
    """
    userName = get_userName(id)
    userTitle = get_userTitle(id)
    userBanners = get_userBanners(id)
    userTimestamp = get_userTimestamp(id)
    userEditTimestamp = get_userEditTimestamp(id)
    userPostTitle = get_userPostTitle(id)
    userComment = get_userComment(id)
    userPostNum = get_userPostNum(id)
    post_data = [id, userName, userTitle, userBanners, userTimestamp, userEditTimestamp, userPostTitle, userComment, userPostNum]
    #print("post_data =", post_data)
    #print()
    return post_data

# Get data for all posts on a single page
def get_post_data_on_page():
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
        print(counter, ". Getting post data for Post #" + id[5:] + " ...")
        post_data = get_post_data(id)
        post_data_on_page.append(post_data)
        counter += 1
    return post_data_on_page


# In[215]:


##### FUNCTIONS TO CHECK DATA #######################################################

def check_num_posts(all_post_data):
    print("---------------------------------------------------------------------------\n")
    print("Checking number of posts...")
    last_post_num = int(all_post_data[-1][-1][1:])
    print("\tLength of all_post_data =", len(all_post_data), "   |   Last post # =", last_post_num)
    if len(all_post_data) == last_post_num:
        return True
    else:
        return False


# In[432]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("---------------------------------------------------------------------------\n")
print("Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# Open URL with a timeout, so you don't wait for ads to load
try:
    print("Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("TimeoutException has been thrown. " + str(ex))
    


# In[433]:


# Get number of pages in the forum
print("---------------------------------------------------------------------------\n")
num_pages = get_num_pages()
print("Number of Pages:", num_pages, "\n")


# In[434]:


# Get post data on the first page
print("---------------------------------------------------------------------------\n")
print("Getting post data on page 1...")
all_post_data = []
page1_result = get_post_data_on_page()
for post in page1_result:
    all_post_data.append(post)
print("Finished getting post data on page 1")
print("Length of all_post_data =", len(all_post_data), "\n")
    


# In[ ]:


# XPath / CSS selector REFERENCES for 'Next >' page navigational button
# XPath: //*[@id="content"]/div/div/div[4]/div[3]/nav/a[7]
# CSS selector: #content > div > div > div:nth-child(5) > div.PageNav > nav > a.text

# If there is more than 1 page in the sub-forum,
# go through each page and extract the post data for each post on each page.
# Else, if there is only 1 page in the sub-forum,
# do nothing.
print("---------------------------------------------------------------------------\n")
print("Checking if there is more than 1 page...")
if num_pages > 1:
    print("More than 1 page detected\n")
    for page in range(2, (num_pages + 1)):
        try:
            print("---------------------------------------------------------------------------\n")
            print("Attempting to open page:", page, "...")
            driver.set_page_load_timeout(timeout_for)
            nextPageURL = myURL + "page-" + str(page)
            driver.get(nextPageURL)
            print("Waiting for", time_to_sleep_for, "seconds to allow page to load.")
            print("Please manually reload page, if necessary.")
            time.sleep(time_to_sleep_for)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
        finally:
            print("Getting post data on page", page, "...")
            result = get_post_data_on_page()
            for post in result:
                all_post_data.append(post)
            print("Finished getting post data on page", page)
            print("Length of all_post_data =", len(all_post_data), "\n")
else:
    print("Only 1 page detected")
    pass


# In[428]:


# Check number of posts
check_num_posts_result = check_num_posts(all_post_data)
print("Length of all_posts_data equals Last post #? --", check_num_posts_result, "\n")
if check_num_posts_result == False:
    print("\tPlease re-run script from the beginning.")
print("---------------------------------------------------------------------------\n")


# In[429]:


##### MAKE PANDAS DATA FRAME OBJECT #################################################
col_names = ['Post ID', 'Username', 'User Title', 'Banners', 'Timestamp', 'Edited Timestamp', 'Post Title', 'Comment', 'Post #']
df = pd.DataFrame(all_post_data, columns = col_names)

print(df)


# In[430]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + file_name), index = None, header=True, encoding='utf-8-sig')

#####################################################################################


# In[233]:


print(len(all_post_data))

