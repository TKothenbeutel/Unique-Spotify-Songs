from os import path
import shutil
import textwrap
from typing import Literal

def initFormat():
  CODESPACEOVERRIDE = True

  """Tests the bolding function to see if it works on the given device."""
  global formatFunction
  formatFunction = True

  #Check if the user already tested for bolding
  if(path.exists('SavedSettings.txt')): #SavedSettings already exists
    with open('SavedSettings.txt', 'r') as file:
      bolded = file.readline()
      if(bolded == 'format\n'):
        formatFunction = True
        return
      elif(bolded == 'no format\n'):
        formatFunction = False
        return

  if(not CODESPACEOVERRIDE):    
    #If file doesn't exist or first line did not give a valid bold setting
    print(f"Before we begin, is {bold('this')} bolded and {underline('this')} underlined? (y/n)")
    isBolded = input().lower()
    if(isBolded == 'y' or isBolded == 'yes'):
      formatFunction = True
      print(f'{bold("Thank you")} for checking!')
    elif(isBolded == 'n' or isBolded == 'no'):
      formatFunction = False
      print(f'{bold("Thank you")} for checking!')
    else:
      print("Sorry, your input could not be understood, please try again.")
      input()
      return initFormat()
  else:
    #Write setting to file
    if(path.exists('SavedSettings.txt')):
      with open("SavedSettings.txt",'r+') as file:
        file.readline() #Skip first line
        kept = file.readlines() #Store other lines
        file.seek(0)
        file.write('format\n' if formatFunction else 'no format\n')
        file.writelines(kept)
        file.truncate()
    else:
      with open('SavedSettings.txt', 'w') as file:
        file.write('format\n' if formatFunction else 'no format\n')
  
  #Write setting to file
  if(path.exists('SavedSettings.txt')):
    with open("SavedSettings.txt",'r+') as file:
      file.readline() #Skip first line
      kept = file.readlines() #Store other lines
      file.seek(0)
      file.write('format\n' if formatFunction else 'no format\n')
      file.writelines(kept)
      file.truncate()
  else:
    with open('SavedSettings.txt', 'w') as file:
      file.write('format\n' if formatFunction else 'no format\n')
  print(f'It is recommended to check out {bold("Settings")} before starting the process.')
  input() #Wait for user
    

def bold(s:str)->str:
  """Formats to bold given string when printed in console"""
  ###Look into blessed to make UI a bit more pretty (may need big overhaul...)
  return f'\u001b[1m{s}\u001b[0m' if formatFunction else f'"{s}"'

def underline(s:str)->str:
  """Formats to underline given string when printed in console. Note: only letters can be underlined"""
  return '\u0332'.join(s + ' ')[:-1] if formatFunction else f'_{s}_'


def wrap_text_to_terminal(text,sep: str | None = " ",end: str | None = "\n"):
    """Wraps text to the current terminal width using textwrap."""
    try:
        terminal_size = shutil.get_terminal_size()  #Get terminal dimensions
        width = terminal_size.columns #Extract the width
    except (AttributeError, OSError):
        #Fallback if breaks (105 is default for my terminal)
        width = 105
    
    wrapped_text = textwrap.fill(text, width=width) # Wrap the text
    return builtins.print(wrapped_text, sep=sep, end=end)

import builtins
def print(value,
    sep: str | None = " ",
    end: str | None = "\n") -> None:
  return wrap_text_to_terminal(str(value),sep=sep,end=end)


if __name__ == "__main__":
  initFormat()
  print(formatFunction)
  print(f"WOAHHHHH {bold('BOLDING')}")
  print(f"HOLLOY COW {underline('WE UNDERLINE')}")
  print("Omg this is such a long text woah i dont even know what to type this is so very long i hope this text wrapping stuff will work properly man let's just hope it works good okay yeah so like good luck i guess i dont know how well this will work.")
  input()
  print("Omg AGAIN this is such a long AGAIN text woah i dont even AGAIN know what to type this AGAIN is so very long i hope AGAIN this text wrapping stuff will work AGAIN properly man let's just hope it works good okay AGAIN yeah so like good luck i guess i dont know how well this AGAIN will work AGAIN.")
  print(123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890)