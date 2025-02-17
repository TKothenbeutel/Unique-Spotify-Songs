"""
File that creates and holds global variable settings.
settings contains a dictionary with setting name key and
a _Setting class value. This file also houses the functions to update
the value and print each setting. Settings are as follows:
**minCount**: Remove songs that have been listened to less times than this number. Default is 2.
**countOverride**: If number is greater than the difference of times listened in range than outside
  of range, then the song will be included in playlist. If -1, it will not do this. Default is 1.
**songPreference**: If song has multiple ids (from it being on different albums), have it keep the
  oldest, newest, both of them, or ask which of the ids to keep every time. Default is ask'
**earlyRange**: Date that the song must be first listened to for it to be possible to be added to
  playlist. Please follow yyyy-mm-dd format. Default is one year from today.
**lastDate**: Last date the program will look at for songs. Please follow yyyy-mm-dd format. Default
  is tomorrow's date.
**earlyDate**: Earliest date the program will look at for songs. Please follow yyyy-mm-dd format. 
  Default is 2000-01-01.
**minMS**: Minimum number of milliseconds the song needs to be played for it to count. Note track fully
  finishing will override this setting. Default is 30,000 (30 seconds).
**prevMinCount**: Determines if songs before the earlyRange should also meet the minumum count
  requirement to be looked at. Default is False.
**gracePeriod**: Period at which the song has a chance to be included in the playlist, regardless of
  how many times the song was listened to. Range starts at day given through today, to allow recent
  new songs a chance to make it in. Please follow yyyy-mm-dd format. Default is a week from today.
**playlistTimer**: Amount of time to wait in between adding each song to given playlist so that the
  'sort by date added' feature will work properly on Spotify. Default is 0.

"""

from os import system, name
from datetime import datetime
from dateutil.relativedelta import relativedelta

class _Setting():
  def __init__(self, name:str, value, message:str, possibleOptions=None, minVal=None, maxVal=None):
    self.name = name
    self.value = value
    self.message = message
    self.options = possibleOptions
    self.min = minVal
    self.max = maxVal
  
  def UpdateValue(self, value):
    if(self.min is not None and value < self.min):
      self.value = self.min
    elif(self.max is not None and value > self.max):
      self.value = self.max
    else:
      self.value = value

  def printWithAbout(self) -> str:
    message = str(self) + '\n'
    message += '   ' + self.message + '\n'
    return message

  def __repr__(self) -> str:
    message = (self.name + ":\t|\t") if len(self.name)>=8 else (self.name + ":\t\t|\t")
    if(self.options): #Setting has multiple options that don't fit type
      for i in range(len(self.options)):
        if(self.value == i):
          message += f'"{self.options[i]}"\t'
        else:
          message += f' {self.options[i]} \t'
    elif(type(self.value) == bool):
      if(self.value):
        message += f'"True"\t False '
      else:
        message += f' True \t"False"'
    else:
      message += f'{self.value}'
    return message

today = datetime.today().date()

