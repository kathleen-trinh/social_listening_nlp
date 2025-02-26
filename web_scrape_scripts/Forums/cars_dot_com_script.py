#!/usr/bin/env python
# coding: utf-8

# In[4]:


#####################################################################################
# cars_dot_com_script.py
#
# Script for scraping a Consumer Reviews page on https://www.cars.com/ using...
# Homepage URL: https://www.cars.com/
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 01/31/2019
# Last Modified: 02/04/2019
#####################################################################################


# In[119]:


##### READ ME #######################################################################
#
# This script is able to scrape the Consumer Reviews for a vehicle on:
# https://www.cars.com/
#
# This script's code should only be executed at portions at a time due to
# ChromeDriver being unable to open the given webpage all the time.
# Please do not run this script as an executable / as a whole.
#
# Before running this script:
# 1. Change the values of the global variables in the "GLOBAL VARIABLES" section
#    as necessary. Please read the notes attached to each when changing the value.
# 2. Reminder: If you change the value of any of the global variables, please
#    re-run the "GLOBAL VARIABLES" section before executing any code that uses
#    the global variable you changed or updated.
# 3. cars.com can only show a maximum of 250 reviews per page. If there are more
#    than 250 reviews for a vehicle, there will be more than one page. This script
#    is only capable of scraping a single page at a time, so please manually change
#    the URL with the next page (after scraping the first page) and re-run the
#    script to scrape the next page separately.
#
# When running this script:
# 1. Messages will print out to the terminal to indicate where the code is
#    currently at during execution.
# 2. If the webpage does not load when ChromeDriver starts, please manually
#    reload the page in the same window until the webpage loads.
# 3. Please allow the webpage to fully load before moving on.
# 4. Please do not click on any buttons that read "Show Full Review".
#    Make sure all reviews have not been expanded by the user.
# 5. Please make sure the browser window displays the top of the page before
#    running the code that expands all reviews.
#
# NOTES:
# 1. If an error occurs during the data extraction process for one post,
#    the post's row will contain empty data on the Pandas data frame and output.
# 2. When extracing post data for one post, an IndexError message may appear to
#    indicate that the post in question did not include all 4 optional fields
#    towards the end of the review. These fields will show as blank strings in
#    the Pandas data frame and output.
#
##### CODE OVERVIEW #################################################################
#
# 1. Start up ChromeDriver and open the given URL on https://www.cars.com/.
# 2. Get all Post IDs associated with a review on the page.
# 3. Expand all reviews by clicking on the "Show Full Review" button on each post.
# 4. Extract the post data for each Post ID and parse certain fields as necessary.
# 5. Add the post's data to the global list (all_post_data) containing the data
#    for all posts.
# 6. Put the data in all_post_data into a Pandas data frame.
# 7. Export the data frame to a .csv file.
#
#####################################################################################


# In[14]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
import os
import re
import string
#####################################################################################


# In[160]:


##### GLOBAL VARIABLES ##############################################################

# Global variable to hold each post data on all pages (DO NOT CHANGE)
all_post_data = []

#####################################################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL of the page you want to scrape (CHANGE AS NEEDED)
# Type: string
# Note: Please make sure the URL links to the Consumer Reviews page of the car
# with the page displaying ALL reviews.
myURL = "https://www.cars.com/research/subaru-outback-2016/consumer-reviews/?pg=1&nr=250"

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
path_to_folder = "C://Users/kathleen.trinh/Documents/Subaru/Outback/"

# File name you want to save the file as (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name = "190204_cars(dot)com_ConsumerReviews_MY16SubaruOutback.csv"

#####################################################################################


# In[137]:


##### FUNCTIONS FOR GENERAL USE #####################################################

