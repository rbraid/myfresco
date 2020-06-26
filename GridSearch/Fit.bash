#!/bin/bash

for STRING in 1.0_80_1._.8_50_1.2_.6_5.7_1.15_.7 1.2_100_1.2_.6_65_1.2_.6_5.7_1.15_.7 1.2_20_1.2_.7_5_1.2_.6_5.7_1.15_.7 1.2_40_1.2_.7_35_1.2_.6_5.7_1.15_.7 1.3_40_1.3_.7_35_1.2_.6_5.7_1.15_.7 1.1_60_1.3_.6_50_1.2_.6_5.7_1.15_.7 1.1_60_.9_.9_5_1.2_.6_5.7_1.15_.7 1.2_20_1.3_.8_50_1.2_.6_5.7_1.15_.7 1.2_40_1.3_.7_65_1.2_.6_5.7_1.15_.7 1.2_80_1.4_.7_20_1.2_.6_5.7_1.15_.7
do
echo -e "Running $STRING"
cd ~/nuclear/mine/fresco/myfresco/GridSearch/work/dir_$STRING
# pwd

mv ~/nuclear/mine/fresco/myfresco/GridSearch/search_$STRING.search .
# ls
#
{
sfresco <<EOF
search_$STRING.search

fix 1
fix 2
fix 5
fix 7
fix 8
fix 9
fix 10
fix 11

min
migrand
end

plot plot_$STRING.plot
exit
EOF
}

python ~/nuclear/mine/fresco/utils/slimgrace2root.py plot_$STRING.plot sfrescoFit_$STRING.root
cp *.plot ~/nuclear/mine/fresco/myfresco/GridSearch/searches/
cp *.sfOUT ~/nuclear/mine/fresco/myfresco/GridSearch/searches/
cp sfrescoFit_*.root ~/nuclear/mine/fresco/myfresco/GridSearch/searches/

done

