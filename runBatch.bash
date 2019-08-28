#!/bin/bash

tput setaf 2
echo -e "Starting from a clean slate"
tput sgr0
bash clean.bash
rm ../outputs/*.par

tput setaf 2
echo -e "Beinning to run Fresco"
tput sgr0
runfresco elastic.in elastic.out
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

nice -n 19  parallel --tmpdir ~/nuclear/mine/fresco/outputs --files --bar --shuf bash runElastic.bash ::: 1.1 1.3 ::: 40 50 60 70 ::: 1.1 1.3 ::: .25 1 ::: 3 9 ::: 1.1 1.3 ::: .25 1

# nice -n 19 parallel --tmpdir ~/nuclear/mine/fresco/outputs --files --bar --shuf bash runElastic.bash ::: 1.1 1.3 ::: 40 120 ::: 1.1 1.3 ::: .5 ::: 3 12 ::: 1.2 ::: .5

# nice -n 19 parallel --tmpdir ~/nuclear/mine/fresco/outputs --files --bar --shuf bash runElastic.bash ::: 1.2 ::: 50 ::: 1.2 ::: .5 ::: 6 ::: 1.2 ::: .5

tput setaf 2
echo -e "Creating Nice Plots"
tput sgr0
python ../utils/batchDraw.py elastic_after_*.root

tput setaf 2
echo -e "Moving fit data to csv"
tput sgr0
python ../utils/parseMINUIT.py ../outputs/par*.par

tput setaf 2
echo -e "All done."
tput sgr0