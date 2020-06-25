#!/bin/bash

nice -n 19 parallel --timeout 300% --bar --shuf bash Search.bash ::: 1.1 1.3 ::: 20 40 60 80 100  ::: .9 1. 1.1 1.2 1.3 1.4 ::: .5 .6 .7 .8 .9 ::: 5 20 35 50 65 ::: 1.2 ::: .6 ::: 5.7 ::: 1.15 ::: .7

echo -e "DONE"