import util
from pymongo import MongoClient
from colorama import Fore
import re


def search_cast_crew(client: MongoClient):
    '''
    Runs the search cast function of the program until the user chooses to return to the main menu
    '''
    wantToSearch = True
    while wantToSearch:
        try:
            wantToSearch = search_cast_crew_individual(client)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue

    util.text_with_loading(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}', 1)
    return


def search_cast_crew_individual(client: MongoClient):
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

    personSep = '-'

    print()
    crewName = util.prompt_nonempty_string('Crew member name:')
    if crewName is None: return False

    crewName = f'^{crewName}$'
    cursor = nameBasicsColl.aggregate(
        [
            {
                "$match":{
                    "primaryName": re.compile(crewName, re.IGNORECASE)
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
        print('\n'+personSep*100+'\n')
        nameID = person["nconst"]
        name = person["primaryName"]
        professions = person["primaryProfession"]

        print(Fore.GREEN + f"Data for movie person: "+ Fore.RESET + f" {name} ({nameID})")
        print(Fore.GREEN +"Professions: " + Fore.RESET, end='')
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
        
        print(Fore.GREEN + "Appearances:" + Fore.RESET)
        i=0
        for item in titlesCursor:
            i+=1
            titleID = item["tconst"]
            job = item["job"]
            char = item["characters"]
            primaryTitle = item["movie"]["primaryTitle"]

            # Played {char} ({job}) in {primaryTitle} ({titleID})
            outStr = f'  {i:>4}) '
            if char:
                outStr += f"Played '{char}' "
                if job:
                    outStr += f"({job}) "
                outStr += "in "
            else:
                outStr += "Worked "
                if job: 
                    outStr += f'as {job} on '
                else:
                    outStr += "on "
            if primaryTitle:
                outStr += f"'{primaryTitle}' ({titleID})"
            else:
                outStr += f" the movie with ID {titleID} (Title unknown)"

            print(outStr)
            enterLoop = True

        print()
        choices = [
            { 'value': 'y', 'name': 'More results' },
            { 'value': 'c', 'name': 'Search again' },
            { 'value': 'n', 'name': 'Return to main menu' }
        ]
        raw_cmd = util.get_valid_inquiry([{
            'type': 'list',
            'name': 'choice',
            'message': 'Would you like to see more results? ',
            'choices': choices
        }])
        command = raw_cmd['choice']

        print ("\033[A                                                                                    \033[A")
        print ("\033[A                                                                                    \033[A")
        
        if command == 'c':
            print('\n' + personSep*100 + '\n Searching for a cast/crew member...')
            return True

        if command == 'n':
            cursor.close()
            titlesCursor.close()
            return False



    separator = '\n' + personSep*100

    if enterLoop:
        tmpStr = "\n\nNo "
    else:
        tmpStr = "\nNo "
    if enterLoop:
        tmpStr += "more "
    tmpStr += "results found.\n"

    if enterLoop:
        finalStr = separator + Fore.RED + tmpStr + Fore.RESET
    else:
        finalStr = Fore.RED + tmpStr + Fore.RESET
    print(finalStr)
    print(personSep*100+'\n')


    choices = [
        { 'value': 'y', 'name': 'Yes' },
        { 'value': 'n', 'name': 'No' }
    ]
    raw_cmd = util.get_valid_inquiry([{
            'type': 'list',
            'name': 'choice',
            'message': 'Would you like to make another search? ',
            'choices': choices
        }])
    command = raw_cmd['choice']

    return command == 'y'
