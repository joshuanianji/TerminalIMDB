from tkinter.ttk import Separator
import util
from InquirerPy import prompt
from colorama import Fore


# colors = BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE


def get_valid_inquiry(questions):
    '''
    Get a valid inquiry from the user

    If the user presses Ctrl+c, exit the program

    Return:
        answers: dictionary of answers
    '''
    while True:
        try:
            return prompt(questions)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue



def search_cast_crew(client):
    wantToSearch = True
    while wantToSearch:
        wantToSearch = searchCast(client)
    return


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

    personSep = '-'

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
        for item in titlesCursor:
            titleID = item["tconst"]
            job = item["job"]
            char = item["characters"]
            primaryTitle = item["movie"]["primaryTitle"]

            # Played {char} ({job}) in {primaryTitle} ({titleID})
            outStr = '  • '
            if char:
                outStr += f"Played '{char}' "
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







    choices = [
        { 'value': 'y', 'name': 'Yes' },
        { 'value': 'n', 'name': 'No' }
    ]
    raw_cmd = get_valid_inquiry([{
            'type': 'list',
            'name': 'choice',
            'message': 'Would you like to make another search?',
            'choices': choices
        }])
    command = raw_cmd['choice']

    return command == 'y'



