#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# facebook_page_script.py
#
# Script for scraping posts and comments on a public Page on Facebook.
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 02/28/2019
# Last Modified: 04/22/2019
#####################################################################################


# In[2]:


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


# In[4]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the Facebook Page you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the Posts section of the page.
#       Should end with "posts/".
myURL = "https://www.facebook.com/pg/uniworldrivercruises/posts/"

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
time_to_sleep_for = 1

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/RiverCruiseProject/Facebook/"

# The first few words you want each output file to include in the beginning in its filename (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
filename_timestamp = "190422-Scraped"
page_title = "Uniworld-Boutique-River-Cruise-Collection"
filename_header = filename_timestamp + "_FBpage_" + page_title
# File extension ".csv" is added later, as each post will have its own output file

#####################################################################################


# In[5]:


##### FUNCTIONS FOR PART 1: SHOWING ALL POSTS ON THE PAGE ###########################

def scroll_to_bottom(scroll_inc, scroll_count):
    print("[FB SCRIPT] Scrolling to bottom of page " + str(scroll_inc) + " times...")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(0, scroll_inc):
        print("[FB SCRIPT]\t" + str(i+1) + ". Scrolling...")
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        # Wait to load page
        time.sleep(time_to_sleep_for)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if last_height == new_height:
            print("[FB SCRIPT] Bottom of page detected. If content is not loading, please wait and try again or reload page.")
        else:
            scroll_count += 1
    print("[FB SCRIPT] Finished scrolling to bottom of page")
    print("[FB SCRIPT] --------------------------------------------------------------------------")
    return scroll_count

# Add function that calls above function repeatedly depending on user input
def scroll_to_bottom_wInput():
    scroll_count = 0
    scroll = True
    while scroll == True:
        user_command = input("[FB SCRIPT] Scroll down page? y/n > ")
        if user_command == "y":
            print("[FB SCRIPT]\tYou entered:'" + user_command + "'")
            scroll_inc = input("[FB SCRIPT] Scroll down how many times? (Please enter a positive integer.) > ")
            # Add while and try/except blocks for input error handling
            print("[FB SCRIPT]\tYou entered:'" + scroll_inc + "'")
            print("[FB SCRIPT] --------------------------------------------------------------------------")
            scroll_count = scroll_to_bottom(int(scroll_inc), scroll_count)
            print("[FB SCRIPT] Total scroll count: ", scroll_count)
        elif user_command == "n":
            print("[FB SCRIPT]\tYou entered:'" + user_command + "'. Proceeding with rest of script...")
            print("[FB SCRIPT] --------------------------------------------------------------------------")
            scroll = False
        else:
            print("[FB SCRIPT]\tInput not recognized.")


# In[6]:


##### FUNCTIONS FOR BUTTON CLICKING #####

def click_postSeeMore(post_element):
    print("[FB SCRIPT] Finding 'See More' button on post...")
    SeeMore_btn = post_element.find_element_by_class_name("see_more_link")
    driver.execute_script("arguments[0].scrollIntoView();", SeeMore_btn)
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, -100);")
    time.sleep(0.5)
    print("[FB SCRIPT] Clicking 'See More' button on post...")
    SeeMore_btn.click()
    
# NOTE: On comments, the See More button is the class "_5v47 fss",
#       which is inside the comment element.
    
def click_commentSeeMore(comment_element):
    print("[FB SCRIPT] Finding 'See More' button on comment...")
    SeeMore_btn = comment_element.find_element_by_class_name("_5v47")
    driver.execute_script("arguments[0].scrollIntoView();", SeeMore_btn)
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, -100);")
    time.sleep(0.5)
    print("[FB SCRIPT] Clicking 'See More' button on comment...")
    SeeMore_btn.click()

