from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('localhost:27017')
db = client.the_incircle_dev_new
print(db.list_collection_names())

def getRoots():
    roots = {}
    for skill in db.skills.find({'parent': {"$exists": False}}):
        roots[skill['_id']] = True
    return roots
        

roots = getRoots()

print('Number of roots : ', len(roots))

def getNonRoots():
    non_roots = []
    for skill in db.skills.find({'parent': {"$exists": True}}):
        non_roots.append(skill)     
    return non_roots   


non_roots = getNonRoots()
print('Number of non roots : ', len(non_roots))


skills_with_no_roots = []

def getRoot(skill):
    duplicates = {}
    depth = 0
    sk = skill
    while(sk['_id'] not in roots):
        if(sk['_id'] in duplicates):
            print('Cycle Detected!!!')
            break
        else:
            duplicates[sk['_id']] = True
            depth = depth + 1   
        if(sk['_id'] == sk['parent']):
            break
        sk = db.skills.find_one({'_id' : ObjectId(sk['parent'])})

        if(sk == None):
            skills_with_no_roots.append(skill['name'])
            #print("\n\n\nSkill: ", skill['name'])
            #print('No root found!')
            break

        if(depth > 1):
            print("\n\n\nSkill: ", skill['name'])
            print("New Parent: ", sk['name'])
    
    textfile = open("skills_with_no_roots.txt", "w")
    for element in skills_with_no_roots:
        textfile.write(element + "\n")
    textfile.close()

    root = None

    if(sk != None):
        root = sk['_id']
    return root


def replaceParent(sk_id, parent):
    #print("root : ", db.skills.find_one({'_id' : parent}))
    #print("skill : ", db.skills.find_one({'_id' : sk_id}))
    
    #print(sk_id)
    
    db.skills.update_one(
                        {
                            '_id' : ObjectId(sk_id)
                        },
                        
                        {
                            '$set' : 
                            {
                                'parent' : parent
                            }
                        }    
                    )
    

for skill in non_roots:
    root = getRoot(skill)
    #replaceParent(skill['_id'], root)
