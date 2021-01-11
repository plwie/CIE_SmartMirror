
import sys
import os
#Start spotify
os.startfile('C:\\Users\\Pup\\AppData\\Roaming\\Spotify\\Spotify.exe')
cid = '286c01e05fb744bbb32719815ad97c32'
secret = 'b290d9c3fbbb458996794462cc1ffadb'
redirURI='http://google.com/' 

from tekore import Spotify, util, scope

cred = (cid, secret, redirURI )
token = util.prompt_for_user_token(*cred, scope=scope.every)

spotify = Spotify(token)

tracks = spotify.current_user_top_tracks(limit=10)
for track in tracks.items:
    print(track.name)
spotify.playback_start_tracks([t.id for t in tracks.items])