# NOTES:
# 1. ALL "View [x] more comments" and "[x] Reply/Replies" buttons must
#    first be clicked to reveal hidden comments and replies so that
#    they display on the page. Failing to do so will not allow the
#    script to capture these comments and replies.
# 2. For both buttons, when clicked on, 50 more comments/replies will
#    be displayed. The button must continuously be found and clicked
#    on to reveal all comments/replies (if there are 50+).
# 3. For replies, after the initial "[x] Reply/Replies" button is
#    clicked, the 50 most recent replies to the comment are displayed.
#    However, if there are still more replies, the button
#    "View previous replies" appears below the initial comment, but
#    above the 50 replies that just loaded. This button must
#    continuously be found and clicked on to reveal all replies (if
#    there are 50+). When clicked again, it will display the next
#    50 most recent replies such that the 100 most recent replies
#    would then currently be displayed.
# 4. For the button to view more comments, the text of the button may
#    be in any of the following formats:
#    a) View more comments
#    b) View 1 more comment
#    c) View # more comments
# 5. For the button to view more replies, the text of the button may
#    be in any of the following formats:
#    a) 1 Reply
#    b) # Replies
#    c) View more replies
#    d) View # more replies
# 6. For both buttons, they belong to class "_4sxc _42ft", however
#    the text associated with each button is located in a different
#    class inside the class "_4sxc _42ft".
# 7. As a visualization, on a post with many comments, each with many
#    replies, the button to view more comments is always located
#    towards the bottom of the post, preceded by many buttons to view
#    more replies. Because of this nature, the easier approach would
#    be to simply find the first element on the post of class
#    "_4sxc _42ft" (by using "_4sxc"), clicking the button, and
#    repeating this process until no such elements are found on the post.
# 8. When a View More comments/replies button is clicked and fails to
#    load the content (infinitely loading), a spinning circle graphic
#    appears and stays to the right side of the button. This graphic is
#    located in the class "_4sxg img _55ym _55yn _55yo". Note that there
#    are no other classes in the HTML starting with "4sxg", so this can
#    be used to filter out the buttons that have already been clicked on
#    but are unable to load more content.

def get_ViewMoreBtnElements(commentSection_element):
    print("[FB SCRIPT] Finding View More comments/replies button elements...")
    ViewMore_btnElements = []
    try:
        ViewMore_btnElements = commentSection_element.find_elements_by_class_name("_4sxc")
    except NoSuchElementException:
        print("[FB SCRIPT]\tNo View More comments/replies button elements detected")
    print("[FB SCRIPT]\t", len(ViewMore_btnElements), "View More comments/replies button elements found")
    return ViewMore_btnElements

def remove_stuckViewMoreBtnElements(ViewMore_btnElements):
    print("[FB SCRIPT] Removing View More comments/replies buttons that are stuck...")
    ViewMore_btns = []
    stuck_btn_count = 0
    for btnElement in ViewMore_btnElements:
        try:
            loading_img = btnElement.find_element_by_class_name("_4sxg")
            stuck_btn_count += 1
        except NoSuchElementException:
            ViewMore_btns.append(btnElement)
        except StaleElementReferenceException:
            # Loading image was possibly present, but content may have successfully loaded
            # when the line to detect the loading image was executed, resulting in a
            # Stale Element Reference Exception to be thrown.
            stuck_btn_count += 1
    print("[FB SCRIPT]\t", stuck_btn_count, "comments/replies sections that are stuck loading have been detected & removed")
    return ViewMore_btns

def get_ViewMoreBtns(commentSection_element):
    print("[FB SCRIPT] Getting View More comments/replies buttons...")
    ViewMore_btnElements = get_ViewMoreBtnElements(commentSection_element)
    ViewMore_btns = remove_stuckViewMoreBtnElements(ViewMore_btnElements)
    print("[FB SCRIPT] ---------------", len(ViewMore_btns), "View More comments/replies buttons found ---------------")
    return ViewMore_btns

