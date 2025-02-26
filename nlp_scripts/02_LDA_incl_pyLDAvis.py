#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#####################################################################################
# LDA_incl_pyLDAvis.py
#
# Description:
# This script performs Latent Dirichlet Allocation (LDA) on a clean corpus.
#
# Version: 0.3
# Date Created: 08/28/2019
# Last Modified: 06/03/2021
#####################################################################################
#
# Note from 06/03/2021:
# Package pyLDAvis v.3.3.0 renamed "pyLDAvis.gensim" to "pyLDAvis.gensim_models"
#
#####################################################################################


# In[ ]:


### GLOBAL VARIABLES ###

PROJECT_FOLDER = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/LDA/"
FILENAME = "Nissan_LEAF_YouTube_ALL_CLEAN"


# In[ ]:


### IMPORTS ###

# Built-in Libraries
import copy
import numpy as np
import os
import pandas as pd
import random
import re
import string
from string import punctuation

# Gensim
import gensim
from gensim import corpora

# pyLDAvis
import pyLDAvis.gensim_models


# In[ ]:


### SET-UP ###

# Load .csv file and put data in dataframe
df = pd.read_csv((PROJECT_FOLDER + FILENAME + ".csv"), header=0, usecols=["my_comment_id", "clean_body_no_stopwords"], encoding='utf-8')

# Rename columns
#df.columns = ["My Comment ID", "Clean Body no stopwords"]

# Print the dataframe's dimentsions
print("Dataframe Dimensions: {} Rows, {} Columns".format(*df.shape))


# In[ ]:


# Print a sample of 5 elements from the dataframe
df.sample(5)


# In[ ]:


"""
# Randomly sample 10,000 rows from the data
random.seed(1)
indices = df.index.values.tolist()

random_10000 = random.sample(indices, 10000)
random_10000[:5]

# Subset the imported data on the selected 2500 indices
train_df = df.loc[random_10000, :]
train_df = train_df.reset_index(drop = True)
train_df.head(2)

# Print a sample of 50 elements from the training dataframe
train_df.sample(50)
"""


# In[ ]:


### MAKE CORPUS ###

# Make a new corpus called text_data (type: list of string)
# where each string corresponds to a document's "Clean Body no stopwords" field
#text_data = train_df["Clean Body no stopwords"].tolist()

# OR use the entire corpus for text_data
text_data = df["clean_body_no_stopwords"].tolist()

# Convert text_data (type: list of string) to a list of lists of strings by
# splitting each string in the original text_data
# Note: text_data becomes a list of lists of strings where
#       each inner list represents a document, and is a list of strings with
#       each string being a token found in that particular document
# Note: The length of the corpus is equal to the number of documents in the training dataframe,
#       but the length of each inner list is dependent on each document.
text_data = [str(text).split() for text in text_data]


# In[ ]:


### BAG-OF-WORDS ###

# Create a gensim corpora dictionary from text_data
# where each entry in the dictionary is a unique word found in the entire corpus
dictionary = corpora.Dictionary(text_data)

# Create a bag-of-words corpus of text_data using the dictionary
# Note: corpus is a list of lists of 2-tuples of integers where
#       each inner list represents a document, and is a list of 2-tuples with
#       each tuple representing a unique word found in the document, such that
#       the first int of the tuple is the dictionary index of the word (SEE: dictionary above), and
#       the second int of the tuple is the term frequency of the corresponding word in the particular document
corpus = [dictionary.doc2bow(text) for text in text_data]

# OPTIONAL: Save the dictionary and bag-of-words corpus
# Original save dictionary line results in error:
# NotImplementedError: Unable to handle scheme 'c', expected one of ('', 'file', 'hdfs', 'http', 'https', 'scp', 'sftp', 'ssh', 'webhdfs'). Extra dependencies required by 'c' may be missing. See <https://github.com/RaRe-Technologies/smart_open/blob/master/README.rst> for details.
#dictionary.save(PROJECT_FOLDER + "dictionary.gensim")
# Following line to save dictionary saves it to cwd.
dictionary.save("dictionary.gensim")


# In[ ]:


### LATENT DIRICHLET ALLOCATION (LDA) ###

# NOTE: The execution of LDA may take some time depending on input size.

# Define k topics for LDA
NUM_TOPICS = 8

# Make the LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word = dictionary, passes = 15)

# Save the LDA model
# Original save LDA model results in error:
# NotImplementedError: Unable to handle scheme 'c', expected one of ('', 'file', 'hdfs', 'http', 'https', 'scp', 'sftp', 'ssh', 'webhdfs'). Extra dependencies required by 'c' may be missing. See <https://github.com/RaRe-Technologies/smart_open/blob/master/README.rst> for details.
#dictionary.save(PROJECT_FOLDER + "dictionary.gensim")
# Following line to save LDA model saves it to cwd.
#ldamodel.save(PROJECT_FOLDER + "LDAmodel" + str(NUM_TOPICS) + ".gensim")
ldamodel.save("LDAmodel" + str(NUM_TOPICS) + ".gensim")


# In[ ]:


### EXAMINE TOPICS ###

