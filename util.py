from colorama import Fore, Back, Style
import time

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

    
