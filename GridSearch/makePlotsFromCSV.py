from ROOT import TFile, TGraph, TH1, TH2D
import pandas as pd

import ROOT

import csv

outF = TFile("plots_from_CSV.root","recreate")

inFrame =  pd.read_csv('Sorted_Grid_Search.csv', sep = ',', dtype={"r0":float, "V": float, "r0": float, "a": float, "W": float, "rW":float, "aW":float})

print "Full inFrame holds {} entries".format(len(inFrame))

inFrame.drop(inFrame[inFrame.r0 != 1.4].index, inplace=True)
inFrame.drop(inFrame[inFrame.a != .9].index, inplace=True)
inFrame.drop(inFrame[inFrame.rW != 1.3].index, inplace=True)
inFrame.drop(inFrame[inFrame.aW != .9].index, inplace=True)

print "After Selecting variables, inFrame holds {} entries".format(len(inFrame))

V_W_plot_blur = TH2D("V_W_plot_blur","Comparing Blurred Chi Square of V vs W;V;W", 25,45,70, 25,30,55)
[V_W_plot_blur.Fill(x,y,z) for x, y, z in zip(inFrame["V"], inFrame["W"], inFrame["BlurChiSquare"])]

V_W_plot_prod = TH2D("V_W_plot_prod","Comparing Product of Blurred Chi Square and Regular Chi Square of V vs W;V;W", 25,45,70, 25,30,55)
[V_W_plot_prod.Fill(x,y,z) for x, y, z in zip(inFrame["V"], inFrame["W"], inFrame["BlurChiSquare"] * inFrame["Chi Square"])]

V_W_plot_init = TH2D("V_W_plot_init","Comparing Regular Chi Square of V vs W;V;W", 25,45,70, 25,30,55)
[V_W_plot_init.Fill(x,y,z) for x, y, z in zip(inFrame["V"], inFrame["W"], inFrame["Chi Square"])]
# for row in inFrame:
#     print row
#     print "V: {}, W: {}".format(row["V"], row["W"])
#     V_W_plot.Fill(row["V"], row["W"], row["BlurChiSquare"])
#
outF.cd()
V_W_plot_prod.Write()
V_W_plot_blur.Write()
V_W_plot_init.Write()
