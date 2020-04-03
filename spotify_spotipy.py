from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util

cid = '286c01e05fb744bbb32719815ad97c32'
secret = 'b290d9c3fbbb458996794462cc1ffadb'
redirURI='http://google.com/' 

util.prompt_for_user_token(username='217othyvsv4xwh6ukz3jd6qli',
                           scope='user-modify-playback-state',
                           client_id=cid,
                           client_secret=secret,
                           redirect_uri=redirURI)

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
available=print(spotify.devices)
spotify.start_playback(device_id=available[0], context_uri='5iZrDgKbyikDJ5sPDMIspv', uris='1Uw2ZFb7B4d3Rz9xv4Rrf4', offset={'position': 0},position_ms=1)




