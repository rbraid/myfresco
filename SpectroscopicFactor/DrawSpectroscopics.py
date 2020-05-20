from ROOT import TFile, TGraph, TGraphErrors, TCanvas, TLegend
import ROOT

frescoF = TFile.Open("transfer_before.root","read")
if not frescoF:
  print "No frescoF"
  quit()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("Mode", help='Input Location & Name')
args = parser.parse_args()

# print "{} mode.".format(args.Mode)

if args.Mode != "oneMinus" and args.Mode != "twoPlus" and args.Mode != "twoMinus":
  print "Mode Unrecognized! Use 'oneMinus', 'twoPlus', or 'twoMinus'"
  quit()

dataPointer = -1
gColor = ROOT.kBlack

if args.Mode == "oneMinus":
  dataPointer = 2
  gColor = ROOT.kRed
elif args.Mode == "twoMinus":
  dataPointer = 3
  gColor = ROOT.kBlue
elif args.Mode == "twoPlus":
  dataPointer = 4
  gColor = ROOT.kGreen

sfrescoF = TFile.Open("{}.root".format(args.Mode),"read")

frescoH = frescoF.Get("G{}".format(dataPointer))
dataHAfter = sfrescoF.Get("G0")
sfrescoH = sfrescoF.Get("G1")

colors = [ROOT.kGreen, ROOT.kRed, ROOT.kBlue, ROOT.kOrange]

canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
canvas.SetLogy()

Dummy = ROOT.TH2F("Dummy","Checking {} SFRESCO".format(args.Mode),90,0,180,1000000,0,10000)
Dummy.GetXaxis().SetTitle("COM Angle in Degrees")
Dummy.GetYaxis().SetTitle("Cross Section in mb/sr")

Dummy.SetStats(ROOT.kFALSE)
Dummy.Draw()

Dummy.SetAxisRange(0,60,"X")
Dummy.SetAxisRange(.0000001,10000,"Y")

leg = TLegend(0.65,.65,.9,.9)

frescoH.SetMarkerColor(ROOT.kBlack)
frescoH.SetLineColor(ROOT.kBlack)
frescoH.SetFillColor(ROOT.kWhite)
leg.AddEntry(frescoH,"FRESCO Raw Output")
frescoH.Draw("sameL")

dataHAfter.SetMarkerColor(ROOT.TColor.GetColorDark(gColor))
dataHAfter.SetLineColor(ROOT.TColor.GetColorDark(gColor))
dataHAfter.SetFillColor(ROOT.kWhite)
dataHAfter.SetMarkerStyle(20)
leg.AddEntry(dataHAfter,"Data")
dataHAfter.Draw("sameP")

sfrescoH.SetMarkerColor(gColor)
sfrescoH.SetLineColor(gColor)
sfrescoH.SetFillColor(ROOT.kWhite)
sfrescoH.SetLineWidth(2)
leg.AddEntry(sfrescoH,"SFRESCO Output")
sfrescoH.Draw("sameL")

leg.Draw()

canvas.SaveAs("SpectroscopicFactor/{}SFRESCO.png".format(args.Mode))
