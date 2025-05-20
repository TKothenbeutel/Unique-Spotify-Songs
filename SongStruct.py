from datetime import datetime
from ProgressBar import ProgressBar
from DataParse import validatedFile

class SongsContainer(object):
  """ """
  class _Song(object):
    '''Class containing needed song information'''

    __slots__ = "uri", "ts", "title", "artist", "album", "count"

    def __init__(self, ts: datetime, song_title: str, song_artist: str, album: str, count:int):
      self.ts = ts
      self.title = song_title
      self.artist = song_artist
      self.album = album
      self.count = count

    def __eq__(self, other) -> bool:
      return self.title == other.title and self.artist == other.artist
    
    def __ne__(self, other) -> bool:
      return not self == other
    
    def __gt__(self, other) -> bool:
      return self.ts > other.ts
    
    def __lt__(self, other) -> bool:
      return self.ts < other.ts
    
    def updateTS(self, ts):
      self.ts = ts

    def __repr__(self) -> str:
      return f'{self.ts}; {self.title} by {self.artist} ({self.count})'

  def __init__(self):
    self._songs = {}  #Dictionary with key = song URI and value = song info
    self._artists = {} #Dictionary with key = artist and value = set of keys

  def addFromFile(self, file: str) -> bool:
    '''Validates a file containing results from past program run, and adds them to self. Returns False if anything fails, otherwise True.'''
    song_dict = validatedFile(file)
    if(song_dict is None):
      return False
    #Ensure each song can be added
    pBar = ProgressBar(len(song_dict), "Validating file contents")
    tempContainer = SongsContainer()
    for uri in song_dict:
      if(type(uri) != str):
        return False
      for detail in ["timestamp","title","artist","album","count"]:
        if(detail not in song_dict[uri]):
          return False
      tempContainer.addSong(uri,
                            song_dict[uri]['timestamp'],
                            song_dict[uri]['title'],
                            song_dict[uri]['artist'],
                            song_dict[uri]['album'],
                            song_dict[uri]['count'])
      pBar.updateProgress()
    pBar.finish()
    self._songs = tempContainer._songs
    self._artists = tempContainer._artists
    return True

  def addSong(self, uri: int, ts, song_title: str, song_artist: str, album: str, count = 1):
    song = self._Song(ts, song_title, song_artist, album, count)
    if(uri in self):  #If song's uri is already in dictionary
      self._addCount(uri)
      if(ts < self.getTS(uri)): #Take the earliest date
        self._updateTS(uri, ts)
    else:  #Else add song to dictionaries
      self._songs[uri] = song
      self._addToArtist(uri)

  def _addToArtist(self, key):
    artist = self.getArtist(key)
    if(artist not in self._artists):
      self._artists[artist] = {key}
    elif(key not in self._artists[artist]):
      self._artists[artist].add(key)

  def __contains__(self, x):
    return x in self._songs
  
  def __getitem__(self, key):
    return self._songs[key]
  
  def __len__(self):
    return len(self._songs)
  
  def __iter__(self):
    for i in self._songs.keys():
      yield i
        
  def artists(self, artist = None):
    if artist:
      return [i for i in self._artists[artist]]
    else:
      return [i for i in self._artists]

  #--Accessors--
  def getTS(self, key):
    return self._songs[key].ts

  def getTitle(self, key):
    return self._songs[key].title

  def getArtist(self, key):
    return self._songs[key].artist
  
  def getAlbum(self, key):
    return self._songs[key].album
  
  def getCount(self, key):
    return self._songs[key].count
  
  #--Mutators--
  def _updateTS(self, key, ts):
    self._songs[key].updateTS(ts)

  def _addCount(self, key):
    self._songs[key].count += 1

  def __delitem__(self, key):
    artist = self._songs[key].artist  
    del self._songs[key]
    self._artists[artist].remove(key)
    if(not self._artists[artist]):
      del self._artists[artist]



