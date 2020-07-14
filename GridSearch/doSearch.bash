#!/bin/bash

nice -n 19 parallel --timeout 300% --bar --shuf bash Search.bash ::: .62 .63 .64 ::: 50 55 60 65 70 ::: 1.0 1.1 1.2 ::: .5 .6 .7 :::  20 25 30 35 40  ::: 1. 1.1 1.2 ::: .5 .6 .7 ::: 5.7 ::: 1.15 ::: .7

echo -e "DONE"