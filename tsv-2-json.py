from colorama import Fore, Back, Style, init
from tqdm import tqdm
import json
import time
import sys
import os

def starting_text():
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
    rainbow = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

    for (text, color) in zip(texts, rainbow):
        if (color == Fore.WHITE):
            print(Style.DIM + color + text + Fore.RESET + Style.RESET_ALL)
        else:
            print(color + text + Fore.RESET)
    
    print('\n\n' + Fore.WHITE + 'Welcome to TSV2JSON! Converting TSV to JSON...' + Fore.RESET)


def tsv2json(input_file,output_file):

    print('\n' + 'Converting ' + Fore.CYAN + input_file + Fore.RESET + ' to ' + Fore.GREEN + output_file + Fore.RESET +'...' )

    arr = []
    file = open(input_file, 'r')
    a = file.readline()

    # The first line consist of headings of the record 
    # so we will store it in an array and move to 
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]

    # progress bar
    # pbar = tqdm(total=len(file.readlines()))

    for line in tqdm(file):
        d = {}
        for t, f in zip(titles, line.split('\t')):

            # Convert each row into dictionary with keys as titles
            NestTitles = ['primaryProfession', 'knownForTitles', 'genres', 'characters']
            if t in NestTitles:
                if t == 'primaryProfession' or t == 'knownForTitles' or t == 'genres':
                    #temp = f.strip().split('\n')[0].split(',')
                    temp = f.strip(' \n').split(',')
                if t == 'characters':
                   # temp = f.strip().split('\n')[0].strip(' "[]').split(',')
                    temp = f.strip('\n "[]').split(',')
                if temp[0] == '\\N':
                    temp = None
                d[t] = temp

            else:
                temp = f.strip()
                if temp == '\\N':
                    temp = None
                d[t] = temp

        # we will use strip to remove '\n'.
        arr.append(d)

    # we will append all the individual dictionaires into list 
    # and dump into file.

    print('\n' + 'Writing data to ' + Fore.GREEN + output_file + Fore.RESET + '...')
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))
    print('\n' + Fore.GREEN + 'Done!' + Fore.RESET)

def main():
    init()
    starting_text()
    #saving the names of the files to be converted in list 
    fileNames = ['name.basics', 'title.basics', 'title.ratings', 'title.principals']
    for name in fileNames:
        input_filename = name + '.tsv'
        output_filename = name + '.json'
        tsv2json(input_filename,output_filename)



#calling the function

if __name__ == '__main__':
    main()