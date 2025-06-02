#Run this file to start the program!

from os import system, name
from Helpers.DataParse import validatedFile, dictToJSON, validatedFolder
import Helpers.Settings as S
from Helpers.SongStruct import MasterSongContainer
from Helpers.ProgressBar import ProgressBar
from os.path import abspath
from datetime import datetime
from Helpers.SpotifyFunctions import SpotifyGateway
from Helpers.Formatting import *

def currentTime():
  return f'{datetime.today().date()}_{str(datetime.today().time()).replace(":","-")[:8]}'

def exportSettings():
  fPath = f"SavedSettings.txt"
  #Access SavedSettings.txt (assume already created because of bold quesiton)
  with open(fPath, 'r+') as file:
    bolded = file.readline()
    file.seek(0)
    file.write(bolded)
    for setting in S.settings:
      if(setting.options is not None): #Get index of option
        file.write(f'{setting.name}: {setting.options[setting.value]}\n')
      else:
        file.write(f'{setting.name}: {setting.value}\n')
    file.truncate()
  print(f'Settings saved at {abspath(fPath)}. Please do not edit, rename, or relocate the file.')
  input()

def importSettings():
  try:
    with open("SavedSettings.txt",'r') as file:
      options = file.readlines()
      for i in options:
        option = i.split(': ')
        if(len(option) == 1):#Skips formatting option
          continue
        numSetting = -1
        #Find setting line corresponds to
        for i in range(len(S.settings)):
          if(option[0] == S.settings[i].name):
            numSetting = i+1
            break

        if(option[1][-1] == '\n'): #Remove newline
          option[1] = option[1][:-1]

        if(numSetting == -1):
          print(f'Could not find option named {option[0]}.')
          continue
        S.updateValue(str(numSetting),option[1])
      print("Settings imported.")
  except FileNotFoundError:
    print('Could not find saved setting file.')
  except Exception as e:
    print(f'Could not import settings due to an error ({e}).')
  input()


def options(abouts = False):
  """Displays the settings and takes in user input to alter them."""
  system('cls' if name == 'nt' else 'clear') #Clear screen

  #Print settings
  if(abouts):
    S.printAbouts()
  else:
    S.printSettings()

  inp = input(f"You may change a setting by inputting {bold('{number} {value}')}, input {bold(underline('a')+'bout')} to learn more/less about the settings, {bold(underline('e')+'xport')} to export current settings, {bold(underline('i')+'mport')} to import previously saved settings, or input {bold(underline('b')+'ack')} to go back. You may also input {bold(underline('d')+'efault')} to revert the settings to their default values. It's recommended to export any changes because the settings will reset upon relaunch.\n\n").lower()
  
  if(inp == 'about' or inp == 'a'): #About
    return options(not abouts)
  elif(len(inp.split(' ')) == 2): #Change setting
    inp = inp.split(' ')
    print()
    S.updateValue(inp[0], inp[1])
  elif(inp == 'export'or inp == 'e'):  #Export
    exportSettings()
  elif(inp == 'import' or inp == 'i'):  #Import
    importSettings()
  elif(inp == 'back' or inp == 'b'):  #Back
    return
  elif(inp == 'default' or inp == 'd'):
    S.init()
    return options()
  else:
    print("Input could not be used. Please try again." )
    input()
  return options(abouts)

def about():
  system('cls' if name == 'nt' else 'clear')
  print(f'Made by {bold("Taylor Kothenbeutel")}')
  input()

def saveResults(songContainer:MasterSongContainer):
  plainSongs = {} #Get dictionary in a readable format
  for key in songContainer.desiredSongs:
    value = songContainer.desiredSongs[key]
    plainSongs[key] = {
      "timestamp":str(value.ts),
      "title":value.title,
      "artist":value.artist,
      "album":value.album,
      "count":value.count
    }
  fPath = f"./Results/{currentTime()}.json"
  resultToJSON = dictToJSON(plainSongs)
  with open(fPath,'w') as file:
    file.write(resultToJSON)
  print(f'\nSong results written to {abspath(fPath)}')
  input()

