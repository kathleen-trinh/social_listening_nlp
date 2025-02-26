#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# youtube_script.py
#
# Script for scraping a comments on a YouTube video using...
# Homepage URL: https://www.youtube.com/
# Tools: Selenium, Chrome Driver
# Data Organizer: Pandas
#
# Version: 2.3
# Date Created: 02/05/2019
# Last Modified: 09/09/2019
#####################################################################################

#####################################################################################
#
# V2.2 Notes:
#
# 1. Added functions to handle and get styled usernames.
#    This function is called if no username is detected for a post after
#    first trying to use the original function to get normal usernames.
# 2. Added function to make custom comment IDs called "My Comment ID" in output.
# 3. Added function to make list of URLs for output
#    where len(URLs) = len(comments) and all items are the same video URL.
# 4. Added function to get video's title from top of page below the video player.
# 5. Added function to make list of video titles for output
#    where len(video_titles) = len(comments) and all items are the same video title.
# 6. Changed global variable v_code to automatically get code from URL:
#    v_code = myURL.split("v=")[1]
#
#####################################################################################

#####################################################################################
#
# V2-3 Notes:
#
# 1. The function get_viewXreplies_elements() from previous versions is depecrated,
#    as the CSS selector for "View [x] replies" buttons is no longer "#more-text".
#    The CSS selector is now simply "#text", which is shared with many other elements
#    on the page. To filter out which elements actually correspond to "View [x] replies",
#    the RegEx "(View).*(repl).*" is used to match against each found element.text.
#    Elements whose text field matches the RegEx are then added to the actual list of
#    "View [x] replies" elements.
# 2. Changed function get_ShowMoreReplies_elements() to check if found elements' text
#    field is equal to "Show more replies". If it does match, the element is then
#    added to the actual list of "Show more replies" elements. This modification is
#    similar to the one mentioned above, except without the use of a RegEx pattern.
# 3. Added funtion to make list of sources for output
#    where len(sources) = len(comments) and all items are the same source, "YouTube".
# 4. Changed output column names to be all lowercase and without whitespace, as follows:
#    - "My Comment ID" -> "my_comment_id"
#    - "source"
#    - "Video Title" -> "video_title"
#    - "Username" -> "username"
#    - "Comment" -> "comment"
#    - "Timestamp" -> "timestamp"
#    - "Timestamp Number" -> "timestamp_number"
#    - "Timestamp Unit" -> "timestamp_unit"
#    - "Edited" -> "edited"
#    - "Upvotes" -> "upvotes"
#    - "URL" -> "url"
#
#####################################################################################


# In[2]:


##### READ ME #######################################################################
#
# This script is able to scrape YouTube video comments on:
# https://www.youtube.com/
#
# This script's code should only be executed at portions at a time due to
# Chrome Driver being unable to open the given webpage all the time.
# Please do not run this script as an executable / as a whole.
#
##### WARNINGS ######################################################################
#
# 1. This script is prone to errors when scraping videos with 2,000+ comments.
#    Videos with 1,500+ comments are iffy...
#    This is because the browser has trouble displaying many comments at once on
#    one page, so if the browser crashes or the page becomes unresponsive,
#    the script will no longer work.
# 2. Please do not scroll or click anywhere on the browser window where Chrome Driver
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
# 2. If the webpage does not load when Chrome Driver starts, please manually
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


# In[3]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import re
import string
import time
#####################################################################################


# In[2057]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have Chrome Driver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver.exe"

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
time_to_sleep_for = 2

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/"

# URL of the video page you want to scrape (CHANGE AS NEEDED)
# Type: string
myURL = "https://www.youtube.com/watch?v=ZH7V2tU3iFc"

# File name you want to save the file as (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
f_timestamp = "211013_14-51-PM"
v_code = myURL.split("v=")[1]
v_title = "We drove these electric cars until they DIED!"
filename = f_timestamp + "_YouTube_" + v_code + "_" + v_title + ".csv"

#####################################################################################


# In[5]:


##### FUNCTIONS FOR PART 1: SHOWING ALL COMMENTS ON THE PAGE ########################

def scroll_to_bottom():
    print("Scrolling to bottom of page...")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
    print("Finished scrolling to bottom of page\n")


# In[6]:


def get_viewXreplies_elements():
    found_elements = driver.find_elements_by_css_selector('#text')
    viewXreplies_elements = []
    for element in found_elements:
        match = re.match("(View).*(repl).*", element.text)
        if match:
            viewXreplies_elements.append(element)
    print("-----", len(viewXreplies_elements), "'View [x] replies' OR 'View reply' elements found -----\n")
    return viewXreplies_elements

