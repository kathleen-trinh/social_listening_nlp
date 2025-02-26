#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# hvac_talk_dot_com_script.py
#
# Script for scraping sub-forums on https://www.nissanclub.com/ using...
# Homepage URL: https://hvac-talk.com/vbb/forum.php
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 02/13/2019
# Last Modified: 02/14/2019
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import math
import os
import re
import time
#####################################################################################


# In[98]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the sub-forum you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the very first page in the sub-forum
myURL = "https://hvac-talk.com/vbb/showthread.php?132085-Waterfurnace-problems"

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
time_to_sleep_for = 5

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/GeothermalProject/HVAC-Talk/"

# File name you want to save the file as (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name_timestamp = "190214"
forum_code = "132085"
forum_title = "Waterfurnace-problems"
file_name = file_name_timestamp + "_HVAC-Talk_" + forum_code + "_" + forum_title + ".csv"

#####################################################################################


# In[87]:


##### FUNCTIONS FOR GENERAL USE #####################################################

def get_num_posts():
    num_results_element = driver.find_elements_by_xpath('//*[@id="postpagestats_above"]')[0]
    num_results = int(num_results_element.text.split()[-1])
    print("Number of Results:", num_results)
    return num_results

def get_num_pages(num_posts):
    # NOTE: Max 13 posts displayed per page
    num_pages = math.ceil(int(num_posts) / 13)
    print("Number of Pages:", num_pages)
    return num_pages

def get_postID_nums(postMsgIDs):
    postIDs = []
    for id in postMsgIDs:
        #print("Trying to match:", id)
        matchObj = re.search( '[0-9]*$', id, flags=0)
        if matchObj:
            #print("Match found:", matchObj.group(0))
            postIDs.append(matchObj.group(0))
        else:
            #print("No match found... ):")
            postIDs.append("")
    return postIDs


# In[88]:


##### FUNCTIONS FOR DATA EXTRACTION #################################################

# XPath REFERENCES for each data field we want to extract for each post
# NOTE: With the exception of the userID, all post elements are associated with a 7 OR 8-digit post number.
# Poster's userID XPath: //*[@id="yui-gen15"]/strong
# NOTE on userIDs: Only "yui-gen" ids associated with a username have a non-empty "title".
# Poster's user title: //*[@id="post_2055013"]/div[1]/div[2]/div[1]/div/span
# Poster's post date XPath: //*[@id="post_2055013"]/div[1]/div[1]/span[1]/span
# Poster's post time XPath: //*[@id="post_2055013"]/div[1]/div[1]/span[1]/span/span
# Poster's post title XPath: //*[@id="post_2055013"]/div[2]/div/h2
# Poster's message XPath: //*[@id="post_message_2055013"]/blockquote
# Poster's Post # XPath: //*[@id="post_2055013"]/div[1]/div[1]/span[2]/a[1]


# In[89]:


def get_userIDs():
    # NOTE: Usernames are extractable from the online status string that pops up
    #       when the mouse hovers over the username or online status icon.
    print("\tAttempting to get User IDs on page...")
    ids_on_page = driver.find_elements_by_xpath("//*[contains(@id, 'yui-gen')]")
    userIDs = []
    for id in ids_on_page:
        online_status = id.get_attribute('title')
        if len(online_status) > 0:
            userIDs.append(online_status.split(" is ")[0])
    print("\t\tLength of userIDs =", len(userIDs))
    return userIDs

def get_postIDs():
    print("\tAttempting to get Post IDs on page...")
    postIDs_on_page = driver.find_elements_by_xpath("//*[contains(@id, 'post_message')]")
    postMsgIDs = []
    for id in postIDs_on_page:
        postID = id.get_attribute('id')
        postMsgIDs.append(postID)
    print("\t\tLength of postMsgIDs =", len(postMsgIDs))
    postIDs = get_postID_nums(postMsgIDs)
    print("\t\tLength of postIDs =", len(postIDs))
    return postIDs

def get_userTitles(postIDs):
    print("\tAttempting to get User Titles on page...")
    userTitles = []
    for id in postIDs:
        userTitle_element = driver.find_elements_by_xpath('//*[@id="post_' + id + '"]/div[1]/div[2]/div[1]/div/span')[0]
        userTitles.append(userTitle_element.text)
    print("\t\tLength of userTitles =", len(userTitles))
    return userTitles

def get_postTimestamps(postIDs):
    print("\tAttempting to get Post Timestamps on page...")
    postTimestamps = []
    for id in postIDs:
        postTimestamp_element = driver.find_elements_by_xpath('//*[@id="post_' + id + '"]/div[1]/div[1]/span[1]/span')[0]
        postTimestamps.append(postTimestamp_element.text)
    print("\t\tLength of postTimestamps =", len(postTimestamps))
    return postTimestamps

def get_postDates(postTimestamps):
    print("\tGetting Post Dates from Post Timestamps...")
    postDates = []
    for timestamp in postTimestamps:
        postDate = timestamp.split(",")[0]
        postDates.append(postDate)
    return postDates

def get_postTimes(postTimestamps):
    print("\tGetting Post Times from Post Timestamps...")
    postTimes = []
    for timestamp in postTimestamps:
        postTime = timestamp.split(", ")[1]
        postTimes.append(postTime)
    return postTimes

