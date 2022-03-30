from pymongo import MongoClient
from getpass import getpass
import os
from colorama import Fore
import colorama
import util
from pymongo.errors import ServerSelectionTimeoutError
from commands.search_title import search_title
from commands.add_cast_crew import add_cast_crew
from commands.search_genre import search_genre
from commands.search_cast_crew import search_cast_crew



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
        reset_screen()
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
            print('Searching for a title...')
            search_title(client)
            reset_screen()

        elif command == 'SG':
            print('Searching for a genre...')
            search_genre(client)
            reset_screen()

        elif command == 'SC':
            print('Searching for a cast/crew member...')
            search_cast_crew(client)
            reset_screen()

        elif command == 'AM':
            print('Adding a new movie...')
            addMovie(client)
            reset_screen()

        elif command == 'AC':
            print('Adding a new cast/crew member...')
            add_cast_crew(client)
            reset_screen()

        else:
            ##### PRINT MADE BY
            print('Exiting...')
            return



def reset_screen(welcome_text = None, show_names = False):
    os.system('cls' if os.name == 'nt' else 'clear')
    util.starting_text(welcome_text, show_names)
    print('-'*70 + '\n')



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
    jsonQuery = dict()
    jsonQuery ['primaryTitle'] = title
    jsonQuery ['originalTitle'] = title
    jsonQuery ['tconst'] = unId
    jsonQuery ['startYear'] = startYear
    jsonQuery ['runtimeMinutes'] = runTime
    jsonQuery ['genres'] = genreList
    jsonQuery ['titleType'] = 'movie'
    jsonQuery ['isAdult'] = None
    jsonQuery ['endYear'] = None
    #arr.append(jsonQuery)
    title_basic_col.insert_one(jsonQuery)
    print(Fore.GREEN + "Record added!" + Fore.RESET)
    input(Fore.CYAN + "Press Enter to return to the main menu." + Fore.RESET)



def main():
    colorama.init()
    client = mongoConnect()
    reset_screen()
    mainMenu(client)
    client.close()


if __name__ == "__main__":
    main()

