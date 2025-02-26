#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# the_farming_forum_script.py
#
# Script for scraping sub-forums/threads on The Farming Forum using...
# Homepage URL: https://thefarmingforum.co.uk
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 03/11/2019
# Last Modified: 03/11/2019
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import string
import time


# In[843]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the thread you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the first page in the thread
#       and that the string ends with a slash "/"
myURL = "https://thefarmingforum.co.uk/index.php?threads/all-things-dairy.24262/"

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
path_to_folder = "C://Users/kathleen.trinh/Documents/MeterProject/TheFarmingForum/"

# File name you want to save the file as (CHANGE FIELDS AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name_date = "190311"
forum_code = "24262"
forum_title = "All-things-Dairy"
file_name = file_name_date + "_TFF_" + forum_code + "_" + forum_title + ".csv"

#####################################################################################


# In[48]:


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
        pages_element = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div/div/div[4]/div[2]/span')
        pages_text = pages_element.text
        pages_text_split = pages_text.split()
        num_pages = int(pages_text_split[-1])
    except NoSuchElementException:
        pass
    return num_pages


# In[871]:


##### FUNCTIONS FOR DATA EXTRACTION #################################################

# Get post IDs
def get_post_ids():
    """
    This function takes in no parameters,
    finds all elements containing an id with "post-" on the current page,
    and returns a list of strings of all found elements.
    This function is used to obtain a list:
    ["post-#######", "post-#######", ...]
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
    This function takes in a string (id) in the form of "post-#######",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the username of the post's author,
    and returns a string (userName), which is the username.
    """
    userName_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[1]/div/h3/div/a')
    userName = userName_element.text
    return userName

# Get userTitle
def get_userTitle(id):
    """
    This function takes in a string (id) in the form of "post-#######",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the title of the user (e.g. "Member"),
    and returns a string (userTitle), which is the user's title.
    """
    userTitle_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[1]/div/h3/div/em')
    userTitle = userTitle_element.text
    return userTitle

# Get userLocation
def get_userLocation(id):
    """
    This function takes in a string (id) in the form of "post-#######",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the location of the user (e.g. "Tyrone, Northern Ireland"),
    which is an optional field and is not always provided,
    and returns a string (userLocation), which is the user's location.
    """
    try:
        userLocation_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[1]/div/div[2]/dl/dd/a')
        userLocation = userLocation_element.text
    except NoSuchElementException:
        return ""
    return userLocation

# Get userTimestamp
def get_userTimestamp(id):
    """
    This function takes in a string (id) in the form of "post-#######",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the timestamp (e.g. "Feb 2, 2011") of the post,
    and returns a string (userTimestamp), which is the timestamp of when the post was made.
    Example: "Feb 2, 2011 at 5:15 PM"
    """
    # XPath is usually: //*[@id="post-5985688"]/div[2]/div[2]/div[1]/span/a/span
    # But is sometimes: //*[@id="post-5985186"]/div[2]/div[3]/div[1]/span/a/span (if post was edited)
    # And is very, very rarely: //*[@id="post-6044890"]/div[2]/div[2]/div[1]/span/a/abbr
    # Or also very rarely:      //*[@id="post-6063372"]/div[2]/div[3]/div[1]/span/a/abbr
    try:
        userTimestamp_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[2]/div[1]/span/a/span')
    except NoSuchElementException:
        try:
            userTimestamp_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[3]/div[1]/span/a/span')
        except NoSuchElementException:
            try:
                userTimestamp_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[2]/div[1]/span/a/abbr')
            except NoSuchElementException:
                userTimestamp_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[3]/div[1]/span/a/abbr')
    userTimestamp = userTimestamp_element.get_attribute("title")
    return userTimestamp

# Get userComment
def get_userComment(id):
    """
    This function takes in a string (id) in the form of "post-#####",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the user's message on the post,
    and returns a string (userComment), which is the main text of the user's message.
    NOTE: This function does not extract any quotes / replies to previous posts.
    """
    userComment_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[1]/article/blockquote')
    userComment = userComment_element.text
    return userComment

