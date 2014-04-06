#!/usr/bin/env python

import png
import math

p_x = 2000
p_y = 1000
log_run = 500
log_results = p_y

start = 2
stop = 4
step = (stop - start) / float(p_x)
y_min = 0.3
y_max = 0.8

y_scale = (y_max - y_min) / p_y

print "start: {0} stop: {1} step: {2}".format(start, stop, step)


def write_png(platten):
  f = open('logistic.png', 'wb')      # binary mode is important
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
  results.append(dict(zip(get_last_vals(r), [1 for x in range(log_results)])))

for (x, values) in enumerate(results):
  #x -= 1
  for v in values:
    y = (((1.0 - v)-y_min) * p_y)* (1.0/(y_max - y_min))
    #if y >= p_y - 1 or y < 0:
    #  print "y: {0}".format(y)
    #  print v
    #if x >= p_x - 1 or x < 0:
    #  print "x: {0}".format(x)
    platten[int(math.floor(y))][x] = 255

write_png(platten)
