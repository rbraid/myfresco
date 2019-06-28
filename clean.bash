#!/bin/bash

echo "Cleaning down to only the input files."

rm --f *.png #--f makes the warning of no files found go away
rm --f fort*
rm --f *frout*
rm --f *.root
rm --f *.out
rm --f *.plot
rm --f *.search
rm --f minuit-saved.dat
