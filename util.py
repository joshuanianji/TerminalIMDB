import time
from typing import Union
from InquirerPy import prompt
from InquirerPy import inquirer
from colorama import Fore, Style
from InquirerPy.validator import EmptyInputValidator
from prompt_toolkit.validation import Validator, ValidationError


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


# InquirePy


def prompt_nonempty_string(msg: str) -> Union[str, None]:
    '''
    Prompts the user for a nonempty string

    Returns None is the user wants to exit back to the main menu
    '''
    while True: 
        nonempty_str = inquirer.text(
            message=msg, 
            validate=EmptyInputValidator()
        ).execute()

        if nonempty_str.upper() == 'EXIT' or nonempty_str.upper() == 'E':
            print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
            return None

        return nonempty_str


def prompt_int_or_e(msg: str):
    '''
    Prompts the user for a nonempty string

    Returns None is the user wants to exit back to the main menu
    '''
    while True: 
        nonempty_str = inquirer.text(
            message=msg, 
            validate=IntOrExitValidator()
        ).execute()

        if nonempty_str.upper() == 'EXIT' or nonempty_str.upper() == 'E':
            print(f'{Fore.CYAN}Returning to main menu...{Fore.RESET}')
            return None

        return int(nonempty_str)


class IntOrExitValidator(Validator):
    def validate(self, document) -> None:
        """Check if user input is a valid number.

        See Also:
            https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html?highlight=validator#input-validation
        """
        text = document.text
        if text.upper() == 'EXIT' or text.upper() == 'E':
            return
        elif text.isdigit():
            return
        else:
            raise ValidationError(
                message='Please enter a valid integer or "EXIT"/"E" to return to Main Menu',
                cursor_position=len(text)
            )