def click_ViewMoreBtns(ViewMore_btns):
    counter = 1
    for btn in ViewMore_btns:
        driver.execute_script("arguments[0].scrollIntoView();", btn)
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(0.5)
        print("[FB SCRIPT]\t" + str(counter) + ". Clicking View More comments/replies button #" + str(counter))# + " ... Location = " + ViewMore_btn_location + " (" + str(attempts) + " attempts remaining)")
        btn.click()
        counter += 1
    print("[FB SCRIPT] --------------------------------------------------------------------------")
        
def click_ALL_ViewMoreBtns(commentSection_element):
    print("[FB SCRIPT] Initiating the process to search for and click on View More comments/replies buttons...")
    ViewMore_btns = get_ViewMoreBtns(commentSection_element)
    if len(ViewMore_btns) == 0:
        print("[FB SCRIPT] No View More comments/replies button elements detected on first search")
    else:
        attempts = 3
        while attempts != 0:
            try:
                click_ViewMoreBtns(ViewMore_btns)
                ViewMore_btns = get_ViewMoreBtns(commentSection_element)
                if len(ViewMore_btns) == 0:
                    print("[FB SCRIPT]\t", (attempts - 1), "attempts to search for buttons remaining")
                    attempts -= 1
                    print("[FB SCRIPT]\t Sleeping for", (time_to_sleep_for), "seconds...")
                    time.sleep(time_to_sleep_for)
                else:
                    attempts = 3
            except WebDriverException:
                print("[FB SCRIPT] Web Driver Exception thrown. Call function click_ALL_ViewMoreBtns() again to retry.")
                attempts = 0
    print("[FB SCRIPT] Ending the process to search for and click on View More comments/replies buttons")
    print("[FB SCRIPT] --------------------------------------------------------------------------")
    
# NOTE: Depending on strength of Internet connection and/or computer's computation capabilities,
#       setting the int variable "attempts" in the function above to a high number can NEVER
#       guarantee that every View More comments/replies buttons will be detected and clicked
#       because detection of such buttons depends on whether the content loads or not. The
#       content may never load or take a very long time to load. In the case of the latter,
#       because it is unpredictable how long it would take for the content to load (if it loads
#       at all), there is no way to hard-wire a surefire method into the code.
#       However, an optional, additional step may be included to continuously execute the
#       function above for a finite number of times. To do so: Write a new function with an
#       int variable "reps", which will be the number of times the function will call the
#       the function above. Use a while loop such that while reps != 0, call the function above.
#       The new function should call the function above "reps" times, which will cause the total
#       number of times the script tries to find and click View More comments/replies buttons
#       to be equal to "reps" * "attempts". Although, it is important to note that this is still
#       not a solution to detect and click every button, but an optional, additional step if the
#       user would like to commit more time and effort to finding as many comments as possible.
#       The user may also add time.sleep() where reasonable in the new function to allow more
#       time and opportunity for the page to load content.

def click_ALL_ViewMoreBtns_wInput(commentSection_element):
    # Initial function call
    print("[FB SCRIPT] Making initial function call of click_ALL_ViewMoreBtns()...")
    click_ALL_ViewMoreBtns(commentSection_element)
    print("[FB SCRIPT] Finished initial function call of click_ALL_ViewMoreBtns()")
    print("[FB SCRIPT] Please manually check if all View More comments/replies buttons were detected and clicked")
    func_recall = True
    while func_recall == True:
        user_command = input("[FB SCRIPT] Call function click_ALL_ViewMoreBtns() again? y/n > ")
        if user_command == "y":
            print("[FB SCRIPT]\tYou entered:'" + user_command + "'. Calling function again...")
            print("[FB SCRIPT] --------------------------------------------------------------------------")
            click_ALL_ViewMoreBtns(commentSection_element)
        elif user_command == "n":
            print("[FB SCRIPT]\tYou entered:'" + user_command + "'. Proceeding with rest of script...")
            print("[FB SCRIPT] --------------------------------------------------------------------------")
            func_recall = False
        else:
            print("[FB SCRIPT]\tInput not recognized.")


# In[7]:


##### FUNCTIONS FOR PART 2: POST DATA EXTRACTION ####################################

