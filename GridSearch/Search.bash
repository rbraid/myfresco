#!/bin/bash

STRINGS="$1_$2_$3_$4_$5_$6_$7_$8_$9_${10}"

mkdir "work/dir_$STRINGS"
cd "work/dir_$STRINGS"

read -r -d '' FINPUT << EOM
11Be on 9Be elastic scattering at 30.14 MeV
NAMELIST
 &FRESCO hcm=0.1 rmatch=60 rintp=0.20 hnl=0.1 rnl=7.00 centre=0.0
	 jtmin=0.0 jtmax=20 absend=0.0010
	 thmin=5.00 thmax=-180.00 thinc=1.00
	 iter=1 iblock=0 nnu=36
 	 chans=1 xstabl=1 listcc=2 TRENEG=0 smats=2
	 elab= 30.14 lin = 1  /

&PARTITION namep='11Be' massp=11.021661 zp=4
           namet='9Be' masst=9.012183 zt=4 nex=1 qval=0.0 /
&STATES jp=0.5 bandp=1 ep=0 cpot=1 jt=0.5 bandt=1 et=0 /
&partition /

&POT kp=1 type=0 shape=0 ap=11. at=9. rc=$1  /
&POT kp=1 type=1 V=$2 vr0=$3  a=$4 /
&POT kp=1 type=2 W=$5  wr0=$6 aw=$7  /
&POT kp=1 type=3 vso=$8 rso=$9 aso=${10}   /
&pot /

&overlap /

&coupling /
EOM

echo "$FINPUT" > input_$STRINGS.in

fresco < input_$STRINGS.in > output_$STRINGS.out

python ~/nuclear/mine/fresco/utils/slimgrace2root.py fort.16 root_$STRINGS.root

cp root_$STRINGS.root ~/nuclear/mine/fresco/myfresco/GridSearch/outs/