def addToPlaylist(songContainer:MasterSongContainer):
  print(f'\nTo add these songs onto a playlist, some information of your {bold("Spotify")} is first needed.')
  #Get username
  username = input(f'Please enter your {bold("Spotify username")} (not your display name): ')
  #Get playlist id (help if needed)
  playlist_id = input(f"Now, please enter the ID of the playlist you would like the songs added to. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID: ")
  if(playlist_id.lower() == 'help' or playlist_id.lower() == 'h'):
    print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
    playlist_id = input("Please enter the desired playlist's id: ")
  
  sp = SpotifyGateway(username, playlist_id)

  #Test
  print()
  print("This program will now ask you to log in to your Spotify account to verify the username and playlist given.")
  print("If you are not already signed in, it will redirect you to Spotify's login page. Please sign in with the account holding the username given")
  print("Next, it will open a new tab that will fail to connect to a webpage. This is normal. You will need to copy the URL of that page, and paste it when asked. Feel free to close that tab afterwards.")
  print("If you have already given this username to the program prior, the new tab step will be ommitted.")
  input()#Wait for user

  print('Now testing to ensure the username and playlist exist.')
  test = sp.validateInformation()
  if(not test): #Test failed
    print(f'Unfortunately, the test was unsuccessful. Please keep in mind to enter your {bold("username")} and a {bold("playlist ID")} that you are the owner of.')
    input(f'Press {bold("Enter")} to try again.\n')
    return addToPlaylist(songContainer)
  #Test passed
  print()
  print("Test has successfully passed. Now it's time to add the songs to the playlist.\n")
  input()#Wait for user

  #If timer is >0, run timed adder
  if(S.settingByName('playlistAddTimer').value > 0):
    sp.addToSpotifyTimed(songContainer.desiredSongs,S.settingByName('playlistAddTimer').value)
  #Else run batch adder
  else:
    sp.addToSpotifyBatch(songContainer.desiredSongs)
  print('All songs successfully added to the playlist.')
  input()
  return

