from colorama import Fore
import util
import time
import re
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from InquirerPy import inquirer
from pprint import pprint


def search_genre(client):
    wantToSearch = True
    while wantToSearch:
        try:
            wantToSearch = search_genre_individual(client)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue

    util.text_with_loading(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}', 1)
    return


def search_genre_individual(client: MongoClient):
    '''
    Search for genres: 
        > The user should be able to provide a genre and a minimum vote count and see all titles under the provided genre 
            (again case-insensitive match) that have the given number of votes or more. 
        > The result should be sorted based on the average rating with the highest rating on top.

    Input: client - pymongo client to be processed

    Return: true if the user wants to continue searching genres, false if they want to exit to the main menu
    '''
    db = client['291db']

    title_basic_collection = db['title_basics']
    
    print(f'{Fore.CYAN}Welcome to Genre search! At any time, enter "EXIT" or "E" to return to main menu.{Fore.RESET}')

    genre = util.prompt_nonempty_string('Which genre do you want to watch?')
    if genre is None: return False

    minVoteCount = util.prompt_int_or_e('Minimum number of votes you would want for the search?')
    if minVoteCount is None: return False
    
    #regex = RegExp(["^", string, "$"].join(""), "i")
    genre = '^' +genre + '$'
    pipeline = [
        {'$unwind': '$genres'},
        {'$match': 
            {'genres': re.compile(genre, re.IGNORECASE)
                # {
                #     '$regex': genre,
                #     '$options': 'i'
                # }
            }
        },
        {'$lookup':
            {'from' : 'title_ratings',
                'localField' :'tconst',
                'foreignField': 'tconst',
                'pipeline': [
                    {'$project':
                        {
                            'numVotes': 1,
                            'averageRating': 1,
                        }
                    }
                ],
                'as' : 'voteAndRating'
            }
        },
        {'$unwind': '$voteAndRating'},
        {'$match': 
            {'voteAndRating.numVotes': 
                {'$gte': minVoteCount}
            }   
        },
        {'$sort':
            {
                'voteAndRating.averageRating':-1,
                'voteAndRating.numVotes': -1
            }
        },
        {'$project':
            {
                '_id': 0,
                'voteAndRating.numVotes': 1,
                'voteAndRating.averageRating': 1,
                'primaryTitle': 1
            }
        }
    ]

    aggResult = title_basic_collection.aggregate(pipeline)

    if aggResult:
        NumHeader,titleHeader, averageRatHeader, numVotes = "No.", 'Title ', 'AR', 'Votes'
        
        print(f'{NumHeader:>4}| {titleHeader: <75} | {averageRatHeader: <4} | {numVotes:}')
        print('-'*94)
        userChoice = True
        start = 0
        
        noResult = True
        while userChoice:
            end = start + 100
            for res in aggResult:
                start += 1
                noResult = False
                print(f'{start:>4}| {res["primaryTitle"]: <75} | {res["voteAndRating"]["averageRating"]: <4} | {res["voteAndRating"]["numVotes"]}') 
                if start > end:
                    break
            else:
                userChoice = False
                if not noResult:
                    print(f'{Fore.GREEN} No more results to display!')
            if userChoice == True: 
                choices = ['See more', 'leave']
                answers = util.get_valid_inquiry([{
                    'type': 'list',
                    'name': 'choice',
                    'message': 'What would you like to do now? (Arrow keys and enter to select)',
                    'choices': choices
                }])
                #print(answers['choice'])
                if answers['choice'] == 'See more':
                    userChoice = True
                else:
                    userChoice = False

    if noResult:
        print(f'{Fore.RED}No movie titles!\n')

    
    choices = [
        { 'value': 'y', 'name': 'Yes' },
        { 'value': 'n', 'name': 'No' }
    ]
    raw_cmd = util.get_valid_inquiry([{
            'type': 'list',
            'name': 'choice',
            'message': 'Would you like to make another search?',
            'choices': choices
        }])
    command = raw_cmd['choice']

    return command == 'y'
