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
    
    time.sleep(0.075) 
    print('\n\n' + Fore.WHITE + 'Welcome to TSV2JSON!' + Fore.RESET)

    time.sleep(0.075) 
    print('\n' + 'Made by ' + Fore.CYAN + 'Vedant' + Fore.RESET + ', ' + Fore.GREEN + 'Kailash' + Fore.RESET + ' and ' + Fore.BLUE + 'Joshua' + Fore.RESET + '.')

    # Boot screen

    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0

    # used to keep the track of
    # the duration of animation
    counttime = 0        

    # pointer for travelling the loading string
    i = 0

    print('\n')
    while (counttime <= 15):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.05) 
        print ("\033[A                             \033[A")
        print('Booting up...' + animation[anicount])
        anicount = (anicount + 1) % 4
        counttime = counttime + 1



def tsv2json(input_file,output_file):

    print('\n' + 'Converting ' + Fore.CYAN + input_file + Fore.RESET + ' to ' + Fore.GREEN + output_file + Fore.RESET +'...' )

    arr = []
    file = open(input_file, 'r', encoding='utf8')
    a = file.readline()

    # The first line consist of headings of the record 
    # so we will store it in an array and move to 
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]

    # find length of file
    pos = file.tell()
    file_length = len(file.readlines())
    file.seek(pos)

    pbar = tqdm(total=file_length)

    for line in file:
        d = {}
        for t, f in zip(titles, line.split('\t')):

           

            NestTitles = ['primaryProfession', 'knownForTitles', 'genres', 'characters']
            #integer titles
            if t == "numVotes" or t == "ordering" or t == "birthYear" or t == "deathYear" or t == "startYear" or t == "endYear" or t == 'runtimeMinutes':
                temp = f.strip()
                if temp != '\\N':
                    d[t] = int(temp)
                else:
                    d[t] = None
            elif t == 'averageRating':
                temp = f.strip()
                if temp != '\\N':
                    d[t] = float(temp)
                else:
                    d[t] = None
                #d[t] = float(f.strip())
            elif t in NestTitles:
             # Convert each row into dictionary with keys as titles
                if t == 'primaryProfession' or t == 'knownForTitles' or t == 'genres':
                    #temp = f.strip().split('\n')[0].split(',')
                    temp = f.strip(' \n').split(',')
                if t == 'characters':
                   # temp = f.strip().split('\n')[0].strip(' "[]').split(',')
                    temp = f.strip('\n "[]').split('","')
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
        pbar.update()
    pbar.close()

    # we will append all the individual dictionaires into list 
    # and dump into file.

    print('Writing data to ' + Fore.GREEN + output_file + Fore.RESET + '...')
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))
    print(Fore.GREEN + 'Done!' + Fore.RESET)

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