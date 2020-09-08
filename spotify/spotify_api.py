import spotipy, subprocess
from spotipy.oauth2 import SpotifyOAuth

from time import sleep
from multiprocessing import Process



class SpotifyPlayer:
    def __init__(self, *args, **kwargs):
        self.scope = "user-read-playback-state,user-modify-playback-state"
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=self.scope, cache_path='CACHE'))
        self.sp.volume = 50
        self.device_id = None 
        self.playlist = None
        self.tracks = None

    @staticmethod
    def run():
        subprocess.call('./run.sh')

    @staticmethod
    def exit():
        subprocess.call('./exit.sh')

    def get_device(self):
        res = self.sp.devices()
        self.device_id = res['devices'][0]['id'] #get the id

        
    def start(self):
        self.sp.start_playback(device_id=self.device_id, uris=self.tracks)


    def get_playlist(self, playlist_id):
        playlist = self.sp.user_playlist(self.sp.me()['id'], playlist_id=playlist_id)
        return playlist

    def get_tracks(self, playlist_id):
        #get all track URIs from a playlist
        # params: playlist_id        
        playlist = self.get_playlist(playlist_id)
        self.tracks = [
                playlist['tracks']['items'][x]['track']['uri'] 
                for x in range(len(playlist['tracks']) - 1)
        ]
 
    def open_spotify(self): # you can use subprocess.Popen instead of the shell files
        #opens spotify on a new process so that code could be run in parallel 
        p1 = Process(target=self.run)
        p1.start()
        sleep(2)

    def volume_up(self):
        if self.sp.volume + 10 < 100:
            self.sp.volume += 10
        else:
            self.sp.volume = 100
    
    def volume_down(self):
        if self.sp.volume - 10 > 0:
            self.sp.volume -= 10
        else:
            self.sp.volume = 0



player = SpotifyPlayer()

player.open_spotify()
player.get_tracks('6QnnCV56shIVTlA11PpsSm')
player.get_device()
player.start()


player.volume_up()
print(player.sp.volume)
sleep(1)
player.volume_up()
print(player.sp.volume)
sleep(1)
player.volume_up()
print(player.sp.volume)

while True:
    decision = input('input something ')
    if decision == 'next':
        player.sp.next_track()
    if decision == 'prev':
        player.sp.previous_track()

