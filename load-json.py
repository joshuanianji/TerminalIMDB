import json
from pymongo import MongoClient

while True:
    try:
        portNumber = input('Please enter the portNumber: ')
        client = MongoClient('mongodb://localhost:'+portNumber)
    except:
        print('Please Enter the correct portNumber. Cannot connect')
    finally:
        break


#create or open the LabH01 database server
db = client["291db"]
    
colNames = ['name_basics', 'title_basics', 'title_ratings', 'title_principals']

collist = db.list_collection_names()
for cName in colNames:
    if cName in collist:
        collection = db[cName]
        collection.drop()
    db.create_collection(cName)

fileJsonNames = ['name.basics', 'title.basics', 'title.ratings', 'title.principals']
for col, name in zip(colNames, fileJsonNames):
    toBeOpened = name + '.json'
    with open(toBeOpened) as f:
        data = json.load(f)
    collection = db[col]
    collection.delete_many({})
    collection.insert_many(data)
    



