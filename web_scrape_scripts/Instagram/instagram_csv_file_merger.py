#!/usr/bin/env python
# coding: utf-8

# In[1]:


# instagram_csv_file_merger.py
#
# Ensure the following:
# 1. All the .csv files you want to merge are in the same folder.
# 2. The output .csv file is in a different folder.
# 3. All the .csv files you want to merge have the same number of columns.


# In[2]:


import os


# In[4]:


directory_name = "C:/Users/kathleen.trinh/Documents/Nissan/Instagram/"

out_directory_name = "C:/Users/kathleen.trinh/Documents/Nissan/"
out_filename = "190429_Instagram_nissanusa_ALL.csv"


# In[5]:


fout=open((out_directory_name + out_filename), "a", encoding="utf-8")

line_count = 0

counter = 1
for filename in os.listdir(directory_name):
    print(str(counter) + ". Merging: " + filename + " ...")
    if counter == 1:
        file = open(directory_name + filename, encoding="utf-8")
        for line in file:
            line_count += 1
            fout.write(line)
        file.close()
    else:
        file = open(directory_name + filename, encoding="utf-8")
        file.readline() # skip the header
        for line in file:
            line_count += 1
            fout.write(line)
        file.close()
    counter += 1


# In[6]:


fout.close()


# In[7]:


print("counter = ", (counter - 1))
print("line_count = ", line_count)