def get_postListElements():
    print("[FB SCRIPT] Getting 'postList_elements', a list of elements, each containing several posts...")
    postList_elements = driver.find_elements_by_class_name("_1xnd")
    print("[FB SCRIPT] Found " + str(len(postList_elements)) + " post list elements")
    return postList_elements

def get_postElements(postList_elements):
    print("[FB SCRIPT] Getting 'post_elements', a list of elements, each pertaining to a single post...")
    post_elements = postList_elements[0].find_elements_by_xpath(".//div[@class='_4-u2 _4-u8']")
    print("[FB SCRIPT] Found a total of " + str(len(post_elements)) + " post elements on the page")
    return post_elements

def get_postUserName(post_element):
    post_userName_element = post_element.find_element_by_class_name("fwb")
    post_userName = post_userName_element.text
    return post_userName

def get_postTimestamp(post_element):
    post_userTimestamp_outerElement = post_element.find_element_by_class_name("_5pcq")
    post_userTimestamp_innerElement = post_userTimestamp_outerElement.find_element_by_tag_name("abbr")
    post_userTimestamp = post_userTimestamp_innerElement.get_attribute("title")
    return post_userTimestamp

def parse_postTimestampDate(timestamp):
    return timestamp.split(", ")[0]

def parse_postTimestampTime(timestamp):
    return timestamp.split(", ")[1]

def get_postText(post_element):
    post_text_element = post_element.find_element_by_class_name("_5pbx")
    post_text = post_text_element.text
    if post_text.endswith("See More"):
        print("[FB SCRIPT]\t'See More' detected at end of post's text")
        click_postSeeMore(post_postText_element)
        print("[FB SCRIPT]\tRe-extracting text...")
        post_text = post_postText_element.text
    return post_text

def get_numComments(post_element):
    numComments = 0
    try:
        numComments_element = post_element.find_element_by_class_name("_3hg-")
        numComments_str = numComments_element.text
        numComments = int(numComments_str.split()[0])
    except ValueError:
        # Displayed number of comments cannot be converted to type int
        numComments = numComments_str.split()[0]
        # Need to add lines of code to find specific number of comments on post
    except NoSuchElementException:
        print("[FB SCRIPT] Did not detect element noting number of comments on post.")
    return numComments

##### FUNCTIONS FOR PART 2: POST DATA EXTRACTION FOR LIVE POSTS #####################

# NOTE: The top line of the post that reads "[Facebook Page Name] was live." is
#       in the span class "fcg" where "[Facebook Page Name]" is inside the span
#       class "fwb", which is inside class "fcg". The text " was live." is
#       located inside of class "fcg", but outside of class "fwb", below it.
# NOTE: It appears that using the find_element_by_class_name("fcg") on a post
#       that is NOT live results in simply getting the "[Facebook Page Name]",
#       which is normally found through using "fwb".

def check_ifLivePost(post_element):
    post_userNameLine_element = post_element.find_element_by_class_name("fcg")
    post_userNameLine = post_userNameLine_element.text
    if post_userNameLine.endswith(" was live."):
        return True
    else:
        return False


# In[8]:


##### FUNCTIONS FOR PART 3: COMMENT DATA EXTRACTION #################################

