from os import path

def initBold():
  """Tests the bolding function to see if it works on the given device."""
  global boldingFunction
  boldingFunction = True

  #Check if the user already tested for bolding
  if(path.exists('SavedSettings.txt')): #SavedSettings already exists
    with open('SavedSettings.txt', 'r') as file:
      bolded = file.readline()
      if(bolded == 'bolding\n'):
        boldingFunction = True
        return
      elif(bolded == 'no bolding\n'):
        boldingFunction = False
        return
      
  #If file doesn't exist or first line did not give a valid bold setting
  print(f"Before we begin, is {bold('this')} bolded? (y/n)")
  isBolded = input().lower()
  if(isBolded == 'y' or isBolded == 'yes'):
    boldingFunction = True
    print(f'{bold("Thank you")} for checking!')
  elif(isBolded == 'n' or isBolded == 'no'):
    boldingFunction = False
    print(f'{bold("Thank you")} for checking!')
  else:
    print("Sorry, your input could not be understood, please try again.")
    input()
    return initBold()
  
  #Write setting to file
  if(path.exists('SavedSettings.txt')):
    with open("SavedSettings.txt",'r+') as file:
      file.readline() #Skip first line
      kept = file.readlines() #Store other lines
      file.seek(0)
      file.write('bolding\n' if boldingFunction else 'no bolding\n')
      file.writelines(kept)
      file.truncate()
  else:
    with open('SavedSettings.txt', 'w') as file:
      file.write('bolding\n' if boldingFunction else 'no bolding\n')
  print(f'It is recommended to check out the {bold("Settings")} before beginning starting the process.')
  input() #Wait for user
    

def bold(s:str)->str:
  """Formats to bold given string when printed in console"""
  ###Look into blessed to make UI a bit more pretty (may need big overhaul...)
  return f'\u001b[1m{s}\u001b[0m' if boldingFunction else f'"{s}"'

if __name__ == "__main__":
  initBold()
  print(boldingFunction)
  print(f"WOAHHHHH {bold('BOLDING')}")