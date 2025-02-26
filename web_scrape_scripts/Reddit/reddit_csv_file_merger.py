#!/usr/bin/env python
# coding: utf-8

# In[11]:


# CSV_file_merger_Reddit.py
#
# Only works if:
# 1. All the .csv files you want to merge are in the same folder.
# 2. The output .csv file is in a different folder.
# 3. All the .csv files you want to merge have the same number of columns.
#
# Use this .csv file merger script if you would like to
# not include duplicate threads in your output file.


# In[82]:


import os


# In[83]:


directory_name = "C:/Users/kathleen.trinh/Documents/Nissan/NissanAltimaGapAnalysis/Reddit/"

out_directory_name = "C:/Users/kathleen.trinh/Documents/Nissan/NissanAltimaGapAnalysis/"
out_filename = "NissanAltima_Reddit_BySearch_ALL.csv"


# In[84]:


# For getting rid of reddit duplicates only:
submission_id_set = set()
duplicates_list = []


# In[87]:


file_count = 0
unique_file_count = 0

for filename in os.listdir(directory_name):
    file_count += 1
    # For getting rid of reddit duplicates only:
    submission_id = filename[-10:-4]
    if submission_id not in submission_id_set:
        submission_id_set.add(submission_id)
        unique_file_count += 1
    else:
        print("\tDuplicate detected:", submission_id)
        duplicates_list.append(filename)

print("file_count =", file_count)
print("unique_file_count =", unique_file_count)
print("Length of submission_id_set =", len(submission_id_set))
print("Length of duplicates_list =", len(duplicates_list))


# In[90]:


fout=open((out_directory_name + out_filename), "a", encoding="utf-8")

submission_id_set = set()

counter = 1
for filename in os.listdir(directory_name):
    print(str(counter) + ". Merging: " + filename + " ...")
    submission_id = filename[-10:-4]
    if submission_id not in submission_id_set:
        submission_id_set.add(submission_id)
        if counter == 1:
            file = open(directory_name + filename, encoding="utf-8")
            for line in file:
                fout.write(line)
            file.close()
        else:
            file = open(directory_name + filename, encoding="utf-8")
            file.readline() # skip the header
            for line in file:
                fout.write(line)
            file.close()
    else:
        print("\tDuplicate thread detected:", filename, "-- Skipping")
    counter += 1


# In[91]:


fout.close()


# In[92]:


print("Filename Count:", (counter - 1))

