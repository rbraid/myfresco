#!/bin/bash
MODE="DEFAULT"

if [ $# -eq 0 ]
then
  echo "Using Full as default"
  MODE="FULL"
elif [ $# -gt 1 ]
then
#   echo "Parameter Mode Active"
  MODE="PARAM"
elif [ $@ == "full" ] || [ $@ == "Full" ] || [ $@ == "FULL" ] 
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

if [ $MODE == "PARAM" ]
then
  echo "$1, $2, $3, $4, $5, $6, $7"
fi

if [ $MODE != "PARAM" ]
then
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
  python ../utils/slimgrace2root.py fort.16 elastic_before.root
  elif [ $MODE == "OPTICAL" ] 
  then
  python ../utils/slimgrace2root.py fort.16 elastic_opticalOnly_before.root
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
elif [ $MODE == "PARAM" ]
then
python ../utils/angdist2fresco.py ../../rb/angulardistribution/angOutReal.root elastic_$1_$2_$3_$4_$5_$6_$7.search $1 $2 $3 $4 $5 $6 $7
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
elif [ $MODE == "PARAM" ]
then
sfresco <<EOF
elastic_$1_$2_$3_$4_$5_$6_$7.search
fix 1
fix 3
fix 6

min
migrand
end

plot elastic_$1_$2_$3_$4_$5_$6_$7.plot
exit
EOF
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
elif [ $MODE == "PARAM" ]
then
python ../utils/slimgrace2root.py elastic_$1_$2_$3_$4_$5_$6_$7.plot elastic_after_$1_$2_$3_$4_$5_$6_$7.root
fi
echo


if [ $MODE == "FULL" ] 
then
tput setaf 2
echo -e "Beinning to make a blurred version of the sfresco fit"
tput sgr0
python ../utils/frescoblur.py elastic_after.root blurred_after.root
elif [ $MODE == "OPTICAL" ] 
then
tput setaf 2
echo -e "Beinning to make a blurred version of the sfresco fit"
tput sgr0
python ../utils/frescoblur.py elastic_opticalOnly_after.root blurred_opticalOnly_after.root
fi
echo



if [ $MODE == "FULL" ] 
then
tput setaf 2
echo -e "Generating nice png"
tput sgr0
python ../utils/plotter.py full
elif [ $MODE == "OPTICAL" ] 
then
tput setaf 2
echo -e "Generating nice png"
tput sgr0
python ../utils/plotter.py optical
elif [ $MODE == "PARAM" ]
then
python ../utils/plotter.py param $1_$2_$3_$4_$5_$6_$7
fi
echo
