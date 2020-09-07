'''
    handle the operating system, delete, select create and read files
'''
import os, getpass, shutil, glob

USERNAME = getpass.getuser() #get the user 
DESKTOP_PATH = f'/home/{USERNAME}/Desktop'
DOWNLOADs_PATH = f'/home/{USERNAME}/Downloads'
DOCUMENTS_PATH = f'/home/{USERNAME}/Documents'
IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.png']
COMPRESSED_EXTENSIONS = ['.zip', '.tar']
DOCUMENTS_EXTENSIONS = ['.pdf', '.txt', '.odp']


def delete_file(assistant):

    if assistant.file_selected:
        assistant.talk('are you sure you want to delete the file ' + assistant.file_selected + '?')
        decision = input('yes/no? ')

        if decision == "yes":
            os.remove("./" + assistant.file_selected)
            assistant.talk('the file (' + assistant.file_selected.split('.')[0] + ") has been removed")
            assistant.file_selected = ''
        else:
            assistant.talk('alright, what would you like me to do?')
    else:
        assistant.talk('there is no file selected yet, please select a file first.')
        select_file(assistant)
        delete_file(assistant)

def select_file(assistant):
    arr = os.listdir()
    file_to_find = input('please input a file name: ')
    
    for file in arr:
        if file_to_find in file:
            assistant.file_selected = file
            assistant.talk('I found the file ' + file_to_find)
            return 
    
    assistant.talk("sorry, I couldn't find the file " + file_to_find + ", would you like me to find another file?")
    decision = input('yes/no? ')
    if decision == 'yes':
        select_file(assistant)
    
def create_file(assistant):
    assistant.talk('what would you like to call the file?')
    file_name = input('Enter a file name: ')
    if file_name:
        with open(file_name, 'wb') as file:
            assistant.talk('what would you like to add to the file?')
            file_content = input('add something to the file (you can leave it empty): ')
            file.write(file_content.encode())
        if file_name in os.listdir():
            assistant.talk(f'your file ({file_name}) has been created.')

def read_file(assistant):
    assistant.talk('which file would you like me to read?')
    select_file(assistant)
    if assistant.file_selected:
        assistant.talk('would you like me to start reading the file?')
        decision = input('yes/no? ')
        if decision == 'yes':
            with open(assistant.file_selected, 'rb') as file:
                content = file.read()
                assistant.talk(content.decode('UTF-8'))

def organize(*args):
    '''
        function to orgaise files
        works only on linux machine for now
        target folders: Desktop, Downloads, Documents
        args: paths to choose where to organize
    '''

    organize_dirs = set()
    
    if 'desktop' in args:
        organize_dirs.add('desktop')
    
    if 'downloads' in args:
        organize_dirs.add('downloads')

    if 'documents' in args:
        organize_dirs.add('documents')

    if 'all' in args:
        organize_dirs.add('desktop')
        organize_dirs.add('downloads')
        organize_dirs.add('documents')

    while organize_dirs:
        dir = organize_dirs.pop()
        if dir == 'downloads':
            organize_downloads()
        elif dir == 'desktop':
            pass
        elif dir == 'documents':
            pass

def check_create_path(path):
    '''
        check if the provided path is a dir, and returns True if it is
        creates a dir if its not a dir, and returns False
        args: path
        returns: isdir(boolean), path(str) 
    '''
    if os.path.exists(path):
        if os.path.isdir(path):
            return True, path
    else:
        os.mkdir(path)
        return False, path

def organize_downloads():
    '''
        function to organize the downloads dir into 4 categories
        Images, Documents, Compressed, Others
    '''
    downloads_cats = ['Images', 'Documents', 'Compressed', 'Others']
    
    # for cat in downloads_cats: # make sure all the cat folders do exist
    #     cat_path = DOWNLOADs_PATH + f'/{cat}'
    #     _, cat_path = check_create_path(cat_path)

    items = os.listdir(DOWNLOADs_PATH) #all items in downlaods
    
    for item in items:
        
        moved = False

        for img_ext in IMAGE_EXTENSIONS:  #handle images
            if item.endswith(img_ext):
                cat_path = DOWNLOADs_PATH + f'/{downloads_cats[0]}'
                check_create_path(cat_path)
                #move to Images
                shutil.move(f'{DOWNLOADs_PATH}/{item}', f'{DOWNLOADs_PATH}/Images/{item}')
                moved = True
        
        for doc_ext in DOCUMENTS_EXTENSIONS:
            if item.endswith(doc_ext):
                cat_path = DOWNLOADs_PATH + f'/{downloads_cats[1]}'
                check_create_path(cat_path)                # move to Documnets
                shutil.move(f'{DOWNLOADs_PATH}/{item}', f'{DOWNLOADs_PATH}/Documents/{item}')
                moved = True

        for compress_ext in COMPRESSED_EXTENSIONS:
            if item.endswith(compress_ext):
                cat_path = DOWNLOADs_PATH + f'/{downloads_cats[2]}'
                check_create_path(cat_path)                #move to Compressed
                shutil.move(f'{DOWNLOADs_PATH}/{item}', f'{DOWNLOADs_PATH}/Compressed/{item}')
                moved = True
        
        if not moved and not os.path.isdir(DOWNLOADs_PATH+f'/{item}'): # if the item is not moved yet
                cat_path = DOWNLOADs_PATH + f'/{downloads_cats[3]}'
                check_create_path(cat_path)            
                shutil.move(f'{DOWNLOADs_PATH}/{item}', f'{DOWNLOADs_PATH}/Others/{item}')