class MasterSongContainer(object):
  """ """
  def __init__(self):
    from Settings import settingByName
    self.desiredSongs = SongsContainer()
    self.previousSongs = SongsContainer()
    #Keep easier reachable references for needed settings
    self.earlyRange = settingByName('beginningDate').value#settings['earlyRange'].value  #Earliest date of desired
    self.lastDate = settingByName('lastDate').value  #Last date of desired
    self.earlyDate = settingByName('earliestDate').value  #Earliest date of previous
    self.minCount = settingByName('minCount').value  #Minimum number of times song should be counted for
    self.msPlayed = settingByName('minMS').value #Minimum milliseconds the track has to be played to count (unless track was finished)
    self.songPref = settingByName('songPreference').value #If same songs with different uris, choice of which to keep
    self.prevCountMatters = settingByName('universalMinCount').value #If True, will follow count rules for previous songs too
    self.gracePeriod = settingByName('songGracePeriod').value #Period at which the count will not matter
    self._convertDatetimes()

  def _convertDatetimes(self):
    """Convert the setting's datetime.date to datetime.datetime (with time of midnight or 23:59) so then it can be used with everything else."""
    midnight = datetime(2000,1,1,0,0,0).time()
    endOfDay = datetime(2000,1,1,23,59,59).time()
    #earlyRange (midnight)
    self.earlyRange = datetime.combine(self.earlyRange, midnight)
    #lastDate (11:59)
    self.lastDate = datetime.combine(self.lastDate, endOfDay)
    #earlyDate (midnight)
    self.earlyDate = datetime.combine(self.earlyDate, midnight)
    #gracePeriod (midnight)
    self.gracePeriod = datetime.combine(self.gracePeriod, midnight)

  def _checkSong(self, song_entry: dict) -> bool:
      """Verifies song by things such as if it was skipped or not, etc. True if ok"""
      #Track unknown? (occurs when song is downloaded custom song)
      if(not song_entry['master_metadata_track_name']):
        return False
      #Was skipped?
      if(song_entry['skipped']):
        return False
      #Ended due to track being done, or if ms played longer than set time?
      if(not(song_entry['reason_end'] == 'trackdone' or song_entry['ms_played'] > self.msPlayed)):
        return False
      return True


  def addSong(self, song_entry:dict) -> None:
    """Takes the entry from the JSON file and adds it to correct container"""
    uri = song_entry['spotify_track_uri']
    ts = datetime.strptime(song_entry['ts'], '%Y-%m-%dT%H:%M:%SZ') #Converts time stamp to dateTime object
    title = song_entry['master_metadata_track_name']
    artist = song_entry['master_metadata_album_artist_name']
    album = song_entry['master_metadata_album_album_name']
    if(self._checkSong(song_entry) and ts < self.lastDate and ts > self.earlyDate):
      if(ts < self.earlyRange):
        self.previousSongs.addSong(uri, ts, title, artist, album)
      else:
        self.desiredSongs.addSong(uri, ts, title, artist, album)
  
  def forceAdd(self, uri:str, title:str, artist:str, album:str) -> None:
    """Given a song uri, title, artist, and album, add it to the desiredSongs"""
    today = datetime.today()
    self.desiredSongs.addSong(uri, today, title, artist, album, count=0)

    
  def forceRemove(self, uri: str) -> None:
    """Finds given song uri and removes it from desiredSongs"""
    if(uri in self.desiredSongs):
      del self.desiredSongs[uri]


  def removeLowCount(self) -> None:
    """Removes all songs that were below minCount"""
    if(self.minCount <= -1):  #Skip this part
      return
    #Remove low counts from previous songs (with flag from setting?)
    if(self.prevCountMatters):
      pBar = ProgressBar(len(self.desiredSongs)+len(self.previousSongs),"Removing low count")
      for key in list(self.previousSongs):
        pBar.updateProgress()
        if(self.previousSongs.getCount(key) < self.minCount):
          del self.previousSongs[key]
    else:
      pBar = ProgressBar(len(self.desiredSongs),"Removing low count")
    #Remove from desired songs
    for key in list(self.desiredSongs):
      pBar.updateProgress()
      if(self.desiredSongs.getTS(key) < self.gracePeriod and self.desiredSongs.getCount(key) < self.minCount):
        del self.desiredSongs[key]
    pBar.finish()


  def combineSongs(self) -> None:
    """Check every song in desiredSongs, and if the titles match, then follow setting to remove specified title."""
    if(self.songPref == 2): #Keep duplicates
      return
    pBar = ProgressBar(len(self.desiredSongs),"Combining songs")
    for artist in self.desiredSongs.artists(): #Go by each artist
      for uri1 in self.desiredSongs.artists(artist):
        pBar.updateProgress()
        if(uri1 not in self.desiredSongs.artists(artist)):
          continue
        for uri2 in self.desiredSongs.artists(artist):
          if(uri1 == uri2): #Same URIs
            continue
          if(self.desiredSongs[uri1] == self.desiredSongs[uri2]): #URI is of same song
            if(self.songPref == 0): #Keep oldest
              if(self.desiredSongs[uri1] > self.desiredSongs[uri2]):
                del self.desiredSongs[uri1]
                break
              else:
                del self.desiredSongs[uri2]
            elif(self.songPref == 1): #Keep newest
              if(self.desiredSongs[uri1] < self.desiredSongs[uri2]):
                del self.desiredSongs[uri1]
                break
              else:
                del self.desiredSongs[uri2]
            elif(self.songPref == 3): #Ask user
              print(f'Found a duplicate URI for {self.desiredSongs.getTitle(uri1)} by {self.desiredSongs.getArtist(uri1)}')
              print(f'\t1. open.spotify.com/track/{uri1[14:]}; from album titled {self.desiredSongs.getAlbum(uri1)}; first listened on {self.desiredSongs.getTS(uri1)}')
              print(f'\t2. open.spotify.com/track/{uri2[14:]}; from album titled {self.desiredSongs.getAlbum(uri2)}; first listened on {self.desiredSongs.getTS(uri2)}')
              response = input("Enter '1', '2', or 'both' to pick which one to keep: ").lower()
              while(response not in ["1","2","both"]):
                response = input("Invalid input. Enter '1', '2', or 'both' to pick which one to keep: ").lower()
              if(response == "1"):
                del self.desiredSongs[uri2]
              elif(response == "2"):
                del self.desiredSongs[uri1]
                break
    pBar.finish()


  def compareContainersURI(self):
    """Remove songs from desiredSongs if it's found in previousSongs"""
    pBar = ProgressBar(len(self.desiredSongs),"Getting unique songs by URI")
    for artist in self.desiredSongs.artists():  #Artists in desiredSongs
      if(artist in self.previousSongs.artists()): #See if artist in previousSongs
        for uri in self.desiredSongs.artists(artist): #Go through each URI in desiredSongs
          pBar.updateProgress()
          if(uri in self.previousSongs.artists(artist)):  #Remove if found in previousSongs
            del self.desiredSongs[uri]
      #Update pBar
      else:
        pBar.updateProgress(len(self.desiredSongs.artists(artist)))
    pBar.finish()
      


  def compareContainersSong(self):
    """Compares desiredSongs song titles and artist to previousSongs'"""
    pBar = ProgressBar(len(self.desiredSongs),"Getting unique songs by song title")
    for artist in self.desiredSongs.artists():  #Artists in desiredSongs
      if(artist in self.previousSongs.artists()): #See if artist in previousSongs
        for uri1 in self.desiredSongs.artists(artist): #Go through each URI in desiredSongs
          pBar.updateProgress()
          for uri2 in self.previousSongs.artists(artist): #Cycle through all URI's of previousSongs
            if(self.desiredSongs[uri1] == self.previousSongs[uri2]): #Same title and artist
              del self.desiredSongs[uri1]
              break
      #Update pBar
      else:
        pBar.updateProgress(len(self.desiredSongs.artists(artist)))
    pBar.finish()


  def cleanup(self):
    """runs functions to cleanup data (do we want?)"""
    pass


  def parse(self):
    """Runs data parsing functions."""
    self.removeLowCount() #Remove low counts
    self.compareContainersURI() #Remove by uris from dict
    self.compareContainersSong() #Remove by songs from dict
    self.combineSongs() #Combine songs with diff uri
  
    


