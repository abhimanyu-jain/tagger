import ssl 
from pymongo import MongoClient
import pprint
import json
import pickle


client = MongoClient('localhost:27017')

##Specify the database to be used
db = client.the_incircle_dev_new
#print(db.list_collection_names())

##Get collection of all userprofiles
userprofiles = db.userprofiles
##Iterate over the collection of userprofiles
userprofile_cursor = userprofiles.find()

##Get collection of all skills
skills = db.skills
##Get cursor to iterate over the collection of skills
skill_cursor = skills.find()

mind_skill_ids = dict()


#Iterate over every skill
for skill in skill_cursor:
    name = skill['name']
    id_ = skill['_id']

    if(mind_skill_ids.get(name) == None):
        mind_skill_ids[name] = id_

    elif(mind_skill_ids[name] > id_):
        mind_skill_ids[name] = id_


count = 0

for userprofile in userprofile_cursor:
	##Obtain list of skills for each userprofile
	userskills = userprofile['skills']
	num_skills = len(userskills)
	
	#List of skill ids for every userprofile that need to be replaced
	lst = []

	##Iterate over list of skills for each userprofile
	for i in range(num_skills):
		##Find the name of each skill
		skill = skills.find_one({'_id' : userskills[i]})
		if (skill == None):
			continue
		
		skill_name = skill['name']
		min_skill_id = mind_skill_ids[skill_name]
		
		if(min_skill_id != skill['_id']):
			count = count + 1
			print("Duplicate detected!!")


print("Total number of duplicate entries :")
print(count)

##Close the connection
client.close()
