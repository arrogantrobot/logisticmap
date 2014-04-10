#!/usr/bin/env python

import png
import math
import json
import sys
import os.path
from multiprocessing import Process, Queue

def get_file_name(conf):
  name = conf['output_name']
  count = 1
  answer = name + ".png"
  while os.path.isfile("./"+answer):
    answer = "{0}_{1}.png".format(name, str(count))
    count += 1
  return answer

def write_png(conf, platten):
  f = open(get_file_name(conf), 'wb')      # binary mode is important
  w = png.Writer(p_x, p_y, greyscale=True)
  w.write(f, platten)
  f.close()

def drange(start, stop, step):
  n = start
  while n < stop:
    yield n
    n += step

def get_last_vals(r, num, y_min, y_max):
  answers = []
  x = 0.05
  for garbage in range(500):
    x = r * x * (1.0 - x)
  count = 0
  while len(answers) < num:
    x = r * x * (1.0 - x)
    if count > 100000:
      break
    count += 1
    if x > y_min and x < y_max:
      answers.append(x)
  return answers

def run_interval(idx, strt, stp, q, p_x, p_y, y_min, y_max):
  print "run_interval({0},{1},{2})".format(idx, strt, stp)
  sub_answers = []
  for r in drange(strt, stp, step):
    vals = get_last_vals(r, p_y, y_min, y_max)
    rslts = dict(
      zip(
        vals, 
        [1 for x in range(len(vals))]
      )
    )
    sub_answers.append(rslts.keys())
  q.put((idx, sub_answers))
  q.close()
  print "exiting thread #{0}, q.qsize(): {1}, len(sub_answers): {2}".format(idx, q.qsize(),len(sub_answers))

if __name__ == "__main__":

  conffile = open(sys.argv[1])
  conf = json.load(conffile)
  scale = float(conf['scale'])
  aspect_ratio = float(conf['aspect_ratio'])
  p_x = int(aspect_ratio * scale)
  p_y = int(scale)
  log_run = 500
  log_results = p_y
  num_threads = int(conf['num_threads']) if conf['num_threads'] else 1

  y_min = float(conf['y_min'])
  y_max = float(conf['y_max'])
  start = float(conf['start'])
  stop = float(conf['stop'])
  step = (stop - start) / float(p_x)

  print "p_x: {0} p_y: {1} y_max: {2}".format(p_x, p_y, y_max)
  print "start: {0} stop: {1} step: {2}".format(start, stop, step)
  platten = []
  for y in range(p_y):
    platten.append([0 for x in range(p_x)])

  results = []
  answers = Queue()
  x_span = p_x / num_threads
  processes = []
  for s in range(num_threads):
    p = Process(target=run_interval, args=(s, start + s*x_span*step, start + (s+1)*x_span*step, answers, p_x, p_y, y_min, y_max))
    p.start()
    processes.append(p)
  
  for n in range(num_threads):
    results.append(answers.get())

  for p in processes:
    p.join()

  sorted_results = []
  for r in sorted(results):
    for v in r[1]:
      sorted_results.append(v)

  for (x, values) in enumerate(sorted_results):
    for v in values:
      y = (1.0 - ((v - y_min) / (y_max - y_min))) * p_y
      if x >= p_x - 1 or x < 0:
        continue
      platten[int(math.floor(y))][x] = 255
  write_png(conf, platten)