if __name__ == "__main__":
  import Settings
  Settings.init()
  Settings.updateValue('earlyRange','2023-10-17')
  Settings.updateValue('songPreference','both')
  #Mann so much testing will be needed...
  test_container = MasterSongContainer()
  #skipped = 1 (eyewishes)
  #unknown = 1 (in desired)
  #len = 9 - 2
  test_songs = [{
    "ts": "2023-10-10T18:34:59Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 75270,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "Eyewishes / Bystanding",
    "master_metadata_album_artist_name": "Lemon Demon",
    "master_metadata_album_album_name": "Dinosaurchestra",
    "spotify_track_uri": "spotify:track:09K7eiTHWsAEGAKGRKnRX6",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "endplay",
    "shuffle": True,
    "skipped": True,
    "offline": False,
    "offline_timestamp": 1697567623,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-11T18:38:29Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 210814,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "A Mask of My Own Face",
    "master_metadata_album_artist_name": "Lemon Demon",
    "master_metadata_album_album_name": "Nature Tapes",
    "spotify_track_uri": "spotify:track:6ibbHAoBrdqJxo345QGumd",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "playbtn",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697567700,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-12T18:42:37Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 247220,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "Two Trucks",
    "master_metadata_album_artist_name": "Lemon Demon",
    "master_metadata_album_album_name": "Nature Tapes",
    "spotify_track_uri": "spotify:track:1s5A0u1dnAeVNur5nPkCpD",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697567910,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-13T18:45:05Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 130006,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "The Satirist's Love Song",
    "master_metadata_album_artist_name": "Lemon Demon",
    "master_metadata_album_album_name": "View-Monster",
    "spotify_track_uri": "spotify:track:6pzys6wwdtCov4bJ4omXfJ",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697568157,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-14T18:48:07Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 182800,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "Haiku",
    "master_metadata_album_artist_name": "Tally Hall",
    "master_metadata_album_album_name": "Marvin's Marvelous Mechanical Museum",
    "spotify_track_uri": "spotify:track:3xfVTbyfrJwPN9bqlXipmw",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697568305,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-17T18:51:41Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 211913,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "Reaganomics",
    "master_metadata_album_artist_name": "Lemon Demon",
    "master_metadata_album_album_name": "Spirit Phone",
    "spotify_track_uri": "spotify:track:6ForyBso37QPHoEM06IDwK",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697568488,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-18T18:55:43Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 242076,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": None,
    "master_metadata_album_artist_name": None,
    "master_metadata_album_album_name": None,
    "spotify_track_uri": None,
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697568701,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-19T19:00:33Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 283640,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "Taken for a Ride",
    "master_metadata_album_artist_name": "Tally Hall",
    "master_metadata_album_album_name": "Marvin's Marvelous Mechanical Museum",
    "spotify_track_uri": "spotify:track:6WJJoWzwlEs8V4lWIZRjAP",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697568943,
    "incognito_mode": False
  },
  {
    "ts": "2023-10-20T19:02:29Z",
    "username": "kothenbeutel",
    "platform": "android",
    "ms_played": 114937,
    "conn_country": "US",
    "ip_addr_decrypted": "138.236.254.48",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "320x200",
    "master_metadata_album_artist_name": "Lemon Demon",
    "master_metadata_album_album_name": "View-Monster",
    "spotify_track_uri": "spotify:track:797Kwr078nL5djUEQFbl33",
    "episode_name": None,
    "episode_show_name": None,
    "spotify_episode_uri": None,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": True,
    "skipped": False,
    "offline": False,
    "offline_timestamp": 1697569234,
    "incognito_mode": False}]
  for i in test_songs:
    test_container.addSong(i)
  test_songs[1]['ts'] = "2023-10-22T19:02:29Z"
  for i in test_songs:
    test_container.addSong(i)
  test_container.removeLowCount()
  print(test_container.previousSongs._songs)
  print()
  print(test_container.desiredSongs._songs)
  print(test_container.desiredSongs._artists)
  test_container.addSong(test_songs[1])
  test_container.compareContainersURI()
  assert "spotify:track:6ibbHAoBrdqJxo345QGumd" not in test_container.desiredSongs._songs
  test_songs[1]['spotify_track_uri'] = "woah"
  test_container.addSong(test_songs[1])
  test_container.compareContainersSong()
  assert "woah" not in test_container.desiredSongs._songs
  test_songs[-2]['spotify_track_uri'] = "eep"
  test_songs[-2]['ts'] = "2023-10-22T20:02:29Z"
  test_container.addSong(test_songs[-2])
  test_container.combineSongs()
  print(test_container.desiredSongs._songs)
  print(dict(test_container.desiredSongs._songs))

  mmm = datetime.today()
  mmm = str(mmm)
  print(mmm)
  