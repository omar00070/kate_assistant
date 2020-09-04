'''
    handle the operating system, delete, select create and read files
'''
import os

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
