#!/bin/bash

# Stabilization for nodes running on different machines, with M = 20

../taco.py stabilize
../taco.py stabilize
../taco.py stabilize
../taco.py stabilize
../taco.py stabilize
../taco.py stabilize

for i in `seq 1 22`;
do
  ../taco.py fix_finger
done  
