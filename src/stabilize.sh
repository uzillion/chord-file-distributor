#!/bin/bash

./taco.py stabilize
./taco.py stabilize
./taco.py stabilize
./taco.py stabilize
./taco.py stabilize
./taco.py stabilize

for i in `seq 1 22`;
do
  ./taco.py fix_finger
done  
