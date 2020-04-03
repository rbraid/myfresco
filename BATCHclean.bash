#!/bin/bash

echo "Cleaning from Batch"

bash clean.bash

rm --f afters/*.root
rm --f outputs/*.png
rm --f search/*.search

rm --f -r /home/ryan/nuclear/mine/outputs/*
