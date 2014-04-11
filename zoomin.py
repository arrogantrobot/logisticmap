#!/usr/bin/env python

import json
import sys
import pprint

if __name__ == "__main__":
  conffile = open(sys.argv[1])
  conf = json.load(conffile)
  
  frames = int(conf['frames'])
  threads = conf['threads']


  scale = conf['scale']
  aspect_ratio = conf['aspect_ratio']
  output_name = conf['output_name']

  zoom_target_x = float(conf['zoom_target_x'])
  zoom_target_y = float(conf['zoom_target_y'])

  x_min_start = float(conf['x_min_start'])
  x_max_start = float(conf['x_max_start'])
  y_min_start = float(conf['y_min_start'])
  y_max_start = float(conf['y_max_start'])

  x_min_stop = float(conf['x_min_stop'])
  x_max_stop = float(conf['x_max_stop'])
  y_min_stop = float(conf['y_min_stop'])
  y_max_stop = float(conf['y_max_stop'])

  answer = {}
  images = []

  x_ratio = (x_max_stop - x_min_stop) / (x_max_start - x_min_start) 
  y_ratio = (y_max_stop - y_min_stop) / (y_max_start - y_min_start) 
  print "xr {0}  yr {1}".format(x_ratio, y_ratio)

  width = x_max_start - x_min_start
  height = y_max_start - y_min_start

  for n in range(frames):
    width = width * (1 - (n * x_ratio))
    height = height * (1 - (n * y_ratio))
    print "w {0}  h {1}".format(width, height)
    images.append( {
      "scale" : scale,
      "aspect_ratio" : aspect_ratio,
      "y_min" : str(zoom_target_y - (height / 2.0)),
      "y_max" : str(zoom_target_y + (height / 2)),
      "start" : str(zoom_target_x - (width / 2)),
      "stop" : str(zoom_target_x + (width / 2)),
      "output_name" : output_name,
      "num_threads" : threads
    })

  answer["images"] = images
  print json.dumps(answer, sort_keys=True, indent=4, separators=(',', ': '))

