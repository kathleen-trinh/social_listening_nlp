#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# reddit_api_praw_subreddit_script.py
#
# Script for: 1) Getting submissions in a subreddit, and
#             2) Getting comments in each submission from part 1.
# using...
# Homepage URL: https://www.reddit.com/
# Tools: Reddit API Praw
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 02/14/2019
# Last Modified: 02/15/2019
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################

import praw
import pandas as pd
import datetime as dt
from praw.models import MoreComments

#####################################################################################


# In[103]:


##### GLOBAL VARIABLES ##############################################################

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string
path_to_folder = "C://Users/kathleen.trinh/Documents/Geothermal/Reddit/"

# File name you want to save the file for the list of submissions as (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
file_name_timestamp = "190215"
subreddit_str = "all"
search_query = "residential geothermal"
file_name = file_name_timestamp + "_Reddit_" + subreddit_str + "_" + search_query
file_ext = ".csv"

#####################################################################################


# In[104]:


##### FUNCTIONS #####################################################################

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def check_dict_len(length, mydict):
    for k in mydict:
        if len(mydict[k]) != length:
            return False
    return True

#####################################################################################


# In[105]:


# Create reddit instance
reddit = praw.Reddit(client_id = "[YOUR_CLIENT_ID]",
                     client_secret = "[YOUR_CLIENT_SECRET]",
                     user_agent = "[YOUR_USER_AGENT]",
                     username = "[YOUR_USERNAME]",
                     password = "[YOUR_PASSWORD]")


# In[106]:


# Create subreddit instance
subreddit = reddit.subreddit(subreddit_str)


# In[107]:


# Get threads in subreddit by either .top or .search
# NOTES:
# 1. Default value for limit=100
#    limit – Can be any number in 1-1000
#    Max value for limit=1000 -- "Reddit’s request limit* is 1000"
# 2. Default value for time_filter='all'
#    time_filter – Can be one of: all, day, hour, month, week, year (default: all)
# 3. subreddit.search(search_query) searches for threads containing search_query in subreddit
#    When using ".search()", results do not have submission.body,
#    so please comment out lines of code that include "body".
#    Using search seems to return 100 results.
# EXAMPLES: top_subreddit = subreddit.top()
#           top_500_subreddit = subreddit.top(limit=500)
#           search_subreddit = subreddit.search(search_query)

my_subreddit = subreddit.search(search_query)


# In[108]:


"""
# PRINT EXAMPLE:
for submission in subreddit.top(limit=1):
    print(submission.id)
    print(submission.title)
    print(submission.body)
    print(submission.author)
    print(submission.num_comments)
    print(submission.score)
    print(submission.upvote_ratio)
    print(submission.distinguished)
    print(submission.stickied)
    print(submission.edited)
    print(submission.url)
    print(submission.created)
"""


# In[109]:


# Put subreddit info into a dictionary
topics_dict = {"id": [],
               "title": [],
               #"body": [],
               "author": [],
               "num_comments": [],
               "score": [],
               "upvote_ratio": [],
               "distinguished": [],
               "stickied": [],
               "edited": [],
               "permalink": [],
               "url":[],
               "created": []}

counter = 1
for submission in my_subreddit:
    print(str(counter) + ". Getting data for submission #" + str(counter) + "...")
    topics_dict["id"].append(submission.id)
    topics_dict["title"].append(submission.title)
    #topics_dict["body"].append(submission.selftext)
    topics_dict["author"].append(submission.author)
    topics_dict["num_comments"].append(submission.num_comments)
    topics_dict["score"].append(submission.score)
    topics_dict["upvote_ratio"].append(submission.upvote_ratio)
    topics_dict["distinguished"].append(submission.distinguished)
    topics_dict["stickied"].append(submission.stickied)
    topics_dict["edited"].append(submission.edited)
    topics_dict["permalink"].append(submission.permalink)
    topics_dict["url"].append(submission.url)
    topics_dict["created"].append(submission.created)
    counter += 1
    


# In[110]:


# Create Pandas data frame
topics_df = pd.DataFrame(topics_dict)


# In[111]:


# Add timestamp column to data frame
_timestamp = topics_df["created"].apply(get_date)
topics_df = topics_df.assign(timestamp = _timestamp)


# In[112]:


# Export Pandas Data Frame object to a .csv file
topics_df.to_csv((path_to_folder + file_name + file_ext), index=None, header=True, encoding='utf-8-sig')

