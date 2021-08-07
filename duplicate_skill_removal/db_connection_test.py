import ssl 
from pymongo import MongoClient
import pprint
import json
import pickle


client = MongoClient('10.0.0.140:27017')
#
##Specify the database to be used
db = client.the_incircle_dev_new
print(db.list_collection_names())
 #mysql-db-connection dbName - theincircle, dbHost - 10.0.0.252, dbPort - 3306, userName - theincircle, userPass - The1nc1rcle#yG1jY,
 #mongodb://theincircle:TheIncircle#123@10.0.0.140:27017/the_incircle_dev_new?retryWrites=true&authSource=admin