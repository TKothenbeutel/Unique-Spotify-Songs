import json

def validatedFile(file, ext = '.json') -> str:
  """Get file inputted by user and ensure it can be used."""
  #Check if extension is correct
  if(file[0-len(ext):] != ext):
    print(f'Please give the absolute file location with extention {ext}.')
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
      print("File specified cannot be found. Please use its absolute location and try again.")
      return None
    #Unaccounted for error
    except Exception as e:
      print(f'Unfortanetely, the program ran into error {e}. Please try again.')
      return None

def readJSON(file:str):
  """Read JSON files and converts it to a python dictionary"""
  try:
    with open(file,'r',encoding='utf-8') as f:
      data = json.load(f)
    return data
  except:
    print("Unable to parse file. Please try again.")
    return None
  
def dictToJSON(dictionary:dict):
  return json.dumps(dictionary, indent=4)



if __name__ == "__main__":
  #validatedFile("C:\Users\tkong\Downloads\Spotify Data\AllTime_my_spotify_data-2024\Spotify Extended Streaming History\Streaming_History_Audio_2020-2022_1.json".replace('\\','/'))
  #k = input()
  #print(validatedFile(k))
  diction = {'hello': 20, 'Hi':123, 'Woah':'heap'}
  fPath = f"./Results/test.json"
  resultToJSON = dictToJSON(diction)
  with open(fPath,'w') as file:
    file.write(resultToJSON)
  
  pass