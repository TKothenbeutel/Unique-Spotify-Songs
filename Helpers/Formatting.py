from os import path

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

if __name__ == "__main__":
  initFormat()
  print(formatFunction)
  print(f"WOAHHHHH {bold('BOLDING')}")
  print(f"HOLLOY COW {underline('WE UNDERLINE')}")