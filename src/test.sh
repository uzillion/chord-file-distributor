#!/bin/bash

PORT=5000 python3 taco.py join
PORT=8000 python3 taco.py join 127.0.1.1 5000

PORT=8000 python3 taco.py stabilize
PORT=5000 python3 taco.py stabilize

for i in `seq 1 22`;
do
  PORT=8000 python3 taco.py fix_finger
  PORT=5000 python3 taco.py fix_finger
done  

#PORT=8000 python3 taco.py disperse ./cache/IMG_20190101_123952_e.jpg 4
