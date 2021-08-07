#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Reading an excel file using Python
import xlrd
from bson.objectid import ObjectId


# In[2]:


# Give the location of the file
loc = ("functional_area & Parent Done (1).xls")


# In[3]:


# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


# In[4]:


# For row 0 and column 0
#print(sheet.cell_value(7, 11))


# In[5]:


parent_skills = {}
functional_roles = {}


# In[6]:


for i in range(2, 111):
    for j in range(3, 17):
        val = sheet.cell_value(i, j)
        v = str(val)
        if not v: #getting rid of empty strings
            continue
        if(isinstance(val, str)):#only process strings
            #print(v)
            key = v
            value = sheet.cell_value(i, 1)
            functional_role = sheet.cell_value(i, 17)
            #print('key = ', key, 'value = ', value, 'functional role = ', functional_role)
            parent_skills[key] = value
            functional_roles[key] = functional_role


# In[7]:


def print_dictionary(dic):
    for keys,values in dic.items():
        print('key : ', keys)
        print('value : ', values)


# In[8]:


#print_dictionary(parent_skills)


# In[9]:


#print_dictionary(functional_roles)


# In[10]:


import ssl 
from pymongo import MongoClient
client = MongoClient('localhost:27017')
## Specify the database to be used
db = client.the_incircle_dev_new
skills = db.skills


# In[11]:


functionalareas = db.functionalareas


# In[12]:


# Function which given a skill name, returns it's entire entry

def getSkillId(skill_name):
    skill = skills.find_one({'name' : skill_name})
    return skill

skill = getSkillId('Accountant')
print(skill)


# In[13]:


# Function which given a functionalarea name, returns it's entire entry

def getFunctionalAreaId(fa_name):
    fa = functionalareas.find_one({'name' : fa_name})
    return fa

fa = getFunctionalAreaId('Sales / Marketing')
print(fa)


# In[14]:


# Iterate over parent_skills dictionary
    # For each key, find the record
    # Find id of value
    # set parent of key to value id


# In[15]:


# Iterate over parent_skills functional_roles
    # For each key, find the record
    # Find id of value
    # set functionalArea of key to value id


# In[31]:


# Function that accepts a skill and it's parent names, and sets the new parent

def setParent(skill, parent):
    skill_id = getSkillId(skill)
    parent_id  = getSkillId(parent)
    if parent_id == None:
        print('Parent ' , parent, ' does not exist!')
        return
    if skill_id == None:
        print('Skill ' , skill, ' does not exist!')
        return
    #print(skill_id['_id'])
    #print(parent_id['_id'])
    db.skills.update({'_id' : skill_id['_id']} ,{'$set': {'parent': ObjectId(parent_id['_id'])}})
    
#setParent('Tally', 'Accountant')


# In[32]:


# Function that accepts a skill and sets it's functional area

def setFa(skill, fa):
    skill_id = getSkillId(skill)
    fa_id = getFunctionalAreaId(fa)
    if fa_id == None:
        print('Functional area ' , fa, ' does not exist!')
        return
    if skill_id == None:
        print('Skill ' , skill, ' does not exist!')
        return
    #print(skill_id['_id'])
    #print(fa_id['_id'])
    db.skills.update({'_id' : skill_id['_id']}
                    ,{'$set': {
                        'functionalArea': ObjectId(fa_id['_id'])
                    }})
    
#setParent('Tally', 'Accounts / Finance')


# In[33]:


# Iterate over skill

for key in parent_skills:
    parent = parent_skills[key]
    setParent(key, parent)


# In[34]:


# Iterate over skill

for key in functional_roles:
    fa = functional_roles[key]
    setFa(key, fa)


# In[ ]:




