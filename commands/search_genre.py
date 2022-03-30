import util
import os
import time
from colorama import Fore



def search_genre(client):
    wantToSearch = True
    while wantToSearch:
        wantToSearch = search_genre_c(client)

    print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')

    return
def search_genre_c(client):
    '''
    Search for genres: 
        > The user should be able to provide a genre and a minimum vote count and see all titles under the provided genre 
            (again case-insensitive match) that have the given number of votes or more. 
        > The result should be sorted based on the average rating with the highest rating on top.

    Input: client - pymongo client to be processed
    '''
    db = client['291db']

    title_basic_collection = db['title_basics']
    
    genre = input('Tell which genre are you interested to watch? ')

    if genre.upper() == 'EXIT' or genre.upper() == 'E':
        print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
        return True

    minVoteCount = util.get_valid_int_E('Tell minimum number of votes you would want for the search? ')

    if not minVoteCount:
        print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
        return True

    
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
        
        print(f"|{titleHeader: <75} | {averageRatHeader: <4} | {numVotes:}")
        userChoice = True
        start = 0
        noResult = True
        while userChoice:
            start = 0
            for res in aggResult:
                start += 1
                noResult = False
                print(f"|{res['primaryTitle']: <75} | {res['voteAndRating']['averageRating']: <4} | {res['voteAndRating']['numVotes']}") 
                if start > 100:
                    break
            else:
                userChoice = False   
            if userChoice == True: 
                choice = input("press Y/y (or anything else for negative) if you want to see more results\n")
                if choice.lower() != 'y':
                    userChoice = False

    if noResult:
        print(f"{Fore.RED}No Movie Title found, you can try to search again\n")

    
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

  

