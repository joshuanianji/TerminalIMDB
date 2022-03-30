from typing import List
from colorama import Fore
import util
from pymongo.mongo_client import MongoClient
from tabulate import tabulate

def search_title(client: MongoClient):
    '''
    Searches titles until the user exits.
    '''
    while True:
        try:
            user_exit = search_title_individual(client)
            if user_exit:
                return
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue

def search_title_individual(client: MongoClient) -> bool:
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
    
    Returns:
        user_exit: true if the user wants to exit back to main page, false if the user wants to continue searching
    """
    print(f'{Fore.CYAN}Please enter in your keywords (space separated), or "EXIT/E" to exit{Fore.RESET}')
    keywords = util.get_valid_input('> ', lambda cmd: cmd.strip() != '', 'Please do not enter an empty string!', True).split()
    
    if keywords[0] == 'EXIT' or keywords[0] == 'E':
        print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
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
        title_count = collection.count_documents(query)

        if title_count == 0:
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
            print(f'Found {Fore.GREEN}{title_count}{Fore.RESET} titles. Select one for more info, or go to bottom for other options. \n')
            start_index = 0
            while True:
                titles = list(collection.find(query).limit(50).skip(start_index)) # turn the cursor into a concrete list.

                headers, choices = get_movies_display_list(titles)

                # Miscellaneous other choices
                other_choices = ['Search Again', 'Back to Main Menu']

                if len(titles) >= 50:
                    print(f'{Fore.YELLOW}There may be more titles below.\n{Fore.RESET}')
                    other_choices.append('See More Titles')

                print(f'{Fore.CYAN}{headers}{Fore.RESET}')
                answers = util.get_valid_inquiry([{
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Arrow keys and enter to select',
                    'choices': other_choices + choices
                }])
                if answers['choice'] == 'Search Again':
                    return False
                elif answers['choice'] == 'Back to Main Menu':
                    return True
                elif answers['choice'] == 'See More Titles':
                    start_index += 50
                    continue
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

    tabulates = []
    ids = []
    for title in titles:
        tconst = title['tconst']
        primary_title = title['primaryTitle']
        original_title = title['originalTitle']
        title_type = title['titleType']
        isAdult = title['isAdult']
        start_year = title['startYear']
        end_year = title['endYear']
        runtime_minutes = title['runtimeMinutes']
        genres = ', '.join(title['genres'])
        data = [tconst, primary_title, original_title, title_type, isAdult, start_year, end_year, runtime_minutes, genres]
        tabulates.append(data)
        ids.append(tconst)


    tabulated = tabulate(tabulates, headers=['tconst', 'Primary Title', 'OG Title', 'Type', 'Adult', 'Start Year', 'End Year', 'Runtime', 'Genres']).split('\n')
    headers = '  ' + tabulated[0]
    
    tabulate_str = tabulated[2:] # now, every element is equally spaced. 
    display_list = []

    for elem, id in zip(tabulate_str, ids):
        display_list.append({
            'name': elem,
            'value': id
        })

    return headers, display_list


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
    if answers['choice'] == 'Search Again':
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

