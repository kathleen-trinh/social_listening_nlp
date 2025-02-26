#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### IMPORTS ###

# Built-in Libraries
import numpy as np
import os
import pandas as pd
import random
import re
import string
from string import punctuation

# NLTK
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize #RegexpTokenizer, 
nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


# In[23]:


### GLOBAL VARIABLES ###

PROJECT_FOLDER = "C://Users/kathleen.trinh/Documents/Nissan/YouTube/"
FILENAME = "Nissan_LEAF_YouTube_ALL"
IN_FILENAME = FILENAME + ".csv"

BADWORDS = [
    'captain', 'character',
    'hawkeye', 'hulk',
    'marvel',
    'player',
]

STOPWORDS = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 
    'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
    'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 
    'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', 
    "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', 
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', 
    "won't", 'wouldn', "wouldn't",
    '´', '‘', '’', '“', '”',
    '[deleted]', 'deleted', '[removed]', 'removed',
    'actual', 'actually', 'add', 'ago', 'agree', 'ah', 'also', 'always', 'amazon', 'answer', 'anything', 'anyway', 'anyways',
    'apparently', 'arent', 'as', 'ask', 'aw', 'aww', 'awww',
    'b', 'bad', 'bc', 'believe', 'bit', 'bot', 'brah', 'bro', 'bruh', 'btw',
    'c', 'call', 'cant', 'congrats', 'congratulation', 'congratulations', 'could', 'couldnt',
    'd', 'damn', 'de', 'definitely', 'dont', 'dude', 'didnt', 'duh', 'dunno',
    'e', 'edit', 'either', 'else', 'en', 'etc', 'even', 'ever', 'everyone', 'exactly',
    'f', 'facebook', 'find', 'found', 'ftw', 'fyi',
    'g', 'gave', 'get', 'gets', 'give', 'gives', 'gl', 'go', 'goes', 'golly', 'gon', 'good', 'google', 'gosh', 'got', 'guess', 'guys',
    'h', 'ha', 'hah', 'haha', 'hahaha', 'happen', 'happens', 'happened', 'hasnt', 'heard', 'hello', 'hes', 'hey', 'heya', 'hi',
    'hm', 'hmm', 'hmmm', 'holy', 'homie', 'http', 'https', 'huh',
    'i', 'idfk', 'idk', 'im', 'imo', 'indeed', 'info', 'irdk', 'isnt',
    'j',
    'k', 'kk', 'kkz', 'know',
    'l', 'la', 'lately', 'left', 'let', 'like', 'link', 'lmao', 'lmfao', 'lol', 'look', 'looks', 'lot', 'lots',
    'm', 'make', 'many', 'may', 'maybe', 'meanwhile', 'message', 'mhm', 'mhmm', 'might', 'much',
    'n', 'na', 'nah', 'name', 'nan', 'nearly', 'next', 'no', 'nope', 'now',
    'o', 'oh', 'ok', 'okay', 'omfg', 'omg', 'one', 'op', 'org',
    'p', 'people', 'please', 'post', 'put',
    'q', 'que', 'question', 'quite',
    'r', 'read', 'really', 'reddit', 'regard', 'regards', 'reply', 'repost', 'right', 'rofl',
    's', 'say', 'says', 'said', 'se', 'see', 'seem', 'shes', 'shit', 'shouldnt', 'shucks', 'slightly', 'someone', 'sometime',
    'sometimes', 'sorry', 'still', 'sub', 'sure',
    't', 'ta', 'talk', 'tbh', 'tell', 'thank', 'thanks', 'thanx', 'thing', 'think', 'tho', 'though', 'thought', 'thread', 'thus',
    'tldr', 'told', 'totally', 'truly', 'two', 'ty',
    'u', 'ugh', 'uh', 'um', 'unless', 'upvote', 'upvotes', 'use', 'usual', 'usually',
    'v', 'via',
    'w', 'want', 'wasnt', 'way', 'well', 'werent', 'whoa', 'wiki', 'wikipedia', 'woah', 'word', 'would', 'wouldnt', 'wow', 'wtf',
    'x',
    'y', 'ya', 'yahoo', 'yay', 'yeah', 'yep', 'yes', 'youd', 'youll', 'youre', 'youve', 'yup',
    'z'
]


# In[3]:


print(STOPWORDS)


# In[42]:


### FUNCTIONS ###

