from typing import Union
from colorama import Fore, Style
import time
from InquirerPy import prompt

RAINBOW = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

def starting_text(welcome_text = None, show_names = False):
    '''
    fancy starting text
    '''
    texts = [
        ' ::::::::   ::::::::    :::        ::::    ::::  :::::::::   ::::::::  ',
        ':+:    :+: :+:    :+: :+:+:        +:+:+: :+:+:+ :+:    :+: :+:    :+: ',
        '      +:+  +:+    +:+   +:+        +:+ +:+:+ +:+ +:+    +:+       +:+  ',
        '    +#+     +#++:++#+   +#+        +#+  +:+  +#+ +#++:++#+      +#+    ',
        '  +#+             +#+   +#+        +#+       +#+ +#+          +#+      ',
        ' #+#       #+#    #+#   #+#        #+#       #+# #+#         #+#       ',
        '##########  ########  #######      ###       ### ###        ########## '
    ]

    for (text, color) in zip(texts, RAINBOW):
        if (color == Fore.WHITE):
            print(Style.DIM + color + text + Fore.RESET + Style.RESET_ALL)
        else:
            print(color + text + Fore.RESET)
    
    if show_names:
        print('\n' + 'Made by ' + Fore.CYAN + 'Vedant' + Fore.RESET + ', ' + Fore.GREEN + 'Kailash' + Fore.RESET + ' and ' + Fore.BLUE + 'Joshua' + Fore.RESET + '.')
    
    if welcome_text is not None:
        time.sleep(0.075) 
        print('\n\n' + Fore.WHITE + welcome_text + Fore.RESET)


def text_with_loading(text, duration=0.75):
    '''
    Displays text with a loading icon.
    Inputs the text to display before the loading icon and the time to wait while displaying the text.

    arguments:
        text: the text to display
        duration: the time to display text
    '''
    # Boot screen
    animation = "|/-\\"
    anicount = 0

    # used to keep the track of
    # the duration of animation
    counttime = 0
    delta = 0.05 # how fast each animation lasts for 

    # pointer for travelling the loading string
    i = 0

    print('\n')
    while (counttime <= duration):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(delta)
        counttime += delta
        print ("\033[A                             \033[A")
        print(text + ' ' + animation[anicount])
        anicount = (anicount + 1) % 4
        counttime = counttime + 1


# Validity stuff

def get_valid_input(prompt, is_valid, error_msg='Please enter a valid input.', upper_case=False) -> str:
    '''
    Takes in a prompt and a predicate, and returns the first valid input from the user

    inputs:
        prompt: the prompt to display to the user
        is_valid: a predicate that takes in the input (that might be converted to upper case) and returns a boolean
        error_msg: the error message to display if the input is invalid
        upper_case: whether or not to convert the input to upper case
    '''
    while True:
        user_input = input(prompt)
        if upper_case:
            user_input = user_input.upper()
        if is_valid(user_input):
            return user_input.strip()
        print(error_msg)

def non_empty_string(prompt) -> str:
    user_input = get_valid_input(prompt, lambda x: len(x) > 0, "Please enter a non empty string")

    return user_input

def get_valid_int_E(prompt) -> int:
    user_input = get_valid_input(prompt, lambda x: x.isdigit() or x.upper() == 'EXIT' or x.upper() == 'E')
    if user_input.upper() == "EXIT" or user_input.upper() == "E":
        return False
    else:
        return int(user_input)


def get_valid_int(prompt) -> int:
    '''
    Get a valid integer from the user
    '''
    user_input = get_valid_input(prompt, lambda x: x.isdigit(), 'Please enter a valid integer.')
    return int(user_input)


def get_in_list(prompt, L) -> str:
    '''
    Gets a valid input from the user that is in the list L
    '''
    return get_valid_input(
        prompt, 
        lambda x: x in list(map(lambda x: x.upper(), L)), 
        'Please enter a valid input (one of: {})'.format(', '.join(L)), 
        True
    )


def get_valid_inquiry(questions):
    '''
    Get a valid inquiry from the user

    If the user presses Ctrl+c, exit the program

    Return:
        answers: dictionary of answers
    '''
    while True:
        try:
            return prompt(questions)
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Escape pressed. Exiting...{Fore.RESET}')
            exit()
        except Exception as e:
            print(f'{Fore.RED}Unknown exception occurred while reading prompt, please retry:{Fore.RESET}\n{e}')
            continue
