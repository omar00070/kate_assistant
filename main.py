import os, random, imaplib, smtplib
from ibm_watson import TextToSpeechV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import handle_os as handle
from read_gmail import read_email_from_gmail
from send_gmail import send_email_from_gmail



API_URL = os.environ.get('WATSON_URL')
API_KEY = os.environ.get('WATSON_API')
AUTHENTICATOR = IAMAuthenticator(API_KEY)
FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_PWD = os.environ.get('FROM_PWD')
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587


class Assistant:
    def __init__(self):
        self.voice = 'en-GB_KateV3Voice'
        self.tts = TextToSpeechV1(authenticator=AUTHENTICATOR)
        self.tts.set_service_url(API_URL)
        self.file_selected = ''
        self.mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        self.mail.login(FROM_EMAIL, FROM_PWD)
        self.mail.select('inbox')
        self.session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    def change_voice(self):
        '''
            function to change the voice of the assistant
        '''
        self.talk('please enter the name of the person you wants.')
        text = input('please choose who you want (Allison/Henry)? ')
        self.voice = "en-US_" + text + 'V3Voice'
        self.talk('Hello, my name is,' + text)

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


def run():
    assistant = Assistant()
    assistant.talk("how can i help you?")
    print('hello, how can i help you? \n')
    running = True 

    while running:
        text = input()
        
        if "what" in text and "can" in text and "do" in text:
            assistant.talk('I can create a file, delete a file, read or update the content of an existing file for now.')
        
        elif "your name" in text:
            name_arr = assistant.voice.split('_')
            assistant.talk('my name is, ' + name_arr[1][0:name_arr[1].index('V')] + ".")

        elif "old" in text and "are" in text:
            assistant.talk('I am one million years old.')
        
        elif "weed" in text:
            assistant.talk('yes man, weed is my life.')
        
        elif "sure" in text:
            assistant.talk('maybe, What do you think?')
        
        elif "change" in text and "voice" in text:
            assistant.change_voice()
            
        elif "exit" in text:
            running = False
        
        elif "find" in text and "file" in text:
            assistant.talk('which file would you like me to find?')
            handle.select_file(assistant)
        
        elif "delete" in text:
            handle.delete_file(assistant)
        
        elif "create" in text:
            handle.create_file(assistant)
        
        elif "read" in text and 'file' in text:
            handle.read_file(assistant)
        
        elif "delete" in text:
            handle.delete_file(assistant)

        elif "thank" in text:
            assistant.talk('you are welcome')

        elif "read" in text and 'email' in text:
            read_email_from_gmail(assistant)
        elif "send" in text and 'email' in text:
            send_email_from_gmail(assistant)
        else:
            assistant.talk(text)


if __name__ == "__main__":
    run()