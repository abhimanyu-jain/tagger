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
##Get cursor to iterate over the collection of userprofiles
skill_cursor = skills.find()

mind_skill_ids = dict()


#Iterate over every userprofile
for skill in skill_cursor:
    name = skill['name']
    id_ = skill['_id']

    if(mind_skill_ids.get(name) == None):
        mind_skill_ids[name] = id_

    elif(mind_skill_ids[name] > id_):
        mind_skill_ids[name] = id_



filehandler = open("replacements.txt", 'rb')
get = pickle.load(filehandler)
filehandler.close()


for key in get:
	u = userprofiles.find({'_id' : key})
	u = u.next()
	values = get[key]
	
	for val in values:
		sks = skills.find({'_id' : val})
		sk = sks.next()
		#print(sk['name'])
		replacement_skill_id = mind_skill_ids[sk['name']]
		#print(replacement_skill_id)

		x = userprofiles.find({'_id': u['_id']})
		print("Initially: ", x.next())

		db.userprofiles.update(
				{
					'_id': u['_id']
				}, 
				
				{
					"$pull": 
					{
						"skills" : sk['_id']
					}
				}
			)
		x = userprofiles.find({'_id': u['_id']})
		print("After deletion:", x.next())
		
		db.userprofiles.update(
				{
					'_id': u['_id']
				}, 
				
				{
					'$push': 
					{
						'skills' : replacement_skill_id
					}
				}		
			)
		x = userprofiles.find({'_id': u['_id']})
		print("After replacement:", x.next())


##Close the connection
client.close()