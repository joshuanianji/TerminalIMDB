from typing import List
from colorama import Fore, Back, Style
import util
from pymongo.mongo_client import MongoClient
from pprint import pprint

def search_title(client: MongoClient, commands):
    '''
    Searches titles until the user exits.
    '''
    while True:
        user_exit = search_title_individual(client, commands)
        if user_exit:
            return

def search_title_individual(client: MongoClient, commands) -> bool:
    """
    Performs an individual search of the titles.
    Search for titles: 
        > The user should be able to provide one or more keywords, and the system should retrieve all titles that match all those keywords (AND semantics). 
        > A keyword matches if it appears in the primaryTitle field (the matches should be case-insensitive). 
        > A keyword also matches if it has the same value as the year field. 
        > For each matching title, display all the fields in title_basics. 
        > The user should be able to select a title to see the rating, the number of votes, the names of cast/crew members and their characters (if any).
    
    Input: 
        client - pymongo client to be processed
        commands: the command dictionary
    
    Returns:
        user_exit: true if the user wants to exit back to main page, false if the user wants to continue searching
    """
    color = commands['ST']['color']
    print(f'{color}Please enter in your keywords (space separated), or "BACK" to exit{Fore.RESET}')
    keywords = util.get_valid_input('> ', lambda cmd: cmd.strip() != '', 'Please do not enter an empty string!', True).split()
    
    if keywords[0] == 'BACK':
        print(f'{color}Returning to main menu...{Fore.RESET}')
        return True 
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
        titles = collection.find(query, { 'primaryTitle': 1, 'tconst': 1 }) # project primary_title
        titles_list = [title for title in titles] # turn a cursor into a concrete list.

        if len(titles_list) == 0:
            choices = ['Search Again', 'Back to Main Menu']
            answers = util.get_valid_inquiry([{
                'type': 'list',
                'name': 'choice',
                'message': 'No titles found for query! What would you like to do?',
                'choices': choices
            }])
            if answers['choice'] == 'Search Again':
                return False
            else:
                return True

        else:
            print(f'Found {Fore.GREEN}{len(titles_list)}{Fore.RESET} titles. Please select one to see more information.')
            choices = get_movies_display_list(titles_list)
            other_choices = ['Search Again', 'Back to Main Menu']
            answers = util.get_valid_inquiry([{
                'type': 'list',
                'name': 'choice',
                'message': 'Arrow keys and enter to select',
                'choices': choices + other_choices
            }])
            if answers['choice'] == 'Search Again':
                return False
            elif answers['choice'] == 'Back to Main Menu':
                return True
            else:
                # here, answers['choice'] will be the ID of the movie (tconst)
                user_choice = show_movie_info(client, answers['choice'])
                return user_choice

def get_movies_display_list(titles: List[dict]) -> List[str]:
    """
    Gets the display list for the movies

    Input: 
        titles - the list of titles to display
    """
    display_list = []
    for title in titles:
        display_list.append({
            'name': title['primaryTitle'] + '\n\t' + title['tconst'],
            'value': title['tconst']
        })
    return display_list


def show_movie_info(client: MongoClient, movie_id: str):
    """
    Displays the information for a movie (the rating, the number of votes, the names of cast/crew members and their characters (if any))

    Input: 
        client - pymongo client to be processed
        choice - the title of the movie to display
    """
    db = client['291db']
    basics = db['title_basics']
    ratings = db['title_ratings']
    principals = db['title_principals']

    movie = basics.find_one({'tconst': movie_id})
    rating = ratings.find_one({'tconst': movie_id})
    # cast = principals.find({'tconst': movie_id, 'category': '$or': ['actor', 'actress']})

    cast_agg = principals.aggregate([
        {
            '$match': {
                'tconst': movie_id,
                '$or': [
                    {'category': 'actor'}, 
                    {'category': 'actress'}
                ]
            }
        },
        {
            '$lookup': {
                'from': 'name_basics',
                'localField': 'nconst',
                'foreignField': 'nconst',
                'as': 'cast_info'
            }
        },
        {
            '$replaceRoot': { 'newRoot': { '$mergeObjects': [ { '$arrayElemAt': [ "$cast_info", 0 ] }, "$$ROOT" ] } }
        },
        { '$project': { 'fromItems': 0 } }
    ])

    crew_agg = principals.aggregate([
        {
            '$match': {
                'tconst': movie_id,
                '$and': [
                    {'category': {'$ne': 'actor'}}, 
                    {'category': {'$ne': 'actress'}}
                ]
            }
        },
        {
            '$lookup': {
                'from': 'name_basics',
                'localField': 'nconst',
                'foreignField': 'nconst',
                'as': 'cast_info'
            }
        },
        {
            '$replaceRoot': { 'newRoot': { '$mergeObjects': [ { '$arrayElemAt': [ "$cast_info", 0 ] }, "$$ROOT" ] } }
        },
        { '$project': { 'fromItems': 0 } }
    ])

    print(f'Info for {Fore.GREEN}{movie["primaryTitle"]}{Fore.RESET}')
    print('=' * (len(movie['primaryTitle']) + 9))

    print(f'Rating: {showRating(float(rating["averageRating"]))}')
    print(f'Votes: {rating["numVotes"]}')

    print ('=' * (len(movie['primaryTitle']) + 9))
    print(f'{Fore.GREEN}Cast{Fore.RESET}')

    for person in cast_agg:
        characters = ', '.join(person['characters'])
        print(f'{person["primaryName"]} as {characters}')

    print ('=' * (len(movie['primaryTitle']) + 9))
    print(f'{Fore.CYAN}Crew{Fore.RESET}')
    for crew in crew_agg:
        print(f'{crew["primaryName"]} as {crew["category"]}')


    choices = ['Search Again', 'Back to Main Menu']
    answers = util.get_valid_inquiry([{
        'type': 'list',
        'name': 'choice',
        'message': 'What would you like to do? (Arrow keys and enter to select)',
        'choices': choices
    }])
    if answers == {}:
        # if the user clicks wit their mouse or smoething
        # we default to search again
        return False
    elif answers['choice'] == 'Search Again':
        return False
    else:
        return True


def showRating(rating: float):
    """
    Displays the rating in a nice way

    Input: 
        rating - the rating to display
    """
    if rating > 7.5:
        return f'{Fore.GREEN}{rating}{Fore.RESET}'
    elif rating > 5.0:
        return f'{Fore.YELLOW}{rating}{Fore.RESET}'
    else:
        return f'{Fore.RED}{rating}{Fore.RESET}'