def print_test_post_data(testID):
    """
    This function is for testing purposes only.
    This function calls the functions in "FUNCTIONS FOR PART 2: POST DATA EXTRACTION"
    and prints out their return values.
    This function takes in a string (id) which is an arbitrary Post ID,
    gets the data for each field on the post,
    and prints the found data to the terminal.
    """
    postAuthLocDate = get_postAuthLocDate(testID)
    print("postAuthLocDate =", postAuthLocDate)
    parsed_postAuthLocDate = parse_postAuthLocDate(postAuthLocDate)
    print("parsed_postAuthLocDate =", parsed_postAuthLocDate)
    postOverallRating = get_postOverallRating(testID)
    print("postOverallRating = ", postOverallRating)
    postTitle = get_postTitle(testID)
    print("postTitle =", postTitle)
    postBody = get_postBody(testID)
    print("postBody =", postBody)
    postComfortRating = get_postComfortRating(testID)
    print("postComfortRating =", postComfortRating)
    postIntDesRating = get_postIntDesRating(testID)
    print("postIntDesRating =", postIntDesRating)
    postPerformanceRating = get_postPerformanceRating(testID)
    print("postPerformanceRating =", postPerformanceRating)
    postValueRating = get_postValueRating(testID)
    print("postValueRating =", postValueRating)
    postReliabilityRating = get_postReliabilityRating(testID)
    print("postReliabilityRating =", postReliabilityRating)
    postExtStylingRating = get_postExtStylingRating(testID)
    print("postExtStylingRating =", postExtStylingRating)
    postOptData = get_postOptData(testID)
    print("postOptData =", postOptData)


# In[138]:


##### FUNCTIONS FOR PART 1: FIND ALL POST IDs #######################################
# NOTE: Every post ID is a 6-digit number

# Get TOTAL number of reviews:
def get_num_reviews():
    """
    This function takes in no parameters,
    finds and returns the total number of reviews on the page
    as an integer.
    """
    num_reviews_element = driver.find_elements_by_xpath('//*[@id="cr-review-listings"]/cars-research-consumer-review-listings/ng-transclude/div[1]/p/b[2]')[0]
    num_reviews = num_reviews_element.text
    return int(num_reviews)

# Step 1 in order to find ALL post IDs:
# Get ALL id tags on page
def get_all_ids_on_page():
    """
    This function takes in no parameters,
    finds all elements containing an id with "postmenu" on the current page,
    and returns a list of strings (ids_as_str) of all found elements.
    """
    print("Getting ids on page...\n")
    ids_on_page = driver.find_elements_by_xpath("//*[@id]")
    ids_as_str = []
    for i in ids_on_page:
        ids_as_str.append(i.get_attribute('id'))
    return ids_as_str

# Step 2 in order to find ALL post IDs:
# Filter list of all IDs on page and get ONLY IDs that are a 6-digit number
def get_post_ids_from_all_ids(all_ids):
    """
    This function takes in a list of strings (all_ids),
    iterates through the list and checks if each string is a 6-digit number.
    It returns a list of strings (all_post_ids) with each string being
    a 6 digit number found in the original given list.
    """
    print("Getting ONLY Post IDs...\n")
    all_post_ids = []
    for id in all_ids:
        if len(id) == 6 and id.isdigit() == True:
            all_post_ids.append(id)
        else:
            pass
    return all_post_ids

# Function to combine Steps 1 and 2:
def get_all_post_ids():
    """
    This function takes in no parameters,
    gets all the ids on the page,
    and returns a list of strings (all_post_ids)
    with each string being a 6-digit Post ID.
    """
    ids_on_page = get_all_ids_on_page()
    all_post_ids = get_post_ids_from_all_ids(ids_on_page)
    return all_post_ids

# Check function to check if length of the list containing the post IDs is equal to the total number of reviews
def check_num_reviews(post_ids, num_reviews):
    """
    This function takes in a list (post_ids)
    and an integer (num_reviews),
    checks if the length of the list is equal to the integer,
    and returns a Boolean True or False.
    """
    if len(post_ids) == num_reviews:
        return True
    else:
        return False


# In[139]:


##### FUNCTIONS FOR PART 2: POST DATA EXTRACTION ####################################
# NOTES:
# 1. Every post is hidden by a "Show Full Review"
# 2. Most posts have the info: "by [postAuthorName] from [postLocation] on [postDate]"
#    Sometimes, the location is omitted: "by [postAuthorName] on [postDate]"
#    However, an excepton is: "by [postAuthorName] from on [postDate]"
# 3. Not all posts include the last 4 fields

# Click on "Show Full Review"
# XPath for "Show Full Review": //*[@id="148125"]/div[3]/a
# CSS selector for "Show Full Review": #\31 48125 > div.show-hide-container > a
# CSS selector note: The Post ID (6 digits) gets split up such that the first digit 
# is after "3", followed by a space " ", followed by the remaining 5 digits.
def click_ShowFullReview():
    """
    This function takes in no parameters,
    finds the first element on the page with the link text 'Show Full Review',
    which should be a button located at the bottom of a review, hiding the rest of its contents,
    and clicks the element (the 'Show Full Review' button).
    """
    ShowFullReview_element = driver.find_element_by_link_text("Show Full Review")
    ShowFullReview_element.click()

