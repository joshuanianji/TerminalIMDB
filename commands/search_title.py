from colorama import Fore, Back, Style
import util
from pymongo.mongo_client import MongoClient

def search_title(client: MongoClient, commands):
    """
    Search for titles: 
        > The user should be able to provide one or more keywords, and the system should retrieve all titles that match all those keywords (AND semantics). 
        > A keyword matches if it appears in the primaryTitle field (the matches should be case-insensitive). 
        > A keyword also matches if it has the same value as the year field. 
        > For each matching title, display all the fields in title_basics. 
        > The user should be able to select a title to see the rating, the number of votes, the names of cast/crew members and their characters (if any).
    
    Input: 
        client - pymongo client to be processed
        commands: the command dictionary
    """
    color = commands['ST']['color']
    print(f'{color}Please enter in your keywords (space separated), or "BACK" to exit{Fore.RESET}')
    keywords = util.get_valid_input('> ', lambda cmd: cmd.strip() != '', 'Please do not enter an empty string!', True).split()
    
    if keywords[0] == 'BACK':
        print(f'{color}Returning to main menu...{Fore.RESET}')
        return
    else:
        and_queries = []
        for keyword in keywords:
            # each of the and_queries test if a keyword matches
            and_queries.append({
                '$or': [
                    {
                        'primaryTitle': {
                            '$regex': keyword,
                            '$options': 'i'
                        }
                    },
                    { 'startYear': keyword }
                ]
            })
        query = {
            '$and': and_queries
        }
        db = client['291db']
        collection = db['title_basics']
        titles = collection.find(query)

        for title in titles:
            print(f'{color}Title: {title["primaryTitle"]}')
            print(f'{color}Year: {title["startYear"]}')
            print(f'{color}Type: {title["titleType"]}')
            print(f'{color}Genres: {title["genres"]}')
            print(f'{color}Runtime: {title["runtimeMinutes"]}')
            print(f'{color}{Style.RESET_ALL}')
        
        print('Done searching movies. Returning to home screen...')
        return

