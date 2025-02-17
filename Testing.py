from time import sleep


if __name__ == "__main__":
  class test(object):
    def __init__(self):
      self.dic = {}

    def __contains__(self, x):
      return x in self.dic
  
    def __iter__(self):
      for i in self.dic.keys():
        yield i

    def __delitem__(self, key):
      del self.dic[key]
  """
  testDict = test()
  testDict.dic['hi'] = 12
  testDict.dic['what'] = 11
  del testDict['hi']
  print(testDict.dic)

  testerrr = input('What: ')
  print(f'You just said {testerrr}. You stupid')
  for i in range(3):
    print(f'{i} seconds have passed',end='\r')
    sleep(1)
  print(f'{3} seconds have passed')
  dontLeaveAha = input()

  def yielder(st):
    for i in st:
      yield i
  st = {1,2,3,4,5,6,7,8,9}
  for i in list(yielder(st)):
    print(i)
    if i == 4 or i == 6:
      st.remove(i)
  print(st)
  """
  mo = {12:0,34:0,56:0}
  for i in [x for x in mo]:
    print(i)
