from ROOT import TFile, TGraph, TGraphErrors, TCanvas, TLegend
import ROOT

scalefactor = 0.77214E-04

def ScaleTGraph(graph):
  for i in range(graph.GetN()):
    graph.GetY()[i] *= scalefactor;
    graph.GetEY()[i] *= scalefactor

  return graph

frescoF = TFile.Open("transfer_before.root","read")
if not frescoF:
  print "No frescoF"
  quit()

dataF = TFile.Open("~/nuclear/mine/rb/angulardistribution/angOutReal.root","read")
if not dataF:
  print "No dataF"
  quit()

sfrescoF = TFile.Open("twoMinus.root","read")

frescoH = frescoF.Get("G3")
dataH = dataF.Get("AD_10Be_d0_s6_pid_g2894_corrected_clean_drop_gam")
dataH = ScaleTGraph(dataH)
dataHAfter = sfrescoF.Get("G0")
sfrescoH = sfrescoF.Get("G1")

colors = [ROOT.kGreen, ROOT.kRed, ROOT.kBlue, ROOT.kOrange]

canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
canvas.SetLogy()

Dummy = ROOT.TH2F("Dummy","Checking 2- SFRESCO",90,0,180,1000000,0,1000)
Dummy.GetXaxis().SetTitle("COM Angle in Degrees")
Dummy.GetYaxis().SetTitle("Cross Section in mb/sr")

Dummy.SetStats(ROOT.kFALSE)
Dummy.Draw()

Dummy.SetAxisRange(0,60,"X")
Dummy.SetAxisRange(.00000001,1000,"Y")

leg = TLegend(0.65,.65,.9,.9)

frescoH.SetMarkerColor(colors[0])
frescoH.SetLineColor(colors[0])
frescoH.SetFillColor(ROOT.kWhite)
leg.AddEntry(frescoH,"FRESCO Raw Output")
frescoH.Draw("sameL")

dataH.SetMarkerColor(colors[1])
dataH.SetLineColor(colors[1])
dataH.SetFillColor(ROOT.kWhite)
dataH.SetMarkerStyle(20)
leg.AddEntry(dataH,"Two Minus Data")
dataH.Draw("sameP")


# dataHAfter.SetMarkerColor(colors[2])
# dataHAfter.SetLineColor(colors[2])
# dataHAfter.SetFillColor(ROOT.kWhite)
# dataH.SetMarkerStyle(20)
# leg.AddEntry(dataHAfter,"Two Minus Data after fit")
# dataHAfter.Draw("sameP")

sfrescoH.SetMarkerColor(colors[2])
sfrescoH.SetLineColor(colors[2])
sfrescoH.SetFillColor(ROOT.kWhite)
leg.AddEntry(sfrescoH,"SFRESCO Output")
sfrescoH.Draw("sameL")

leg.Draw()

canvas.SaveAs("twoMinusSFRESCO.png")

