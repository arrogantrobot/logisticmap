#!/usr/bin/env python

import json
import sys

if __name__ == "__main__":
  conffile = open(sys.argv[1])
  conf = json.load(conffile)
  
  frames = int(conf['frames'])
  threads = conf['threads']

  x_min_start = float(conf['x_min_start'])
  x_max_start = float(conf['x_max_start'])
  y_min_start = float(conf['y_min_start'])
  y_max_start = float(conf['y_max_start'])

  x_min_stop = float(conf['x_min_stop'])
  x_max_stop = float(conf['x_max_stop'])
  y_min_stop = float(conf['y_min_stop'])
  y_max_stop = float(conf['y_max_stop'])

  scale = conf['scale']
  aspect_ratio = conf['aspect_ratio']
  output_name = conf['output_name']


  answer = {}

  images = []

  y_min_step = (y_min_stop - y_min_start) / float(frames)
  y_max_step = (y_max_stop - y_max_start) / float(frames)
  x_min_step = (x_min_stop - x_min_start) / float(frames)
  x_max_step = (x_max_stop - x_max_start) / float(frames)

  for n in range(frames):
    images.append( {
      "scale" : scale,
      "aspect_ratio" : aspect_ratio,
      "y_min" : str(y_min_start + n * y_min_step),
      "y_max" : str(y_max_start + n * y_max_step),
      "start" : str(x_min_start + n * x_min_step),
      "stop" : str(x_max_start + n * x_max_step),
      "output_name" : output_name,
      "num_threads" : threads
    })

  answer["images"] = images
  print json.dumps(answer, sort_keys=True, indent=4, separators=(',', ': '))

