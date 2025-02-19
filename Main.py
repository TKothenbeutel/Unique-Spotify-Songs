import _importENVVar

from os import system, name
from DataParse import validatedFile, dictToJSON, validatedFolder
import Settings as S
from SongStruct import MasterSongContainer
from ProgressBar import ProgressBar
from os.path import abspath
from datetime import datetime
from SpotifyFunctions import SpotifyGateway

def bold(s:str)->str:
  """Formats to bold given string when printed in console"""
  ###Look into blessed to make UI a bit more pretty (may need big overhaul...)
  return f'\u001b[1m{s}\u001b[0m' if True else f'"{s}"'

def currentTime():
  return f'{datetime.today().date()}_{str(datetime.today().time()).replace(":","-")[:8]}'

def exportSettings():
  fPath = f"savedSettings.txt"
  with open(fPath,'w') as file:
    for setting in S.settings:
      if(setting.options is not None): #Get index of option
        file.write(f'{setting.name}: {setting.options[setting.value]}\n')
      else:
        file.write(f'{setting.name}: {setting.value}\n')
  print(f'Settings saved at {abspath(fPath)}. Please do not edit or relocate file.')
  input(f'Press {bold("Enter")} to return')
  return

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
  except FileNotFoundError:
    print('Could not find saved setting file.')
  except Exception as e:
    print(f'Could not import settings due to an error ({e}).')
  input(f'Press {bold("Enter")} to return')
  return

def options():
  """Displays the settings and takes in user input to alter them."""
  S.printSettings()
  while(True):
    inp = input(f'You may change a setting by inputting {bold("{number} {value}")}, input {bold("about")} to learn more about each setting, {bold("export")} to export current settings, {bold("import")} to import previously saved settings, or input {bold("back")} to go back.\n')
    
    if(inp.lower() == 'about'): #About
      print()
      S.printAbouts()
    elif(len(inp.split(' ')) == 2): #Change setting
      inp = inp.split(' ')
      print()
      S.updateValue(inp[0], inp[1])
      inp = ''
    elif(inp.lower() == 'export'):  #Export
      exportSettings()
      S.printSettings()
    elif(inp.lower() == 'import'):  #Import
      importSettings()
      S.printSettings()
    elif(inp.lower() == 'back'):  #Back
      return
    else:
      print('Input given could not be used. Please try again.')

def about():
  system('cls' if name == 'nt' else 'clear')
  print(f'Made by {bold("Taylor Kothenbeutel")}')
  input(f'Press {bold("Enter")} to return')

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

def addToPlaylist(songContainer:MasterSongContainer):
  print(f'\nTo add these songs onto a playlist, some information of your {bold("Spotify")} is first needed.')
  #Get username
  username = input(f'Please enter your {bold("Spotify username")} (not your display name): ')
  #Get playlist id (help if needed)
  playlist_id = input(f"Now, please enter the id of the playlist you would like the songs added to. Enter {bold('help')} for information on how to retrieve a playlist's id: ")
  if(playlist_id.lower() == 'help'):
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
  
  #If timer is >0, run timed adder
  if(S.settingByName('playlistTimer').value > 0):
    sp.addToSpotifyTimed(songContainer.desiredSongs,S.settingByName('playlistTimer').value)
  #Else run batch adder
  else:
    sp.addToSpotifyBatch(songContainer.desiredSongs)
  print('All songs successfully added to the playlist.')
  return


def welcome():
  """Prints messages that appear at the start of the program."""
  system('cls' if name == 'nt' else 'clear')
  print(f'Welcome to the {bold("Spotify Unique Song Parser")}!')
  print(f'{bold("Start")}: Gather you Spotify data and parse through it')
  print(f'{bold("Settings")}: View and change the settings')
  print(f'{bold("About")}: Learn more about this program')
  print(f'{bold("Exit")}: Close the program')
  inp = input('\n\n').lower()
  if(inp == 'start'):
    return run()
  elif(inp == 'settings'):
    options()
    print()
    return welcome()
  elif(inp == 'about'):
    about()
    print()
    return welcome()
  elif(inp == 'exit'):
    return
  else:
    print("Couldn't use input. Please try again\n")
    return welcome()
    
def run():
  #Major variables
  dataContainer = [] #Each item will contain a dictionary of what the JSON file had
  songContainer = MasterSongContainer() #Settings transfer over
  
  system('cls' if name == 'nt' else 'clear')
  print("Let's begin!\n")

  #Gather files
  print("First, let's get every file containing songs from your all time Spotify history.")
  print(f'Please input a file location (the file should be called {bold("Streaming_History_Audio")}....json) or a folder containing the files, and input "Done" when all files have been imported in.')
  while(True):
    inp = input(f'Enter file location or {bold("Done")} here: ')
    if(inp.lower() == 'done'):
      break
    if(inp[0] == '"' and inp[-1] == '"'): #Disregard quotations around location
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
  print(f"With adding all the songs to respective containers, {bold(str(len(songContainer.desiredSongs)))} of the {bold(str(len(songContainer.desiredSongs)+len(songContainer.previousSongs)))} songs are potential unique songs listened to in the given range. Let's shrink that number!")

  input()#Wait for user

  #Parse
  print("Now that all songs have been accounted for, let's get parsing!")
  songContainer.parse()
  
  print()#Spacing

  #Announce results
  print(f"Parsing is now complete! In the end, {bold(str(len(songContainer.desiredSongs)))} are found to be unique songs. That's a lot of songs (probably)!\n")

  #Save for later or add to playlist
  while(True):
    inp = input(f"Would you like to {bold('save')} the results, {bold('add')} the unique songs to a playlist, or do {bold('both')} options? ").lower()
    if(inp == 'save'):
      saveResults(songContainer)
      break
    elif(inp == 'add'):
      addToPlaylist(songContainer)
      break
    elif(inp == 'both'):
      saveResults(songContainer)
      addToPlaylist(songContainer)
      break
    else:
      print(f'{inp} is not a valid option. Please respond with either {bold("save")}, {bold("add")}, or {bold("both")} to choose.')

  #After saving/adding/bothing
  print(f'This program is now finished. {bold("Thank you for using it!")}')
  input()
  return


if __name__ == "__main__":
  _importENVVar.instantiate()
  S.init()
  welcome()