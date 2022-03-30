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
from commands.add_movie import add_movie
from commands.search_cast import search_cast


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
            { 'value': 'EX', 'name': 'Exit application' }
        ]
        raw_cmd = util.get_valid_inquiry([{
                'type': 'list',
                'name': 'choice',
                'message': 'Welcome to the main menu! Enter your selection below (arrow keys and enter)',
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
            search_cast(client)
            reset_screen()

        elif command == 'AM':
            print('Adding a new movie...')
            add_movie(client)
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


def main():
    colorama.init()
    client = mongoConnect()
    reset_screen()
    mainMenu(client)
    client.close()


if __name__ == "__main__":
    main()

