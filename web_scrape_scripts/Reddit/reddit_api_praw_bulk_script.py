#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# reddit_api_praw_bulk_script.py
#
# Description:
# Given an input CSV file of search terms and subreddits to include in the search,
# this script scrapes comments on Reddit submissions / threads.
#
# Homepage URL: https://www.reddit.com/
# Tools: Reddit API Praw
# Data Organizer: Pandas
#
# Version: 2.2
# Date Created: 08/22/2019
# Last Modified: 09/09/2019
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################

import datetime as dt
import pandas as pd
import re

import praw
from praw.models import MoreComments

#####################################################################################


# In[7]:


##### GLOBAL VARIABLES ##############################################################

# Path to the project folder (CHANGE AS NEEDED)
# Type: string ending with "/"
PROJECT_FOLDER = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/Reddit/"

# Folder name of folder holding search result files (CHANGE AS NEEDED)
# Type: string ending with "/"
SUBREDDIT_FOLDER = "Subreddits/"

# Folder name of folder holding submission comments (CHANGE AS NEEDED)
# Type: string ending with "/"
SUBMISSIONS_FOLDER = "Submissions/"

# File name of the .csv input file (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with ".csv"
IN_FILENAME = "LEAF Social Listening Sources - Reddit.csv"

# Sample size of the input dataframe to use for script execution
# Type: integer
SAMPLE_SIZE = 0

# Date of script execution (YYMMDD) used for output filename purposes (CHANGE AS NEEDED)
# Type: string
DATE = "210914"

#####################################################################################


# In[4]:


##### FUNCTIONS #####################################################################

def get_subreddit_names(input_df, rem_rslash=True):
    subRs = [col for col in input_df][1:]
    if rem_rslash == True:
        subRs = [sub.split("r/")[-1] for sub in subRs]
    return subRs

def get_search_terms(input_df, as_dict=False):
    search_terms = list(input_df.loc[:, "Search Term"])
    #search_terms.remove("ENTIRE SUBREDDIT")
    search_terms = [term.split("\n")[0] for term in search_terms]
    if as_dict == False:
        return search_terms
    else:
        index_vals = [i for i in range(0, len(search_terms))]
        search_terms_dict = dict(zip(search_terms, index_vals))
        return search_terms_dict
    
def get_subR_search_dict(input_df, subR_name, search_terms):
    search_values = input_df.loc[:, subR_name]
    search_values = [str(x).upper() for x in search_values]
    subR_search_dict = dict(zip(search_terms, search_values))
    return subR_search_dict

#####################################################################################

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def check_dict_len(length, mydict):
    for k in mydict:
        if len(mydict[k]) != length:
            return False
    return True

def print_submission_info(reddit_submission):
    print(reddit_submission.id)
    print(reddit_submission.title)
    #print(reddit_submission.body)
    print(reddit_submission.author)
    print(reddit_submission.num_comments)
    print(reddit_submission.score)
    print(reddit_submission.upvote_ratio)
    print(reddit_submission.distinguished)
    print(reddit_submission.stickied)
    print(reddit_submission.edited)
    print(reddit_submission.url)
    print(reddit_submission.created)
    
def make_subreddit_filename(subreddit_name, search_query):
    if subreddit_name == "":
        subreddit_name = "all"
    if search_query == "ENTIRE SUBREDDIT":
        search_query = "all"
    filename = "Reddit Subreddit_" + subreddit_name + " Search_" + search_query + " " + DATE
    return filename

def make_submission_filename(subreddit_name, search_query, submission_ID):
    if subreddit_name == "":
        subreddit_name = "ALL"
    if search_query == "ENTIRE SUBREDDIT":
        search_query = "ALL"
    filename = "Reddit Subreddit_" + subreddit_name + " Search_" + search_query + " SubID_" + submission_ID + " " + DATE
    return filename

def make_submission_filename(submission_ID):
    filename = "Reddit SubID_" + submission_ID + " " + DATE
    return filename
    
#####################################################################################

# Get threads in subreddit by either .top or .search
# NOTES:
# 1. Default value for limit is limit=100
#    limit – Can be any number in 1-1000
#    Max value for limit is limit=1000 -- "Reddit’s request limit* is 1000"
# 2. Default value for time_filter is time_filter='all'
#    time_filter – Can be one of: all, day, hour, month, week, year (default: all)
# 3. subreddit.search(search_query) searches for threads containing "search_query" in "subreddit"
#    When using the function ".search()", results do not have submission.body,
#    so please comment out lines of code that include "body".
#    Using search seems to return 100 results.
# EXAMPLES: top_subreddit = subreddit.top()
#           top_500_subreddit = subreddit.top(limit=500)
#           search_subreddit_results = subreddit.search(search_query, limit=None)

