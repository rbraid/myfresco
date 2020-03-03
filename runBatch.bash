#!/bin/bash

tput setaf 2
echo -e "Starting from a clean slate"
tput sgr0
bash clean.bash
rm ../outputs/*.par

tput setaf 2
echo -e "Beinning to run Fresco"
tput sgr0
fresco < elastic.in > elastic.out
echo

tput setaf 2
echo -e "Beinning to convert Fresco output to ROOT output"
tput sgr0
python ../utils/slimgrace2root.py fort.16 elastic_before.root


# tput setaf 2
# echo -e "Beinning to calculate normalization"
# tput sgr0
# python ../utils/calcNorm.py elastic_before.root ../../rb/angulardistribution/angOutReal.root elastic_norm.root


tput setaf 2
echo -e "Beinning to convert angular distribution to the search file for sfresco"
tput sgr0
python ../utils/angdist2fresco.py ../../rb/angulardistribution/angOutReal.root elastic.search

tput setaf 2
echo -e "Beginning to run the parallel sfresco fits for different parameters"
tput sgr0

nice -n 19 parallel --timeout 300%  --tmpdir ~/nuclear/mine/outputs/ --files --bar --shuf bash runElastic.bash ::: .9 1.1 1.3 ::: 15 25 50 100  ::: 1. 1.15 1.3 ::: .4 .8 ::: 4  8 ::: 1.2  1.4 ::: .4 .8

tput setaf 2
echo -e "Creating Nice Plots"
tput sgr0
python ../utils/batchDraw.py afters/elastic_after_*.root

tput setaf 2
echo -e "Moving fit data to csv"
tput sgr0
python ../utils/parseMINUIT.py ../../outputs/par*.par

tput setaf 2
echo -e "Making Pairplot from csv"
tput sgr0
python ../utils/checkCorrelations.py

rm *trace
rm *snap

tput setaf 2
echo -e "All done."
tput sgr0