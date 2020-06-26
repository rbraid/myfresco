#!/bin/bash
MODE="FULL"
UTILDIR="/home/ryan/nuclear/mine/fresco/utils"
ANGDIR="/home/ryan/nuclear/mine/rb/angulardistribution"

tput setaf 2
echo -e "Beinning to run Elastic"
tput sgr0
bash clean.bash

tput setaf 2
echo -e "Beinning to run Fresco"
tput sgr0
fresco < elastic.in > elastic.out
echo

tput setaf 2
echo -e "Beinning to convert Fresco output to ROOT output"

python $UTILDIR/slimgrace2root.py fort.16 elastic_before.root


# tput setaf 2
# echo -e "Beinning to calculate normalization"
# tput sgr0
# python $UTILDIR/calcNorm.py elastic_before.root ~/nuclear/mine/rb/angulardistribution/angOutReal.root elastic_norm.root

tput setaf 2
echo -e "Beinning to convert angular distribution to the search file for sfresco"
tput sgr0

python $UTILDIR/angdist2fresco.py $ANGDIR/angOutReal.root elastic.search False
python $UTILDIR/angdist2fresco.py $ANGDIR/angOutReal.root elastic_rRuth.search True

sfresco <<EOF
elastic_rRuth.search

plot elastic_rRuth.plot
exit
EOF

tput setaf 2
echo -e "Beinning to run sfresco"
tput sgr0

sfresco < sfrescoCommands.txt

sfresco <<EOF
elastic_rRuth.search
fix 1
fix 3
fix 4
fix 5
fix 6
fix 7
fix 8
fix 9
fix 10
fix 11

min
migrand
end

fix 2
step 3 1
step 4 .01
step 5 .01

min
migrand
migrand
end

fix 3
fix 4
fix 5

step 6 1
step 7 .1

min
migrand
end

step 2 .001
step 3 .01
step 4 .001
step 5 .001

min
migrand
end

plot elastic_rRuth_after.plot
exit
EOF

echo
echo

tput setaf 2
echo -e "Beinning to convert sfresco output to ROOT"
tput sgr0

python $UTILDIR/slimgrace2root.py elastic.plot elastic_after.root
python $UTILDIR/slimgrace2root.py elastic_rRuth.plot elastic_rRuth_before.root
python $UTILDIR/slimgrace2root.py elastic_rRuth_after.plot elastic_rRuth_after.root

echo

# tput setaf 2
# echo -e "Beinning to make a blurred version of the sfresco fit"
# tput sgr0
# python $UTILDIR/frescoblur.py elastic_after.root blurred_after.root


tput setaf 2
echo -e "Generating nice png"
tput sgr0
python $UTILDIR/plotter.py full True
python $UTILDIR/plotter.py full False
echo