# NOTES:
# 1. Using "_42ef" causes the top "Write a comment..." input section
#    and any "Write a reply..." input sections to also be included in
#    the list of found elements.
# 2. The "Write a post..." text and all "Write a reply..." texts are
#    found in the class "_1p1v", which is inside class "_42ef". (The
#    class "_1p1t" is not seen in other "_42ef" classes that hold an
#    actual comment made by another user. In other words, class "_1p1v"
#    can be used to filter out "Write a reply..." input boxes from
#    actual comments.) "Write a comment..." texts are found in the
#    class "_7c-t".
# 3. Using "_72vr", which is located inside the class "_42ef",
#    will cause only comments already made on the post to appear in the
#    resulting list of elements. However, the class "_72vr" is only
#    comprised of the comment's poster's username and text. It does not
#    include the classes noting the comment's timestamp and reactions.
# 4. The timestamp of the comment is in the class "livetimestamp",
#    which is located inside the class "_6qw7", which is located inside
#    class "_42ef", but NOT inside class "_72vr".
# 5. In order to also extract the timestamp and reactions, "_42ef"
#    should be used when finding comment elements.
# 6. In the case of the very first "Write a comment..." input section
#    found at the top of the comment section on any post, one can
#    simply exclude the 1st item in the list of found "_42ef" elements
#    because it would be the 1st found element.
# 7. However, because "Write a reply..." input sections are found in the
#    middle of actual comments, it is necessary to include a step to
#    remove these elements from the list of found "_42ef" elements.

def get_commentSectionElement(post_element):
    print("[FB SCRIPT] Getting post's comment section element...")
    commentSection_element = post_element.find_element_by_class_name("_3w53")
    return commentSection_element

def get_commentElements(commentSection_element):
    print("[FB SCRIPT] Getting single comment/reply element(s)...")
    # 1. Get single comment/reply elements
    comment_elements = commentSection_element.find_elements_by_class_name("_42ef")[1:]
    print("[FB SCRIPT] Found a total of " + str(len(comment_elements)) + " element(s) of class '_42ef'")
    # 2. Find elements pertaining to "Write a reply..." input sections
    input_elements = []
    i = 0
    print("[FB SCRIPT] Finding input elements in class '_42ef' elements...")
    for comment_element in comment_elements:
        try:
            input_signifier = comment_element.find_element_by_class_name("_1p1v")
            if input_signifier.text == "Write a reply...":
                print("[FB SCRIPT]\t" + str(i+1) + ". Found 'Write a reply...' section")
                input_elements.append(comment_element)
                i += 1
            else:
                print("[FB SCRIPT] Found '_1p1v' class inside a class '_42ef' element, but text does not equal 'Write a reply...'")
        except NoSuchElementException:
            # Element is an expected comment
            pass
    print("[FB SCRIPT] Found a total of " + str(i) + " input element(s)")
    # 3. Remove elements pertaining to "Write a reply..." input sections
    if len(input_elements) != 0:
        print("[FB SCRIPT] Removing input elements from comment elements...")
        for input_element in input_elements:
            comment_elements.remove(input_element)
    print("[FB SCRIPT] Found a total of " + str(len(comment_elements)) + " comment element(s)")
    return comment_elements

def get_commentUserName(comment_element):
    # NOTE: Class "_6qw4" is inside class "_72vr"
    comment_userName = comment_element.find_element_by_class_name("_6qw4").text
    return comment_userName

def get_commentTimestamp(comment_element):
    # NOTE: Class "livetimestamp" is inside class "_6qw7"
    comment_timestamp = comment_element.find_element_by_class_name("livetimestamp").get_attribute("title")
    if comment_timestamp == "":
        comment_timestamp = comment_element.find_element_by_class_name("livetimestamp").get_attribute("data-tooltip-content")
    return comment_timestamp

def parse_commentTimestampDate(timestamp):
    # Monday, April 15, 2019 at 5:56 PM
    #print("timestamp =", timestamp)
    split_timestamp = timestamp.split()[1:-3]
    #print("split_timestamp =", split_timestamp)
    month = split_timestamp[0]
    if month == "January":
        month = "1"
    elif month == "February":
        month = "2"
    elif month == "March":
        month = "3"
    elif month == "April":
        month = "4"
    elif month == "May":
        month = "5"
    elif month == "June":
        month = "6"
    elif month == "July":
        month = "7"
    elif month == "August":
        month = "8"
    elif month == "September":
        month = "9"
    elif month == "October":
        month = "10"
    elif month == "November":
        month = "11"
    elif month == "December":
        month = "12"
    else:
        month = "ERROR"
    day = split_timestamp[1][:-1]
    year = split_timestamp[2]
    return month + "/" + day + "/" + year

