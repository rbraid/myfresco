#!/bin/bash

tput setaf 2
echo -e "Beinning to run Elastic Optical Only"
tput sgr0

bash clean.bash

tput setaf 2
echo -e "Beinning to run Fresco"
tput sgr0
runfresco elastic_opticalOnly.in elastic_opticalOnly.out
echo 
tput setaf 2
echo -e "Beinning to convert Fresco output to ROOT output"
tput sgr0
python ../utils/out2root.py elastic_opticalOnly.out elastic_opticalOnly_before.root
tput setaf 2
echo -e "Beinning to calculate normalization"
tput sgr0
python ../utils/calcNorm.py elastic_opticalOnly_before.root ../../rb/angulardistribution/angOutReal.root elastic_opticalOnly_norm.root
tput setaf 2
echo -e "Beinning to convert angular distribution to the search file for sfresco"
tput sgr0
python ../utils/angdist2fresco.py ../../rb/angulardistribution/angOutReal.root elastic_opticalOnly.search
tput setaf 2
echo -e "Beinning to run sfresco"
tput sgr0
sfresco < sfrescoCommands_opticalOnly.txt
echo
echo
tput setaf 2
echo -e "Beinning to convert sfresco output to ROOT"
tput sgr0
python ../utils/slimgrace2root.py elastic_opticalOnly.plot elastic_opticalOnly_after.root
echo

# root -l elastic_opticalOnly_after.root
tput setaf 2
echo -e "Generating nice png"
tput sgr0
python ../utils/plotter.py
echo
