#!/bin/bash
MODE="DEFAULT"
# if [[ $@ = "full" || $@ = "Full" || $@ = "FULL"]] then
if [ $@ == "full" ] || [ $@ == "Full" ] || [ $@ == "FULL" ] 
then
  echo "Full Mode Active"
  MODE="FULL"
elif [ $@ == "optical" ] || [ $@ == "Optical" ] || [ $@ == "OPTICAL" ] 
then
  echo "Optical Only Active"
  MODE="OPTICAL"
else
  echo "Error, Expect 'full' or 'optical' as an argument"
  return 0
fi

tput setaf 2
if [ $MODE == "FULL" ] 
then
  echo -e "Beinning to run Elastic"
elif [ $MODE == "OPTICAL" ] 
then
  echo -e "Beinning to run Elastic Optical Only"
fi
tput sgr0
bash clean.bash

tput setaf 2
echo -e "Beinning to run Fresco"
tput sgr0
if [ $MODE == "FULL" ] 
then
runfresco elastic.in elastic.out
elif [ $MODE == "OPTICAL" ] 
then
runfresco elastic_opticalOnly.in elastic_opticalOnly.out
fi
echo 

tput setaf 2
echo -e "Beinning to convert Fresco output to ROOT output"
tput sgr0
if [ $MODE == "FULL" ] 
then
python ../utils/out2root.py elastic.out elastic_before.root
elif [ $MODE == "OPTICAL" ] 
then
python ../utils/out2root.py elastic_opticalOnly.out elastic_opticalOnly_before.root
fi

tput setaf 2
echo -e "Beinning to calculate normalization"
tput sgr0
if [ $MODE == "FULL" ] 
then
python ../utils/calcNorm.py elastic_before.root ../../rb/angulardistribution/angOutReal.root elastic_norm.root
elif [ $MODE == "OPTICAL" ] 
then
python ../utils/calcNorm.py elastic_opticalOnly_before.root ../../rb/angulardistribution/angOutReal.root elastic_opticalOnly_norm.root
fi

tput setaf 2
echo -e "Beinning to convert angular distribution to the search file for sfresco"
tput sgr0
if [ $MODE == "FULL" ] 
then
python ../utils/angdist2fresco.py ../../rb/angulardistribution/angOutReal.root elastic.search
elif [ $MODE == "OPTICAL" ] 
then
python ../utils/angdist2fresco.py ../../rb/angulardistribution/angOutReal.root elastic_opticalOnly.search
fi

tput setaf 2
echo -e "Beinning to run sfresco"
tput sgr0
if [ $MODE == "FULL" ] 
then
sfresco < sfrescoCommands.txt
elif [ $MODE == "OPTICAL" ] 
then
sfresco < sfrescoCommands_opticalOnly.txt
fi
echo
echo


tput setaf 2
echo -e "Beinning to convert sfresco output to ROOT"
tput sgr0
if [ $MODE == "FULL" ] 
then
python ../utils/slimgrace2root.py elastic.plot elastic_after.root
elif [ $MODE == "OPTICAL" ] 
then
python ../utils/slimgrace2root.py elastic_opticalOnly.plot elastic_opticalOnly_after.root
fi
echo

tput setaf 2
echo -e "Beinning to make a blurred version of the sfresco fit"
tput sgr0
if [ $MODE == "FULL" ] 
then
python ../utils/frescoblur.py elastic_after.root blurred_after.root
elif [ $MODE == "OPTICAL" ] 
then
python ../utils/frescoblur.py elastic_opticalOnly_after.root blurred_opticalOnly_after.root
fi
echo


tput setaf 2
echo -e "Generating nice png"
tput sgr0
if [ $MODE == "FULL" ] 
then
python ../utils/plotter.py full
elif [ $MODE == "OPTICAL" ] 
then
python ../utils/plotter.py optical
fi
echo
