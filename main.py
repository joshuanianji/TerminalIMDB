from pymongo import MongoClient
from getpass import getpass
import os


def mongoConnect():
    """
    Takes user input for a port number and connects to the mongoDB database
    Returns the resulting client 
    """
    while True:
        port = input("Enter a port: ")
        try:
            if port:
                client = MongoClient(f'mongodb://localhost:{port}')
            else:
                client = MongoClient()
        except Exception as err:
            print(f"Invalid port: {err}\nPlease try again!")
        else:
            return client


def printAppHeader():
    #TODO: Print 291 MP2 here in 2-3 lines 
    print("291 MP2")



def mainMenu(client):
    
    

    menuMessage = "Welcome to the main menu! Enter your selection below!"

    # Generate help message
    helpMessage = ""
    commands = ['ST', 'SG', 'SC', 'AM', 'AC', 'EX']
    tasks = ['Search for a title', 'Search for a genre', 'Search for a cast/crew member', 'Add a new movie', 'Add a new cast/crew member', 'Close the connection']
    for (command,task) in zip(commands, tasks):
        helpMessage += f"{command} - {task}\n"
    helpMessage = helpMessage.strip()
    help = False

    while True:
        if not help:
            os.system("cls" if os.name == "nt" else "clear")
            printAppHeader()
            print("Welcome to the main menu! Enter your selection below!")
        print(helpMessage)
        help = False

        # Get user command input
        while True:
            command = input("> ").upper()
            if command != "H" and command not in commands:
                print("Invalid command. Press 'H' for help.")
            else:
                break

        if command == 'H':
            help = True

        elif command == 'ST':
            os.system("cls" if os.name == "nt" else "clear")
            printAppHeader()
            print('Searching for a title...')
            searchTitle(client)
            print("Press Enter to return to the main menu.")
            getpass(prompt="")
            
        elif command == 'SG':
            os.system("cls" if os.name == "nt" else "clear")
            printAppHeader()
            print('Searching for a genre...')
            searchGenre(client)
            print("Press Enter to return to the main menu.")
            getpass(prompt="")
            
        
        elif command == 'SC':
            os.system("cls" if os.name == "nt" else "clear")
            printAppHeader()
            print('Searching for a cast/crew member...')
            searchCast(client)
            print("Press Enter to return to the main menu.")
            getpass(prompt="")
        
        elif command == 'AM':
            os.system("cls" if os.name == "nt" else "clear")
            printAppHeader()
            print('Adding a new movie...')
            addMovie(client)
            print("Press Enter to return to the main menu.")
            getpass(prompt="")
        
        elif command == 'AC':
            os.system("cls" if os.name == "nt" else "clear")
            printAppHeader()
            print('Adding a new cast/crew member')
            addCast(client)
            print("Press Enter to return to the main menu.")
            getpass(prompt="")

        else:
            print('Exiting...')
            return








def searchTitle(client):
    pass



def searchGenre(client):
    pass



def searchCast(client):
    pass



def addMovie(client):
    pass



def addCast(client):
    pass



















def main():
    client = mongoConnect()
    mainMenu(client)



if __name__ == "__main__":
    main()



























































