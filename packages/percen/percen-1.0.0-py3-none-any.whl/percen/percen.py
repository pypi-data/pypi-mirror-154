import random

class Percen:

  def __init__(self):
    pass

  def general(self, percentage : int) -> True or False:
    #확률값이 1이상인지 체크
    if percentage <= 0:
      raise ValueError('Please enter a number greater than or equal to 1 for the probability value!')
      
    check_number = random.randrange(0, 101)
    if percentage > check_number:
      return True
    else:
      return False

  def detail(self, percentage : int) -> dict:
    #확률값이 1이상인지 체크
    if percentage <= 0:
      raise ValueError('Please enter a number greater than or equal to 1 for the probability value!')
      
    check_number = random.randrange(0, 101)
    if percentage > check_number:
      result = {
        'result' : True,
        'percentage' : f"{percentage}%",
        'check_number' : check_number
      }
      return result
    else:
      result = {
        'result' : False,
        'percentage' : f"{percentage}%",
        'check_number' : check_number
      }
      return result