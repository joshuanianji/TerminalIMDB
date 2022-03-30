import util
from colorama import Fore
from InquirerPy import inquirer
from pymongo import MongoClient
from pymongo.collection import Collection


def add_movie(client: MongoClient):
    wantToSearch = True
    while wantToSearch:
        try:
            wantToSearch = add_movie_individual(client)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue

    print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')


def add_movie_individual(client: MongoClient):
    '''
    Add a movie: 
        > The user should be able to add a row to title_basics by providing a unique id, a title, a start year, a running time and a list of genres. 
        > Both the primary title and the original title will be set to the provided title, the title type is set to movie 
            and isAdult and endYear are set to Null (denoted as \\N).

    Input: client - pymongo client to be processed

    Return: true if the user wants to continue adding movies, false if they want to exit to the main menu
    '''
    db = client['291db']
    title_basic_col = db['title_basics']
    print(f'{Fore.CYAN}\nAdd movie home page! At any prompt, type "E" or "EXIT" to go back to the main menu{Fore.RESET}')

    unique_id = prompt_unique_id(title_basic_col)
    if unique_id is None: return False

    title = util.prompt_nonempty_string('Movie Title:')
    if title is None: return False

    startYear = util.prompt_int_or_e('Start year:')
    if startYear is None: return False

    runTime = util.prompt_int_or_e('Running time (int):')
    if runTime is None: return False

    genreList = util.prompt_nonempty_string('Genres (comma separated):').split(',')
    if genreList is None: return False

    jsonQuery = {
        'tconst': unique_id,
        'primaryTitle': title,
        'originalTitle': title,
        'startYear': startYear,
        'runtimeMinutes': runTime,
        'titleType': 'movie',
        'genres': genreList,
        'isAdult': None,
        'endYear': None
    }
    title_basic_col.insert_one(jsonQuery)
    title_basic_col.create_index('tconst')

    print(f'{Fore.GREEN}Movie {title} added successfully!{Fore.RESET}')

    choices = ['Add another', 'Back to Main Menu']
    answers = util.get_valid_inquiry([{
        'type': 'list',
        'name': 'choice',
        'message': 'What would you like to do now? (Arrow keys and enter to select)',
        'choices': choices
    }])

    return answers['choice'] == 'Add another'


def prompt_unique_id(title_basic_col: Collection):
    '''
    Prompts the user for a unique id.

    Returns None is the user wants to exit back to the main menu
    '''
    while True: 
        unique_id = inquirer.text(message='Unique movie ID').execute()
        if unique_id.upper() == 'EXIT' or unique_id.upper() == 'E':
            print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
            return None

        res = title_basic_col.find_one({'tconst': unique_id})
        
        if res:
            print(f'{Fore.RED}Movie ID {unique_id} not unique, please choose another!...{Fore.RESET}')
            continue
        else:
            return unique_id
