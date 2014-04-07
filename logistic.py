#!/usr/bin/env python

import png
import math
import json
import sys

conffile = open(sys.argv[1])
conf = json.load(conffile)
scale = float(conf['scale'])
aspect_ratio = float(conf['aspect_ratio'])
p_x = int(aspect_ratio * scale)
p_y = int(scale)
log_run = 500
log_results = p_y

y_min = float(conf['y_min'])
y_max = float(conf['y_max'])
start = float(conf['start'])
stop = float(conf['stop'])
step = (stop - start) / float(p_x)


print "p_x: {0} p_y: {1} y_max: {2}".format(p_x, p_y, y_max)

print "start: {0} stop: {1} step: {2}".format(start, stop, step)


def write_png(platten):
  f = open(conf['output_name'], 'wb')      # binary mode is important
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
  for garbage in range(log_results):
    x = r * x * (1.0 - x)
    if x > y_min and x < y_max:
      answers.append(x)
  return answers

platten = []
for y in range(p_y):
  platten.append([0 for x in range(p_x)])

results = []
for r in drange(start, stop, step):
  vals = get_last_vals(r)
  results.append(dict(zip(vals, [1 for x in range(len(vals))])))

print "len(results): {0}".format(len(results))
for (x, values) in enumerate(results):
  x -= 1
  for v in values:
    y = (1.0 - ((v - y_min) / (y_max - y_min))) * p_y
    #y = (1.0 - ((v * (1.0 / (y_max - y_min))) - y_min)) * p_y
    #print "y: {0}".format(y)
    #print "y = (1.0 - (({0} * (1.0 / ({1} - {2}))) - {2}) * {3})".format(v, y_max, y_min, p_y)
    #if y >= p_y - 1 or y < 0:
      #print "y: {0}".format(y)
    if x >= p_x - 1 or x < 0:
      #print "x: {0}".format(x)
      continue
    platten[int(math.floor(y))][x] = 255

write_png(platten)