def click_viewXreplies():
    viewXreplies_elements = get_viewXreplies_elements()
    if len(viewXreplies_elements) == 0:
        print("No 'View [x] replies' OR 'View reply' buttons detected\n")
    else:
        counter = 1
        for element in viewXreplies_elements:
            try:
                print(counter, ". Attempting to click 'View [x] replies' OR 'View reply' button #", counter, "...")
                driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(2)
                driver.execute_script("window.scrollBy(0, -60);")
                time.sleep(0.5)
                element.click()
            except NoSuchElementException as e:
                print(counter, ". NoSuchElementException occurred trying to click 'View [x] replies' OR 'View reply' button #", counter)
                print("Please execute this piece of code again OR reload page and try again")
                break
            except StaleElementReferenceException as e:
                print(counter, ". StaleElementReferenceException occurred trying to click 'View [x] replies' OR 'View reply' button #", counter)
                print("Please reload page and try again")
                break
            except:
                print(counter, ". Unknown error occurred trying to click 'View [x] replies' OR 'View reply' button #", counter)
                print("Please reload page and try again")
                break
            finally:
                time.sleep(2)
                counter += 1


# In[7]:


def get_ShowMoreReplies_elements():
    found_elements = driver.find_elements_by_css_selector('#continuation > yt-next-continuation > paper-button > yt-formatted-string')
    viewXreplies_elements = []
    for element in found_elements:
        if element.text == "Show more replies":
            viewXreplies_elements.append(element)
    print("\n-----", len(viewXreplies_elements), "'Show more replies' elements found -----\n")
    return viewXreplies_elements

def click_ShowMoreReplies(ShowMoreReplies_elements):
    counter = 1
    for element in ShowMoreReplies_elements:
        try:
            print(counter, ". Attempting to click 'Show more replies' button #", counter, "...")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(2)
            driver.execute_script("window.scrollBy(0, -60);")
            time.sleep(0.5)
            element.click()
        except NoSuchElementException as e:
            print(counter, ". NoSuchElementException occurred trying to click 'View [x] replies' OR 'View reply' button #", counter)
            print("Please (a) execute this piece of code again OR (b) reload page and try again")
            return -1
        except StaleElementReferenceException as e:
            print(counter, ". StaleElementReferenceException occurred trying to click 'Show more replies' button #", counter)
            print("Please reload page and try again")
            return -2
        except:
            print(counter, ". Error occurred trying to click 'Show more replies' button #", counter)
            print("Please reload page and try again")
            return -3
        finally:
            time.sleep(2)
            counter += 1
    return 0

def click_ALL_ShowMoreReplies():
    ShowMoreReplies_elements = get_ShowMoreReplies_elements()
    if len(ShowMoreReplies_elements) == 0:
        print("No 'Show more replies' buttons detected\n")
    else:
        finding_replies = True
        while finding_replies == True:
            result = click_ShowMoreReplies(ShowMoreReplies_elements)
            # Check if error occurred
            if result < 0:
                finding_replies = False
            # Check if there is a need for consequent iteration (any more 'Show more replies' buttons)
            ShowMoreReplies_elements = get_ShowMoreReplies_elements()
            if len(ShowMoreReplies_elements) == 0:
                print("No more 'Show more replies' buttons detected\n")
                finding_replies = False
            else:
                pass


# In[8]:


##### FUNCTIONS FOR PART 2: POST DATA EXTRACTION ####################################

def get_video_title():
    print("Getting video title...")
    title_element = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
    title = title_element.text
    print("Video title:", title)
    return title

def get_normal_usernames():
    print("Attempting to get normal usernames...")
    username_elements = driver.find_elements_by_xpath('//*[@id="author-text"]/span')
    print("\tLength of username_elements =", len(username_elements))
    usernames = []
    for element in username_elements:
        usernames.append(element.text)
    print("\tLength of usernames =", len(usernames))
    return usernames

def get_styled_usernames():
    print("Attempting to get styled usernames...")
    styled_username_elements = driver.find_elements_by_xpath('//*[@id="name"]/yt-formatted-string')
    print("\tLength of styled_username_elements =", len(styled_username_elements))
    styled_usernames = []
    for element in styled_username_elements:
        styled_usernames.append(element.text)
    print("\tLength of styled_usernames =", len(styled_usernames))
    return styled_usernames

def count_empty_usernames(usernames):
    print("Counting empty usernames in normal_usernames...")
    count = 0
    for name in usernames:
        if len(name) == 0:
            count += 1
    print("\tNumber of empty usernames in normal_usernames =", count)
    return count