# Get the string containing the post's: author name, location, and date
# XPath for "by [postAuthorName] from [postLocation] on [postDate]": //*[@id="148125"]/p[2]
def get_postAuthLocDate(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page containing the Author, Location, and Date
    for the given Post ID,
    and returns the found string (postAuthLocDate).
    """
    postAuthLocDate_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/p[2]')[0]
    postAuthLocDate = postAuthLocDate_element.text
    #print("postAuthLocDate =", postAuthLocDate)
    return postAuthLocDate

# Get the Overall Star Rating
# XPath for the post's Overall Star Rating: //*[@id="148125"]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postOverallRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the Overall Star Rating (out of 5 stars)
    for the given Post ID,
    and returns a string (postOverallRating), which should be the number of stars.
    """
    postOverallRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/cars-star-rating')[0]
    postOverallRating = postOverallRating_element.get_attribute("rating")
    #print("postOverallRating =", postOverallRating)
    return postOverallRating

# Get the post's Title
# XPath for the post's Title: //*[@id="148125"]/p[1]/a
def get_postTitle(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the post's Title
    for the given Post ID,
    and returns the found string (postTitle).
    """
    postTitle_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/p[1]/a')[0]
    postTitle = postTitle_element.text
    #print("postTitle =", postTitle)
    return postTitle

# Get the post's Body (the author's inputted textual review)
# XPath for the post's Body: //*[@id="148125"]/p[3]
def get_postBody(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the post's Body
    for the given Post ID,
    and returns the found string (postBody).
    """
    postBody_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/p[3]')[0]
    postBody = postBody_element.text
    #print("postBody = ", postBody)
    return postBody

# Get the Comfort Rating
# XPath for the Comfort Rating: //*[@id="148125"]/div[1]/div[1]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postComfortRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the 'Comfort' Rating (out of 5)
    for the given Post ID,
    and returns a string (postComfortRating), which should be the number rating.
    """
    postComfortRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div[1]/cars-star-rating')[0]
    postComfortRating = postComfortRating_element.get_attribute("rating")
    #print("postComfortRating =", postComfortRating)
    return postComfortRating

# Get the Interior Design Rating
# XPath for the Interior Design Rating: //*[@id="148125"]/div[1]/div[3]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postIntDesRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the 'Interior Design' Rating (out of 5)
    for the given Post ID,
    and returns a string (postIntDesRating), which should be the number rating.
    """
    postIntDesRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div[3]/cars-star-rating')[0]
    postIntDesRating = postIntDesRating_element.get_attribute("rating")
    #print("postIntDesRating =", postIntDesRating)
    return postIntDesRating

# Get the Performance Rating
# XPath for the Performance Rating: //*[@id="148125"]/div[1]/div[5]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postPerformanceRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the 'Performance' Rating (out of 5)
    for the given Post ID,
    and returns a string (postPerformanceRating), which should be the number rating.
    """
    postPerformanceRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div[5]/cars-star-rating')[0]
    postPerformanceRating = postPerformanceRating_element.get_attribute("rating")
    #print("postPerformanceRating =", postPerformanceRating)
    return postPerformanceRating

# Get the Value for the Money Rating
# XPath for the Value for the Money Rating: //*[@id="148125"]/div[1]/div[2]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postValueRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the 'Value for the Money' Rating (out of 5)
    for the given Post ID,
    and returns a string (postValueRating), which should be the number rating.
    """
    postValueRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div[2]/cars-star-rating')[0]
    postValueRating = postValueRating_element.get_attribute("rating")
    #print("postValueRating =", postValueRating)
    return postValueRating

# Get the Reliability Rating
# XPath for the Reliability Rating: //*[@id="148125"]/div[1]/div[4]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postReliabilityRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the 'Reliability' Rating (out of 5)
    for the given Post ID,
    and returns a string (postReliabilityRating), which should be the number rating.
    """
    postReliabilityRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div[4]/cars-star-rating')[0]
    postReliabilityRating = postReliabilityRating_element.get_attribute("rating")
    #print("postReliabilityRating =", postReliabilityRating)
    return postReliabilityRating

# Get the Exterior Styling Rating
# XPath for the Exterior Styling Rating: //*[@id="148125"]/div[1]/div[6]/cars-star-rating
# NOTE: The actual rating is under an attribute called "rating"
def get_postExtStylingRating(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the element on the page for the 'Exterior Styling' Rating (out of 5)
    for the given Post ID,
    and returns a string (postExtStylingRating), which should be the number rating.
    """
    postExtStylingRating_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/div[1]/div[6]/cars-star-rating')[0]
    postExtStylingRating = postExtStylingRating_element.get_attribute("rating")
    #print("postExtStylingRating =", postExtStylingRating)
    return postExtStylingRating

# Get the optional data, which includes --
# NOTE: Not every review includes very part.
# 1. type of car: "Purchased a ['New' or 'Used'] car"
# 2. car use: "Uses car for _______"
# 3. recommend: "['Does' or 'Does not'] recommend this car!!"
# 4. number of people who found the review useful:
#    NOTE: Not every review has been found useful / not useful.
#    A. If voted: "[x] out of [y] people found this review helpful. Did you?"
#    B. If never voted: "Did you find this review helpful?"
def get_postOptData(id):
    """
    This function takes in a string (id), which should be a Post ID,
    finds the elements on the page for the last 4 optional fields.
    It returns a tuple with 4 items corresponding to these fields:
    (postNewOrUsed, postCarUse, postRecommend, postNumFoundUseful)
    """
    # Default value for all 4 optional fields is an empty string
    postNewOrUsed = ""
    postCarUse = ""
    postRecommend = ""
    postNumFoundUseful = ""
    for i in ["4", "5", "6", "7"]:
        try:
            postOptData_element = driver.find_elements_by_xpath('//*[@id="' + id + '"]/p[' + i + ']')[0]
            postOptData = postOptData_element.text
            if postOptData.startswith("Purchased a"):
                postNewOrUsed = postOptData.split()[2]
            elif postOptData.startswith("Uses car for"):
                postCarUse = postOptData.split("Uses car for ")[1]
            elif postOptData.startswith("Does recommend"):
                postRecommend = "Yes"
            elif postOptData.startswith("Does not recommend"):
                postRecommend = "No"
            elif postOptData[0].isdigit():
                postNumFoundUseful = " ".join(postOptData.split()[0:4])
            elif postOptData == "Did you find this review helpful?":
                postNumFoundUseful = "No votes"
        except IndexError as e:
            print("\tIndexError: No more optional fields found for post: " + id)
            #print("\t\tError Message: " + str(e))
            break
    return (postNewOrUsed, postCarUse, postRecommend, postNumFoundUseful)

#####################################################################################

def get_postData(id):
    """
    This function takes in a string (id), which should be a Post ID,
    gets the value for each of the fields in the review,
    and returns a list of 20 items corresponding to each field in the review
    for the given Post ID.
    """
    print("Getting data for Post", id, "...")
    postAuthLocDate = get_postAuthLocDate(id)
    parsed_postAuthLocDate = parse_postAuthLocDate(postAuthLocDate)
    postOverallRating = get_postOverallRating(id)
    postTitle = get_postTitle(id)
    postBody = get_postBody(id)
    postComfortRating = get_postComfortRating(id)
    postIntDesRating = get_postIntDesRating(id)
    postPerformanceRating = get_postPerformanceRating(id)
    postValueRating = get_postValueRating(id)
    postReliabilityRating = get_postReliabilityRating(id)
    postExtStylingRating = get_postExtStylingRating(id)
    postOptData = get_postOptData(id)
    postData = [id, # Post ID
                parsed_postAuthLocDate[0], # Name of post's author
                parsed_postAuthLocDate[1], # Location (optional)
                parsed_postAuthLocDate[5], # Year
                parsed_postAuthLocDate[3], # Month
                parsed_postAuthLocDate[4], # Day of Month
                parsed_postAuthLocDate[2], # Day of Week
                postOverallRating, # Overall Star Rating
                postTitle, # Title of post
                postBody, # Body of post
                postComfortRating, # Comfort Rating
                postIntDesRating, # Interior Design Rating
                postPerformanceRating, # Performance Rating
                postValueRating, # Value for the Money Rating
                postReliabilityRating, # Reliability Rating
                postExtStylingRating, # Exterior Styling Rating
                postOptData[0], # New or Used (optional)
                postOptData[1], # car use (optional)
                postOptData[2], # Recommend - Yes or No (optional)
                postOptData[3] # Number of people who found review useful
               ]
    return postData


# In[140]:


##### FUNCTIONS FOR PART 3: POST DATA PARSING #######################################

# Parse the string: "by [postAuthorName] from [postLocation] on [postDate]"
# NOTE: Not all reviews include a location.
def parse_postAuthLocDate(AuthLocDate):
    """
    This function takes in a string (AuthLocDate),
    which should be in the same or a similar wording as:
    'by [postAuthorName] from [postLocation] on [postDate]'
    and returns a tuple with 6 items corresponding to:
    (postAuthor, postLocation, postDayOfWeek, postMonth, postDay, postYear)
    """
    #print("AuthLocDate =", AuthLocDate)
    split1 = AuthLocDate.split("by ")
    split2 = split1[-1].split(" from ")
    split3 = split2[-1].split(" on ")
    postAuthor = split2[0]
    postLocation = ""
    if len(split2) == 2:
        postLocation = split3[0]
    else:
        postAuthor = split3[0]
    if " from on " in AuthLocDate and postLocation.startswith("on "):
        postLocation = ""
    postDate = split3[-1].split()
    postDayOfWeek = postDate[-4]
    postMonth = postDate[-3]
    postDay = postDate[-2]
    postYear = postDate[-1]
    return (postAuthor, postLocation, postDayOfWeek, postMonth, postDay, postYear)

#####################################################################################


# In[161]:


##### IMPLEMENTATION ################################################################

# Setting up the ChromeDriver
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
    


# In[162]:


# Get all Post IDs, number of reviews, and check if they match

all_post_ids = get_all_post_ids()    
print("Number of Post IDs:", len(all_post_ids), "\n")

num_reviews = get_num_reviews()
print("Total number of consumer reviews:", num_reviews, "\n")

check_num_reviews_result = check_num_reviews(all_post_ids, num_reviews)
print("All Post IDs found? --", check_num_reviews_result, "\n")


# In[153]:


#####################################################################################
# This section is a scratch paper for testing all outputs using a single ID

#testID = all_post_ids[0]
#testID = all_post_ids[1]
#testID = "141573" #Same as above
#testID = all_post_ids[2]
#testID = "215718"
#testID = "256998"

#print_test_post_data("139142")
#print("\n")
#print(get_postData("139142"))

#####################################################################################


# In[163]:


# Click on "Show Full Review" button for all posts / reviews
print("Clicking on 'Show Full Review' for all posts...")
for i in range(len(all_post_ids)):
    try:
        print((i + 1), ". Attempting to click 'Show Full Review' button #", (i + 1), "...")
        click_ShowFullReview()
    except NoSuchElementException as e:
        print((i + 1), ". NoSuchElementException occurred trying to click 'Show Full Review' button #", (i + 1))
    except:
        print((i + 1), "Error occurred trying to click 'Show Full Review' button #", (i + 1))
        


# In[164]:


# Global variable used as a counter for printing purposes (1 - number of all reviews)
counter = 1

# For each Post ID, get the post data
for id in all_post_ids:
    try:
        print("\nCOUNTER =", counter)
        postData = get_postData(id)
        all_post_data.append(postData)
        print("Got data for Post", id, "!")
    except:
        print("Unexpected Error occurred while getting Post", id)
        print("Post", id, "will be empty on output")
        all_post_data.append([id])
    finally:
        counter += 1


# In[165]:


# Create Pandas Data Frame

col_names = ["Post ID",
            "Author Name",
            "Location",
            "Year",
            "Month",
            "Day",
            "Day of Week",
            "Overall Rating",
            "Title",
            "Body",
            "Comfort Rating",
            "Interior Design Rating",
            "Performance Rating",
            "Value for the Money Rating",
            "Reliability Rating",
            "Exterior Styling Rating",
            "New or Used",
            "Car Use",
            "Recommend",
            "Useful Review"]

df = pd.DataFrame(all_post_data, columns = col_names)


# In[166]:


print(df)


# In[167]:


# Export Pandas Data Frame object to a .csv file
df.to_csv((path_to_folder + file_name), index = None, header=True)


# In[159]:


# Close ChromeDriver
driver.close()

