import util
from pymongo import MongoClient
from pymongo.collection import Collection
from InquirerPy import inquirer
from colorama import Fore
from InquirerPy.validator import EmptyInputValidator
from prompt_toolkit.validation import Validator, ValidationError


def search_cast(client: MongoClient):
    wantToSearch = True
    while wantToSearch:
        try:
            wantToSearch = search_cast_individual(client)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue

    print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
    time.sleep(3)
    return


def search_cast_individual(client: MongoClient):
    '''
    Search for cast/crew members:
        > The user should be able to provide a cast/crew member name and see all professions of the member and for each title the member had 
            a job, the primary title, the job and character (if any). 
        > Matching of the member name should be case-insensitive.

    Input: client - pymongo client to be processed

    Return: true if the user wants to continue adding movies, false if they want to exit to the main menu
    '''

    db = client['291db']
    nameBasicsColl = db['name_basics']
    titlePrincipalsColl = db['title_principals']

    personSep = '#'
    roleSep = '-'

    crew_name = util.prompt_nonempty_string('Crew member name:')
    if crew_name is None: return False

    cursor = nameBasicsColl.aggregate(
        [
            {
                '$match':{
                    'primaryName':{
                        '$regex': crew_name,
                        '$options': 'i'
                    }
                }
            },
            {
                '$project':{
                    'nconst': 1,
                    'primaryName': 1,
                    'primaryProfession': 1
                }
            }
        ]
    )

    enterLoop = False
    for person in cursor:
        print('\n\n'+personSep*100+'\n')
        nameID = person['nconst']
        name = person['primaryName']
        professions = person['primaryProfession']

        print(f'Data for movie person: {name} ({nameID})')
        print('Professions: ', end='')
        print(*professions, sep=', ')

        # Find all the titles the movie person has participated in 
        titlesCursor = titlePrincipalsColl.aggregate(
            [
                # Find all the instances of the movie person in title_principals
                {
                    '$match': {
                        'nconst': nameID
                    }
                },
                # Find the title of the movie mentioned in that instance
                {
                    '$lookup': {
                        'from': 'title_basics',
                        'localField': 'tconst',
                        'foreignField': 'tconst',
                        'as': 'movie'
                    }
                },
                # Extract characters from array
                {
                    '$unwind': {
                        'path': '$characters',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                # Extract role as an object, from an array
                {
                    '$unwind': {
                        'path': '$movie',
                        'preserveNullAndEmptyArrays': True
                    }
                }
            ]
        )
        print(roleSep*100)
        for item in titlesCursor:
            titleID = item['tconst']
            job = item['job']
            char = item['characters']
            primaryTitle = item['movie']['primaryTitle']

            # Played {char} ({job}) in {primaryTitle} ({titleID})
            if char:
                outStr = f'Played "{char}" '
                if job:
                    outStr += f'({job}) in '
                else:
                        outStr += f'in '
            else:
                outStr = 'Worked on '
            
            if primaryTitle:
                outStr += f'"{primaryTitle}" ({titleID})'
            else:
                outStr += f' the movie with ID {titleID} (Title unknown)'

            print(outStr)
            enterLoop = True
        
        choices = ['More Results', 'Back to Main Menu']
        answers = util.get_valid_inquiry([{
            'type': 'list',
            'name': 'choice',
            'message': 'What would you like to do now? (Arrow keys and enter to select)',
            'choices': choices
        }])

        if answers['choice'] == 'More Results':
            continue 
        else:
            cursor.close()
            titlesCursor.close()
            return False

        
    if enterLoop:
        tmpStr = '\n' + personSep*100 + '\nNo '
    else:
        tmpStr = '\nNo '
    if enterLoop:
        tmpStr += 'more '
    tmpStr += 'results found, press Enter to return to the main menu.'

    print('\n') # Add a newline to make it look nicer
    choices = ['Search Again', 'Back to Main Menu']
    answers = util.get_valid_inquiry([{
        'type': 'list',
        'name': 'choice',
        'message': tmpStr,
        'choices': choices
    }])

    return answers['choice'] == 'Search Again'
