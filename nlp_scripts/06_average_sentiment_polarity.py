#!/usr/bin/env python
# coding: utf-8

# In[1]:


# average_sentiment_polarity.py
#
# Description:
# This script takes the output file from the R Sentiment Polarity script as input, and
# averages each comment's overall sentiment polarity score, given the scores of individual sentences.
#
# It creates 2 output files:
# 1. a .csv file with my_comment_id and sentiment_polarity, the calculated averaged scores
# 2. a .csv file with my_comment_id, body, and sentiment_polarity
#
# Version: 1.0
# Date Created: 01/13/2020
# Last Modified: 01/13/2020


# In[2]:


import os
import pandas as pd
import numpy as np


# In[38]:


PROJECT_FOLDER = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/"
IN_FILENAME = "Nissan_LEAF_YouTube_PolarityScores"
OUT_FILENAME = "Nissan_LEAF_YouTube_PolarityScores_AVG"


# In[39]:


df = pd.read_csv((PROJECT_FOLDER + IN_FILENAME + ".csv"), header=0, encoding='utf-8')


# In[40]:


df


# In[41]:


counter = 0
for index, row in df.iterrows():
    print(row["my_comment_id"], "\t", row["element_id"], "\t", row["sentence_id"], "\t", row["sentiment"])
    counter += 1
    if counter == 10:
        break


# In[42]:


GROUPED_SENTIMENTS = dict()

for index, row in df.iterrows():
    try:
        GROUPED_SENTIMENTS[row["my_comment_id"]][0] += row["sentiment"]
        GROUPED_SENTIMENTS[row["my_comment_id"]][1] += 1
    except KeyError:
        GROUPED_SENTIMENTS[row["my_comment_id"]] = [row["sentiment"]]
        GROUPED_SENTIMENTS[row["my_comment_id"]].append(1)
    except:
        print("Unknown error occurred -- breaking for loop")
        break


# In[43]:


GROUPED_SENTIMENTS


# In[44]:


DATA = dict()

for key, value in GROUPED_SENTIMENTS.items():
    DATA[key] = value[0] / value[1]


# In[45]:


DATA


# In[46]:


df = pd.DataFrame(list(DATA.items()), columns=["my_comment_id", "sentiment_polarity"])


# In[47]:


df


# In[48]:


df.to_csv((PROJECT_FOLDER + OUT_FILENAME + ".csv"), index=None, header=True, encoding='utf-8')


# In[49]:


# Join averaged sentiment polarity score values with original input .csv file

OG_FILE = "C://Users/kathleen.trinh.TDI/OneDrive - OneWorkplace/Documents/Nissan/[2021-09] LEAF - UK/YouTube - LDA/Nissan_LEAF_YouTube_ALL_CLEAN_LDA_output_parsed.csv"

og_df = pd.read_csv((OG_FILE), header=0, usecols=["my_comment_id", "body"], encoding='utf-8')
#og_df = og_df.rename(columns={"Post ID": "my_comment_id", "Body": "body"})


# In[50]:


og_df


# In[51]:


joined_df = og_df.join(df.set_index("my_comment_id"), on="my_comment_id")


# In[52]:


joined_df


# In[53]:


joined_df.to_csv((PROJECT_FOLDER + OUT_FILENAME + "_withBody.csv"), index=None, header=True, encoding='utf-8')


# In[54]:


# Join averaged sentiment polarity score values with LDA output .csv file

OG_FILE = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/Nissan_LEAF_YouTube_ALL_CLEAN_LDA_output_parsed.csv"

og_df = pd.read_csv((OG_FILE), header=0, encoding='utf-8')
#og_df = og_df.rename(columns={"My Comment ID": "my_comment_id", "Body": "body"})


# In[55]:


og_df


# In[56]:


joined_df = og_df.join(df.set_index("my_comment_id"), on="my_comment_id")


# In[57]:


joined_df


# In[58]:


joined_df.to_csv((PROJECT_FOLDER + OUT_FILENAME + "_withLDATopicDistributions.csv"), index=None, header=True, encoding='utf-8')


# In[61]:


# Join LDA topic distribution scores AND averaged sentiment polarity score values with original file containing metadata

OG_FILE = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/Nissan_LEAF_YouTube_ALL.csv"

og_df = pd.read_csv((OG_FILE), header=0, encoding='utf-8')
og_df = og_df.rename(columns={"comment": "body"})


# In[62]:


og_df


# In[63]:


joined_df = og_df.join(df.set_index("my_comment_id"), on="my_comment_id", how="inner")


# In[64]:


joined_df


# In[65]:


joined_df.to_csv((PROJECT_FOLDER + OUT_FILENAME + "_withMetadata.csv"), index=None, header=True, encoding='utf-8')

