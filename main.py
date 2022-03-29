from re import L
from pymongo import MongoClient, TEXT
from getpass import getpass
import os
from colorama import Fore, Back, Style
import colorama
import util
from pymongo.errors import ServerSelectionTimeoutError
import time
from commands.search_title import search_title, show_movie_info

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


commands = {
    'ST': {
        'name': 'Search for a title',
        'color': Fore.RED
    },
    'SG': {
        'name': 'Search for a genre',
        'color': Fore.YELLOW
    },
    'SC': {
        'name': 'Search for a cast/crew member',
        'color': Fore.GREEN
    },
    'AM': {
        'name': 'Add a movie',
        'color': Fore.BLUE
    },
    'AC': {
        'name': 'Add a new cast/crew member',
        'color': Fore.CYAN
    },
    'EX': {
        'name': 'Close the connection',
        'color': Fore.MAGENTA
    }
}

def mainMenu(client):
    '''
    Main user interface for the program
    Handles user inputs and processes the database client appropriately

    Input: client - pymongo client to be processed
    '''

    # Generate help message
    helpMessage = ''
    for cmd, data in commands.items():
        helpMessage += f"{data['color']} {cmd} - {data['name']}{Fore.RESET}\n"
    helpMessage = helpMessage.strip()
    help = False

    while True:
        if not help:
            reset_screen('Welcome to the main menu! Enter your selection below!', show_names = True)
        print(helpMessage)
        help = False

        # Get user command input

        command = util.get_valid_input('> ', lambda cmd: cmd == 'H' or cmd in commands, 'Invalid command. Press "H" for help.', True)

        # Handle user input
        if command == 'H':
            help = True

        elif command == 'ST':
            reset_screen()
            print('Searching for a title...')
            search_title(client, commands)
            # Remove after implementing exit commands in searchTitle()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'SG':
            reset_screen()
            print('Searching for a genre...')
            searchGenre(client)
            # Remove after implementing exit commands in searchGenre()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'SC':
            reset_screen()
            print('Searching for a cast/crew member...')
            searchCast(client)
            # Remove after implementing exit commands in searchCast()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'AM':
            reset_screen()
            print('Adding a new movie...')
            addMovie(client)
            # Remove after implementing exit commands in addMovie()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'AC':
            reset_screen()
            print('Adding a new cast/crew member')
            addCast(client)
            # Remove after implementing exit commands in addCast()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        else:
            print('Exiting...')
            return




###TODO: Fill out all functions below

def reset_screen(welcome_text = None, show_names = False):
    os.system('cls' if os.name == 'nt' else 'clear')
    util.starting_text(welcome_text, show_names)






