from ibm_watson import TextToSpeechV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import os
import random

AUTHENTICATOR = IAMAuthenticator('lVyR5F8qJC-9TnxxqCNluUR7hGjBKuDsMqWUIl4K-ZHX')


class Assistant:
    def __init__(self):
        self.voice = 'en-GB_KateV3Voice'
        self.tts = TextToSpeechV1(authenticator=AUTHENTICATOR)
        self.tts.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/fde40e41-11bb-419a-8ae5-cde3ebd72536')
        self.file_selected = ''

    def change_voice(self,newperson):
        self.voice = "en-US_" + newperson + 'V3Voice'

    def talk(self,string):
        r = random.randint(1, 1000000)
        audio_file = "audio_" + str(r) + ".mp3"
        
        try:
            with open(audio_file, 'wb') as audio:
                res = self.tts.synthesize(string, accept='audio/mp3', voice=self.voice).get_result()
                audio.write(res.content)
            
            playsound('./'+audio_file)
            os.remove('./'+audio_file)
        
        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            os.remove('./'+audio_file)



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

def select_file(assistant):
    arr = os.listdir()
    assistant.talk('which file would you like me to find?')
    file_to_find = input('please input a file name: ')
    for file in arr:
        if file_to_find in file:
            assistant.file_selected = file
            assistant.talk('I found the file ' + file_to_find)
            return 
    assistant.talk("sorry, I couldn't find the file " + file_to_find)

def run():
    assistant = Assistant()
    assistant.talk("how can i help you?")
    print('hello, how can i help you? \n')
    run = True 

    while run:
        text = input()
        
        if "what" in text and "can" in text and "do" in text:
            assistant.talk('I can create a file, delete a file, read or update the content of an existing file for now.')
        elif "your name" in text:
            name_arr = assistant.voice.split('_')
            assistant.talk('my name is ' + name_arr[1][0:name_arr[1].index('V')] + ".")

        elif "old" in text and "are" in text:
            assistant.talk('I am one million years old.')
        elif "weed" in text:
            assistant.talk('yes man, weed is my life.')
        elif "sure" in text:
            assistant.talk('maybe, What do you think?')
        elif "change" in text and "person" in text:
            assistant.talk('please enter the name of the person you want sir.')
            text = input('please choose who you want')
            assistant.voice = assistant.change_voice(text)
            assistant.talk('Hello my name is,' + text)
        elif "lenovo" in text:
            assistant.talk("no, I don't think so, It's shit man")
        elif "exit" in text:
            run = False
        
        elif "find" in text and "file" in text:
            select_file(assistant)
        
        elif "delete" in text:
            delete_file(assistant)
       
        else:
            assistant.talk(text)


if __name__ == "__main__":
    run()