# Get userPostNum (post # in sub-forum)
def get_userPostNum(id):
    """
    This function takes in a string (id) in the form of "post-#######",
    which should be the Post ID of a post on the page,
    finds the element corresponding to the Post #,
    and returns a string (userPostNum) in the format "#[number]".
    """
    # XPath is usually: //*[@id="post-5985688"]/div[2]/div[2]/div[2]/a
    # But is sometimes: //*[@id="post-5985186"]/div[2]/div[3]/div[2]/a (if post was edited)
    try:
        userPostNum_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[2]/div[2]/a')
    except NoSuchElementException:
        userPostNum_element = driver.find_element_by_xpath('//*[@id="' + id + '"]/div[2]/div[3]/div[2]/a')
    userPostNum = userPostNum_element.text
    return userPostNum

# Get data for a single post
def get_post_data(id, URL):
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
    userLocation = get_userLocation(id)
    userTimestamp = get_userTimestamp(id)
    userComment = get_userComment(id)
    userPostNum = get_userPostNum(id)
    MyCommentID = "TFF_" + forum_code + "_Com" + userPostNum[1:]
    post_data = [MyCommentID, id, userName, userTitle, userLocation, userTimestamp, userComment, userPostNum, URL]
    #print("post_data =", post_data)
    #print()
    return post_data

# Get data for all posts on a single page
def get_post_data_on_page(URL):
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
        post_data = get_post_data(id, URL)
        post_data_on_page.append(post_data)
        counter += 1
    return post_data_on_page


# In[45]:


##### FUNCTIONS TO CHECK DATA #######################################################

def check_num_posts(all_post_data):
    print("---------------------------------------------------------------------------\n")
    print("Checking number of posts...")
    last_post_num = int(all_post_data[-1][-2][1:])
    print("\tLength of all_post_data =", len(all_post_data), "   |   Last post # =", last_post_num)
    if len(all_post_data) == last_post_num:
        return True
    else:
        return False


# In[854]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("---------------------------------------------------------------------------\n")
print("Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[855]:


# Open URL with a timeout, so you don't wait for ads to load
try:
    print("Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("TimeoutException has been thrown. " + str(ex))


# In[876]:


# Get number of pages in the forum
print("---------------------------------------------------------------------------\n")
num_pages = get_num_pages()
print("Number of Pages:", num_pages, "\n")


# In[846]:


"""
# Get post data on the first page
print("---------------------------------------------------------------------------\n")
print("Getting post data on page 1...")
all_post_data = []
page1_result = get_post_data_on_page(myURL)
for post in page1_result:
    all_post_data.append(post)
print("Finished getting post data on page 1")
print("Length of all_post_data =", len(all_post_data), "\n")
"""


# In[891]:


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
            result = get_post_data_on_page(nextPageURL)
            for post in result:
                all_post_data.append(post)
            print("Finished getting post data on page", page)
            print("Length of all_post_data =", len(all_post_data), "\n")
else:
    print("Only 1 page detected\n")
    pass


# In[894]:


# Check number of posts
check_num_posts_result = check_num_posts(all_post_data)
print("Length of all_posts_data equals Last post #? --", check_num_posts_result, "\n")
if check_num_posts_result == False:
    print("\tPlease re-run script from the beginning.")
print("---------------------------------------------------------------------------\n")


# In[895]:


##### MAKE PANDAS DATA FRAME OBJECT #################################################
col_names = ['My Comment ID', 'Post ID', 'Username', 'User Title', 'Location', 'Timestamp', 'Comment', 'Post #', 'URL']
df = pd.DataFrame(all_post_data, columns = col_names)

print(df)


# In[896]:


df


# In[897]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + file_name), index = None, header=True, encoding='utf-8-sig')

#####################################################################################