def forceAddRemove(songContainer:MasterSongContainer) -> bool:
  """Asks user if they would like to force add/remove songs. Returns True if they did do either."""
  containerAltered = False
  system('cls' if name == 'nt' else 'clear')

  #Force add
  inp = input(f"I'm sure you got some great songs snagged already, but would you like any songs forced in the collection, regardless of the song's uniqueness? {bold('(y/n)')} ").lower()

  if(inp == 'y' or inp == 'yes'):
    print("Sounds good! Please note that the timestamp added to these songs will be today's date and current time. If you save your song results, the songs added via this method will have a count of 0.")
    print()#Spacer

    sp = SpotifyGateway(None, None)
    songs = {}

    print("If you enter a playlist ID, the program may take you to a new tab with a broken webpage. This is normal. This tab builds the connection between this program and Spotify. What you will need to do is to copy the URL and paste it into the terminal when asked. Feel free to close the tab afterward.")
    print("If you have done this step before, this step will be omitted.")
    input()
    while(True):
      inp = input(f"Please enter the ID of the playlist or the absolute JSON file path (either Spotify's history file or file from previous results) containing the songs you would like added. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting playlist IDs, or enter {bold(underline('c')+'ancel')} if you would not like to add songs: ")
      print()#Spacer
      if(inp.lower() == 'help' or inp.lower() == 'h'):
        print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
        inp = input("Please enter the desired playlist's id: ")
        print()#Spacer
      if(inp.lower() == 'done' or inp.lower() == 'd'):
        break
      elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
        songs = {}
        break
      else:
        #Check if inp is JSON
        if(inp[-5:] == ".json"):
          fileRes = validatedFile(inp)
          if(type(fileRes) == dict): #Program's JSON
            for uri in fileRes:
              songs[uri] = fileRes[uri]
            print(f"Found {len(fileRes)} songs from this file.")
            input()#Wait for user
          elif(type(fileRes) == list): #Spotify's JSON
            for song in fileRes:
              songs[song['spotify_track_uri']] = {
                'title' : song['master_metadata_track_name'],
                'artist' : song['master_metadata_album_artist_name'],
                'album' : song['master_metadata_album_album_name']
              }
            print(f"Found {len(fileRes)} songs from this file.")
            input()#Wait for user

        else: #Playlist ID
          track_results = sp.getPlaylistSongs(inp)
          if(track_results is None):
            print("The input could not be used. This could mean that the file location was not valid or the playlist given is empty. Remember to enter an item one at a time. Please try again.")
            input()#Wait for user
            continue
          for song in track_results:
            songs[song['track']['uri']] = {
              'title' : song['track']['name'],
              'artist' : song['track']['artists'][0]['name'],
              'album' : song['track']['album']['name']
            }
          print(f"Found {len(track_results)} songs from this playlist.")
          input()#Wait for user
    
    if(len(songs)>0):
      print("Time to add these songs to the collection!")
      input()
      pBar = ProgressBar(len(songs), 'Adding songs to collection')
      for uri in songs:
        if(uri in songContainer.desiredSongs):
          pBar.updateProgress() #Song already in collection
        else:
          containerAltered = True
          songContainer.forceAdd(uri, songs[uri]['title'], songs[uri]['artist'], songs[uri]['album'])
          pBar.updateProgress()
      pBar.finish()
      print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
      input()#Wait for user
    system('cls' if name == 'nt' else 'clear')
  elif(inp == 'n' or inp == 'no'):
    pass
  else:
    print("Input could not be used. Please try again." )
    input()
    return forceAddRemove(songContainer)

  #Force remove
  while(True):#While loop in case input could not be read
    inp = input(f"Would you like to force remove any songs from this collection? {bold('(y/n)')} ").lower()
    
    if(inp == 'y' or inp == 'yes'):
      print("Sounds good!")
      print()#Spacer

      sp = SpotifyGateway(None, None)
      songs = []
      print("If you enter a playlist ID, the program may take you to a new tab with a broken webpage. This is normal. This tab builds the connection between this program and Spotify. What you will need to do is to copy the URL and paste it into the terminal when asked. Feel free to close the tab afterward.")
      print("If you have done this step before, this step will be omitted.")
      input()
      while(True):
        print(f"Please enter any of the following to remove included songs from the collection:")
        print(f"   * Spotify playlist ID\n   * JSON absolute file path (Spotify's streaming history file or previous results)\n   * Artist name (case-sensitive)\n   * Song title/URI")
        inp = input(f"Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting items for removal, or enter {bold(underline('c')+'ancel')} if you would not like to remove any songs: ")
        print()#Spacer
        if(inp.lower() == 'help' or inp.lower() == 'h'):
          print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
          inp = input("Please enter the desired playlist's ID, artist name, or song title: ").lower()
          print()#Spacer
        if(inp.lower() == 'done' or inp.lower() == 'd'):
          break
        elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
          songs = []
          break
        else:#Input of artist/song/playlist
          artistResult = list(songContainer.desiredSongs.artists(inp))
          songResult = songContainer.desiredSongs.findSongTitle(inp)
          if(artistResult or songResult): #Input was an artist or song
            if(artistResult and songResult): #Choose which
              print(f"{bold(inp)} is both an artist and a song name. Which would you like removed?")
              while(True):
                opt = input(f"Input {underline('1')} for the artist or {underline('2')} for song: ")
                if(opt == '1'):
                  songResult = []
                  break
                elif(opt == '2'):
                  artistResult = []
                  break
              print("Input could not be used. Please try again.")
              input()#Wait for user
            if(artistResult): #Remove artist
              songs += artistResult
              print(f"Found {len(artistResult)} songs from this artist.")
              input()#Wait for user
            else:
              if(len(songResult) > 1):
                print(f"There are {bold(len(songResult))} songs with that title found in the collection. Select which one you would like removed.")
                for i in range(len(songResult)):
                  song = songContainer.desiredSongs[songResult[i]]
                  print(f"{i+1}. {song.title} by {bold(song.artist)} on {bold(song.album)}.")
                while(True):
                  opt = input(f"Select a song: ")
                  try:
                    opt = int(opt) -1
                    assert opt >= 0
                    songResult = [songResult[opt]]
                    break
                  except:
                    print("Input could not be used. Please try again.")
                    input()#Wait for user
                    continue
              song = songContainer.desiredSongs[songResult[0]]
              while(True):
                opt = input(f"Are you sure you want to remove {bold(song.title)} by {bold(song.artist)} on {bold(song.album)}? {bold('(y/n)')} ").lower()
                if(opt == 'n' or opt == 'no'):
                  print("Song will not be removed.")
                  input()#Wait for user
                  break
                elif(opt == 'y' or opt == 'yes'):
                  songs.append(songResult[0])
                  print("Song added to be removed.")
                  input()#Wait for user
                  break
                else:
                  print("Input could not be used. Please try again.")
                  input()#Wait for user 

          #Check if inp is JSON
          elif(inp[-5:] == ".json"):
            fileRes = validatedFile(inp)
            if(type(fileRes) == dict): #Program's JSON
              for uri in fileRes:
                songs.append(uri)
              print(f"Found {len(fileRes)} songs from this file.")
              input()#Wait for user
            elif(type(fileRes) == list): #Spotify's JSON
              for song in fileRes:
                songs.append(song['spotify_track_uri'])
              print(f"Found {len(fileRes)} songs from this file.")
              input()#Wait for user

          #Check if inp is URI
          elif(inp in songContainer.desiredSongs): #URI with spotify:track
            song = songContainer.desiredSongs[inp]
            while(True):
                opt = input(f"Are you sure you want to remove {bold(song.title)} by {bold(song.artist)} on {bold(song.album)}? {bold('(y/n)')} ").lower()
                if(opt == 'n' or opt == 'no'):
                  print("Song will not be removed.")
                  input()#Wait for user
                  break
                elif(opt == 'y' or opt == 'yes'):
                  songs.append(inp)
                  print("Song added to be removed.")
                  input()#Wait for user
                  break
                else:
                  print("Input could not be used. Please try again.")
                  input()#Wait for user 
          elif("spotify:track:"+inp in songContainer.desiredSongs):#URI without spotify:track
            inp = "spotify:track:"+inp
            song = songContainer.desiredSongs[inp]
            while(True):
                opt = input(f"Are you sure you want to remove {bold(song.title)} by {bold(song.artist)} on {bold(song.album)}? {bold('(y/n)')} ").lower()
                if(opt == 'n' or opt == 'no'):
                  print("Song will not be removed.")
                  input()#Wait for user
                  break
                elif(opt == 'y' or opt == 'yes'):
                  songs.append(inp)
                  print("Song added to be removed.")
                  input()#Wait for user
                  break
                else:
                  print("Input could not be used. Please try again.")
                  input()#Wait for user

          else: #inp was a playist (or not found artist/song/file)
            track_results = sp.getPlaylistSongs(inp)
            if(track_results is None):
              print("The input could not be used. This could mean that the artist or song is not in the collection, the file location was not valid, or the playlist given is empty. Remember to enter an item one at a time. Please try again.")
              input()#Wait for user
              continue
            for song in track_results:
              songs.append(song['track']['uri'])
            print(f"Found {len(track_results)} songs from this playlist.")
            input()#Wait for user
      
      if(len(songs) > 0):
        print("Time to remove these songs from the collection!")
        input()
        prevLen = len(songContainer.desiredSongs)
        pBar = ProgressBar(len(songs), 'Removing songs from collection')
        for uri in songs:
          songContainer.forceRemove(uri)
          pBar.updateProgress()
        pBar.finish()
        if(prevLen > len(songContainer.desiredSongs)):
          containerAltered = True
        print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
        input()#Wait for user
      system('cls' if name == 'nt' else 'clear')
      return containerAltered
    elif(inp == 'n' or inp == 'no'):
      return containerAltered
    else:
      print("Input could not be used. Please try again.")
      input()#Wait for user
      system('cls' if name == 'nt' else 'clear')
      continue


def welcome():
  """Prints messages that appear at the start of the program."""
  system('cls' if name == 'nt' else 'clear')
  print(f'Welcome to the {bold("Spotify Unique Song Parser")}!')
  print(f'{bold(underline("S")+"tart")}: Start the process to parse through your data')
  print(f'{bold(underline("R")+"esume")}: Use previous program results and skip the parsing')
  print(f'{bold("Se"+underline("t")+"tings")}: View and change settings')
  print(f'{bold(underline("A")+"bout")}: Learn more about this program')
  print(f'{bold(underline("E")+"xit")}: Close the program')
  inp = input('\n\n').lower()
  if(inp == 'start' or inp == 's'):
    return run()
  elif(inp == 'resume' or inp == 'r'):
    return resume()
  elif(inp == 'settings' or inp == 't'):
    options()
    return welcome()
  elif(inp == 'about' or inp == 'a'):
    about()
    return welcome()
  elif(inp == 'exit' or inp == 'q' or inp == 'e'):
    return
  else:
    print("Input could not be used. Please try again.")
    input()
    return welcome()
    
def run():
  #Major variables
  dataContainer = [] #Each item will contain a dictionary of what the JSON file had
  songContainer = MasterSongContainer() #Settings transfer over
  
  system('cls' if name == 'nt' else 'clear')
  print("Let's begin!\n")
  input()

  #Gather files
  print("First, let's get every file containing songs from your extended Spotify streaming history.")
  print(f'Please input a file location (the file should be called {bold("Streaming_History_Audio")}...{bold(".json")}) or a folder containing the files, and input {bold(underline("d")+"one")} when all files have been imported in.')
  while(True):
    inp = input(f'Enter file/folder location or {bold(underline("d")+"one")} here: ')
    if(inp.lower() == 'done' or inp.lower() == 'd'):
      break
    if(len(inp) > 2 and inp[0] == '"' and inp[-1] == '"'): #Disregard quotations around location
      inp = inp[1:-1]
    #Check if location is folder
    if(".json" not in inp):
      data = validatedFolder(inp)
      if(data):
        dataContainer += data
    else:
      if(inp.split('/')[-1][:23] != "Streaming_History_Audio"):
        print(f"Cannot use this file. The file must be {bold('Streaming_History_Audio_')}... and be of type {bold("JSON")}.")
        continue
      data = validatedFile(inp)
      if(data):
        dataContainer.append(data)
        print('File succesfully imported.')

  print()#Spacing

  print('Great! Time to add them into containers for easier parsing.')
  
  input()#Wait for user

  #Get total number of songs
  numberSongs = 0
  for i in dataContainer:
    numberSongs += len(i)

  #Add songs to collection
  pBar = ProgressBar(numberSongs, 'Adding songs to containers')
  for chunk in dataContainer:
    for entry in chunk:
      pBar.updateProgress()
      songContainer.addSong(entry)
  pBar.finish()

  #Adding to container results
  print(f"After adding all the songs to their respective containers, {bold(len(songContainer.desiredSongs))} of the {bold(len(songContainer.desiredSongs)+len(songContainer.previousSongs))} songs are potentially unique songs listened to in the given range. Let's shrink that number!")

  input()#Wait for user

  #Parse
  print("Now that all songs have been accounted for, let's get parsing!")
  input()
  songContainer.parse()
  
  print()#Spacing

  #Announce results
  print(f"Parsing is now complete! In all, the program found {bold(len(songContainer.desiredSongs))} unique songs. That's a lot of songs (probably)!")

  input()#Wait for user

  #Force add or remove any songs
  forceAddRemove(songContainer)

  #Sort collection
  songContainer.sort()

  #Save for later or add to playlist
  while(True):
    inp = input(f"Would you like to {bold(underline('s')+'ave')} the results, {bold(underline('a')+'dd')} the unique songs to a playlist, or do {bold(underline('b')+'oth')} options?\n").lower()
    if(inp == 'save' or inp == 's'):
      saveResults(songContainer)
      break
    elif(inp == 'add' or inp == 'a'):
      addToPlaylist(songContainer)
      break
    elif(inp == 'both' or inp == 'b'):
      saveResults(songContainer)
      addToPlaylist(songContainer)
      break
    else:
      print(f'{inp} is not a valid option. Please respond with either {bold(underline("s")+"ave")}, {bold(underline("a")+"dd")}, or {bold(underline("b")+"oth")} to choose.')
      input()

  #After saving/adding/bothing
  print(f'This program is now finished. {bold("Thank you for using it!")}')
  input()#Wait for user
  return

