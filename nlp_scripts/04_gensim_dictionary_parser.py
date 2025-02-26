#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#####################################################################################
# gensim_dictionary_parser.py
#
# Description:
# This script loads a previously made gensim dictionary file
# (most likely with filename "dictionary.gensim" or similar)
# into memory to make a .csv output file containing:
# 1. the word ID of each word in the dictionary
# 2. the actual word corresponding to each word ID
# 3. the collection frequency of each word
#    (the number of times the word occurs across the entire corpus)
# 4. the document frequency of each word
#    (the number of documents the word occurs in)
#
# Gensim's corpora.dictionary documentation:
# https://radimrehurek.com/gensim/corpora/dictionary.html
#
# Date Created: 09/18/2019
# Last Modified: 09/19/2019
#####################################################################################


# In[67]:


### GLOBAL VARIABLES ###

PROJECT_FOLDER = "C:/Users/kathleen.trinh/Documents/Subaru/Crosstrek/LDA/"

DICTIONARY_FILE = "dictionary.gensim"

OUTPUT_FILE1 = "dictionary_original_order"
OUTPUT_FILE2 = "dictionary_lexicographical_order"


# In[68]:


### IMPORTS ###

# Built-in Libraries
import numpy as np
import os
import pandas as pd
import re

# Gensim
import gensim
from gensim import corpora


# In[69]:


# Load previously made dictionary
dictionary = corpora.Dictionary.load(PROJECT_FOLDER + DICTIONARY_FILE)


# In[70]:


# Save dictionary to text file with words in their original order
#dictionary.save_as_text(fname=(PROJECT_FOLDER + OUTPUT_FILE1 + ".txt"), sort_by_word=False)

# Save dictionary to text file with words sorted by lexicographical order
#dictionary.save_as_text(fname=(PROJECT_FOLDER + OUTPUT_FILE2 + ".txt"), sort_by_word=True)


# In[71]:


# Print the length of the dictionary
len(dictionary)


# In[72]:


# Initialize a dict object to store the gensim dictionary's data into
word_dict = {}

# Start with the actual words and their IDs using id2token
for w_id, word in dictionary.id2token.items():
    word_dict[w_id] = [word]


# In[73]:


# If using id2token does not work, use token2id to start
if len(word_dict) == 0:
    for word, w_id in dictionary.token2id.items():
        word_dict[w_id] = [word]


# In[74]:


# Add the collection frequency of each word
for w_id, c_freq in dictionary.cfs.items():
    word_dict[w_id].append(c_freq)

# Add the document frequency of each word
for w_id, d_freq in dictionary.dfs.items():
    word_dict[w_id].append(d_freq)


# In[75]:


column_names = ["word_id", "word", "collection_frequency", "document_frequency"]

data = [[k, v[0], v[1], v[2]] for (k,v) in word_dict.items()]


# In[76]:


df = pd.DataFrame(data, columns=column_names)


# In[77]:


df.sample(5)


# In[79]:


df.to_csv((PROJECT_FOLDER + OUTPUT_FILE1 + ".csv"), index=None, header=True, encoding='utf-8')


# In[80]:


# Sort rows by lexicographical order
sorted_data = [[k, v[0], v[1], v[2]] for (k,v) in sorted(word_dict.items(), key=lambda item: item[1][0])]


# In[81]:


sorted_df = pd.DataFrame(sorted_data, columns=column_names)


# In[82]:


sorted_df.sample(5)


# In[83]:


sorted_df.to_csv((PROJECT_FOLDER + OUTPUT_FILE2 + ".csv"), index=None, header=True, encoding='utf-8')

