import os
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ProgressBar import ProgressBar

class SpotifyGateway():
  
  def __init__(self, username: str, playlist: str):
    self.token = spotipy.util.prompt_for_user_token(username=username,
                                                 scope="user-library-read,playlist-modify-private,playlist-modify-public",
                                                 client_id=os.environ['SPOTIPY_CLIENT_ID'],
                                                 client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                                                 redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])
    self.sp = spotipy.Spotify(auth=self.token)
    self.playlist = playlist
    self.username = username

  def validateInformation(self) -> bool:
    """Attempts to retrieve information from given playlist to ensure information has been entered correctly."""
    try:
      playlist = self.sp.playlist(self.playlist)
      return playlist['owner']['id'] == self.username
    except:
      return False
    
  def getPlaylistSongs(self, playlist_id: str):
    try:
      results = self.sp.user_playlist_tracks(self.username, playlist_id)
      tracks = results['items']
      while results['next']:
        results = self.sp.next(results)
        tracks.extend(results['items'])
      return tracks
    except:
      return None
  
  def addToSpotifyTimed(self,songs:dict,time:float):
    """Takes in a dictionary with the URIs as keys and adds each song to the playlist one at a time"""
    pBar = ProgressBar(len(songs),"Adding songs to playlist")
    for uri in songs:
      pBar.updateProgress()
      self.sp.user_playlist_add_tracks(self.username, self.playlist, [uri])
      sleep(time)
    pBar.finish()

  def addToSpotifyBatch(self,songs:dict):
    """Takes in a dictionary with the URIs as keys and adds each song to the playlist in batches"""
    length = len(songs)
    pBar = ProgressBar(length,"Adding songs to playlist")
    URIs = list(songs)
    begIndex = 0
    #Add songs in bactches of 100
    while(length - begIndex >= 100):
      pBar.updateProgress(100)
      self.sp.user_playlist_add_tracks(self.username, self.playlist, URIs[begIndex:begIndex+100])
      begIndex += 100
    #Add remaining songs
    pBar.updateProgress(length-begIndex)
    self.sp.user_playlist_add_tracks(self.username, self.playlist, URIs[begIndex:])
    pBar.finish()



if __name__ == "__main__":
  import DataParse as DataParse
  #Delete from final
  os.environ['SPOTIPY_CLIENT_ID'] = '2bad936b5dec4ee286a3bed50cbb9a57'
  os.environ['SPOTIPY_CLIENT_SECRET'] = '56f4163387904965b66bf8130908e4fb'
  os.environ['SPOTIPY_REDIRECT_URI'] = 'https://127.0.0.1'
  '''
  temp = DataParse.validatedFile("sophomoreResults.json")
  test = {}
  for i in temp:
    if('sp' in i):
      test[i] = temp[i]
  for i in test:
    print(i, test[i])
    break
  '''
  test = {'69G9nIj6Pb1HfqFXa9DGFs':20}
  sp = SpotifyGateway('kothenbeutel','0DAaXxZpR5S0AszP2ThL6A')#'4ciSROGT0MXGOHO0QyyQZG')#'0GVSAKCLow1SlOZPq325c7')
  sp.addToSpotifyTimed(test,0.01)
  #sp.addToSpotifyBatch(test)
  #print(sp.validateInformation())
  #test = sp.getPlaylistSongs()
  #print(len(test))
  #print(type(test))
  #print(test[0])
  #print()
  #print(test[0]['track'].keys())
  #print(test[0]['track']['uri'])
  #print(test[0]['track']['artists'][0]['name'])
  #print(test[0]['track']['album']['name'])
  #print(test[0]['track']['name'])
  #print(sp.sp.user_playlist_tracks(None,'4ciSROGT0MXGOHO0QyyQZG'))

  #sp = SpotifyGateway(None, None)
  #print(sp.sp.user_playlist_tracks(None, 'notRealPlaylist'))

  """
  "spotify:track:1MsU7LDRTqvMaKbptPp72z": {
        "timestamp": "2024-02-17 00:02:01",
        "title": "For The Wicked",
        "artist": "Friday Pilots Club",
        "album": "For The Wicked",
        "count": 2
    },
  """

