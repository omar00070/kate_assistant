import os, random, imaplib, smtplib
from ibm_watson import TextToSpeechV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import handle_os as handle
from read_gmail import read_email_from_gmail
from send_gmail import send_email_from_gmail
from spotify.spotify_api import SpotifyPlayer
from multiprocessing import Process
from gtts import gTTS


API_URL = os.environ.get('WATSON_URL')
API_KEY = os.environ.get('WATSON_API')
AUTHENTICATOR = IAMAuthenticator(API_KEY)
FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_PWD = os.environ.get('FROM_PWD')
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587


class Assistant:
    def __init__(self, host="watson"):
        self.host = host
        self.voice = 'en-GB_KateV3Voice'
        self.tts = TextToSpeechV1(authenticator=AUTHENTICATOR)
        self.tts.set_service_url(API_URL)
        self.file_selected = ''
        self.mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        self.mail.login(FROM_EMAIL, FROM_PWD)
        self.mail.select('inbox')
        self.session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.player = SpotifyPlayer()

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

        if self.host == 'watson':        
            try:
                with open(audio_file, 'wb') as audio:
                    res = self.tts.synthesize(string, accept='audio/mp3', voice=self.voice).get_result()
                    audio.write(res.content)
                
                playsound('./'+audio_file)
                os.remove('./'+audio_file)
            
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)
                os.remove('./'+audio_file)
        
        elif self.host == 'google':
            if string == '':
                string = 'nothing'
            tts = gTTS(string)
            tts.save(audio_file)
            playsound('./'+audio_file)
            os.remove('./'+audio_file)


    def play_spotify(self):
        #opens the spotify player and gets tracks to play
        #and starts playing
        self.player.open_spotify()
        self.player.get_tracks('6QnnCV56shIVTlA11PpsSm')
        self.player.get_device()
        self.player.start()
        return True

    def control_spotify(self):
        #function to control spotify
        #you can control spotify with inputs at the moment
        #param: none, TODO: params are going to be tracks and playlists

        control = input('control spotify')
        if 'next' in control:
            self.player.sp.next_track()
        if 'previous' in control:
            self.player.sp.previous_track()
        if 'pause' in control:
            self.player.sp.pause_playback()
        if 'play' in control:
            self.player.sp.start_playback()
        if 'up' in control:
            self.player.volume_up()
        if 'down' in control:
            self.player.volume_down()
        if 'exit' in control:
            SpotifyPlayer.exit()
            return False
        return True

def run():
    assistant = Assistant('google')
    assistant.talk("how can i help you?")
    print('hello, how can i help you? \n')
    running = True 
    playing = False

    while running:
        if playing:
            playing = assistant.control_spotify()
        text = input('write something: ')
        
        if "what" in text and "can" in text and "do" in text:
            assistant.talk('I can create a file, delete a file, read or update the content of an existing file for now.')
        
        elif "your name" in text:
            name_arr = assistant.voice.split('_')
            assistant.talk('my name is, ' + name_arr[1][0:name_arr[1].index('V')] + ".")

        elif "old" in text and "are" in text:
            assistant.talk('I am one million years old.')
            
        elif "spotify" in text:
            assistant.talk('playing spotify')
            playing = assistant.play_spotify()
            
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





# player.volume_up()
# print(player.sp.volume)
# sleep(1)
# player.volume_up()
# print(player.sp.volume)
# sleep(1)
# player.volume_up()
# print(player.sp.volume)

# while True:
#     decision = input('input something ')
#     if decision == 'next':
#         player.sp.next_track()
#     if decision == 'prev':
#         player.sp.previous_track()


if __name__ == "__main__":
    run()