def get_submission_IDs(subR_submission_IDs, subreddit, subreddit_name, search_query, make_output=True):
    
    if search_query == "ENTIRE SUBREDDIT":
        my_subreddit = subreddit.top(limit=None)
        search_query = "all"
    else:
        my_subreddit = subreddit.search(search_query, limit=None)
        
    # Set up dictionary to put subreddit info into (if make_output == True)
    topics_dict = {"search_subreddit": [],
                   "search_query": [],
                   "subreddit": [],
                   "id": [],
                   "title": [],
                   "body": [],
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
    
    # For each submission in the search result, get the submission ID,
    # and put subreddit info into the dictionary if make_output == True
    counter = 1
    for submission in my_subreddit:
        if submission.num_comments > 0:
            print(str(counter) + ". Getting submission ID for submission #" + str(counter) + " | submission ID = " + submission.id)
            subR_submission_IDs.add(submission.id)
            if make_output == True:
                print("\t Noting info about submission #" + str(counter) + "...")
                topics_dict["search_subreddit"].append(subreddit_name)
                topics_dict["search_query"].append(search_query)
                topics_dict["subreddit"].append(submission.permalink.split("/")[2])
                topics_dict["id"].append(submission.id)
                topics_dict["title"].append(submission.title)
                topics_dict["body"].append(submission.selftext)
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
        else:
            print(str(counter) + ". NOT getting submission ID for submission #" + str(counter) + " because it has 0 comments | submission ID = " + submission.id)
        counter += 1
    
    # If make_output == True, make .csv output for the search results in the subreddit
    if make_output == True:
        # Create Pandas DataFrame
        topics_df = pd.DataFrame(topics_dict)
        # Add timestamp column to DataFrame
        _timestamp = topics_df["created"].apply(get_date)
        topics_df = topics_df.assign(timestamp = _timestamp)
        # Export Pandas DataFrame object to a .csv file
        filename = make_subreddit_filename(subreddit_name, search_query)
        print("\nMaking .csv output for info about " + str(len(topics_dict)) + " submissions found in subreddit '" + subreddit_name + "' with search query '" + search_query + "' -- " + filename + ".csv")
        topics_df.to_csv((PROJECT_FOLDER + SUBREDDIT_FOLDER + filename + ".csv"), index=None, header=True, encoding='utf-8-sig')
        
    return subR_submission_IDs

#####################################################################################

def get_comments(reddit, submission_ID):
    
    # Create submission instance
    submission = reddit.submission(id=submission_ID)
    
    # Only need to call this once per submission because:
    # "Calling replace_more() is destructive.
    # Calling it again on the same submission instance has no effect."
    try:
        submission.comments.replace_more(limit=None)
    except:
        print("\tWARNING: Encountered error while trying to replace 'MoreComments'")
        print("\tProceeding with data extraction process...")
    
    # Print number of comments in submission
    print("\tDetected " + str(submission.num_comments) + " comments in submission: " + submission_ID)
    
    # Set up dictionary to put comment info into
    comments_dict = {"my_comment_id": [],
                     "subreddit": [],
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
    
    # Get the info for the original post of the thread, which is contained in the submission object
    comments_dict["my_comment_id"].append("Reddit_" + submission.id + "_" + submission.id + "_Com0")
    comments_dict["subreddit"].append(submission.permalink.split("/")[2])
    comments_dict["link_id"].append(submission.id)
    comments_dict["title"].append(submission.title)
    comments_dict["id"].append(submission.id)
    # If the body of the post is empty, then the "body" field is identical to the submission's title
    # (submission.selftext) returns an empty string if the submission is a link post
    if submission.selftext == "":
        comments_dict["body"].append(submission.title)
    # Else, if the body is not empty, the "body" field is constructed as:
    # [submission's title] + [2 newline characters "\n\n"] + [submission's body]
    else:
        comments_dict["body"].append(submission.title + "\n\n" + submission.selftext)
    comments_dict["author"].append(submission.author)
    comments_dict["is_submitter"].append("TRUE")
    comments_dict["score"].append(submission.score)
    comments_dict["parent_id"].append(submission.id)
    comments_dict["distinguished"].append(submission.distinguished)
    comments_dict["stickied"].append(submission.stickied)
    comments_dict["edited"].append(submission.edited)
    comments_dict["permalink"].append(submission.permalink)
    comments_dict["created"].append(submission.created)
    
    # For each comment in the submission and put comment info into the dictionary
    counter = 1
    for comment in submission.comments.list():
        #print(". ", end = "")
        # Only get the comment's info if the comment has not been deleted or removed
        if ("deleted" not in comment.body) and ("removed" not in comment.body):
            MyCommentID = "Reddit_" + comment.link_id + "_" + comment.id + "_Com" + str(counter)
            comments_dict["my_comment_id"].append(MyCommentID)
            comments_dict["subreddit"].append(comment.permalink.split("/")[2])
            comments_dict["link_id"].append(comment.link_id)
            comments_dict["title"].append(submission.title)
            comments_dict["id"].append(comment.id)
            comments_dict["body"].append(comment.body)
            comments_dict["author"].append(comment.author)
            comments_dict["is_submitter"].append(comment.is_submitter)
            comments_dict["score"].append(comment.score)
            comments_dict["parent_id"].append(comment.parent_id)
            comments_dict["distinguished"].append(comment.distinguished)
            comments_dict["stickied"].append(comment.stickied)
            comments_dict["edited"].append(comment.edited)
            comments_dict["permalink"].append(comment.permalink)
            comments_dict["created"].append(comment.created)
            counter += 1
    #print()
    
    # Create Pandas DataFrame
    comments_df = pd.DataFrame(comments_dict)
    # Add timestamp column to DataFrame
    _timestamp = comments_df["created"].apply(get_date)
    comments_df = comments_df.assign(timestamp = _timestamp)
    # Export Pandas DataFrame object to a .csv file
    filename = make_submission_filename(submission_ID)
    print("\tMaking comments output for submission: " + submission_ID + " -- " + filename + ".csv")
    comments_df.to_csv((PROJECT_FOLDER + SUBMISSIONS_FOLDER + filename + ".csv"), index=None, header=True, encoding='utf-8-sig')
    print("\n" + (50 * "-") + "\n")

#####################################################################################

def search_subreddit(reddit, input_df, subreddit_name, search_terms):
    
    # Make dict for subreddit search info
    subR_search_dict = get_subR_search_dict(input_df, subreddit_name, search_terms)
    
    # Change subreddit_name to empty string if searching "ALL of Reddit"
    if subreddit_name == "ALL of Reddit":
        subreddit_name = "all"
    
    # Create subreddit instance
    subreddit = reddit.subreddit(subreddit_name)
    
    # Set of submission IDs in subreddit to avoid repetition
    subR_submission_IDs = set()
    
    # For each search term, get submission IDs of threads in search result
    for term in search_terms:
        if subR_search_dict[term] == "TRUE":
            print("SEARCH: Searching subreddit '"+ subreddit_name + "' with search query '" + term + "'...\n")
            subR_submission_IDs = get_submission_IDs(subR_submission_IDs, subreddit, subreddit_name, term)
        else:
            print("SEARCH: NOT searching subreddit '"+ subreddit_name + "' with search query '" + term + "' because subR_search_dict[" + term + "] = " + subR_search_dict[term])
        print("\n" + (50 * "-") + "\n")
        
    #print("\n" + (50 * "-") + "\n")
    print("Found a total of", len(subR_submission_IDs), "threads after searches in subreddit:", subreddit_name)
    print("\n" + (50 * "-") + "\n")
        
    # For each unique submission ID found after all searches in the subreddit, extract the comments in the thread
    counter = 1
    for ID in subR_submission_IDs:
        print(str(counter) + ". Getting comment data for submission #" + str(counter) + " | submission ID = " + ID + " ...")
        get_comments(reddit, ID)
        counter += 1

#####################################################################################


# In[5]:


##### MAIN FUNCTION #################################################################

def main():
    
    # Load .csv input file
    input_df = pd.read_csv((PROJECT_FOLDER + IN_FILENAME), header=0, encoding='utf-8-sig')
    
    # Get sample size (if applicable)
    if SAMPLE_SIZE > 0:
        input_df = input_df.sample(SAMPLE_SIZE)
        
    # Print input_df
    print("INPUT DATAFRAME:")
    print(input_df)
    print("\n" + (50 * "-") + "\n")
    
    # Get subreddit names from dataframe
    subreddit_names = get_subreddit_names(input_df)
    
    # Get search terms from dataframe
    search_terms = get_search_terms(input_df)
    
    # Create reddit instance
    reddit = praw.Reddit(client_id = "[YOUR_CLIENT_ID]",
                         client_secret = "[YOUR_CLIENT_SECRET]",
                         user_agent = "[YOUR_USER_AGENT]",
                         username = "[YOUR_USERNAME]",
                         password = "[YOUR_PASSWORD]")
    
    # Set of submission IDs to avoid repetition
    #ALL_submission_IDs = set()
    
    # For each subreddit,
    # search the subreddit for the intended search terms,
    # and extract comments in each submission / thread from the overall search results,
    # making an output .csv file for each relevant submission's / thread's comments.
    for subR_name in subreddit_names:
        search_subreddit(reddit, input_df, subR_name, search_terms)
        
    print("Finished Reddit data extraction!")

#####################################################################################


# In[8]:


main()