def get_ALL_usernames():
    print("Attempting to get ALL usernames...")
    normal_usernames = get_normal_usernames()
    num_empty_usernames = count_empty_usernames(normal_usernames)
    if num_empty_usernames == 0:
        print("\tNo empty usernames found")
        return normal_usernames
    else:
        styled_usernames = get_styled_usernames()
        if len(styled_usernames) == num_empty_usernames:
            print("\tNumber of found styled usernames = number of empty usernames? -- True")
            print("Replacing empty usernames and generating new usernames list...")
            usernames = []
            i = 0
            for name in normal_usernames:
                if len(name) > 0:
                    usernames.append(name)
                else:
                    usernames.append(styled_usernames[i])
            if len(usernames) == len(normal_usernames):
                print("\tLength of usernames = normal_usernames? -- True")
                print("Successfully replaced empty usernames with styled usernames")
                return usernames
            else:
                print("\tLength of usernames = normal_usernames? -- False")
                print("\t\tUnable to replace all empty usernames -- returning normal_usernames")
                return normal_usernames
        else:
            print("\tNumber of found styled usernames = number of empty usernames? -- False")
            print("\t\tLeaving empty usernames as is")
            return normal_usernames

def get_ALL_timestamps():
    print("Attempting to get ALL timestamps...")
    # //*[@id="header-author"]/yt-formatted-string/a
    timestamp_elements = driver.find_elements_by_xpath('//*[@id="header-author"]/yt-formatted-string/a')
    print("Length of timestamp_elements =", len(timestamp_elements))
    timestamps = []
    for element in timestamp_elements:
        timestamps.append(element.text)
    print("Length of timestamps =", len(timestamps))
    return timestamps

def parse_timestamp(timestamp_str):
    timestamp_split = timestamp_str.split()
    timestamp_number = timestamp_split[0]
    timestamp_unit = timestamp_split[1]
    timestamp_edited = "No"
    if timestamp_split[-1] == "(edited)":
        #print("Edited post detected")
        timestamp_edited = "Yes"
    parsed_timestamp = (timestamp_number, timestamp_unit, timestamp_edited)
    return parsed_timestamp

def get_ALL_parsed_timestamps(timestamps):
    print("Attempting to get ALL parsed timestamp data...")
    timestamp_numbers = []
    timestamp_units = []
    timestamp_edited = []
    for timestamp in timestamps:
        parsed_timestamp = parse_timestamp(timestamp)
        timestamp_numbers.append(parsed_timestamp[0])
        timestamp_units.append(parsed_timestamp[1])
        timestamp_edited.append(parsed_timestamp[2])
    parsed_timestamps = (timestamp_numbers, timestamp_units, timestamp_edited)
    print("Length of timestamp_numbers =", len(parsed_timestamps[0]))
    print("Length of timestamp_units =", len(parsed_timestamps[1]))
    print("Length of timestamp_edited =", len(parsed_timestamps[2]))
    return parsed_timestamps

# NOTE: This get_ALL_comments function is unable to get a URL/link inside of a comment.
#       Example: See Ade Yudha's comment on this video -- https://www.youtube.com/watch?reload=9&v=LmcciZ50nPs
def get_ALL_comments():
    print("Attempting to get ALL comments...")
    comment_elements = driver.find_elements_by_xpath('//*[@id="content-text"]')
    print("Length of comment_elements =", len(comment_elements))
    comments = []
    for element in comment_elements:
        comments.append(element.text)
    print("Length of comments =", len(comments))
    return comments

def get_ALL_upvotes():
    print("Attempting to get ALL upvotes...")
    upvote_elements = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')
    print("Length of upvote_elements =", len(upvote_elements))
    upvotes = []
    for element in upvote_elements:
        num_votes = element.text
        if len(num_votes) > 0:
            upvotes.append(num_votes)
        else:
            upvotes.append("0")
    print("Length of upvotes =", len(upvotes))
    return upvotes


# In[9]:


##### FUNCTIONS FOR PART 3: DATA ADDITION ###########################################

def make_MyCommentIDs(comment_count):
    comment_IDs = []
    for i in range(1, (comment_count + 1)):
        comment_ID = "YT_" + v_code + "_Com" + str(i)
        comment_IDs.append(comment_ID)
    return comment_IDs

def make_sources(comment_count):
    sources = ["YouTube" for x in range(0, comment_count)]
    return sources

def make_video_titles(comment_count, title):
    titles = [title for x in range(0, comment_count)]
    return titles

def make_URLs(comment_count):
    URLs = [myURL for x in range(0, comment_count)]
    return URLs


# In[10]:


##### IMPLEMENTATION ################################################################

