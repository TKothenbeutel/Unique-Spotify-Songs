import json
from os import listdir
#from Helpers.Formatting import *
from Formatting import *

def validatedFile(file, ext = '.json') -> str:
  """Get file inputted by user and ensure it can be used."""
  #Check if extension is correct
  if(file[0-len(ext):] != ext):
    print(f'Please give the absolute file location with extention {bold(ext)}.')
  else:
    #Attempt to open and close file
    try:
      fileTest = open(file, 'r')
      fileTest.close()
      if(ext == '.json'):
        return readJSON(file)
      else:
        return file
    #File can not be found at specified location
    except FileNotFoundError:
      print(f"File specified cannot be found. Please use its {bold('absolute location')} and try again.")
      return None
    #Unaccounted for error
    except Exception as e:
      print(f'Unfortanetely, the program ran into error {bold(e)}. Please try again.')
      return None

def validatedFolder(folder:str) -> list:
  """Get correct files inside given folder."""
  try:
    files = listdir(folder)
    spotify_audio_files = []
    print("These files were successfully imported:")
    for i in files:
      if(i.endswith(".json") and i[:23] == "Streaming_History_Audio"):
        if('\\' in folder):
          i = folder + '/' + i
        else:
          i = folder + '/' + i
        dump = readJSON(i)
        if(dump is not None):
          print(i)
          spotify_audio_files.append(dump)
    return spotify_audio_files
  except FileNotFoundError:
    print("Could not find the folder given. Please try again.")

def readJSON(file:str):
  """Read JSON files and converts it to a python dictionary"""
  try:
    with open(file,'r',encoding='utf-8') as f:
      data = json.load(f)
    return data
  except:
    print(f"Unable to parse file {file}. Please try again.")
    return None
  
def dictToJSON(dictionary:dict):
  return json.dumps(dictionary, indent=4)



if __name__ == "__main__":
  #validatedFile("C:\Users\tkong\Downloads\Spotify Data\AllTime_my_spotify_data-2024\Spotify Extended Streaming History\Streaming_History_Audio_2020-2022_1.json".replace('\\','/'))
  #k = input()
  #print(validatedFile(k))
  '''
  diction = {'hello': 20, 'Hi':123, 'Woah':'heap'}
  fPath = f"./Results/test.json"
  resultToJSON = dictToJSON(diction)
  with open(fPath,'w') as file:
    file.write(resultToJSON)
  '''
  folder = "/workspaces/Unique-Spotify-Songs/Spotify Extended Streaming History"
  data = validatedFolder(folder)
  #print(data)
  files = listdir(folder)
  #with open(folder+'/'+files[0],'r',encoding='utf-8') as f:
    #print(json.load(f))