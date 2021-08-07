#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ssl 
from pymongo import MongoClient


# In[2]:


client = MongoClient('127.0.0.1:27017')


# In[3]:


db = client.the_incircle_dev_new
print(db.list_collection_names())


# In[4]:


# Reading an excel file using Python
import xlrd
from bson.objectid import ObjectId


# In[5]:


# Give the location of the file
loc = ("skill_replacement_list.xls")


# In[9]:


# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


# In[13]:


# For row 0 and column 0
print(sheet.cell_value(33908, 3))



def replace_skill(sk_id, replacement_name):
    db.skills.update_one
    (
        {
            '_id': ObjectId(sk_id)
        }, 

        {
          "$set": { 
           'name': replacement_name
          }

        }
    )


# In[27]:


row_min = 0
row_max = 33909

col_min = 0
col_max = 4


# In[61]:


true_and_same_count = 0
true_and_diff_count = 0

false_and_same_count = 0
false_and_diff_count = 0

for row in range(0, row_max):
    # Number of Trues where values are different
    # Number of Trues where values are same
    skill_id = sheet.cell_value(row, 1)
    original_skill = sheet.cell_value(row, 2)
    replacement_skill = sheet.cell_value(row, 3)
    truth_val = sheet.cell_value(row, 4)
    if (original_skill == replacement_skill):
        if((truth_val == 'True') | (truth_val == 'TRUE') | (truth_val == 'Ture') | (truth_val == 'TURE') | 
           (truth_val == 1)):
            true_and_same_count = true_and_same_count + 1
        elif((truth_val == 'False') | (truth_val == 'FALSE') | (truth_val == 'Fasle') | 
             (truth_val == 'FASLE') | (truth_val == 'Fales') | (truth_val == 'FALES')| (truth_val == 0)):
            false_and_same_count = false_and_same_count + 1
            db.skills.delete_one({'_id' : ObjectId(skill_id)})
        else:
            print(sheet.cell_value(row, 0))

    else:
        if((truth_val == 'True') | (truth_val == 'TRUE') | (truth_val == 'Ture') | (truth_val == 'TURE') | 
           (truth_val == 1)):
            true_and_diff_count = true_and_diff_count + 1
            replace_skill(skill_id, replacement_skill)
        elif((truth_val == 'False') | (truth_val == 'FALSE') | (truth_val == 'Fasle') | 
             (truth_val == 'FASLE') | (truth_val == 'Fales') | (truth_val == 'FALES') | (truth_val == 0)):
            false_and_diff_count = false_and_diff_count + 1
            db.skills.delete_one({'_id' : ObjectId(skill_id)})
        else:
            print(sheet.cell_value(row, 0))

    # Number of Falses where values are different
    # Number of Falses where values are same
    accounted_for = true_and_same_count + true_and_diff_count + false_and_same_count + false_and_diff_count

    
print('True and same : ', true_and_same_count)
print('True and different : ', true_and_diff_count)
print('False and same : ', false_and_same_count)
print('False and different : ', false_and_diff_count)
print('Accounted for :', accounted_for)