def print_LDA_topics_with_words(ldamodel, num_words):
    topics = ldamodel.print_topics(NUM_TOPICS, num_words)
    for topic in topics:
        print("Topic #" + str(topic[0]))
        words = topic[1].split(" + ")
        print("Words in Topic:")
        w_counter = 1
        for word in words:
            print("\tWord #" + str(w_counter) + ": " + word)
            w_counter += 1
        print()

print_LDA_topics_with_words(ldamodel, 50)


# In[ ]:


### LDA VISUALIZATION ###

lda_display = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary, sort_topics = False)
pyLDAvis.display(lda_display)


# In[ ]:


### MAKE LDA HTML OUTPUT ###

pyLDAvis.save_html(lda_display, (PROJECT_FOLDER + "LDAdisplay" + str(NUM_TOPICS) +  ".html"))


# In[ ]:


### MAKE LDA OUTPUT FILE FOR TOPIC DISTRIBUTIONS FOR EACH DOC ###

BoW_reps = []
topic_dist_lists = []

for doc in corpus:
    BoW_reps.append(doc)
    topic_dist_vector = ldamodel[doc]
    topic_dist_lists.append(topic_dist_vector)
    print(". ", end = "")


# In[ ]:


# Reload .csv file and put data in dataframe
output_df = pd.read_csv((PROJECT_FOLDER + FILENAME + ".csv"), header=0, encoding='utf-8')

output_df = output_df.assign(BoW_Representation = BoW_reps)
output_df = output_df.assign(Topic_Distribution = topic_dist_lists)


# In[ ]:


output_df.sample(5)


# In[ ]:


output_df.to_csv((PROJECT_FOLDER + FILENAME + "_LDA_output.csv"), index=None, header=True, encoding='utf-8')


# In[ ]:


### PARSE EACH TOPIC DISTRIBUTION LIST FOR EACH DOC ###

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
    doc_counter = 0
    for TD_list in topic_dist_lists:
        #print((20 * "-"), ("Doc #" + str(doc_counter)), (20 * "-"))
        topic_lists = parse_TD_list(topic_lists, doc_counter, TD_list)
        doc_counter += 1
        #print()
        #print(". ", end = "")
    print()
    return topic_lists

topic_lists = init_TopicProbLists(10)
topic_lists = parse_TopicDistLists(topic_dist_lists[0:10], topic_lists)

print((20 * "-"), "END RESULT", (20 * "-"))
for T_list in topic_lists:
    print(T_list)


# In[ ]:


topic_lists


# In[ ]:


topic_lists = init_TopicProbLists(len(topic_dist_lists))
topic_lists = parse_TopicDistLists(topic_dist_lists, topic_lists)


# In[ ]:


print(len(topic_dist_lists))
print(topic_lists)


# In[ ]:


for i in range(0, NUM_TOPICS):
    for j in range(550, 560):
        print(topic_lists[i][j], ", ", end = "")
    print()


# In[ ]:


output_df = output_df.assign(Topic_1 = topic_lists[0])
output_df = output_df.assign(Topic_2 = topic_lists[1])
output_df = output_df.assign(Topic_3 = topic_lists[2])
output_df = output_df.assign(Topic_4 = topic_lists[3])
output_df = output_df.assign(Topic_5 = topic_lists[4])
output_df = output_df.assign(Topic_6 = topic_lists[5])
output_df = output_df.assign(Topic_7 = topic_lists[6])
output_df = output_df.assign(Topic_8 = topic_lists[7])
#output_df = output_df.assign(Topic_9 = topic_lists[8])
#output_df = output_df.assign(Topic_10 = topic_lists[9])
#output_df = output_df.assign(Topic_11 = topic_lists[10])
#output_df = output_df.assign(Topic_12 = topic_lists[11])
#output_df = output_df.assign(Topic_13 = topic_lists[12])
#output_df = output_df.assign(Topic_14 = topic_lists[13])
#output_df = output_df.assign(Topic_15 = topic_lists[14])
#output_df = output_df.assign(Topic_16 = topic_lists[15])
#output_df = output_df.assign(Topic_17 = topic_lists[16])
#output_df = output_df.assign(Topic_18 = topic_lists[17])
#output_df = output_df.assign(Topic_19 = topic_lists[18])
#output_df = output_df.assign(Topic_20 = topic_lists[19])


# In[ ]:


output_df.sample(5)


# In[ ]:


output_df.to_csv((PROJECT_FOLDER + FILENAME + "_LDA_output_parsed.csv"), index=None, header=True, encoding='utf-8')


# In[ ]:


### MAKE LDA TOPICS AND WORDS OUTPUT FILE ###

def make_LDA_topics_dict(ldamodel, num_words):
    topics = ldamodel.print_topics(NUM_TOPICS, num_words)
    topics_dict = {
        "Topic": [],
        "Top 30 Terms": []
    }
    for topic in topics:
        t_num = "Topic " + str(topic[0])
        topics_dict["Topic"].append(t_num)
        words = topic[1].split(" + ")
        topics_dict["Top 30 Terms"].append(words)
    return topics_dict

topics_dict = make_LDA_topics_dict(ldamodel, 30)
topics_df = pd.DataFrame(topics_dict)


# In[ ]:


topics_df


# In[ ]:


topics_df.to_csv((PROJECT_FOLDER + FILENAME + "_LDA_topics.csv"), index=None, header=True, encoding='utf-8')

