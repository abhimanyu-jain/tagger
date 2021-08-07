#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlrd
from bson.objectid import ObjectId

loc = ("skills-single-parent-active.xls")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
print(sheet.cell_value(15287, 1))


# In[2]:


# Iterate over sheet and create lists of ids and skill names

lst_ids = []
lst_names = []

max_rows = 15288


for row in range(1, max_rows):
    _id = str(sheet.cell_value(row, 1))
    _id = _id[1:len(_id)-1]
    name = sheet.cell_value(row, 2)

    lst_ids.append(_id)
    lst_names.append(name)
    

print('Number of ids : ',len(lst_ids))
print('Number of names : ', len(lst_names))


# In[3]:


name_to_list_of_words_mapping = {}

for name in lst_names:
    name_to_list_of_words_mapping[name] = name.split()
    
print(name_to_list_of_words_mapping['Nail Artist'])


# In[4]:


loc2 = ("qualified_parents.xls")
wb2 = xlrd.open_workbook(loc2)
sheet2 = wb2.sheet_by_index(0)
print(sheet2.cell_value(110, 1))


# In[5]:


qualified_parents = []

for i in range(2,111):
    skill = sheet2.cell_value(i, 1)
    qualified_parents.append(skill)

print(qualified_parents)


# In[6]:


qualified_parents_dict = {}

for sk in qualified_parents:
    words = sk.split()
    
    for word in words:
        if(word in qualified_parents_dict):
            lst = qualified_parents_dict[word]
        else:
            lst = []
        lst.append(sk)
        qualified_parents_dict[word] = lst
        
print(qualified_parents_dict)


# In[7]:


qualified_replacements = {}

for name in name_to_list_of_words_mapping:
    words = name_to_list_of_words_mapping[name]
    
    replacements = set()
    
    for word in words:
        if(word in qualified_parents_dict):
            replacements = replacements.union(set(qualified_parents_dict[word]))
    qualified_replacements[name] = replacements


# In[8]:


print(len(qualified_replacements))


# In[9]:


print(qualified_replacements['Project Lead Developer'])


# In[11]:


import ssl 
from pymongo import MongoClient
client = MongoClient('127.0.0.1:27017')
db = client.the_incircle_dev_new
print(db.list_collection_names())


# In[54]:


def find_skill_id(name):
    skill = db.skills.find_one({'name' : name})
    _id = None
    if(skill != None):
        _id = skill['_id']
    return _id


# In[71]:


def replaceParent(skill_id, new_parent_id):
    print(
            db.skills.update
            (
                {
                    '_id': skill_id
                }, 

                {
                  "$set": { 
                   'parent': ObjectId(new_parent_id)
                  }

                },
                upsert=True
            )
        )
    print('Parent Id After change : ', db.skills.find_one({'_id' : skill_id})['parent'])


# In[72]:


import random

for qr in qualified_replacements:
    ln = len(qualified_replacements[qr])
    if(ln > 0):
        skill = qr
        parent = random.sample(list(qualified_replacements[qr]), 1)[0]
        
        skill_id = find_skill_id(skill)
        new_parent_id = find_skill_id(parent)
        replaceParent(skill_id, new_parent_id)
        


# In[ ]:




