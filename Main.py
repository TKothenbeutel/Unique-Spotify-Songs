import _importENVVar

from os import system, name
from DataParse import validatedFile, dictToJSON, validatedFolder
import Settings as S
from SongStruct import MasterSongContainer
from ProgressBar import ProgressBar
from os.path import abspath
from datetime import datetime
from SpotifyFunctions import SpotifyGateway
from Formatting import *

def currentTime():
  return f'{datetime.today().date()}_{str(datetime.today().time()).replace(":","-")[:8]}'

def exportSettings():
  fPath = f"savedSettings.txt"
  #Access savedSettings.txt (assume already created because of bold quesiton)
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
  print(f'Settings saved at {abspath(fPath)}. Please do not edit or relocate file.')
  input()

def importSettings():
  try:
    with open("savedSettings.txt",'r') as file:
      options = file.readlines()
      for i in options:
        option = i.split(': ')
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

  inp = input(f'You may change a setting by inputting {bold("{number} {value}")}, input {bold(underline("a")+"bout")} to learn more/less about each setting, {bold(underline("e")+"xport")} to export current settings, {bold(underline("i")+"mport")} to import previously saved settings, or input {bold(underline("b")+"ack")} to go back. You may also input {bold(underline("d")+"efault")} to revert the settings back to their default values.\n\n').lower()
  
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
    print('Input given could not be used. Please try again.')
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
  print(f'\nSong results written in {abspath(fPath)}')
  input()

def addToPlaylist(songContainer:MasterSongContainer):
  print(f'\nTo add these songs onto a playlist, some information of your {bold("Spotify")} is first needed.')
  #Get username
  username = input(f'Please enter your {bold("Spotify username")} (not your display name): ')
  #Get playlist id (help if needed)
  playlist_id = input(f"Now, please enter the id of the playlist you would like the songs added to. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's id: ")
  if(playlist_id.lower() == 'help' or playlist_id.lower() == 'h'):
    print(f"To retrieve a playlist's id, please follow these instructions:\n\t1. Open a web browser and sign into your {bold('Spotify')} account\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This keysmash of characters is your playlist id.")
    playlist_id = input("Please enter the desired playlist's id: ")
  
  sp = SpotifyGateway(username, playlist_id)

  #Test
  print('Making sure playlist is valid and accessible...')
  test = sp.validateInformation()
  if(not test): #Test failed
    print(f'Unfortunately, the test was unsuccesful. Please keep in mind to enter your {bold("username")} and a {bold("playlist id")} that you are the owner of.')
    input(f'Press {bold("Enter")} to try again.\n')
    return addToPlaylist(songContainer)
  #Test passed
  print("Test has successfully passed. Now it's time to add the songs to the playlist.\n")
  input()#Wait for user

  #If timer is >0, run timed adder
  if(S.settingByName('playlistTimer').value > 0):
    sp.addToSpotifyTimed(songContainer.desiredSongs,S.settingByName('playlistTimer').value)
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
  inp = input(f"I'm sure you got some great songs snagged already, but would you like any songs required to be in this data, regardless of the song's uniqueness? {bold('(y/n)')} ").lower()

  if(inp == 'y' or inp == 'yes'):
    print("Sounds good! To do this, get a playlist (or multiple) containing songs you would like to be force added to this data. Please note that timestamp added these songs will be today's date and current time. If you save your song results, the songs added through this method will have a count of 0.")
    input()

    sp = SpotifyGateway(None, None)
    songs = []
    while(True):
      playlist = input(f"Please enter the id of the playlist containing the songs you would like added. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's id, or enter {bold(underline('d')+'one')} when you are finished inputting playlist ids: ")
      if(playlist.lower() == 'help' or playlist.lower() == 'h'):
        print(f"To retrieve a playlist's id, please follow these instructions:\n\t1. Open a web browser and sign into your {bold('Spotify')} account\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This keysmash of characters is your playlist id.")
        playlist = input("Please enter the desired playlist's id: ")
      elif(playlist.lower() == 'done' or playlist.lower() == 'd'):
        break
      else:
        track_results = sp.getPlaylistSongs(playlist)
        if(track_results is None):
          print("The input given could not be read properly, or the playlist given is empty. Remember to enter a playlist id one at a time. Please try again.")
          input()#Wait for user
          continue
        songs += track_results
        print(f"Found {len(track_results)} songs from this playlist.")
        input()#Wait for user
    
    if(len(songs)>0):
      print("Time to add these songs to the data!")
      input()
      pBar = ProgressBar(len(songs), 'Adding songs to dataset')
      for song in songs:
        uri = song['track']['uri']
        if(uri in songContainer.desiredSongs):
          pBar.updateProgress() #Song already in dataset
        else:
          containerAltered = True
          title = song['track']['name']
          artist = song['track']['artists'][0]['name']
          album = song['track']['album']['name']
          songContainer.forceAdd(uri, title, artist, album)
          pBar.updateProgress()
      pBar.finish()
      print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
      input()#Wait for user
    system('cls' if name == 'nt' else 'clear')
  elif(inp == 'n' or inp == 'no'):
    pass
  else:
    print("Sorry, that input couldn't be read, please try again.")
    input()
    return forceAddRemove()

  #Force remove
  while(True):#While loop in case input could not be read
    inp = input(f"Would you like any songs to be forced removed from this data? {bold('(y/n)')} ").lower()
    
    if(inp == 'y' or inp == 'yes'):
      print("Sounds good! To do this, get a playlist (or multiple) containing songs you would like to be force removed from this data.")
      input()

      sp = SpotifyGateway(None, None)
      songs = []
      while(True):
        playlist = input(f"Please enter the id of the playlist containing the songs you would like removed. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's id, or enter {bold(underline('d')+'one')} when you are finished inputting playlist ids: ")
        if(playlist.lower() == 'help' or playlist.lower() == 'h'):
          print(f"To retrieve a playlist's id, please follow these instructions:\n\t1. Open a web browser and sign into your {bold('Spotify')} account\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This keysmash of characters is your playlist id.")
          playlist = input("Please enter the desired playlist's id: ")
        elif(playlist.lower() == 'done' or playlist.lower() == 'd'):
          break
        else:
          track_results = sp.getPlaylistSongs(playlist)
          if(track_results is None):
            print("The input given could not be read properly, or the playlist given is empty. Remember to enter a playlist id one at a time. Please try again.")
            input()#Wait for user
            continue
          songs += track_results
          print(f"Found {len(track_results)} songs from this playlist.")
          input()#Wait for user
      
      if(len(songs)>0):
        print("Time to remove these songs from the data!")
        input()
        prevLen = len(songContainer.desiredSongs)
        pBar = ProgressBar(len(songs), 'Removing songs from dataset')
        for song in songs:
          uri = song['track']['uri']
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
      input("Sorry, that input couldn't be read, please try again. ")
      system('cls' if name == 'nt' else 'clear')
      continue