def convert_utf8(s):
    return str(s)

def remove_urls(s):
    s = re.sub(r"[^\s]*www.[^\s]*", "", str(s))
    s = re.sub(r"[^\s]*co.uk[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.biz[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.com[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.edu[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.gov[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.info[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.net[^\s]", "", str(s))
    s = re.sub(r"[^\s]*.org[^\s]", "", str(s))
    return s

def remove_mentions(s):
    s = re.sub(r"\@\b\w*\s", "", s)
    return s
    
def remove_star_words(s):
    return re.sub(r"[^\s]*[\*]+[^\s]*", "", str(s))

def remove_numbers(s):
    return re.sub(r"[^\s]*[0-9]+[^\s]*", "", str(s))

def remove_punctuation(s):
    global punctuation
    for p in punctuation:
        s = str(s).replace(p, " ")
    return s

def remove_shortwords(s):
    s = word_tokenize(s)
    s = " ".join([w for w in s if len(w) > 3])
    return s

# Using default global en_stopwords as list of stopwords
def remove_stopwords(s):
    global en_stopwords
    s = word_tokenize(s)
    s = " ".join([w for w in s if w not in en_stopwords])
    return s

# Using user-defined STOPWORDS as list of stopwords
def remove_stopwords(s):
    s = word_tokenize(s)
    no_stopwords = []
    for w in s:
        if w not in STOPWORDS:
            no_stopwords.append(w)
    no_stopwords = " ".join(no_stopwords)
    return no_stopwords

