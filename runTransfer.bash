#!/bin/bash
MODE="UNDEFINED"
UTILDIR="/home/ryan/nuclear/mine/fresco/utils"
ANGDIR="/home/ryan/nuclear/mine/rb/angulardistribution"

echo
tput setaf 2
echo -e "Cleaning"
tput sgr0
bash clean.bash

tput setaf 2
echo -e "Beinning to run Fresco"
tput sgr0
fresco < transfer.in > transfer.out

tput setaf 2
echo -e "Beinning to convert Fresco output to ROOT output"
tput sgr0
python $UTILDIR/slimgrace2root.py fort.16 transfer_before.root


tput setaf 2
echo -e "Beinning to convert angular distribution to the search file for sfresco"
tput sgr0
tput setaf 1
echo -e "NOT IMPLEMENTED, SHORT CIRCUIT PAST SFRESCO"
tput sgr0
# python $UTILDIR/angdist2fresco.py $ANGDIR/angOutReal.root transfer.search


# tput setaf 2
# echo -e "Beinning to run sfresco"
# tput sgr0
# sfresco < sfrescoCommands.txt
#
# elif [ $MODE == "PARAM" ]
# then
# sfresco <<EOF
# elastic_$1_$2_$3_$4_$5_$6_$7.search
# fix 1
#
# min
# migrand
# end
#
# plot elastic_$1_$2_$3_$4_$5_$6_$7.plot
# exit
# EOF
# fi
# echo
# echo
#
# tput setaf 2
# echo -e "Beinning to convert sfresco output to ROOT"
# tput sgr0
#
# UTILDIR/slimgrace2root.py elastic.plot elastic_after.root


# tput setaf 2
# echo -e "Beinning to make a blurred version of the sfresco fit"
# tput sgr0
# python $UTILDIR/frescoblur.py transfer_after.root blurred_after_transfer.root
#
# echo


tput setaf 2
echo -e "Generating nice png"
tput sgr0
python $UTILDIR/realDraw.py

echo


tput setab 2
printf "All done"
tput sgr0
echo
