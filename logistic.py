#!/usr/bin/env python

import png
import math
import json
import sys
import os.path
import Queue
import threading

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

def get_file_name():
  name = conf['output_name']
  count = 1
  answer = name + ".png"
  while os.path.isfile("./"+answer):
    answer = "{0}_{1}.png".format(name, str(count))
    count += 1
  return answer

def write_png(platten):
  f = open(get_file_name(), 'wb')      # binary mode is important
  w = png.Writer(p_x, p_y, greyscale=True)
  w.write(f, platten)
  f.close()

def drange(start, stop, step):
  n = start
  while n < stop:
    yield n
    n += step

def get_last_vals(r):
  answers = []
  x = 0.05
  for garbage in range(log_run):
    x = r * x * (1.0 - x)
  count = 0
  while len(answers) < log_results*2:
    x = r * x * (1.0 - x)
    if count > 100000:
      break
    count += 1
    if x > y_min and x < y_max:
      answers.append(x)
  return answers

def run_interval(idx, strt, stp, q):
  print "run_interval({0},{1},{2})".format(idx, strt, stp)
  sub_answers = []
  for r in drange(strt, stp, step):
    vals = get_last_vals(r)
    rslts = dict(
      zip(
        vals, 
        [1 for x in range(len(vals))]
      )
    )
    sub_answers.append(rslts.keys())
  q[idx] = sub_answers

platten = []
for y in range(p_y):
  platten.append([0 for x in range(p_x)])

results = []
answers = Queue.Queue()
answer_dict = {}
x_span = p_x / num_threads
threads = []
for s in range(num_threads):
  if num_threads == 1:
    run_interval(s, start + s*x_span*step, start + (s+1)*x_span*step, answer_dict)
  else:
    t = threading.Thread(target=run_interval, args=(s, start + s*x_span*step, start + (s+1)*x_span*step, answer_dict))
    t.daemon = True
    t.start()
    threads.append(t)
if num_threads > 1:
  for t in threads:
    t.join()

for key in range(num_threads):
  for l in answer_dict[key]:
    results.append(l)


print "starting to enumerate"
for (x, values) in enumerate(results):
  x -= 1
  for v in values:
    #for v in d.keys():
    y = (1.0 - ((v - y_min) / (y_max - y_min))) * p_y
    if x >= p_x - 1 or x < 0:
      continue
    platten[int(math.floor(y))][x] = 255
print "done enumerating"
write_png(platten)