def get_postTitles(postIDs):
    print("\tAttempting to get Post Titles on page...")
    postTitles = []
    for id in postIDs:
        try:
            postTitle_element = driver.find_elements_by_xpath('//*[@id="post_' + id + '"]/div[2]/div/h2')[0]
            postTitles.append(postTitle_element.text)
        except IndexError as e:
            #print("\t\tPost #", id, "did not include a post title.")
            postTitles.append("")
    print("\t\tLength of postTitles =", len(postTitles))
    return postTitles

def get_postMessages(postIDs):
    print("\tAttempting to get Post Messages on page...")
    postMessages = []
    for id in postIDs:
        postMessage_element = driver.find_elements_by_xpath('//*[@id="post_message_' + id + '"]/blockquote')[0]
        postMessages.append(postMessage_element.text)
    print("\t\tLength of postMessages =", len(postMessages))
    return postMessages

def get_postNumbers(postIDs):
    print("\tAttempting to get Post Numbers on page...")
    postNumbers = []
    for id in postIDs:
        postNumber_element = driver.find_elements_by_xpath('//*[@id="post_' + id + '"]/div[1]/div[1]/span[2]/a[1]')[0]
        postNumbers.append(postNumber_element.text)
    print("\t\tLength of postNumbers =", len(postNumbers))
    return postNumbers


# In[90]:


def get_pageData():
    pageData = []
    userIDs = get_userIDs()
    postIDs = get_postIDs()
    userTitles = get_userTitles(postIDs)
    postTimestamps = get_postTimestamps(postIDs)
    postDates = get_postDates(postTimestamps)
    postTimes = get_postTimes(postTimestamps)
    postTitles = get_postTitles(postIDs)
    postMessages = get_postMessages(postIDs)
    postNumbers = get_postNumbers(postIDs)
    if (len(userIDs) == len(postIDs) == len(userTitles) == len(postTimestamps) == len(postDates) == 
        len(postTimes) == len(postTitles) == len(postMessages) == len(postNumbers)):
        print("Lengths of all data field lists are equal to each other? -- True")
        for i in range(0, len(postIDs)):
            pageData.append([postIDs[i],
                            userIDs[i],
                            userTitles[i],
                            postTimestamps[i],
                            postDates[i],
                            postTimes[i],
                            postTitles[i],
                            postMessages[i],
                            postNumbers[i]])
        print("\tLength of pageData =", len(pageData))
        return pageData
    else:
        print("Lengths of all data field lists are equal to each other? -- False")
        return -1

def add_pageData(all_postData, pageData):
    print("\tAdding pageData to all_postData...")
    for postData in pageData:
        all_postData.append(postData)
    return all_postData


# In[48]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[99]:


# Open URL with a timeout, so you don't wait for ads to load
try:
    print("Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("TimeoutException has been thrown. " + str(ex))


# In[100]:


num_posts = get_num_posts()
num_pages = get_num_pages(num_posts)


# In[101]:


# Get first page's data
print("---------------------------------------------------------------------------\n")
print("Attempting to get post data on Page 1...")
all_postData = get_pageData()
if all_postData == -1:
    print("\tError occurred trying to get post data on Page 1.")
    print("\tPlease re-get data for current page.")
else:
    print("Finished getting post data on Page 1.\n")


# In[ ]:


# Get consequent pages' data
if num_pages > 1:
    print("---------------------------------------------------------------------------\n")
    print(num_pages, "pages detected.\n")
    for page in range(2, (num_pages + 1)):
        nextURL = myURL + "/page" + str(page)
        try:
            print("---------------------------------------------------------------------------\n")
            print("Attempting to open URL:", nextURL)
            driver.set_page_load_timeout(timeout_for)
            driver.get(nextURL)
            print("\tSleeping for", time_to_sleep_for, "seconds to allow page to load...")
            time.sleep(time_to_sleep_for)
            print("Attempting to get post data on Page " + str(page) + "...")
            pageData = get_pageData()
            if pageData == -1:
                print("\tError occurred trying to get post data on Page" + str(page) + ".")
                retries = 3
                while pageData == -1 and retries != 0:
                    print("\tRetrying to get post data... Retries =", retries)
                    pageData = get_pageData()
                    retries -= 1
                if pageData == -1:
                    print("\tExhausted retries to get post data.")
                    print("Stopping data extraction process.\n")
                    break
                else:
                    add_pageData(all_postData, pageData)
            else:
                add_pageData(all_postData, pageData)
            print("\tLength of all_postData =", len(all_postData))
            print("Finished getting post data on Page " + str(page) + ".\n")
        except TimeoutException as ex:
            print("TimeoutException has been thrown. " + str(ex))
            print("Stopping data extraction process.\n")
            break
else:
    print("---------------------------------------------------------------------------\n")
    print("Only 1 page detected.\n")
    


# In[95]:


# Check length of all_postData
print("---------------------------------------------------------------------------\n")
if len(all_postData) == num_posts:
    print("Length of all_postData is equal to number of posts? -- True\n")
else:
    print("Length of all_postData is equal to number of posts? -- False")
    print("\tDifference =", (num_posts - len(all_postData)), "\n")
    


# In[96]:


##### MAKE PANDAS DATA FRAME OBJECT #################################################
col_names = ['Post ID', 'Username', 'User Title', 'Timestamp', 'Date', 'Time', 'Post Title', 'Message', 'Post #']
df = pd.DataFrame(all_postData, columns = col_names)

print(df)


# In[97]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + file_name), index = None, header=True, encoding='utf-8-sig')

#####################################################################################


# In[54]:


postIDsTEST = get_postIDs()
print(postIDsTEST)

