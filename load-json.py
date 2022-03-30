import os
import json
import time 
import colorama
from pymongo import MongoClient
from InquirerPy import inquirer
from colorama import Fore, Style
from pymongo.errors import ServerSelectionTimeoutError
from InquirerPy.validator import NumberValidator


def starting_text():
    '''
    fancy starting text
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    texts = [
        ':::        ::::::::      :::     :::::::::       ::::::::::: ::::::::   ::::::::  ::::    ::: ',
        ':+:       :+:    :+:   :+: :+:   :+:    :+:          :+:    :+:    :+: :+:    :+: :+:+:   :+: ',
        '+:+       +:+    +:+  +:+   +:+  +:+    +:+          +:+    +:+        +:+    +:+ :+:+:+  +:+ ',
        '+#+       +#+    +:+ +#++:++#++: +#+    +:+          +#+    +#++:++#++ +#+    +:+ +#+ +:+ +#+ ',
        '+#+       +#+    +#+ +#+     +#+ +#+    +#+          +#+           +#+ +#+    +#+ +#+  +#+#+# ',
        '#+#       #+#    #+# #+#     #+# #+#    #+#      #+# #+#    #+#    #+# #+#    #+# #+#   #+#+# ',
        '########## ########  ###     ### #########        #####      ########   ########  ###    #### '
    ]
    rainbow = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

    for (text, color) in zip(texts, rainbow):
        if (color == Fore.WHITE):
            print(Style.DIM + color + text + Fore.RESET + Style.RESET_ALL)
        else:
            print(color + text + Fore.RESET)
    
    time.sleep(0.075) 
    print('\n\n' + Fore.WHITE + 'Welcome to Load JSON!' + Fore.RESET)

    time.sleep(0.075) 
    print('\n' + 'Made by ' + Fore.CYAN + 'Vedant' + Fore.RESET + ', ' + Fore.GREEN + 'Kailash' + Fore.RESET + ' and ' + Fore.BLUE + 'Joshua' + Fore.RESET + '.')

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
    collist = None
    while True:
        try:
            portNumber = inquirer.text(
                message='Please enter the portNumber: ', 
                validate=NumberValidator()
            ).execute()
            client = MongoClient(host = 'localhost', port = int(portNumber), serverSelectionTimeoutMS = 15)
            #create or open the LabH01 database server
            db = client['291db']
            colNames = ['name_basics', 'title_basics', 'title_ratings', 'title_principals']
            collist = db.list_collection_names()
            break
        except ServerSelectionTimeoutError:
            print(f'{Fore.RED}Invalid port number!{Fore.RESET}')
            continue
        except Exception as err:
            print(f'{Fore.RED}Error connecting to mongoDB!\n{err}\nPlease try again!{Fore.RESET}')
            continue

    print(Fore.GREEN + 'Connected to MongoDB!' + Fore.RESET)

    for cName in colNames:
        if cName in collist:
            collection = db[cName]
            collection.drop()
        db.create_collection(cName)

    fileJsonNames = ['name.basics', 'title.basics', 'title.ratings', 'title.principals']
    for col, name in zip(colNames, fileJsonNames):
        toBeOpened = name + '.json'
        print('\n' + 'Opening ' + Fore.GREEN + toBeOpened + Fore.RESET + '...')
        with open(toBeOpened) as f:
            data = json.load(f)
        collection = db[col]
        collection.delete_many({})
        print('Inserting data into ' + Fore.CYAN + col + Fore.RESET + '...')
        collection.insert_many(data)

    print(Fore.GREEN + 'Done!' + Fore.RESET)

    db['title_basics'].create_index('tconst')
    db['title_ratings'].create_index('tconst')
    db['name_basics'].create_index('nconst')
    db['title_principals'].create_index('nconst')
    db['title_principals'].create_index('tconst')



def main():
    colorama.init()
    starting_text()
    prog()
    

if __name__ == '__main__':
    main()