import util
from pprint import pprint
from colorama import Fore
from InquirerPy import inquirer
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient


def add_cast_crew(client: MongoClient):
    '''
    Searches titles until the user exits.
    '''
    wantToAdd = True
    while wantToAdd:
        try:
            wantToAdd = add_cast_crew_individual(client)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue

    util.text_with_loading(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}', 1)
    return

def add_cast_crew_individual(client: MongoClient):
    '''
    Runs an individual run of adding cast/crew members
    
    Returns:
        True if the user wants to exit back to the main screen, false otherwise.
    '''
    db = client['291db']
    title = db['title_basics']
    name = db['name_basics']
    principals = db['title_principals']

    print(f'{Fore.CYAN}\nAdding cast/crew member. At any time, enter "EXIT" or "E" to go back to main menu{Fore.RESET}')
    
    member_id = get_member_id(name) # nm0000009
    if member_id is None:
        return False
    
    title_id = get_title_id(title) # tt0910935
    if title_id is None:
        return False

    category = util.prompt_nonempty_string(msg='Enter the category:')
    if category is None:
        return False
    
    # Set ordering to the largest ordering listed for the title plus one
    prinFind = principals.find_one({'tconst': title_id})
    if prinFind:
        order = list(principals.find({'tconst': title_id}).sort('ordering', -1).limit(1))[0]['ordering'] + 1
    else:
        order  = 1
    


    obj = {
        'tconst': title_id,
        'nconst': member_id,
        'category': category,
        'ordering': order,
        'job': None,
        'characters': None
    }
    print('\nAdding cast/crew member:')
    pprint(obj)
    print('\n')

    proceed = inquirer.confirm(message='Confirm add cast/crew member?', default=True).execute()
    if proceed:
        principals.insert_one(obj)
        print(f'{Fore.GREEN}Successfully added cast/crew member!{Fore.RESET}')
    else:
        print(f'{Fore.YELLOW}Scrapping crew member...{Fore.RESET}')
        return False

    choices = ['Add another', 'Back to Main Menu']
    answers = util.get_valid_inquiry([{
        'type': 'list',
        'name': 'choice',
        'message': 'What would you like to do now? (Arrow keys and enter to select)',
        'choices': choices
    }])
    return answers['choice'] == 'Add another'


def get_member_id(name: Collection):
    '''
    Prompts the user for a member_id
    
    Returns none if the user wants to exit to the main menu
    '''
    while True: # nm0000009
        member_id = inquirer.text(message='Enter the member id:').execute()
        if member_id.upper() == 'EXIT' or member_id.upper() == 'E':
            return None

        # check to see if the member_id is in the database
        if name.count_documents({'nconst': member_id}) == 0:
            print(f'{Fore.RED}Member id not found in database! Please retry...{Fore.RESET}')
            continue
        else:
            member = list(name.find({'nconst': member_id}).limit(1))[0]
            print(f'Selected: {Fore.GREEN}{member["primaryName"]}{Fore.RESET}')
            return member_id 


def get_title_id(title: Collection):
    '''
    Prompts the user for a member_id
    
    Returns none if the user wants to exit to the main menu
    '''
    while True: # tt0910935
        title_id = inquirer.text(message='Enter the title id:').execute()
        if title_id.upper() == 'EXIT' or title_id.upper() == 'E':
            return None
        
        # check to see if the title_id is in the database
        if title.count_documents({'tconst': title_id}) == 0:
            print(f'{Fore.RED}Title id not found in database! Please retry...{Fore.RESET}')
            continue
        else:
            movie = list(title.find({'tconst': title_id}).limit(1))[0]
            print(f'Selected: {Fore.GREEN}{movie["primaryTitle"]}{Fore.RESET}')
            return title_id