# Setting up the Chrome Driver
print("Setting up Chrome Driver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[2058]:


# Open URL with a timeout
try:
    print("Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("TimeoutException has been thrown. " + str(ex))


# In[1899]:


# Print the following instructions to users:
print("TO USER:")
print("\t1. Please click on the 'Skip Ad' button inside the video player and/or pause the video if ")
print("\t   you do not want the video to play as you are scraping the page, as you cannot interrupt ")
print("\t   the Chrome Driver window by scrolling or clicking while the script is running.")
print("\t2. If the pop-up for Subscribing to YouTube Premium pops up in the bottom left-hand corner, ")
print("\t   please click the 'No Thanks' button.")
print("\t3. Please manually scroll down the page enough to load the first few comments before ")
print("\t   executing the line of code to automatically scroll down to the bottom of the page.")
print("\t4. Please keep in mind that the following line of code will not always successfully scroll ")
print("\t   down to the bottom of the page on the first try, as it may stop and seem finished ")
print("\t   if comments take a long time to load. If this is the case, please execute the line of ")
print("\t   multiple times until it truly scrolls to the bottom.")


# In[2059]:


# Please manually scroll down the page to get the first few comments to load,
# then execute the following line of code.

# Scroll to the bottom of the page to reveal all comments...
# May need to call this function multiple times depending on quality of Internet connection
# as the programmed wait time is not long enough to allow content to load.
scroll_to_bottom()


# In[2060]:


# Get total number of comments
# Note: Currently, I don't know what will happen if the video has 0 comments.
# XPath to "[x] Comments" below video description: //*[@id="count"]/yt-formatted-string
num_comments_element = driver.find_elements_by_xpath('//*[@id="count"]/yt-formatted-string')[0]
num_comments = num_comments_element.text
num_comments = num_comments.split()[0]
print(num_comments)


# In[2061]:


# Click on "View [x] replies"
# Case for 1 reply: "View reply"
# Case for multiple replies: "View [x] replies"
click_viewXreplies()


# In[2062]:


# Click on "Show more replies"
# All cases: "Show more replies" (regardless if there is only 1 more reply to show)
click_ALL_ShowMoreReplies()


# In[2063]:


# Get video title
video_title = get_video_title()


# In[2064]:


# Get all usernames
usernames = get_ALL_usernames()


# In[2065]:


# Get all timestamps ("[time] ago")
timestamps = get_ALL_timestamps()


# In[2066]:


# Parse all timestamps:
parsed_timestamps = get_ALL_parsed_timestamps(timestamps)


# In[2067]:


# Get all comments
comments = get_ALL_comments()


# In[2068]:


# Get all upvotes
upvotes = get_ALL_upvotes()


# In[2069]:


if (len(usernames) == 
    len(timestamps) == 
    len(parsed_timestamps[0]) == 
    len(parsed_timestamps[1]) ==
    len(parsed_timestamps[2]) ==
    len(comments)):
    print("Lengths of usernames, timestamps, 3 fields in parsed_timestamps, and comments are equal? -- True\n")
else:
    print("Lengths of usernames, timestamps, 3 fields in parsed_timestamps, and comments are equal? -- False")
    print("Please re-run script.\n")


# In[2070]:


# Make custom comment IDs "My Comment IDs"
MyCommentIDs = make_MyCommentIDs(len(comments))

# Make list of sources (all comments should have the same source, "YouTube")
sources = make_sources(len(comments))

# Make list of video titles (all comments should have the same video title)
video_titles = make_video_titles(len(comments), video_title)

# Make list of URLs (all comments should have the same video URL)
URLs = make_URLs(len(comments))


# In[2071]:


print("Captured comments: ", len(comments), "/", num_comments)


# In[2072]:


# Make custom comment IDs "My Comment IDs"
MyCommentIDs = make_MyCommentIDs(len(comments))

# Make list of video titles (all comments should have the same video title)
video_titles = make_video_titles(len(comments), video_title)

# Make list of URLs (all comments should have the same video URL)
URLs = make_URLs(len(comments))


# In[2073]:


# Create Pandas DataFrame

# New column names
data = {"my_comment_id": MyCommentIDs,
        "source": sources,
        "video_title": video_titles,
        "username": usernames,
        "comment": comments,
        "timestamp": timestamps,
        "timestamp_number": parsed_timestamps[0],
        "timestamp_unit": parsed_timestamps[1],
        "edited": parsed_timestamps[2],
        "upvotes": upvotes,
        "url": URLs}

df = pd.DataFrame(data)


# In[2074]:


df


# In[2075]:


print(df.iloc[0]["comment"])


# In[2076]:


# Export Pandas DataFrame object to a .csv file using encoding='utf-8-sig'
df.to_csv((path_to_folder + filename), index = None, header=True, encoding='utf-8-sig')

# # Export Pandas DataFrame object to a .csv file using encoding='utf-8'
df.to_csv((path_to_folder + "utf-8_" + filename), index = None, header=True, encoding='utf-8')


# In[2077]:


# Close Chrome Driver
driver.close()

