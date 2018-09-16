#!/usr/bin/python

import sys,time;
from random import randint;
from random import shuffle;
from termcolor import colored;
import matplotlib.pyplot as plt;
from matplotlib import cm;
from stats import Stats;
import argparse


user_name = "Ananya";



class Operator():
  def __init__(self):
    self.name = "noop"
    self.type = "binary"

class Multiply(Operator):
  def __init__(self):
    Operator.__init__(self)
    self.name = "multiply"
    self.symbol = "x"
    self.default_param1_range = [0,10]
    self.default_param2_range = [0,10]

  def evaluate(self, param1, param2):
    return param1 * param2
  
  def get_question(self, param1, param2):
    return "%d %s %d " % (param1, self.symbol, param2)    
  

class Factors(Operator):
  def __init__(self):
    Operator.__init__(self)
    self.name = "factors"
    self.symbol = " factors "
    self.type = "unary"
    self.default_param1_range = [0,100]

  def evaluate(self, param1, param2):
    return param1 * param2

  def get_question(self, param1, param2):
    return "Factors of %d" % (param1 * param2)    

class Add(Operator):
  def __init__(self):
    Operator.__init__(self)
    self.name = "add"
    self.symbol = "+"
    self.default_param1_range = [0,10]
    self.default_param2_range = [1,2]

  def evaluate(self, param1, param2):
    return param1 + param2;
  
  def get_question(self, param1, param2):
    return "%d + %d " % (param1, param2)    

class Subtract(Operator):
  def __init__(self):
    Operator.__init__(self)
    self.name = "subtract"
    self.symbol = "-"
    self.default_param1_range = [0,10]
    self.default_param2_range = [1,2]

  def evaluate(self, param1, param2):
    return param1 - param2

  def get_question(self, param1, param2):
    return "%d - %d " % (param1, param2)    

class Divide(Operator):
  def __init__(self):
    Operator.__init__(self)
    self.name = "divide"
    self.symbol = "/"
    self.default_param1_range = [0,10]
    self.default_param2_range = [1,2]

  def evaluate(self, param1, param2):
    return param1 / param2



def say_bye():
  sys.stdout.write("See you next time %s!\n" % user_name);

def exit(operator, stats):
  stats.print_stats(operator)
  say_bye()
  sys.exit(0)


def get_range(string):
  l = string.split(':')
  int_range = map(lambda x:int(x), l)
  return int_range


def main():
  global user_name
  parser = argparse.ArgumentParser()
  operator_group = parser.add_mutually_exclusive_group(required=True)
  
  operator_group.add_argument('-a','--add', 
    help="use for addition questions", 
      action='store_true')
  operator_group.add_argument('-m','--multiply', 
    help="use for multiplication questions", 
    action='store_true')
  operator_group.add_argument('-s', '--subtract', 
    help="use for subtraction questions", 
    action='store_true')
  operator_group.add_argument('-d','--divide', 
    help="use for division questions", 
    action='store_true')
  operator_group.add_argument('-f','--factors', 
    help="use for division questions", 
    action='store_true')
  parser.add_argument('-n','--name', 
    help="use this name for the test taker",
    default='Ananya')


  parser.add_argument('-p', '--parameter',
    help = "parameters for questions",
    action='append')

  args = parser.parse_args(sys.argv[1:])
  print args

  operator = None
  if args.add == True:
    operator = Add()
  elif args.multiply == True:
    operator = Multiply()
  elif args.subtract == True:
    operator = Subtract()
  elif args.divide == True:
    operator = Divide()
  elif args.factors == True:
    operator = Factors()

  params = args.parameter
  param1_range = get_range(params[0])
  param2_range = get_range(params[1])
  user_name = args.name

  if (param1_range == None):
    param1_range = operator.default_param1_range
  if param2_range == None:
    param2_range = operator.default_param2_range
  stats = Stats(param1_range, param2_range)


  questions = []
  for param1 in range(param1_range[0], param1_range[1]+1):
    for param2 in range(param2_range[0], param2_range[1]+1):
      questions.append((param1, param2))
  shuffle(questions)
  
  total_questions = len(questions)
  
  for index, question in enumerate(questions):
    param1=question[0]
    param2=question[1]
    ask_question(index, total_questions, operator, param1, param2, stats)
  exit(operator, stats)


def ask_question(current_index, total, operator, param1, param2, stats):
    correct = False
    t0 = time.time()
    while (correct != True):
      sys.stdout.write("%d of %d> %s = " % (current_index, total, operator.get_question(param1, param2)))
      ans = sys.stdin.readline().strip()
      time_diff = time.time() - t0
      if (ans == "exit") or (ans == "bye") :
        exit(operator, stats)
      if (ans == "pause") or (ans == "wait"):
        while (ans != "ready"):
          sys.stdout.write("ok... I'm waiting.. type start when you are ready.. ")
          ans = sys.stdin.readline().strip()
        t0 = time.time()
      else:
        number_ans = int(ans)
        stats.add_statistic(operator, param1,param2,number_ans,time_diff)
        if (operator.evaluate(param1, param2) != number_ans):
          print colored("Oops...",'red')
        else:
          correct = True
          print colored("Correct!",'green'), colored("%d" % int(time_diff), 'blue'), "seconds\n"


main()
