import json
from pymongo import MongoClient
import time 


def starting_text():
    '''
    fancy starting text
    '''
    texts = [
        ':::        ::::::::      :::     :::::::::       ::::::::::: ::::::::   ::::::::  ::::    ::: ',
        ':+:       :+:    :+:   :+: :+:   :+:    :+:          :+:    :+:    :+: :+:    :+: :+:+:   :+: ',
        '+:+       +:+    +:+  +:+   +:+  +:+    +:+          +:+    +:+        +:+    +:+ :+:+:+  +:+ ',
        '+#+       +#+    +:+ +#++:++#++: +#+    +:+          +#+    +#++:++#++ +#+    +:+ +#+ +:+ +#+ ',
        '+#+       +#+    +#+ +#+     +#+ +#+    +#+          +#+           +#+ +#+    +#+ +#+  +#+#+# ',
        '#+#       #+#    #+# #+#     #+# #+#    #+#      #+# #+#    #+#    #+# #+#    #+# #+#   #+#+# ',
        '########## ########  ###     ### #########        #####      ########   ########  ###    #### '
    ]

    for text in texts:
        print(text)
    
    time.sleep(0.075) 
    print('\n\nWelcome to Load JSON!')
    time.sleep(0.075) 
    print('\nMade by Vedant, Kailash and Joshua.')

    # Boot screen
    animation = "|/-\\"
    anicount = 0

    # used to keep the track of
    # the duration of animation
    counttime = 0        

    # pointer for travelling the loading string
    i = 0

    print('\n')
    while (counttime <= 15):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.05) 
        print ("\033[A                             \033[A")
        print('Booting up...' + animation[anicount])
        anicount = (anicount + 1) % 4
        counttime = counttime + 1


def prog():
    while True:
        try:
            portNumber = input('Please enter the portNumber: ')
            client = MongoClient('mongodb://localhost:'+portNumber)
        except:
            print('Please Enter the correct portNumber. Cannot connect')
            continue
        finally:
            break
    
    print('Connected to MongoDB!')

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
        print('\n' + 'Opening ' + toBeOpened + '...')
        with open(toBeOpened) as f:
            data = json.load(f)
        collection = db[col]
        collection.delete_many({})
        print('Inserting data into ' + col + '...')
        collection.insert_many(data)

    print('Done!')


def main():
    starting_text()
    prog()
    

if __name__ == '__main__':
    main()