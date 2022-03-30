from pymongo import MongoClient
from getpass import getpass
import os
from colorama import Fore
import colorama
import util
from pymongo.errors import ServerSelectionTimeoutError
from commands.search_title import search_title
from commands.add_cast_crew import add_cast_crew
from commands.search_genre import search_genre
from commands.add_movie import add_movie


def mongoConnect():
    """
    Takes user input for a port number and connects to the mongoDB database
    Returns the resulting client 
    """
    while True:
        try:
            # port = util.get_valid_int('Enter a port: ')
            port = 27017
            if port:
                client = MongoClient(host = 'localhost', port = int(port), serverSelectionTimeoutMS = 15)
                client.server_info()
                util.text_with_loading(f'{Fore.GREEN}Connected to MongoDB database! Moving to main menu...{Fore.RESET}')
            else:
                client = MongoClient()
        except ServerSelectionTimeoutError as e:
            print(f'{Fore.RED}Invalid port number {port}!{Fore.RESET}')
            continue
        except Exception as err:
            print(f'{Fore.RED}Invalid port! {err}\nPlease try again!{Fore.RESET}')
            continue
        else:
            return client



def mainMenu(client):
    '''
    Main user interface for the program
    Handles user inputs and processes the database client appropriately

    Input: client - pymongo client to be processed
    '''

    while True:
        reset_screen()
        choices = [
            { 'value': 'ST', 'name': 'Search for a title' },
            { 'value': 'SG', 'name': 'Search for a genre' },
            { 'value': 'SC', 'name': 'Search for a cast/crew member' },
            { 'value': 'AM', 'name': 'Add a movie' },
            { 'value': 'AC', 'name': 'Add a cast/crew member' },
            { 'value': 'EX', 'name': 'Exit application' }
        ]
        raw_cmd = util.get_valid_inquiry([{
                'type': 'list',
                'name': 'choice',
                'message': 'Welcome to the main menu! Enter your selection below (arrow keys and enter)',
                'choices': choices
            }])
        command = raw_cmd['choice']
        
        if command == 'ST':
            print('Searching for a title...')
            search_title(client)
            reset_screen()

        elif command == 'SG':
            print('Searching for a genre...')
            search_genre(client)
            # Remove after implementing exit commands in searchGenre()
            #print("Press Enter to return to the main menu.")
           # getpass(prompt="")
            reset_screen()

        elif command == 'SC':
            print('Searching for a cast/crew member...')
            searchCast(client)
            reset_screen()

        elif command == 'AM':
            print('Adding a new movie...')
            add_movie(client)
            reset_screen()

        elif command == 'AC':
            print('Adding a new cast/crew member...')
            add_cast_crew(client)
            # Remove after implementing exit commands in addCast()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")
            reset_screen()

        else:
            ##### PRINT MADE BY
            print('Exiting...')
            return




###TODO: Fill out all functions below

def reset_screen(welcome_text = None, show_names = False):
    os.system('cls' if os.name == 'nt' else 'clear')
    util.starting_text(welcome_text, show_names)
    print('-'*70 + '\n')



def searchCast(client):
    """
    Search for cast/crew members:
        > The user should be able to provide a cast/crew member name and see all professions of the member and for each title the member had 
            a job, the primary title, the job and character (if any). 
        > Matching of the member name should be case-insensitive.

    Input: client - pymongo client to be processed
    """

    db = client["291db"]
    nameBasicsColl = db["name_basics"]
    titlePrincipalsColl = db["title_principals"]

    personSep = '#'
    roleSep = '-'

    crewName = input("Enter the cast/crew name: ").lower()
    if crewName == 'exit' or crewName == 'e':
        return

    cursor = nameBasicsColl.aggregate(
        [
            {
                "$match":{
                    "primaryName":{
                        "$regex": crewName,
                        "$options": "i"
                    }
                }
            },
            {
                "$project":{
                    "nconst":1,
                    "primaryName":1,
                    "primaryProfession":1
                }
            }
        ]
    )

    enterLoop = False
    for person in cursor:
        print('\n\n'+personSep*100+'\n')
        nameID = person["nconst"]
        name = person["primaryName"]
        professions = person["primaryProfession"]

        print(f"Data for movie person: {name} ({nameID})")
        print("Professions: ", end='')
        print(*professions, sep=', ')

        # Find all the titles the movie person has participated in 
        titlesCursor = titlePrincipalsColl.aggregate(
            [
                # Find all the instances of the movie person in title_principals
                {
                    "$match": {
                        "nconst": nameID
                    }
                },
                # Find the title of the movie mentioned in that instance
                {
                    "$lookup": {
                        "from": 'title_basics',
                        "localField": 'tconst',
                        "foreignField": 'tconst',
                        "as": 'movie'
                    }
                },
                # Extract characters from array
                {
                    "$unwind": {
                        "path": "$characters",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                # Extract role as an object, from an array
                {
                    "$unwind": {
                        "path": "$movie",
                        "preserveNullAndEmptyArrays": True
                    }
                }
            ]
        )
        print(roleSep*100)
        for item in titlesCursor:
            titleID = item["tconst"]
            job = item["job"]
            char = item["characters"]
            primaryTitle = item["movie"]["primaryTitle"]

            # Played {char} ({job}) in {primaryTitle} ({titleID})
            if char:
                outStr = f"Played '{char}' "
                if job:
                    outStr += f"({job}) in "
                else:
                        outStr += f"in "
            else:
                outStr = "Worked on "
            
            if primaryTitle:
                outStr += f"'{primaryTitle}' ({titleID})"
            else:
                outStr += f" the movie with ID {titleID} (Title unknown)"

            print(outStr)
            enterLoop = True

        leave = input("\nPress Enter to see more results (or enter exit to return to the main menu): ").lower()
        if leave == 'exit':
            cursor.close()
            titlesCursor.close()
            return
        
    if enterLoop:
        tmpStr = '\n' + personSep*100 + "\nNo "
    else:
        tmpStr = "\nNo "
    if enterLoop:
        tmpStr += "more "
    tmpStr += "results found, press Enter to return to the main menu."
    input(tmpStr)
    return















def main():
    colorama.init()
    client = mongoConnect()
    reset_screen()
    mainMenu(client)
    client.close()


if __name__ == "__main__":
    main()

