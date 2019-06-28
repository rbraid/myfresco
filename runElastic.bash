#!/bin/bash

bash clean.bash

runfresco elastic.in elastic.out
python ../utils/out2root.py elastic.out elastic_before.root
python ../utils/calcNorm.py elastic_before.root ../../rb/angulardistribution/angOutReal.root elastic_norm.root
python ../utils/angdist2fresco.py ../../rb/angulardistribution/angOutReal.root elastic.search

sfresco < sfrescoCommands.txt

