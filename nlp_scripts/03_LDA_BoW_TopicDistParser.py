#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# LDA_topic_distribution_parser.py
#
# Description:
# This script takes the LDA output file and
# parses it to separate the topic distribution scores into separate columns.
#
# Version: 0.3
# Date Created: 09/03/2019
# Last Modified: 07/16/2020
#####################################################################################


# In[2]:


### GLOBAL VARIABLES ###

PROJECT_FOLDER = "C:/Users/kathleen.trinh/Documents/Nike/Women's Plus Size/LDA Reddit/"
FILENAME = "Nike_Women's-Plus-Size_Reddit_ALL_CLEAN_LDA_output"

# Specify the number of topics previously used for the LDA process
NUM_TOPICS = 12


# In[3]:


### IMPORTS ###

import copy
import numpy as np
import os
import pandas as pd
import re
import string


# In[4]:


### SET-UP ###

# Load .csv file and put data in dataframe
df = pd.read_csv((PROJECT_FOLDER + FILENAME + ".csv"), header=0, encoding='utf-8')

# Rename columns
#df.columns = ["My Comment ID", "Clean Body no stopwords"]

# Print the dataframe's dimensions
print("Dataframe Dimensions: {} Rows, {} Columns".format(*df.shape))

# Sample the df's data
df.sample(5)


# In[7]:


### FUNCTION TO MAKE topic_dist_lists FROM LDA OUTPUT FILE'S DF ###

def make_topic_dist_lists_from_df(df):
    topic_dist_lists = []
    raw_topic_dist_lists = []
    for row in df["Topic_Distribution"]:
        split_row = row.split("[]()")
        raw_topic_dist_lists.append(split_row)
    for r_TD_list in raw_topic_dist_lists:
        TD_list = []
        no_brackets_string = r_TD_list[0].strip("[]")
        string_list = no_brackets_string.split("), ")
        string_list = [tuple_string.strip("()") for tuple_string in string_list]
        for tuple_string in string_list:
            topic_num = int(tuple_string.split(", ")[0])
            topic_prob = float(tuple_string.split(", ")[1])
            TD_list.append((topic_num, topic_prob))
        topic_dist_lists.append(TD_list)
    return topic_dist_lists

### PARSE EACH TOPIC DISTRIBUTION LIST FOR EACH DOC ### (vvv FUNCTIONS FROM OVERALL LDA SCRIPT vvv)

def init_TopicProbLists(num_docs):
    init_list = [0 for x in range(0, num_docs)]
    topic_lists = [copy.deepcopy(init_list) for x in range(0, NUM_TOPICS)]
    return topic_lists

def parse_TD_list(topic_lists, doc_counter, TD_list):
    for topic_prob_pair in TD_list:
        topic_num = topic_prob_pair[0]
        probability = topic_prob_pair[1]
        #print("Topic #" + str(topic_num) + " probability = " + str(probability))
        #print("\t Accessing... topic_lists[" + str(topic_num) + "][" + str(doc_counter) + "]")
        topic_lists[topic_num][doc_counter] = probability
        #for T_list in topic_lists:
        #    print(T_list)
    return topic_lists
        
def parse_TopicDistLists(topic_dist_lists, topic_lists):
    print("Parsing ", end = "")
    doc_counter = 0
    for TD_list in topic_dist_lists:
        #print((20 * "-"), ("Doc #" + str(doc_counter)), (20 * "-"))
        topic_lists = parse_TD_list(topic_lists, doc_counter, TD_list)
        doc_counter += 1
        #print()
        print(". ", end = "")
    print()
    return topic_lists


# In[ ]:


topic_dist_lists = make_topic_dist_lists_from_df(df)
print("Length of topic_dist_lists:", len(topic_dist_lists))


# In[8]:


print("Testing functions with 10 lists...")
topic_lists = init_TopicProbLists(10)
topic_lists = parse_TopicDistLists(topic_dist_lists[0:10], topic_lists)

print((20 * "-"), "END RESULT", (20 * "-"))
for T_list in topic_lists:
    print(T_list)


# In[9]:


print("Processing all lists in topic_dist_lists (", len(topic_dist_lists), "items )...")

topic_lists = init_TopicProbLists(len(topic_dist_lists))
topic_lists = parse_TopicDistLists(topic_dist_lists, topic_lists)


# In[14]:


# Print the first 10 values of each topic list to see if data populated
i = 1
for T_list in topic_lists:
    print("Topic #" + str(i) + ": " + str(T_list[0:10]))
    i += 1


# In[15]:


for i in range(0, NUM_TOPICS):
    for j in range(8400, 8430):
        print(topic_lists[i][j], ", ", end = "")
    print()


# In[ ]:


# Reload .csv file and put data in dataframe
#output_df = pd.read_csv((PROJECT_FOLDER + FILENAME + ".csv"), header=0, encoding='utf-8')


# In[16]:


df = df.assign(Topic_1 = topic_lists[0])
df = df.assign(Topic_2 = topic_lists[1])
df = df.assign(Topic_3 = topic_lists[2])
df = df.assign(Topic_4 = topic_lists[3])
df = df.assign(Topic_5 = topic_lists[4])
df = df.assign(Topic_6 = topic_lists[5])
df = df.assign(Topic_7 = topic_lists[6])
df = df.assign(Topic_8 = topic_lists[7])
df = df.assign(Topic_9 = topic_lists[8])
df = df.assign(Topic_10 = topic_lists[9])
df = df.assign(Topic_11 = topic_lists[10])
df = df.assign(Topic_12 = topic_lists[11])
#output_df = output_df.assign(Topic_13 = topic_lists[12])
#output_df = output_df.assign(Topic_14 = topic_lists[13])
#output_df = output_df.assign(Topic_15 = topic_lists[14])
#output_df = output_df.assign(Topic_16 = topic_lists[15])
#output_df = output_df.assign(Topic_17 = topic_lists[16])
#output_df = output_df.assign(Topic_18 = topic_lists[17])
#output_df = output_df.assign(Topic_19 = topic_lists[18])
#output_df = output_df.assign(Topic_20 = topic_lists[19])


# In[17]:


df.sample(5)


# In[18]:


df.to_csv((PROJECT_FOLDER + FILENAME + "_LDA_output_parsed.csv"), index=None, header=True, encoding='utf-8')

