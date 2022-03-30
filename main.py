from pymongo import MongoClient
from getpass import getpass
import os
from colorama import Fore
import colorama
import util
from pymongo.errors import ServerSelectionTimeoutError
from commands.search_title import search_title
from commands.add_cast_crew import add_cast_crew

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
        choices = [
            { 'value': 'ST', 'name': 'Search for a title' },
            { 'value': 'SG', 'name': 'Search for a genre' },
            { 'value': 'SC', 'name': 'Search for a cast/crew member' },
            { 'value': 'AM', 'name': 'Add a movie' },
            { 'value': 'AC', 'name': 'Add a cast/crew member' },
            { 'value': 'EX', 'name': 'Exit' }
        ]
        raw_cmd = util.get_valid_inquiry([{
                'type': 'list',
                'name': 'choice',
                'message': 'Welcome to the main menu! Enter your selection below!',
                'choices': choices
            }])
        command = raw_cmd['choice']
        
        if command == 'ST':
            reset_screen()
            print('Searching for a title...')
            search_title(client)

        elif command == 'SG':
            reset_screen()
            print('Searching for a genre...')
            searchGenre(client)
            # Remove after implementing exit commands in searchGenre()
           # print("Press Enter to return to the main menu.")
            #getpass(prompt="")

        elif command == 'SC':
            reset_screen()
            print('Searching for a cast/crew member...')
            searchCast(client)

        elif command == 'AM':
            reset_screen()
            print('Adding a new movie...')
            addMovie(client)
            # Remove after implementing exit commands in addMovie()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'AC':
            reset_screen()
            add_cast_crew(client)

        else:
            print('Exiting...')
            return




###TODO: Fill out all functions below

def reset_screen(welcome_text = None, show_names = False):
    os.system('cls' if os.name == 'nt' else 'clear')
    util.starting_text(welcome_text, show_names)
    print('-'*70 + '\n')






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
    
    os.system('cls' if os.name == 'nt' else 'clear')
    genre = input('Tell which genre are you interested to watch? ')

    if genre.upper() == 'EXIT' or genre.upper() == 'E':
        print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
        return True

    minVoteCount = util.get_valid_int_E('Tell minimum number of votes you would want for the search? ')

    if not minVoteCount:
        print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
        return True
        
    # while True:
    #     try:
           
    #         if minVoteCount < 0:
    #             raise ValueError('value needs to be >= 0')
    
    #     except Exception as e:
    #             print(e.args)
    #     else:
    #         break

    
    pipeline = [
        { "$unwind": "$genres"},
        {"$match": 
            {"genres": 
                {
                    '$regex': genre,
                    '$options': 'i'
                }
            }
        },
        {"$lookup":
            {"from" : "title_ratings",
                "localField" :"tconst",
                "foreignField": "tconst",
                "pipeline": [
                    {"$project":
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
            {"voteAndRating.numVotes": 
                {"$gte": minVoteCount}
            }   
        },
        {"$sort":
            {
                "voteAndRating.averageRating":-1
                #"voteAndRating.numVotes": -1
            }
        },
        {"$project":
            {
                "_id": 0,
                "voteAndRating.numVotes": 1,
                "voteAndRating.averageRating": 1,
                "primaryTitle": 1
            }
        }
    ]

    aggResult = title_basic_collection.aggregate(pipeline)

    if aggResult:
        titleHeader, averageRatHeader, numVotes = "Title ", "AR", "Votes"
        
        print(f"|{titleHeader: <70} | {averageRatHeader: <4} | {numVotes:}")
        userChoice = True
        start = 0
        noResult = True
        while userChoice:
            start = 0
            for res in aggResult:
                start += 1
                noResult = False
                print(f"|{res['primaryTitle']: <70} | {res['voteAndRating']['averageRating']: <4} | {res['voteAndRating']['numVotes']}") 
                if start > 100:
                    break
            else:
                userChoice = False   
            if userChoice == True: 
                choice = input("press Y/y (or anything else for negative) if you want to see more results\n")
                if choice.lower() != 'y':
                    userChoice = False

    if noResult:
        print("No Movie Title found, you can try to search again\n")

    print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
    return True
    


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



def addMovie(client):
    """
    Add a movie: 
        > The user should be able to add a row to title_basics by providing a unique id, a title, a start year, a running time and a list of genres. 
        > Both the primary title and the original title will be set to the provided title, the title type is set to movie 
            and isAdult and endYear are set to Null (denoted as \\N).

    Input: client - pymongo client to be processed
    """
    db = client['291db']
    title_basic_col = db['title_basics']
    res = title_basic_col.find({'primaryTitle': 'AlmerTheMuneer'})
    for j in res:
        print(j)
    #return
    unId = input("Enter a unique id for the movie to be added\n")
    title = input("Enter a title of the movie to be added\n")
    startYear = util.get_valid_int_E("Enter the start year \n")
    runTime = util.get_valid_int_E("Enter the running time\n")
    genreList = input("Enter the genres seperated by a comma\n").split(',')
    #arr = []
    jsonQuery = dict()
    jsonQuery ['primaryTitle'] = title
    jsonQuery['originalTitle'] = title
    jsonQuery['tconst'] = unId
    jsonQuery['startYear'] = startYear
    jsonQuery['runtimeMinutes'] = runTime
    jsonQuery['genres'] = genreList
    jsonQuery['titleType'] = 'movie'
    jsonQuery['isAdult'] = None
    jsonQuery['endYear'] = None
    #arr.append(jsonQuery)
    title_basic_col.insert_one(jsonQuery)
   
  
    



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
    reset_screen()
    mainMenu(client)
    client.close()


if __name__ == "__main__":
    main()

