#!/usr/bin/env python

import png
import math

p_x = 2000
p_y = 1000
log_run = 500
log_results = p_y

start = 1.0
stop = 4.0
step = (stop - start) / float(p_x)
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
    answers.append(x)
  return answers

platten = []
for y in range(p_y):
  platten.append([0 for x in range(p_x)])

results = []
for r in drange(start, stop, step):
  results.append(dict(zip(get_last_vals(r), [1 for x in range(log_results)])))

for (x, values) in enumerate(results):
  x -= 1
  for v in values:
    if v >= 1 or v < 0:
      print "v: {0}".format(v)
    platten[int(math.floor((1 - v) * p_y))][x] = 255

write_png(platten)