def parse_commentTimestampTime(timestamp):
    comment_timestamp_split = timestamp.split()[5:]
    comment_timestampTime = ' '.join(comment_timestamp_split)
    return comment_timestampTime

def get_commentText(comment_element):
    # NOTES:
    # 1. Class "_3l3x" is inside class "_72vr"
    # 2. Comments that are composed of solely a picture or sticker do NOT
    #    have a "_3l3x" class at all.
    try:
        comment_text = comment_element.find_element_by_class_name("_3l3x").text
        if comment_text.endswith("See More"):
            print("[FB SCRIPT]\t'See More' detected at end of comment's text")
            click_commentSeeMore(comment_element)
            print("[FB SCRIPT]\tRe-extracting text...")
            comment_text = comment_element.find_element_by_class_name("_3l3x").text
        return comment_text
    except NoSuchElementException:
        print("[FB SCRIPT]\tNo text section detected in comment")
        return None


# In[9]:


##### FUNCTIONS FOR PART 4: MISC. FUNCTIONS #########################################

def make_filename(timestampDate, timestampTime):
    timestampDate_split = timestampDate.split("/")
    month = timestampDate_split[0]
    if len(month) == 1:
        month = "0" + month
    day = timestampDate_split[1]
    if len(day) == 1:
        day = "0" + day
    year = timestampDate_split[2]
    filenameDate = year + month + day
    filenameTime = timestampTime.replace(":", "-")
    filenameTime = filenameTime.replace(" ", "")
    filename = filename_header + "_Posted-" + filenameDate + "_" + filenameTime + ".csv"
    return filename


# In[10]:


##### FUNCTIONS FOR PART 5: PUTTING IT ALL TOGETHER #################################

def report_postData(post_element):
    print("[FB SCRIPT] Getting original post's data...")
    # Get original poster's username
    post_userName = get_postUserName(post_element)
    print("\tOriginal Poster Username:", post_userName)
    # Get original post's timestamp
    post_timestamp = get_postTimestamp(post_element)
    print("\tOriginal Post's Timestamp:", post_timestamp)
    post_timestampDate = parse_postTimestampDate(post_timestamp)
    print("\tOriginal Post's Date:", post_timestampDate)
    post_timestampTime = parse_postTimestampTime(post_timestamp)
    print("\tOriginal Post's Time:", post_timestampTime)
    # Get number of comments on post
    numComments = get_numComments(post_element)
    print("\tNumber of Comments on Original Post:", numComments)
    # Make filename
    filename = make_filename(post_timestampDate, post_timestampTime)
    return filename

def get_single_commentData(comment_element):
    # Get comment's poster's username
    comment_userName = get_commentUserName(comment_element)
    #print("Comment's Poster Username:", comment_userName)
    # Get comment's timestamp
    comment_timestamp = get_commentTimestamp(comment_element)
    #print("Comment's Timestamp:", comment_timestamp)
    comment_timestampDate = parse_commentTimestampDate(comment_timestamp)
    #print("Comment's Date:", comment_timestampDate)
    comment_timestampTime = parse_commentTimestampTime(comment_timestamp)
    #print("Comment's Time:", comment_timestampTime)
    # Get comment's text
    comment_postText = get_commentText(comment_element)
    # Check if function to get text returned None 
    if comment_postText == None:
        return None
    #print("Comment's Text:", comment_postText)
    return [comment_userName, comment_timestampDate, comment_timestampTime, comment_postText]

def get_commentData_onPost(post_element):
    # Get comment section element
    commentSection_element = get_commentSectionElement(post_element)
    # Click on any and all View More comments/replies buttons on the comment section of the post
    click_ALL_ViewMoreBtns_wInput(commentSection_element)
    # Get single comment/reply elements
    comment_elements = get_commentElements(commentSection_element)
    # Check length of comment_elements
    if len(comment_elements) == 0:
        print("[FB SCRIPT] No comments detected on post -- Not extracting comment data for post")
        return None
    all_commentData = []
    for comment_element in comment_elements:
        comment_data = get_single_commentData(comment_element)
        if comment_data != None:
            all_commentData.append(comment_data)
    return all_commentData
    
