from sys import argv
from os.path import isdir 
from os import listdir, rmdir, mkdir
import shutil
import re


if len(argv)>=2:
    path=argv[1]
else:
    path=input('Input path to folder you wish to sort: ')


supported_extensions={
'images':  ('JPEG', 'PNG', 'JPG', 'SVG'),
'video':    ('AVI', 'MP4', 'MOV', 'MKV'),
'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
'audio':    ('MP3', 'OGG', 'WAV', 'AMR'),
'archives': ('ZIP', 'GZ', 'TAR')
}
extension_to_folder_dict={}
for key in supported_extensions:
    if not isdir(f'{path}/{key}'):
        mkdir(path,key)
    for extension in supported_extensions[key]:
        extension_to_folder_dict.update({extension.lower():key})

def sort(path,top_folder):
    while True:
        try:
            files_in_directory=listdir(path)
        except WindowsError:
            path=input('Input valid path: ')
        else:
            break
    for file in files_in_directory:
        file_path=f'{path}/{file}'
        if isdir(file_path) and file not in ['archives','video','audio','documents','images']:
            sort(file_path,top_folder)
            rmdir(file_path)
        else:
            file=file.rsplit('.',1)
            file[0]=normalize(file[0])
            try:
                shutil.move(file_path,top_folder+extension_to_folder_dict[file[1]])
            except:
                pass

    

def normalize(string):
    trans_table=str.maketrans('ĄąĆćĘęŃńÓóŚśŻżŹź','AaCcEeNnOoSsZzZz')
    normalized_string = string.translate(trans_table)
    if not normalized_string.isalnum():
        normalized_string=re.sub('\W+',lambda match: '_'*len(match.group(0)),normalized_string)
    return normalized_string

sort(path,path)