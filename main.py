from pymongo import MongoClient
from getpass import getpass
import os
from colorama import Fore, Back, Style
import colorama
import util
from pymongo.errors import ServerSelectionTimeoutError


def mongoConnect():
    """
    Takes user input for a port number and connects to the mongoDB database
    Returns the resulting client 
    """
    while True:
        try:
            port = int(input('Enter a port: '))
            if port:
                client = MongoClient(host = 'localhost', port = port, serverSelectionTimeoutMS = 15)
                client.server_info()
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


commands = {
    'ST': {
        'name': 'Search for a title',
        'color': Fore.RED
    },
    'SG': {
        'name': 'Search for a genre',
        'color': Fore.YELLOW
    },
    'SC': {
        'name': 'Search for a cast/crew member',
        'color': Fore.GREEN
    },
    'AM': {
        'name': 'Add a movie',
        'color': Fore.BLUE
    },
    'AC': {
        'name': 'Add a new cast/crew member',
        'color': Fore.CYAN
    },
    'EX': {
        'name': 'Close the connection',
        'color': Fore.MAGENTA
    }
}

def mainMenu(client):
    '''
    Main user interface for the program
    Handles user inputs and processes the database client appropriately

    Input: client - pymongo client to be processed
    '''

    # Generate help message
    helpMessage = ''
    for cmd, data in commands.items():
        helpMessage += f"{data['color']} {cmd} - {data['name']}{Fore.RESET}\n"
    helpMessage = helpMessage.strip()
    help = False

    while True:
        if not help:
            reset_screen('Welcome to the main menu! Enter your selection below!', show_names = True)
        print(helpMessage)
        help = False

        # Get user command input
        while True:
            command = input("> ").upper()
            if command != "H" and command not in commands:
                print("Invalid command. Press 'H' for help.")
            else:
                break


        # Handle user input
        if command == 'H':
            help = True

        elif command == 'ST':
            reset_screen()
            print('Searching for a title...')
            searchTitle(client)
            # Remove after implementing exit commands in searchTitle()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'SG':
            reset_screen()
            print('Searching for a genre...')
            searchGenre(client)
            # Remove after implementing exit commands in searchGenre()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'SC':
            reset_screen()
            print('Searching for a cast/crew member...')
            searchCast(client)
            # Remove after implementing exit commands in searchCast()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'AM':
            reset_screen()
            print('Adding a new movie...')
            addMovie(client)
            # Remove after implementing exit commands in addMovie()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        elif command == 'AC':
            reset_screen()
            print('Adding a new cast/crew member')
            addCast(client)
            # Remove after implementing exit commands in addCast()
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        else:
            print('Exiting...')
            return




###TODO: Fill out all functions below

def reset_screen(welcome_text = None, show_names = False):
    os.system('cls' if os.name == 'nt' else 'clear')
    util.starting_text(welcome_text, show_names)


def searchTitle(client):
    """
    Search for titles: 
        > The user should be able to provide one or more keywords, and the system should retrieve all titles that match all those keywords (AND semantics). 
        > A keyword matches if it appears in the primaryTitle field (the matches should be case-insensitive). 
        > A keyword also matches if it has the same value as the year field. 
        > For each matching title, display all the fields in title_basics. 
        > The user should be able to select a title to see the rating, the number of votes, the names of cast/crew members and their characters (if any).
    
    Input: client - pymongo client to be processed
    """
    #TODO
    pass



def searchGenre(client):
    """
    Search for genres: 
        > The user should be able to provide a genre and a minimum vote count and see all titles under the provided genre 
            (again case-insensitive match) that have the given number of votes or more. 
        > The result should be sorted based on the average rating with the highest rating on top.

    Input: client - pymongo client to be processed
    """
    #TODO
    pass



def searchCast(client):
    """
    Search for cast/crew members:
        > The user should be able to provide a cast/crew member name and see all professions of the member and for each title the member had 
            a job, the primary title, the job and character (if any). 
        > Matching of the member name should be case-insensitive.

    Input: client - pymongo client to be processed
    """
    #TODO
    pass



def addMovie(client):
    """
    Add a movie: 
        > The user should be able to add a row to title_basics by providing a unique id, a title, a start year, a running time and a list of genres. 
        > Both the primary title and the original title will be set to the provided title, the title type is set to movie 
            and isAdult and endYear are set to Null (denoted as \\N).

    Input: client - pymongo client to be processed
    """
    #TODO
    pass



def addCast(client):
    """
    Add a cast/crew member: 
        > The user should be able to add a row to title_principals by providing a cast/crew member id, a title id, and a category. 
        > The provided title and person ids should exist in name_basics and title_basics respectively (otherwise, proper messages should be given), 
            the ordering should be set to the largest ordering listed for the title plus one (or 1 if the title is not listed in title_principals) 
            and any other field that is not provided (including job and characters) set to Null.

    Input: client - pymongo client to be processed
    """
    #TODO
    pass



















def main():
    colorama.init()
    client = mongoConnect()
    mainMenu(client)
    client.close()



if __name__ == "__main__":
    main()

