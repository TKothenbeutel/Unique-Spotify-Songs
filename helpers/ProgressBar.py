#Class that will print out a progress bar on the same line of terminal
#Used with other classes so the user can see the progress of the parsing
#Example of progress bar: =====-----  50/100; Removing duplicates
#To instantiate, instance will be created, and every interation of whatever
#will call updateProgress, which will add one and rewrite the bar on the terminal
#In total, outer function should create class, call updateProgress, and call finish

from helpers.Formatting import *

class ProgressBar():
  def __init__(self, items: int, description: str, starting_num = 0):
    self.description = description
    self.items = items
    self.progress = starting_num
    self.bar_lines = 10
    self.displayProgress()
  
  def displayProgress(self) -> None:
    #Get number of bars now completed
    completedBars = int((self.progress/self.items)*10)
    message = '='*completedBars + '-'*(self.bar_lines-completedBars)
    #Add remaining elements
    message += f'\t{self.progress}/{self.items}; {bold(self.description)}'
    #Print onto terminal
    print(message,end='\r')

  def updateProgress(self, value=1) -> None:
    self.progress += value
    self.displayProgress()

  def finish(self) -> None:
    print('          ',end='\r') #Remove '=' artifacts
    print(f'{underline("Complete")}\t{self.progress}/{self.items}; {bold(self.description)}')
    #'Destroy' class
    self.description = None
    self.items = None
    self.progress = None
    self.bar_lines = None

if __name__ == "__main__":
  initFormat()
  from time import sleep
  total_items = 100
  testBar = ProgressBar(total_items, "Test Bar")
  for i in range(total_items):
    sleep(0.03)
    testBar.updateProgress()
  testBar.finish()