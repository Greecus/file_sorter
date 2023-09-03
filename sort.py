from sys import argv
from os.path import isfile, isdir 
from os import listdir
import shutil
import re



if len(argv)>=2:
    path=argv[1]
else:
    path=input('Input path to folder you wish to sort: ')

def sort(path):
    while True:    
        try:
            files_in_directory=listdir(path)
        except WindowsError:
            path=input('Input valid path: ')
        else:
            break
    for file in files_in_directory:
        print(file)
        if isdir(f'{path}/{file}'):
            sort(f'{path}/{file}')
        else:
            name_and_extension=re.match('(\S+).(\S+)',file)
            print(name_and_extension.groups())

def normalize(string):
    pass

sort(path)