def resume():
  system('cls' if name == 'nt' else 'clear')
  print("Welcome back! Let's get your previously saved data.")
  input()

  masterSongs = MasterSongContainer()

  print(f"First, please input the {bold('abolute path')} of your results from previously using this program. Ensure this file has not been altered, otherwise, the program may not be able to read the file.")
  file = input(f'Enter file location here: ')
  if(len(file) > 2 and file[0] == '"' and file[-1] == '"'): #Disregard quotations around location
      file = file[1:-1]
  addResult = masterSongs.desiredSongs.addFromFile(file)
  while(not addResult):
    input("Please try again.\n")
    print(f"Input the {bold('abolute path')} of your results from previously using this program. Ensure this file has not been altered, otherwise the program may not be able to use that file.")
    file = input(f'Enter file location here: ')
    if(len(file) > 2 and file[0] == '"' and file[-1] == '"'): #Disregard quotations around location
      file = file[1:-1]
    addResult = masterSongs.desiredSongs.addFromFile(file)
  
  #Songs added
  print(f"All {len(masterSongs.desiredSongs)} songs have been imported. Let's move on.")
  input()#Wait for user

  #Force add/remove
  altered = forceAddRemove(masterSongs)
  
  #Sort collection
  masterSongs.sort()

  #Check if results were altered
  if(altered):
    while(True):
      inp = input(f"Since the results were just altered, would you like to {bold(underline('s')+'ave')} the results to a new file, {bold(underline('a')+'dd')} the unique songs to a playlist, or do {bold(underline('b')+'oth')} options?\n").lower()
      if(inp == 'save' or inp == 's'):
        saveResults(masterSongs)
        break
      elif(inp == 'add' or inp == 'a'):
        addToPlaylist(masterSongs)
        break
      elif(inp == 'both' or inp == 'b'):
        saveResults(masterSongs)
        addToPlaylist(masterSongs)
        break
      else:
        print(f'{inp} is not a valid option. Please respond with either {bold(underline("s")+"ave")}, {bold(underline("a")+"dd")}, or {bold(underline("b")+"oth")} to choose.')
        input()
  else: #Results were not altered
    print("Okay, time for the star of this show: adding these songs to a Spotify playlist!")
    input()#Wait for user
    addToPlaylist(masterSongs)

  #After adding
  print(f'This program is now finished. {bold("Thank you for using it!")}')
  input()#Wait for user
  return
  

if __name__ == "__main__":
  system('cls' if name == 'nt' else 'clear')
  initFormat()
  S.init()
  welcome()