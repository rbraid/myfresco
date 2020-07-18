from ROOT import TFile, TGraph, TGraphErrors, TCanvas, TLegend
import ROOT

frescoF = TFile.Open("transfer_before.root","read")
if not frescoF:
  print "No frescoF"
  quit()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("Mode", help='Input Location & Name')
parser.add_argument("rRuth", help="Ratio to Rutherford?", default = "False")
args = parser.parse_args()

# print "{} mode.".format(args.Mode)

if args.Mode != "oneMinus" and args.Mode != "twoPlus" and args.Mode != "twoMinus":
  print "Mode Unrecognized! Use 'oneMinus', 'twoPlus', or 'twoMinus'"
  quit()

if args.rRuth == "True" or args.rRuth == "TRUE":
  args.rRuth = True
else:
  args.rRuth = False

dataPointer = -1
gColor = ROOT.kBlack

if args.Mode == "oneMinus":
  dataPointer = 3
  gColor = ROOT.kRed
elif args.Mode == "twoMinus":
  dataPointer = 4
  gColor = ROOT.kBlue
elif args.Mode == "twoPlus":
  dataPointer = 2
  gColor = ROOT.kGreen

sfrescoF = TFile.Open("{}.root".format(args.Mode),"read")

frescoH = frescoF.Get("G{}".format(dataPointer))
dataHAfter = sfrescoF.Get("G0")
sfrescoH = sfrescoF.Get("G1")

colors = [ROOT.kGreen, ROOT.kRed, ROOT.kBlue, ROOT.kOrange]

canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
canvas.SetLogy()

Dummy = ROOT.TH2F("Dummy","SFRESCO Spectroscopic Factor Check for {}".format(args.Mode),90,0,180,1000000,0,1000)
if args.rRuth:
    Dummy = ROOT.TH2F("Dummy","SFRESCO Spectroscopic Factor Check for {}".format(args.Mode),90,0,180,1000000,0,10)

Dummy.GetXaxis().SetTitle("COM Angle in Degrees")
Dummy.GetYaxis().SetTitle("Cross Section in mb/sr")

Dummy.SetStats(ROOT.kFALSE)
Dummy.Draw()

Dummy.SetAxisRange(0,90,"X")
Dummy.SetAxisRange(.001,1000,"Y")
if args.rRuth:
    Dummy.SetAxisRange(.001,10,"Y")


leg = TLegend(0.65,.65,.9,.9)

dataHAfter.SetMarkerColor(ROOT.TColor.GetColorDark(gColor))
dataHAfter.SetLineColor(ROOT.TColor.GetColorDark(gColor))
dataHAfter.SetFillColor(ROOT.kWhite)
dataHAfter.SetMarkerStyle(20)
leg.AddEntry(dataHAfter,"Experimental Data")
dataHAfter.Draw("sameP")

sfrescoH.SetMarkerColor(gColor)
sfrescoH.SetLineColor(gColor)
sfrescoH.SetFillColor(ROOT.kWhite)
sfrescoH.SetLineWidth(2)
sfrescoH.SetLineStyle(2)
leg.AddEntry(sfrescoH,"SFRESCO Fit of Spectroscopic Factor")
sfrescoH.Draw("sameL")

if not args.rRuth:
    frescoH.SetMarkerColor(ROOT.kBlack)
    frescoH.SetLineColor(ROOT.kBlack)
    frescoH.SetFillColor(ROOT.kWhite)
    leg.AddEntry(frescoH,"Spectroscopic Factor = 1")
    frescoH.Draw("sameL")

leg.Draw()

if args.rRuth:
    canvas.SaveAs("SpectroscopicFactor/{}SFRESCO_rRuth.png".format(args.Mode))
else:
    canvas.SaveAs("SpectroscopicFactor/{}SFRESCO.png".format(args.Mode))
