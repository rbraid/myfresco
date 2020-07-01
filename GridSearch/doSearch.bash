#!/bin/bash

nice -n 19 parallel --timeout 300% --bar --shuf bash Search.bash ::: .63 .9 1.2 ::: 40 50 60 70 ::: .9 1. 1.1 1.2 1.3 1.4 ::: .5 .7 .9 ::: 5 20 35 50  ::: .9 1.1 1.3 ::: .5 .7 .9 ::: 5.7 ::: 1.15 ::: .7

echo -e "DONE"