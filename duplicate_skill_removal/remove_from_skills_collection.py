import ssl 
from pymongo import MongoClient
import pprint
import json
import pickle


client = MongoClient('localhost:27017')

##Specify the database to be used
db = client.the_incircle_dev_new

##Get collection of all skills
skills = db.skills
##Get cursor to iterate over the collection of userprofiles
skill_cursor = skills.find()

mind_skill_ids = dict()

count = 0

#Iterate over every userprofile
for skill in skill_cursor:
    name = skill['name']
    id_ = skill['_id']

    if(mind_skill_ids.get(name) == None):
        mind_skill_ids[name] = id_

    elif(mind_skill_ids[name] > id_):
        count = count + 1
        mind_skill_ids[name] = id_
    else:
        count = count + 1

print(count)

skill_cursor.rewind()


deletion_list = []
count = 0
for skill in skill_cursor:
    name = skill['name']
    id_ = skill['_id']

    if(id_ > mind_skill_ids.get(name)):
        deletion_list.append(id_)
        count = count+1
print(count)


for id in deletion_list:
    db.skills.delete_one({'_id' : id})