def extract_data(post_element):
    print("[FB SCRIPT] Checking if post was a Live Post...")
    # Check if post was a live post
    LivePost_check = check_ifLivePost(post_element)
    print("\tOriginal Post is Live Post:", LivePost_check)
    if LivePost_check == True:
        print("[FB SCRIPT] Post is a Live Post -- Not extracting data for post")
        return None
    ("[FB SCRIPT] Post is a NOT a Live Post -- Will attempt to extract data for this post")
    # Print post data to terminal and make filename
    filename = report_postData(post_element)
    # Get all comment data
    all_commentData = get_commentData_onPost(post_element)
    # Check if function returned None (no comments on post)
    if all_commentData == None:
        return None
    # Set up column names for output file
    col_names = ["Username", "Date", "Time", "Comment"]
    # Make Pandas Data Frame object
    df = pd.DataFrame(all_commentData, columns = col_names)
    print("[FB SCRIPT] --------------------------------------------------------------------------")
    print(df)
    print("[FB SCRIPT] --------------------------------------------------------------------------")
    # Export Pandas Data Frame object to a .csv file
    df.to_csv((path_to_folder + filename), index=None, header=True, encoding="utf-8-sig")
    return 0


# In[11]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
print("[FB SCRIPT] Setting up ChromeDriver...\n")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# In[13]:


# NOTE: If you want to get more than just the first few posts:
# 1. Manually log into Facebook in the window Chrome Driver is operating.
# 2. Reload the Facebook page you want to scrape (while logged in).
# This will allow you to view more posts than a user that is not logged in.

# Open URL with a timeout
try:
    print("[FB SCRIPT] Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("[FB SCRIPT] TimeoutException has been thrown. " + str(ex))


# In[14]:


# Scroll to the bottom of the page to reveal posts...
# NOTES:
# 1. scroll_inc is an integer (defined under GLOBAL VARIABLES), which is the number of times
#   "scroll_to_bottom()" is called in the below for loop. Having a finite number will allow
#    the user to stop loading posts if and when desired.
# 2. It is advised to have scroll_inc be a small number and simply execute the below
#    function repeatedly to load posts incrementally, rather than all at once.
# 3. The user may reach a point where Facebook will no longer automatically load more
#    posts when you reach the bottom, and therefore, may need to manually click on the
#    "See More" button if they wish to load more posts on the page.

scroll_to_bottom_wInput()


# In[16]:


# Get the elements holding the lists of posts
# postLists_elements is a list in which each item is a WebElement
# representing a section on the page containing 7 or 8 or something posts.

postList_elements = get_postListElements()

# NOTE: If there is no lag when loading posts as Chrome Driver scrolls down,
#       the number of found elements should be 1 more than the scroll_count.


# In[17]:


# Get ALL elements representing a post on the page
# NOTE: All posts should be written by the page's owner (e.g. company, manager of the acct, etc.)
#       Because of the onion-like structure of the Facebook html,
#       the following line of code can be called on the first item in postList_elements,
#       as it should be the element representing the outermost list of posts in html.

post_elements = get_postElements(postList_elements)

# NOTE: If you 1) right-click on the page
#              2) click on "Inspect"
#              3) hit ctrl+f to search in the html
#              4) put "_4-u2 _4-u8" in the search box
#       The number of found post elements (from the code) should be 1 less
#       than (or around) the number of search results found in the "Inspect" html


# In[55]:


test_post = post_elements[0]


# In[56]:


##### ORIGINAL POST DATA EXTRACTION #####

print("[FB SCRIPT] Getting original post's data...\n")

# Check if post was a live post
LivePost_check = check_ifLivePost(test_post)
print("Original Post is Live Post:", LivePost_check)

# Get original poster's username
post_userName = get_postUserName(test_post)
print("Original Poster Username:", post_userName)

# Get original post's timestamp
post_timestamp = get_postTimestamp(test_post)
print("Original Post's Timestamp:", post_timestamp)
post_timestampDate = parse_postTimestampDate(post_timestamp)
print("Original Post's Date:", post_timestampDate)
post_timestampTime = parse_postTimestampTime(post_timestamp)
print("Original Post's Time:", post_timestampTime)


# In[57]:


# Get original post's text

# There are 2 ways to get the original post's text:
# Method 1:
# 1. Get the element with the class name "_5pbx"
# 2. Get the post's text with element.text
# Method 2:
# 1. Get the <p> element(s) pertaining to the post's text
#    using element.find_elements_by_tag_name("p") on:
#    a) the element with the class name "_5pbx", or
#    b) the element of the entire post. (This works because
#       all <p> element(s) under this element pertain to the
#       post's text. There are no other <p> elements that
#       hold extraneous textual data.)
# 2. Get the text of each <p> element separately
# 3. Join all extracted text.
#
# NOTES:
# 1. No matter which method is used, if the post's text contains "See More",
#    it MUST be clicked for ALL of the text to be extracted.
# 2. "See More" will appear in the result text using Method 1, but will NOT
#    appear anywhere in the result text(s) using Method 2.
# 3. Even if Method 2 is used, the text hidden by the "See More" on the page
#    will not appear in the extracted text even if it is hardcoded in the HTML.
# 4. The <p> element(s) containing any text that is hidden under a "See More"
#    are placed under the <div class="text_exposed_show">.

post_text = get_postText(test_post)
print("Original Post's Text:")
print(post_text)


# In[58]:


# Get number of comments on post
numComments = get_numComments(test_post)
print("Number of Comments:", numComments)


# In[59]:


##### DEFAULT POST'S COMMENT DATA EXTRACTION #####

# Get comment section element
commentSection_element = get_commentSectionElement(test_post)


# In[60]:


# NOTES:
# 1. ALL "View [x] more comments" and "[x] Reply/Replies" buttons must
#    first be clicked to reveal hidden comments and replies so that
#    they display on the page. Failing to do so will not allow the
#    script to capture these comments and replies.

# Click on any and all View More comments/replies buttons on the comment section of the post
click_ALL_ViewMoreBtns_wInput(commentSection_element)


# In[61]:


# Get single comment/reply elements
comment_elements = get_commentElements(commentSection_element)


# In[ ]:


test_comment = comment_elements[44]


# In[ ]:


# Get comment's poster's username
comment_userName = get_commentUserName(test_comment)
print("Comment's Poster Username:", comment_userName)

# Get comment's timestamp
comment_timestamp = get_commentTimestamp(test_comment)
print("Comment's Timestamp:", comment_timestamp)
comment_timestampDate = parse_commentTimestampDate(comment_timestamp)
print("Comment's Date:", comment_timestampDate)
comment_timestampTime = parse_commentTimestampTime(comment_timestamp)
print("Comment's Time:", comment_timestampTime)

# Get comment's text
comment_userPost = get_commentText(test_comment)
print("Comment's Text:", comment_userPost)


# In[66]:


# Open URL with a timeout
try:
    print("[FB SCRIPT] Attempting to open URL:", myURL, "\n")
    driver.set_page_load_timeout(timeout_for)
    driver.get(myURL)
except TimeoutException as ex:
    isrunning = 0
    print("[FB SCRIPT] TimeoutException has been thrown. " + str(ex))


# In[231]:


scroll_to_bottom_wInput()


# In[232]:


postList_elements = get_postListElements()


# In[233]:


post_elements = get_postElements(postList_elements)


# In[282]:


current_post = post_elements[416]


# In[283]:


result = extract_data(current_post)
if result != None:
    print("[FB SCRIPT] Check folder for output file")
    
    