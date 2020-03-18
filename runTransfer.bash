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
