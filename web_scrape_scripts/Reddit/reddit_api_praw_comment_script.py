#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# reddit_api_praw_comment_script.py.py
#
# Description:
# Script for getting comments in each reddit submission, using...
#
# The output file from: Reddit_API_Praw_Subreddit_Script_v1.py
# Homepage URL: https://www.reddit.com/
# Tools: Reddit API Praw
# Data Organizer: Pandas
#
# Version: 2.1
# Date Created: 02/15/2019
# Last Modified: 03/14/2019
#####################################################################################

#####################################################################################
#
# V2.1 Notes:
#
# 1. Added lines that will add a custom comment ID for each Reddit comment scraped
#    for a project. It will be contained in the "My Comment ID" column of the
#    Pandas DataFrame.
#
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################

import praw
import pandas as pd
import datetime as dt
from praw.models import MoreComments

#####################################################################################


# In[258]:


##### GLOBAL VARIABLES ##############################################################

# Path to the folder you want to save the file in (CHANGE AS NEEDED)
# Type: string ending with "/"
path_to_folder = "C://Users/kathleen.trinh/Documents/Geothermal/Reddit/"

# File name of the .csv file containing the list of submissions (CHANGE AS NEEDED)
# which is the output .csv file from running the script: reddit_api_praw_subreddit_script.py
# Type: string
# Note: Please end it with ".csv"
filename_timestamp = "190219"
subreddit_str = "hvacadvice"
#filename = "Reddit_" + subreddit_str + "_" + filename_timestamp
search_query = "York"
filename = "Reddit_" + subreddit_str + "_" + search_query + "_" + filename_timestamp
file_ext = ".csv"
submissions_filename = path_to_folder + filename + file_ext

#####################################################################################


# In[259]:


##### FUNCTIONS #####################################################################

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def check_dict_len(length, mydict):
    for k in mydict:
        print("\tLength of", k, "=", len(mydict[k]))
        if len(mydict[k]) != length:
            return False
    return True

#####################################################################################


# In[260]:


# Load .csv file containing list of threads in subreddit
topics_df = pd.read_csv(submissions_filename, usecols=['id', 'title', 'num_comments'], header=0, encoding='utf-8-sig')
print(topics_df)


# In[261]:


# Create reddit instance
reddit = praw.Reddit(client_id = "[YOUR_CLIENT_ID]",
                     client_secret = "[YOUR_CLIENT_SECRET]",
                     user_agent = "[YOUR_USER_AGENT]",
                     username = "[YOUR_USERNAME]",
                     password = "[YOUR_PASSWORD]")


# In[262]:


# Create subreddit instance
subreddit = reddit.subreddit(subreddit_str)


# In[264]:


# Get comments in each thread in subreddit
print(len(topics_df["id"]), "threads detected in subreddit:", subreddit_str, "\n")

counter = 0
total_comments = 0
num_threads_zero_comments = 0

for submission_id in topics_df["id"]:
    
    print("---------------------------------------------------------------------------\n")
    _counter = counter + 1
    print(str(_counter) + ". Getting comment data for submission #" + str(_counter) + ", id = " + submission_id + "...")
    num_comments_in_thread = topics_df["num_comments"][counter]
    print("\t" + str(num_comments_in_thread) + " comments detected in submission: " + str(submission_id))
    
    # Only get comment data if num_comments_in_thread > 0
    
    if num_comments_in_thread > 0:
        
        # Create submission instance
        submission = reddit.submission(id=submission_id)
    
        # Only need to call this once per submission because:
        # "Calling replace_more() is destructive.
        # Calling it again on the same submission instance has no effect."
        try:
            submission.comments.replace_more(limit=None)
        except:
            print("Encountered error while trying to replace 'MoreComments'")
            print("\tProceeding with data extraction process anyway...")
    
        # Put comment info into a dictionary
        comments_dict = {"My Comment ID": [] ,
                         "link_id": [],
                         "title": [],
                         "id": [],
                         "author": [],
                         "body": [],
                         "is_submitter": [],
                         "score": [],
                         "parent_id": [],
                         "distinguished": [],
                         "stickied": [],
                         "edited": [],
                         "permalink": [],
                         "created": []}
    
        i = 1
        for comment in submission.comments.list():
            total_comments += 1
            MyCommentID = "Reddit_" + comment.link_id + "_Com" + str(i)
            i += 1
            comments_dict["My Comment ID"].append(MyCommentID)
            comments_dict["link_id"].append(comment.link_id)
            comments_dict["title"].append(submission.title)
            comments_dict["id"].append(comment.id)
            comments_dict["author"].append(comment.author)
            comments_dict["body"].append(comment.body)
            comments_dict["is_submitter"].append(comment.is_submitter)
            comments_dict["score"].append(comment.score)
            comments_dict["parent_id"].append(comment.parent_id)
            comments_dict["distinguished"].append(comment.distinguished)
            comments_dict["stickied"].append(comment.stickied)
            comments_dict["edited"].append(comment.edited)
            comments_dict["permalink"].append(comment.permalink)
            comments_dict["created"].append(comment.created)    
    
        print("\tMaking output for submission: " + submission_id + "...\n")
        # Create Pandas DataFrame
        comments_df = pd.DataFrame(comments_dict)
    
        # Add timestamp column to DataFrame
        _timestamp = comments_df["created"].apply(get_date)
        comments_df = comments_df.assign(timestamp = _timestamp)
    
        # Export Pandas DataFrame object to a .csv file
        comments_df.to_csv((path_to_folder + filename + "_" + submission_id + file_ext),
                           index=None,
                           header=True,
                           encoding='utf-8-sig')
    
    # If num_comments_in_thread <= 0
    else:
        num_threads_zero_comments += 1
        print("\tNOT getting comment data for submission: " + submission_id + "\n")
    
    counter += 1


# In[265]:


print("---------------------------------------------------------------------------\n")
print("Number of threads with 0 comments =", num_threads_zero_comments)
print("Number of output files should be =", (len(topics_df["id"]) - num_threads_zero_comments), "\n")
print("Total comments extracted =", total_comments, "\n")

