from sys import argv
import os
import shutil
import re
import json

#getting path to folder to sort from console or from arguments
if len(argv)>=2:
    path=argv[1]
else:
    path=input('Input path to folder you wish to sort: ')

#creating dictionaries folder:extention and extention:folder for further use
folders_to_extensions={
'images':   ('JPEG', 'PNG', 'JPG', 'SVG'),
'video':    ('AVI', 'MP4', 'MOV', 'MKV'),
'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
'audio':    ('MP3', 'OGG', 'WAV', 'AMR'),
'archives': ('ZIP', 'GZ', 'TAR')
}
extension_to_folder_dict={}
for key in folders_to_extensions:
    if not os.path.isdir(os.path.join(path,key)):
        os.mkdir(os.path.join(path,key))
    for extension in folders_to_extensions[key]:
        extension_to_folder_dict.update({extension.lower():key})

#main part of the app. path for path of current folder. top_path for path of folder where sorting started(its for recognizing recurency)
def sort(path,top_folder):
    #getting correct path to existing directory
    while True:
        try:
            files_in_directory=os.listdir(path)
        except WindowsError:
            path=input('Input valid path: ')
        else:
            break
    #recognizing, normalizing, moving and renaming files
    for file in files_in_directory:
        file_path=os.path.join(path,file)
        if os.path.isdir(file_path) and file not in ['archives','video','audio','documents','images']:
            empty=sort(file_path,top_folder)
            if empty:
                os.rmdir(file_path)
        elif os.path.isfile(file_path) and file not in ['sorted_files.txt']:
            file=file.rsplit('.',1)
            norm_file=normalize(file[0]),file[1]
            if norm_file[1] in ('zip', 'gz', 'tar'):
                os.mkdir(norm_file[0])
                shutil.unpack_archive(file_path,os.path.join(top_folder,extension_to_folder_dict[norm_file[1]],norm_file[0]))
            elif extension_to_folder_dict.get(norm_file[1]):
                os.rename(file_path,os.path.join(top_folder,extension_to_folder_dict[norm_file[1]],'.'.join(norm_file)))
    #creating file with list of all sorted files
    if path==top_folder:
        sorted_files={}
        for folder_name in folders_to_extensions:
            files_in_folder=[path.rsplit('\\')[-1] for path in os.listdir(os.path.join(top_folder,folder_name))]
            sorted_files.update({folder_name:files_in_folder})
        with open(os.path.join(top_folder,'sorted_files.txt'),'w') as f:
            json.dump(sorted_files,f)
    return not bool(os.listdir(path))

#function normalizing. changes polish letters to english counterparts and changes all symbols other than letters, numbers and _ to _
def normalize(string):
    trans_table=str.maketrans('ĄąĆćĘęŁłŃńÓóŚśŻżŹź','AaCcEeLlNnOoSsZzZz')
    normalized_string = string.translate(trans_table)
    if not normalized_string.isalnum():
        normalized_string=re.sub('\W+',lambda match: '_'*len(match.group(0)),normalized_string)
    return normalized_string

sort(path,path)