def searchGenre(client):
    """
    Search for genres: 
        > The user should be able to provide a genre and a minimum vote count and see all titles under the provided genre 
            (again case-insensitive match) that have the given number of votes or more. 
        > The result should be sorted based on the average rating with the highest rating on top.

    Input: client - pymongo client to be processed
    """
    #TODO
    db = client['291db']

    title_basic_collection = db['title_basics']
    title_rating_collection = db['title_ratings']

    title_basic_collection.create_index('tconst')
    title_rating_collection.create_index('tconst')
    
  #  print(title_basic_collection.index_information())
    #title_basic_collection.create_index([("genres", TEXT)])
    
        
    genre = input('Tell which genre are you interested to watch? ')


    while True:
        try:
            minVoteCount = int(input('Tell minimum number of votes you would want for the search? '))
            if minVoteCount < 0:
                raise ValueError('value needs to be >= 0')
    
        except Exception as e:
                print(e.args)
        else:
            break








        

    pipeline = [
            { "$unwind": "$genres"},
        {"$match": 
            {"genres": genre
            }
        },
        {   
            "$lookup":
            {
                "from" : "title_ratings",
                "localField" :"tconst",
                "foreignField": "tconst",
                "pipeline":
                [
                    {
                        "$project":
                        {
                            "numVotes": 1,
                            "averageRating": 1,
                        }
                    }
                ],
                "as" : "voteAndRating"
            }
        },
        {"$unwind": "$voteAndRating"},
        {"$match": 
          {"voteAndRating.numVotes": {"$gte": minVoteCount}
               }   
           },
        {"$sort":
            {
                "voteAndRating.averageRating":-1
            }
        }
           
            ]
    #{"$gte": minVoteCount}



    pipeline1 = [
        {
            "$lookup":   {
                    "from" : "title_ratings",
                    # "localField" :"tconst",
                    # "foreignField": "tconst",
                    "let":{"vote":"numVotes"},
                    "pipeline":
            [
                {"$match": 
                    {"numVotes": {"$gte": minVoteCount}
                       # "expr": {"$gte": [, "$minVoteCount"]}
                    } },
                {
                     "$project":  
                    {
                    "_id": 0,
                    }
                }
            ],
                    "as" : "voteAndRating"
            }
                # "project":  
                # {
                #     "_id": 0,
                #     "numVotes": 1, 
                #     "tconst": 1,
                #     "primaryTitle": 1,
                #  },
                  
        }
    ]
    
    #aggResult2 = title_basic_collection.aggregate(pipeline1)
    aggResult = title_basic_collection.aggregate(pipeline)
    count = 0
    # for res in aggResult2:
    #     print(res)
    #     count+=1
    #     if count == 3:
    #         break
            
    count = 0     
    for res in aggResult:
        print(res)
        count+=1
        if count == 3:
            break
    #genreList = title_basic_collection.find_one({'genres': genre})
   # print(genreList)
    
    

    






def searchCast(client):
    """
    Search for cast/crew members:
        > The user should be able to provide a cast/crew member name and see all professions of the member and for each title the member had 
            a job, the primary title, the job and character (if any). 
        > Matching of the member name should be case-insensitive.

    Input: client - pymongo client to be processed
    """
    #TODO
    pass



def addMovie(client):
    """
    Add a movie: 
        > The user should be able to add a row to title_basics by providing a unique id, a title, a start year, a running time and a list of genres. 
        > Both the primary title and the original title will be set to the provided title, the title type is set to movie 
            and isAdult and endYear are set to Null (denoted as \\N).

    Input: client - pymongo client to be processed
    """
    

    pass



def addCast(client):
    """
    Add a cast/crew member: 
        > The user should be able to add a row to title_principals by providing a cast/crew member id, a title id, and a category. 
        > The provided title and person ids should exist in name_basics and title_basics respectively (otherwise, proper messages should be given), 
            the ordering should be set to the largest ordering listed for the title plus one (or 1 if the title is not listed in title_principals) 
            and any other field that is not provided (including job and characters) set to Null.

    Input: client - pymongo client to be processed
    """
    #TODO
    pass



















def main():
    colorama.init()
    client = mongoConnect()
    mainMenu(client)
    client.close()



def main_2():
    pipeline1 = [
        {
            "$lookup":   {
                    "from" : "title_ratings",
                    # "localField" :"tconst",
                    # "foreignField": "tconst",
                    "let":{"vote":"numVotes"},
                    "pipeline":[
                     {"$match": {
                        "expr": {"$gte": ["$$vote", "$minVoteCount"]}
                     } },
                     {
                     "$project":  
                    {
                    "_id": 0,
                    }}],
                    "as" : "voteAndRating"
            }
                # "project":  
                # {
                #     "_id": 0,
                #     "numVotes": 1, 
                #     "tconst": 1,
                #     "primaryTitle": 1,
                #  },
                  
        }
    ]
    from pprint import pprint
    colorama.init()
    client = mongoConnect()
    title_basic_collection = client['291db']['title_basic']
    aggResult2 = title_basic_collection.aggregate(pipeline1)
    for res in aggResult2:
        pprint(res)
    client.close()


def main_3():
    # tt0083528
    colorama.init()
    client = mongoConnect()
    show_movie_info(client, 'tt0083528')
    client.close()

if __name__ == "__main__":
    main()

