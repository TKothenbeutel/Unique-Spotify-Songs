"""
File that creates and holds global variable settings.
settings contains a dictionary with setting name key and
a _Setting class value. This file also houses the functions to update
the value and print each setting. Settings are as follows:

*Base*
**beginningDate**: 
  The date that a song must be first listened to for it possible to be added to the collection. Please follow yyyy-mm-dd format. Default is one year from today.
**minCount**:
  Remove songs that have been listened to fewer times than this number. Default is 2.
**minMS**: 
  Minimum number of milliseconds (1,000ms = 1 second) the song needs to be listened to in one sitting for it to count in this data. Note: track fully finishing will override this setting. Default is 30,000.
**songPreference**: 
  If a song has multiple IDs (usually from it being on different albums), have it keep the oldest, newest, both copies, or ask which of the IDs to keep every time. Default is ask.
*Extras*
**minCountOverride**: 
  If a song has been listened to this many more times in the collection range than out of it, then it will be included in the collection. If this number is -1, it will not do this. Default is -1.
**earliestDate**: 
  The earliest date this program will parse through in the given data. Please follow yyyy-mm-dd format. Default is 2000-01-01.
**lastDate**: 
  The last date this program will parse through in the given data. Please follow yyyy-mm-dd format. Default is tomorrow's date.
**playlistAddTimer**: 
  Amount of time (in seconds) to wait in between adding each song to the given playlist so that the 'sort by date added' feature will work properly on Spotify. Default is 0.
**songGracePeriod**: 
  Period at which a song has a chance to be included in the playlist, regardless if it reaches minCount (will still be rejected if it was listened to before earlyRange). The range starts from the given day through today. Please follow yyyy-mm-dd format. Default is a week from today.
**universalMinCount**: 
  Determines if songs before beginningDate should also meet the minimum count requirement to be looked at. Default is False.
"""

from os import system, name
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Helpers.Formatting import *

class _Setting():
  def __init__(self, name:str, value, message:str, possibleOptions=None, minVal=None, maxVal=None):
    self.index =  ''
    self.name = name
    self.value = value
    self.message = message
    self.options = possibleOptions
    self.min = minVal
    self.max = maxVal

  def setIndex(self, index: str):
    self.index = index
  
  def updateValue(self, value):
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
    tab = ' '*5
    spaces = ' ' * (19-len(self.name))
    message = (f'{self.index}  {underline(self.name)}:{spaces}|{tab}')
    if(self.options): #Setting has multiple options that don't fit type
      for i in range(len(self.options)):
        if(self.value == i):
          message += f'{bold(self.options[i])}{tab}'
        else:
          message += f'{self.options[i]}{tab}'
    elif(type(self.value) == bool):
      if(self.value):
        message += f'{bold("True")}{tab}False'
      else:
        message += f'True{tab}{bold("False")}'
    else:
      message += f'{bold(self.value)}'
    return message

today = datetime.today().date()

EXTRA_START = 4 #First index of extras settings 

def init():
  global settings

  #Base
  beginningDate = _Setting('beginningDate',today-relativedelta(year=today.year-1),"The date that a song must be first listened to for it possible to be added to the collection. Please follow yyyy-mm-dd format. Default is one year from today.")
  minCount = _Setting('minCount',2,"Remove songs that have been listened to fewer times than this number. Default is 2.")
  minMS = _Setting('minMS',30_000,"Minimum number of milliseconds (1,000ms = 1 second) the song needs to be listened to in one sitting for it to count in this data. Note: track fully finishing will override this setting. Default is 30,000.")
  songPreference = _Setting('songPreference',3,"If a song has multiple IDs (usually from it being on different albums), have it keep the oldest, newest, both copies, or ask which of the IDs to keep every time. Default is ask.",('oldest','newest','both','ask'))

  #Extras
  minCountOverride = _Setting('minCountOverride',-1,"If a song has been listened to this many more times in the collection range than out of it, then it will be included in the collection. If this number is -1, it will not do this. Default is -1.")
  earliestDate = _Setting('earliestDate',datetime(2000,1,1).date(),"The earliest date this program will parse through in the given data. Please follow yyyy-mm-dd format. Default is 2000-01-01.")
  lastDate = _Setting('lastDate',today+relativedelta(days=1),"The last date this program will parse through in the given data. Please follow yyyy-mm-dd format. Default is tomorrow's date.")
  playlistAddTimer = _Setting('playlistAddTimer',0,"Amount of time (in seconds) to wait in between adding each song to the given playlist so that the 'sort by date added' feature will work properly on Spotify. Default is 0.")
  songGracePeriod = _Setting('songGracePeriod',today-relativedelta(days=7),"Period at which a song has a chance to be included in the playlist, regardless if it reaches minCount (will still be rejected if it was listened to before earlyRange). The range starts from the given day through today. Please follow yyyy-mm-dd format. Default is a week from today.")
  universalMinCount = _Setting('universalMinCount',False,"Determines if songs before beginningDate should also meet the minimum count requirement to be looked at. Default is False.")
  

  settings = [
              beginningDate,
              minCount,
              minMS,
              songPreference,
              minCountOverride,
              earliestDate,
              lastDate,
              playlistAddTimer,
              songGracePeriod,
              universalMinCount
            ]
  
  for i in range(len(settings)):
    if(i < 9):
      settings[i].setIndex(f'{i+1}. ')
    else:
      settings[i].setIndex(f'{i+1}.')

def settingByName(name:str):
  for setting in settings:
    if setting.name == name:
      return setting
  return None
  


def printSettings():
  print(f'Base:')
  for i in range(len(settings)):
    if(i == EXTRA_START):
      print(f'\nExtra:')
    print(settings[i])
  print()

def printAbouts():
  print(f'Base:')
  for i in range(len(settings)):
    if(i == EXTRA_START):
      print(f'\nExtra:')
    print(settings[i].printWithAbout())

def updateValue(setting:str, value:str):
  """Verifies value and setting given, then updates setting."""
  #Convert setting to int
  if(setting[-1] == '.'): #Remove period
    setting = setting[:-1]

  if(setting.isdecimal()):
    setting = int(setting) -1
  else:
    print(f'Please input a {bold("number")} corresponding to the setting, followed by a {bold("value")}.')
    return input()
  
  #Verify setting typed exists
  if(setting < 0 or setting > len(settings)):  #Setting does not exist
    print(f'{bold(setting+1)} is not a possible setting option.')
    return input()

  sName = settings[setting].name

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
      settings[setting].updateValue(newNum)
    except:
      print(f'{bold(value)} is not a valid choice for setting {bold(sName)}.')
      return input()
  elif(type(settings[setting].value) == type(value)): #Value is correct type
    settings[setting].updateValue(value)
  else: #Value is not correct
    print(f'{bold(sName)} must take input of type {bold(type(settings[setting].value))}.')
    return input()
  return  
  

if __name__ == "__main__":
  #Initialize settings
  init()
  #Print settings
  printSettings()
  
  #Pass cases
  updateValue('2','20')
  updateValue('2','-20')  #Snap to -1
  updateValue('10.','2.5')
  updateValue('3','Oldest')
  updateValue('4','2001-09-11')
  updateValue('8.', 'TRUE')
  #Fail cases
  updateValue('0','Null')
  updateValue('2.','1999-05-12')
  updateValue('3','never')
  #Print about section
  printAbouts()