# NOT USED
def get_lemma_v1(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

# NOT USED
def get_lemma_v2(word):
    return WordNetLemmatizer().lemmatize(word)

def penn2morphy(penntag, returnNone=False):
    morphy_tag = {'NN':wn.NOUN, 'JJ':wn.ADJ,
                  'VB':wn.VERB, 'RB':wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return None if returnNone else ''

def lemmatize(s):
    lemmas = []
    tokens = word_tokenize(s)
    tagged_tokens = nltk.pos_tag(tokens)
    for pair in tagged_tokens:
        new_pos = penn2morphy(pair[1])
        if new_pos != "":
            lemma = WordNetLemmatizer().lemmatize(pair[0], pos = new_pos)
        else:
            lemma = WordNetLemmatizer().lemmatize(pair[0])
        lemmas.append(lemma)
    s = " ".join(lemmas)
    return s

def drop_empty_rows(df):
    for index, row in df.iterrows():
        if row["clean_body_no_stopwords"] == "":
            df.drop(index, inplace=True)
        elif row["clean_body_no_stopwords"] == "NaN":
            df.drop(index, inplace=True)
        elif row["clean_body"] == "deleted":
            df.drop(index, inplace=True)
        elif row["clean_body"] == "removed":
            df.drop(index, inplace=True)
        elif row["body"] == "body":
            df.drop(index, inplace=True)
    return df


# In[33]:


### SET-UP ###

# Load .csv file and put data in dataframe
df = pd.read_csv((PROJECT_FOLDER + IN_FILENAME), header=0, usecols=["my_comment_id", "comment"], encoding='utf-8')

#df.columns = ["My Comment ID", "Body"]
df.columns = ["my_comment_id", "body"]

# Print the dataframe's dimentsions
print("Dataframe Dimensions: {} Rows, {} Columns".format(*df.shape))

# Print a sample of 5 elements from the dataframe
df.sample(5)


# In[34]:


### TEST FUNCTIONS WITH SUBSET ###

test_df = df.sample(25)


# In[43]:


### TEXT PRE-PROCESSING PART 1: CHAR REMOVAL & CONVERSION ###

# Add a new column, "Clean Body", to the training dataframe
# by converting each document's "Body" to type string
test_df["clean_body"] = test_df["body"].map(convert_utf8)

# Remove mentions to other usernames from each document's "Clean Body"
test_df["clean_body"] = test_df["clean_body"].map(remove_mentions)

# Remove URLs from each document's "Clean Body"
test_df["clean_body"] = test_df["clean_body"].map(remove_urls)

# Remove star words from each document's "Clean Body"
test_df["clean_body"] = test_df["clean_body"].map(remove_star_words)

# Remove numbers from each document's "Clean Body"
test_df["clean_body"] = test_df["clean_body"].map(remove_numbers)

# Remove punctuation marks from each document's "Clean Body"
test_df["clean_body"] = test_df["clean_body"].map(remove_punctuation)

# Convert all characters in each document's "Clean Body" to lowercase
test_df["clean_body"] = test_df["clean_body"].map(lambda x: x.lower())

# Print a sample of 5 elements from the training dataframe
test_df.sample(5)


# In[44]:


### TEXT PRE-PROCESSING PART 2: STOPWORDS ###

# Add a new column, "Clean Body no stopwords", to the training dataframe,
# which is the text from "Clean Body" with NO stopwords
test_df["clean_body_no_stopwords"] = test_df["clean_body"].map(remove_stopwords)

# Remove short words (3 chars or less)
#train_df["Clean Body no stopwords"] = train_df["Clean Body"].map(remove_shortwords)

# Print a sample of 5 elements from the training dataframe
test_df.sample(5)


# In[45]:


test_df


# In[46]:


### CLEAN ENTIRE CORPUS IF TEST RESULTS ARE OK ###


# In[47]:


### TEXT PRE-PROCESSING PART 1: CHAR REMOVAL & CONVERSION ###

# Add a new column, "Clean Body", to the training dataframe
# by converting each document's "Body" to type string
df["clean_body"] = df["body"].map(convert_utf8)

# Remove URLs from each document's "Clean Body"
df["clean_body"] = df["clean_body"].map(remove_urls)

# Remove star words from each document's "Clean Body"
df["clean_body"] = df["clean_body"].map(remove_star_words)

# Remove numbers from each document's "Clean Body"
df["clean_body"] = df["clean_body"].map(remove_numbers)

# Remove punctuation marks from each document's "Clean Body"
df["clean_body"] = df["clean_body"].map(remove_punctuation)

# Convert all characters in each document's "Clean Body" to lowercase
df["clean_body"] = df["clean_body"].map(lambda x: x.lower())

# Print a sample of 5 elements from the training dataframe
df.sample(5)


# In[48]:


### TEXT PRE-PROCESSING PART 2: STOPWORDS ###

# Add a new column, "Clean Body no stopwords", to the training dataframe,
# which is the text from "Clean Body" with NO stopwords
df["clean_body_no_stopwords"] = df["clean_body"].map(remove_stopwords)

# Remove short words (3 chars or less)
#train_df["Clean Body no stopwords"] = train_df["Clean Body"].map(remove_shortwords)


# In[49]:


# Print a sample of 5 elements from the training dataframe
df.sample(5)


# In[50]:


### TEXT PRE-PROCESSING PART 3: LEMMATIZATION ###

# Lemmatize each token in each document
df["clean_body_no_stopwords"] = df["clean_body_no_stopwords"].map(lemmatize)


# In[51]:


# Print a sample of 5 elements from the training dataframe
df.sample(5)


# In[52]:


### TEXT PRE-PROCESSING PART 4: STOPWORDS (AGAIN) ###

# Add a new column, "Clean Body no stopwords", to the training dataframe,
# which is the text from "Clean Body" with NO stopwords
df["clean_body_no_stopwords"] = df["clean_body_no_stopwords"].map(remove_stopwords)

# Remove short words (3 chars or less)
#train_df["Clean Body no stopwords"] = train_df["Clean Body"].map(remove_shortwords)


# In[53]:


# Print a sample of 5 elements from the training dataframe
df.sample(5)


# In[54]:


### DROP EMPTY ROWS ###

# Print the dataframe's dimensions
print("Dataframe Dimensions (with empty rows): {} Rows, {} Columns".format(*df.shape))

try:
    df = drop_empty_rows(df)
except MemoryError as e:
    print("Memory Error thrown:")
    print(e)


# In[55]:


# Print the dataframe's dimensions
print("Dataframe Dimensions (after removing empty rows): {} Rows, {} Columns".format(*df.shape))


# In[56]:


df


# In[57]:


### OUTPUT ###

df.to_csv((PROJECT_FOLDER + FILENAME + "_CLEAN.csv"), index=None, header=True, encoding='utf-8')


# In[58]:


### MAKE SHUFFLED DATAFRAME ###

shuffled_df = df.sample(frac=1)


# In[59]:


shuffled_df


# In[33]:


### OUTPUT SHUFFLED DATAFRAME ###

df.to_csv((PROJECT_FOLDER + FILENAME + "_CLEAN_SHUFFLED.csv"), index=None, header=True, encoding='utf-8')