def init():
  global settings
  
  minCount = _Setting('minCount',2,'Remove songs that have been listened to less times than this number. Default is 2.', minVal=1)
  countOverride = _Setting('countOverride',1,'If number is greater than the difference of times listened in range than outside of range, then the song will be included in playlist. If -1, it will not do this. Default is 1.',minVal=-1)
  songPreference = _Setting('songPreference',3,'If song has multiple ids (from it being on different albums), have it keep the oldest, newest, both of them, or ask which of the ids to keep every time. Default is ask',('oldest','newest','both','ask'))
  earlyRange = _Setting('earlyRange',today-relativedelta(year=today.year-1),'Date that the song must be first listened to for it to be possible to be added to playlist. Please follow yyyy-mm-dd format. Default is one year from today.')
  lastDate = _Setting('lastDate',today+relativedelta(days=1),"Last date the program will look at for songs. Please follow yyyy-mm-dd format. Default is tomorrow's date.")
  earlyDate = _Setting('earlyDate',datetime(2000,1,1).date(),'Earliest date the program will look at for songs. Please follow yyyy-mm-dd format. Default is 2000-01-01.')
  minMS = _Setting('minMS', 30000,'Minimum number of milliseconds the song needs to be played for it to count. Note track fully finishing will override this setting. Default is 30,000 (30 seconds).',minVal=0)
  prevMinCount = _Setting('prevMinCount', False, 'Determines if songs before the earlyRange should also meet the minumum count requirement to be looked at. Default is False.')
  gracePeriod = _Setting('gracePeriod',today-relativedelta(days=7),'Period at which the song has a chance to be included in the playlist, regardless of how many times the song was listened to. Range starts at day given through today, to allow recent new songs a chance to make it in. Please follow yyyy-mm-dd format. Default is a week from today.')
  playlistTimer = _Setting('playlistTimer',0.0,"Amount of time to wait in between adding each song to given playlist so that the 'sort by date added' feature will work properly on Spotify. Default is 0.",minVal=0.0)

  settings = {'minCount':minCount,
              'countOverride':countOverride,
              'songPreference':songPreference,
              'earlyRange':earlyRange,
              'lastDate':lastDate,
              'earlyDate':earlyDate,
              'minMS':minMS,
              'prevMinCount':prevMinCount,
              'gracePeriod':gracePeriod,
              'playlistTimer':playlistTimer}
  


def printSettings():
  system('cls' if name == 'nt' else 'clear')
  for i in settings:
    print(settings[i])
  print()

def printAbouts():
  system('cls' if name == 'nt' else 'clear')
  for i in settings:
    print(settings[i].printWithAbout())

def updateValue(setting:str, value:str):
  """Verifies value and setting given, then updates setting."""
  #Verify setting typed exists
  if(not setting in settings):  #Setting does not exist
    print(f'{setting} is not a valid setting.')
    return

  #Convert value to proper type
  if(value.count('-') == 2):  #Value may be datetime
    try:
      date = value.split('-')
      value = datetime(int(date[0]),int(date[1]),int(date[2])).date()
    except:
      pass  #Could not convert to datetime

  elif(value[0]=='-' and len(value) > 1):  #Value may be a negative number
    if(value[1:].isdigit()):
      value = int(value)
    elif(value[1:].replace('.','',1).isdigit()):
      value = float(value)

  elif(value.isdigit()):  #Value may be an int
    value = int(value)

  elif(value.replace('.','',1).isdigit()):  #Value may be a float
    value = float(value)

  elif(value.lower() == 'true'):
    value = True
  elif(value.lower() == 'false'):
    value = False

  #Update value if matches type
  if(settings[setting].options):  #Setting has custom options
    try:
      newNum = settings[setting].options.index(value.lower())
      settings[setting].UpdateValue(newNum)
    except:
      print(f'{value} is not a valid choice for setting {setting}.')
      input('Press "Enter" to return')
      return printSettings()
  elif(type(settings[setting].value) == type(value)): #Value is correct type
    settings[setting].UpdateValue(value)
  else: #Value is not correct
    print(f'{setting} must take input of type {type(settings[setting].value)}.')
    input('Press "Enter" to return')
    return printSettings()
  printSettings()  
  

if __name__ == "__main__":
  #Initialize settings
  init()
  #Print settings
  printSettings()
  '''
  #Pass cases
  updateValue('countOverride','20')
  updateValue('countOverride','-20')
  updateValue('playlistTimer','2.5')
  updateValue('songPreference','Oldest')
  updateValue('earlyRange','2001-09-11')
  updateValue('prevMinCount', 'TRUE')
  #Fail cases
  updateValue('notASetting','Null')
  updateValue('countOverride','1999-05-12')
  updateValue('songPreference','never')
  #Print about section
  printAbouts()
  '''