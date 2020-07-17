#!/bin/bash
UTILDIR="/home/ryan/nuclear/mine/fresco/utils"

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
MODES=(twoMinus oneMinus twoPlus)
for MODE in "${MODES[@]}"
do
tput setaf 2
echo -e "Generating search file for ${MODE}"
tput sgr0
python SpectroscopicFactor/GenerateSearchFile.py ${MODE}
done

for MODE in "${MODES[@]}"
do
tput setaf 2
echo -e "Spawning SFRESCO for ${MODE}"
tput sgr0
{
sfresco >${MODE}_sfresco.out <<EOF
${MODE}.search

min
migrand
migrand
end

plot ${MODE}.plot
exit
EOF
} &

done
tput setaf 3
echo "Waiting..."
tput sgr0
wait

for MODE in "${MODES[@]}"
do
tput setaf 2
echo -e "Beinning to convert SFresco output to ROOT output"
tput sgr0
python $UTILDIR/slimgrace2root.py ${MODE}.plot ${MODE}.root

tput setaf 2
echo -e "Fit Results for ${MODE}"
tput sgr0
python SpectroscopicFactor/printResults.py ${MODE}_sfresco.out

tput setaf 2
echo -e "Generating pngs"
tput sgr0
python SpectroscopicFactor/DrawSpectroscopics.py ${MODE} False
echo
done

# tput setaf 2
# echo -e "Generating Back-Calculated Distributions"
# tput sgr0
# python ../utils/backCalculate.py

tput setab 2
printf "All done"
tput sgr0
echo
