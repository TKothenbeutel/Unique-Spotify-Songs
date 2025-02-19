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
  import DataParse
  #Delete from final
  os.environ['SPOTIPY_CLIENT_ID'] = '***REMOVED***'
  os.environ['SPOTIPY_CLIENT_SECRET'] = '***REMOVED***'
  os.environ['SPOTIPY_REDIRECT_URI'] = '***REMOVED***'
  temp = DataParse.validatedFile("sophomoreResults.json")
  test = {}
  for i in temp:
    if('sp' in i):
      test[i] = temp[i]
  for i in test:
    print(i, test[i])
    break
  sp = SpotifyGateway('kothenbeutel','4ciSROGT0MXGOHO0QyyQZG')#'0GVSAKCLow1SlOZPq325c7')
  #sp.addToSpotifyTimed(test,0.01)
  #sp.addToSpotifyBatch(test)
  print(sp.validateInformation())

