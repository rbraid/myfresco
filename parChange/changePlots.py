from ROOT import TGraph, TMultiGraph, TFile, TCanvas
import ROOT

def MakePlot(PlotList, Mode):
    colors = [ROOT.kRed,ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kCyan, ROOT.kMagenta]

    MG = TMultiGraph()
    MG.SetTitle("Varying {};Center of Mass Angle in Degrees;Cross Section in mb/sr".format(Mode))
    MG.SetTitle("MG_{}".format(Mode))
    MG.SetName("MG_{}".format(Mode))
    legend = ROOT.TLegend(0.65,.65,.9,.9)

    Zipper = zip(PlotList,colors)

    for plot, color in Zipper:
        plot.SetMarkerColor(ROOT.kWhite)
        plot.SetLineColor(color)
        plot.SetFillColor(ROOT.kWhite)
        plot.SetLineWidth(2)
        MG.Add(plot,"L")
        legend.AddEntry(plot,plot.GetName())

    MG.Draw("AL")
    canvas.SetLogy()
    MG.GetXaxis().SetTitle("Center of Mass Angle in Degrees")
    MG.GetYaxis().SetTitle("Cross Section in mb/sr")
    MG.Draw()
    legend.Draw()

    canvas.SaveAs("vary_{}.png".format(Mode))

canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)

outFile = TFile.Open("diagChangePlots.root","recreate")

VList = [20,40,60,80,100]
VHistos = []
for potential in VList:
    fileName = "elastic_V{}.root".format(potential)
    tmpFile = TFile.Open(fileName,"read")
    if not tmpFile:
        print "Didn't Find {}".format(fileName)
        continue
    tmpG = tmpFile.Get("G0")
    if not tmpG:
        print "No G0 in {}".format(fileName)
        continue
    tmpG.SetName("V{}".format(potential))
    outFile.cd()
    tmpG.Write()
    VHistos.append(tmpG)

RHistos = []
for radius in range(9,15):
    fileName = "elastic_R{}.root".format(radius)
    tmpFile = TFile.Open(fileName,"read")
    if not tmpFile:
        print "Didn't Find {}".format(fileName)
        continue
    tmpG = tmpFile.Get("G0")
    if not tmpG:
        print "No G0 in {}".format(fileName)
        continue
    tmpG.SetName("R{}".format(radius))
    outFile.cd()
    tmpG.Write()
    RHistos.append(tmpG)

AHistos = []
for diffuseness in range(6,10):
    fileName = "elastic_A{}.root".format(diffuseness)
    tmpFile = TFile.Open(fileName,"read")
    if not tmpFile:
        print "Didn't Find {}".format(fileName)
        continue
    tmpG = tmpFile.Get("G0")
    if not tmpG:
        print "No G0 in {}".format(fileName)
        continue
    tmpG.SetName("A{}".format(diffuseness))
    outFile.cd()
    tmpG.Write()
    AHistos.append(tmpG)

MakePlot(VHistos,"V")
MakePlot(RHistos,"R")
MakePlot(AHistos,"A")
