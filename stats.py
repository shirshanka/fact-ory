import numpy as np;
import sys
import matplotlib.pyplot as plt;
from matplotlib import cm;
from termcolor import colored;

class Stats():
  def __init__(self, param1_range, param2_range):
    self._total_times = 0;
    self._total_time = 0.0;
    self._wrong_answers = [];
    self._time_dict = {};
    self._param1_range = param1_range
    self._param2_range = param2_range
    self._param1_length = param1_range[1] - param1_range[0] + 1
    self._param2_length = param2_range[1] - param2_range[0] + 1
    self._red_color = 1.0
    self._green_color = 0.3
    self._cream_color = 0.6
    self._default_color = np.nan
    self._wrong_color = 1000.0
    self._time_penalty = 2.0 # time penalty for wrong answer is 5 seconds

    self._result_matrix = np.full((self._param1_length, self._param2_length), self._default_color)
  
  def add_statistic(self, operator, param1,param2,ans,time_diff):
    self.add_time_statistic(param1, param2, time_diff)
    x_axis = param1 - self._param1_range[0]
    y_axis = param2 - self._param2_range[0]
    curr_value = self._result_matrix[x_axis][y_axis]
    incr_value = time_diff
    if (operator.evaluate(param1, param2) != ans):
      # wrong answer
      self.add_wrong_answer(param1,param2,ans)
      incr_value = incr_value + self._time_penalty
    else:
      # right answer: do nothing
      pass

    if np.isnan(curr_value):
      self._result_matrix[x_axis][y_axis] = incr_value
    else:
      self._result_matrix[x_axis][y_axis] = curr_value + incr_value

    
  def add_time_statistic(self, param1, param2, time_diff):
    self._total_times = self._total_times +1;
    self._total_time = self._total_time + time_diff;
    if not self._time_dict.has_key(param1):
      self._time_dict[param1] = []
    if not self._time_dict.has_key(param2):
      self._time_dict[param2] = []

    self._time_dict[param1].append(time_diff)
    self._time_dict[param2].append(time_diff)

  def add_wrong_answer(self, param1, param2, answer_given):
    self._wrong_answers.append((param1,param2, answer_given))

    
  def get_avg_time(self):
    return (self._total_time / self._total_times);


  def print_stats(self, operator):
    sys.stdout.write("You took an average of %0.2f seconds to answer each question!\n" % self.get_avg_time());    
    if self._wrong_answers != []:
      print("Here were the answers you got wrong...")

    for (f1,f2,ans) in self._wrong_answers:
      print ("%d %s %d = " % (f1,operator.symbol,f2)), colored("%d" % ans, "red"), "Correct answer is ", colored("%d" % operator.evaluate(f1,f2), "green")

    row_labels = range(self._param1_range[0],self._param1_range[1]+1)
    col_labels = range(self._param2_range[0],self._param2_range[1]+1)
    #plt.matshow(self._result_matrix, cmap=cm.Spectral_r, vmin=0, vmax=1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(self._result_matrix, interpolation='nearest', vmin=0)
    fig.colorbar(cax)
    plt.gca().set_aspect('auto')
    row_ticks = range(len(row_labels))
    col_ticks = range(len(col_labels))

    if (len(row_labels) > 10):
      skip_every = int(len(row_labels) / 10);
      row_labels = row_labels[0::skip_every]
      row_ticks = row_ticks[0::skip_every]

    if (len(col_labels) > 10):
      skip_every = int(len(col_labels)/10)
      col_labels = col_labels[0::skip_every]
      col_ticks = col_ticks[0::skip_every]

    plt.xticks(col_ticks, col_labels)
    plt.yticks(row_ticks, row_labels)
    plt.show()


if __name__=="__main__":
  print "hello world"
