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
echo -e "Generating initial pngs, and splitting angular distributions into pure states"
tput sgr0
python $UTILDIR/realDraw.py

tput setaf 2
echo -e "Generating search file"
tput sgr0
python SpectroscopicFactor/GenerateSearchFile.py 2-

tput setaf 2
echo -e "Running SFRESCO"
tput sgr0
sfresco <<EOF
twoMinus.search

min
migrand
end

plot twoMinus.plot
exit
EOF

echo
echo

tput setaf 2
echo -e "Beinning to convert SFresco output to ROOT output"
tput sgr0
python $UTILDIR/slimgrace2root.py twoMinus.plot twoMinus.root

tput setaf 2
echo -e "Generating pngs"
tput sgr0
python SpectroscopicFactor/DrawSpectroscopics.py 2-
echo


tput setab 2
printf "All done"
tput sgr0
echo