def welcome():
  """Prints messages that appear at the start of the program."""
  system('cls' if name == 'nt' else 'clear')
  print(f'Welcome to the {bold("Spotify Unique Song Parser")}!')
  print(f'{bold(underline("S")+"tart")}: Start the process to parse through your data')
  print(f'{bold(underline("R")+"esume")}: Use previous program results and skip the parsing')
  print(f'{bold(underline("Set")+"tings")}: View and change settings')
  print(f'{bold(underline("A")+"bout")}: Learn more about this program')
  print(f'{bold(underline("E")+"xit")}: Close the program')
  inp = input('\n\n').lower()
  if(inp == 'start' or inp == 's'):
    return run()
  elif(inp == 'resume' or inp == 'r'):
    return resume()
  elif(inp == 'settings' or inp == 'set'):
    options()
    return welcome()
  elif(inp == 'about' or inp == 'a'):
    about()
    return welcome()
  elif(inp == 'exit' or inp == 'q' or inp == 'e'):
    return
  else:
    print("Couldn't use input. Please try again")
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
  print("First, let's get every file containing songs from your all time Spotify history.")
  print(f'Please input a file location (the file should be called {bold("Streaming_History_Audio")}...{bold(".json")}) or a folder containing the files, and input "Done" when all files have been imported in.')
  while(True):
    inp = input(f'Enter file/folder location or {bold(underline("D")+"one")} here: ')
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
      data = validatedFile(inp)
      if(data):
        dataContainer.append(data)
        print('File succesfully imported.')
        input()

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
  print(f"With adding all the songs to respective containers, {bold(len(songContainer.desiredSongs))} of the {bold(len(songContainer.desiredSongs)+len(songContainer.previousSongs))} songs are potential unique songs listened to in the given range. Let's shrink that number!")

  input()#Wait for user

  #Parse
  print("Now that all songs have been accounted for, let's get parsing!")
  input()
  songContainer.parse()
  
  print()#Spacing

  #Announce results
  print(f"Parsing is now complete! In the end, {bold(len(songContainer.desiredSongs))} are found to be unique songs. That's a lot of songs (probably)!\n")

  input()#Wait for user

  #Force add or remove any songs
  forceAddRemove()

  #Save for later or add to playlist
  while(True):
    inp = input(f"Would you like to {bold(underline('s')+'ave')} the results, {bold(underline('a')+'dd')} the unique songs to a playlist, or do {bold(underline('b')+'oth')} options? \n").lower()
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

  print(f"First, please input the {bold('abolute path')} of your results from previously using this program. Ensure this file has not been altered, otherwise the program may not be able to use that file.")
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
  print(f"All {len(masterSongs.desiredSongs)} songs have been imported! Let's move on.")
  input()#Wait for user

  #Force add/remove
  altered = forceAddRemove(masterSongs)
  
  #Check if results were altered
  if(altered):
    while(True):
      inp = input(f"Because the results were just altered, would you like to {bold(underline('s')+'ave')} the results to a new file, {bold(underline('a')+'dd')} the unique songs to a playlist, or do {bold(underline('b')+'oth')} options?\n").lower()
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
  _importENVVar.instantiate()
  system('cls' if name == 'nt' else 'clear')
  S.init()
  initFormat()
  welcome()