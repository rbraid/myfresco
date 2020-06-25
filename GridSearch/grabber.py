from ROOT import TFile, TGraph, TF1, TCanvas, TMultiGraph, TGraphErrors
import ROOT
import argparse
from array import array

def killXErr(graph):
  if not graph:
    return

  ArrX = array('d')
  ArrY = array('d')
  ArrXErr = array('d')
  ArrYErr = array('d')

  for point in range(graph.GetN()):
    ArrX.append(graph.GetX()[point])
    ArrY.append(graph.GetY()[point])
    ArrXErr.append(0)
    ArrYErr.append(graph.GetEY()[point])

  tmpG = TGraphErrors(len(ArrX),ArrX,ArrY,ArrXErr,ArrYErr)
  tmpG.SetName(graph.GetName()+"_noErr")
  tmpG.SetTitle(graph.GetTitle())
  tmpG.GetXaxis().SetTitle(graph.GetXaxis().GetTitle())
  tmpG.GetYaxis().SetTitle(graph.GetYaxis().GetTitle())
  #tmpG.Write()
  return tmpG

def graphFunc(x):
   return tmpHisto.Eval(x[0]);

def TGraphToTF1(graph):
    xmin = graph.GetX()[0]
    xmax = graph.GetX()[graph.GetN()-1]
    f = TF1("f", graphFunc, xmin, xmax)
    return f

def ScaleTGraph(graph,scalefactor):
    for i in range(graph.GetN()):
        graph.GetY()[i] = graph.GetY()[i]*scalefactor
        graph.GetEY()[i] = graph.GetEY()[i]*scalefactor

    graph.GetYaxis().SetTitle("Cross section in mb/sr")
    return graph

def MakePlot(PlotList,name):
    canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)

    colors = [ROOT.kRed,ROOT.kBlue, ROOT.kGreen, ROOT.kCyan, ROOT.kMagenta] # ROOT.kOrange+1,

    MG = TMultiGraph()
    MG.SetTitle("Best Fits per Chi Square;Center of Mass Angle in Degrees;Cross Section in mb/sr")
    MG.SetTitle("MG")
    MG.SetName(name)
    legend = ROOT.TLegend(0.3,.65,.9,.9)

    # if len(PlotList) >6:
    #     PlotList = PlotList[:6]
    #     print "Cutting PlotList length for {}".format(name)
    #
    Zipper = zip(PlotList,colors)
    #
    # MG.Add(dataG,"P")
    # legend.AddEntry(dataG,"Data")
    i=2
    for bigInfo, color in Zipper:
        plot = bigInfo[-1]
        plot.SetMarkerColor(ROOT.kWhite)
        plot.SetLineColor(color)
        plot.SetFillColor(ROOT.kWhite)
        plot.SetLineWidth(2)
        plot.SetLineStyle(i)
        i += 1
        MG.Add(plot,"L")
        legend.AddEntry(plot,"chiSquare("+str(int(bigInfo[0]))+")_"+plot.GetName())

        dataPlot = bigInfo[-2]
        dataPlot.SetMarkerColor(ROOT.TColor.GetColorDark(color))
        dataPlot.SetLineColor(ROOT.TColor.GetColorDark(color))
        dataPlot.SetFillColor(ROOT.kWhite)
        MG.Add(dataPlot,"P")
        legend.AddEntry(dataPlot,"data_chiSquare("+str(int(bigInfo[0]))+")_"+plot.GetName())

    MG.Draw("AL")
    canvas.SetLogy()
    MG.GetXaxis().SetTitle("Center of Mass Angle in Degrees")
    MG.GetYaxis().SetTitle("Cross Section in mb/sr")
    MG.Draw()
    legend.Draw()

    outF.cd()
    MG.Write()

    canvas.SaveAs("{}.png".format(name))

def CalcNorm(fg, dg):
  datY = dg.GetY()[0]
  datX = dg.GetX()[0]

  fresY = fg.Eval(datX)

  return fresY/datY

def MakeCSV(myList):
    csvOut = open("grabber.csv","w")
    csvOut.write("Item Number, Chi Square, rC, V, r0, a, W\n")
    i = 0
    for item in myList:
        csvOut.write("{},{},{},{},{},{},{}\n".format(i,item[0],item[2],item[3],item[4],item[5],item[6]))
        i +=1
    csvOut.close()

def MakeCorrGraphs(bigList):
    for varSpot in range(2,7):
        chiSquare = array('d')
        varVal = array('d')
        varName = "Default"
        if varSpot == 2:
            varName = "rC"
        elif varSpot == 3:
            varName = "V"
        elif varSpot == 4:
            varName = "r0"
        elif varSpot == 5:
            varName = "a"
        elif varSpot == 6:
            varName = "W"
        else:
            varName = "FellThrough_{}".format(varSpot)

        # print "VarSpot {}, VarName {}".format(varSpot,varName)

        for littleList in bigList:
            # print "chiSquare: {}, varVal: {}".format(littleList[0], float(littleList[varSpot]))
            chiSquare.append(littleList[0])
            varVal.append(float(littleList[varSpot]))

        tmpGraph = TGraph(len(chiSquare),chiSquare,varVal)
        tmpGraph.SetTitle("Correlation Check;ChiSquare;"+varName)
        tmpGraph.SetName(varName+"_vs_ChiSquare")
        tmpGraph.Write()

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")

myargs = parser.parse_args()

dataF = TFile.Open("~/nuclear/mine/rb/angulardistribution/angOutReal.root","read")
if not dataF:
    print "No DataF"
    quit()
dataG = dataF.Get("AD_d0_s0_pid_11Be_sub")
if not dataG:
    print "No dataG"
    quit()

# dataG = ScaleTGraph(dataG, norm)
# dataG = killXErr(dataG)

dataG.SetName("Data_Graph")
dataG.SetMarkerColor(ROOT.kBlack)
dataG.SetLineColor(ROOT.kBlack)
dataG.SetMarkerStyle(20)
dataG.SetFillColor(ROOT.kWhite)

outF = TFile.Open("outGrabber.root","recreate")
dataG.Write()

myDataList = []

for fileStr in myargs.files:
    deets = fileStr.split("_")
    tmpFile = TFile.Open(fileStr,"read")
    if not tmpFile:
        print "Error opening {}".format(fileStr)
        continue

    tmpHisto = tmpFile.Get("G0")
    if not tmpHisto:
        print "No G0 in {}".format(fileStr)
        continue

    outF.cd()
    # newName = "rC({})_V({})_r({})_a({})_W({})_rW({})_aW({})_Vso({})_rso({})_aso({})".format(deets[1],deets[2],deets[3],deets[4],deets[5],deets[6],deets[7],deets[8],deets[9],deets[10].replace('.root',''))
    newName = "rC({})_V({})_r({})_a({})_W({})".format(deets[1],deets[2],deets[3],deets[4],deets[5])

    tmpHisto.SetName(newName)
    tmpHisto.Write()

    tmpNorm = CalcNorm(tmpHisto,dataG)
    tmpDataG = dataG.Clone("tmpDataG")
    tmpScaledDataG = ScaleTGraph(tmpDataG,tmpNorm)
    tmpScaledDataG.SetName(newName+"_data")

    func = TGraphToTF1(tmpHisto)
    chiSquare = tmpScaledDataG.Chisquare(func)

    tmpList = [chiSquare, newName, deets[1],deets[2],deets[3],deets[4],deets[5],deets[6],deets[7],deets[8],deets[9],deets[10].replace('.root',''), tmpScaledDataG, tmpHisto]
    myDataList.append(tmpList)

myDataList.sort(key=lambda x: x[0])

MakeCSV(myDataList)

# MakeCorrGraphs(myDataList)
# MakePlot(myDataList,"First_Five")
#
curatedList = []
#procedure: drop rC above 1.3, and below 1.1
#drop r0 not equal to rC
#sort by chi square and select widely varying models to compare

# curatedList.append(myDataList[345]) #low V and W
# curatedList.append(myDataList[181]) #high V and W
# curatedList.append(myDataList[253]) #high R vals with medium potentials
# curatedList.append(myDataList[121]) #low R vals with medium-high potentials
# curatedList.append(myDataList[157]) # average all together
# #didn't pay attention to a much, since we saw it had a smaller effect
# MakePlot(curatedList,"Ryans_Curated_Five")
#
# #
curatedList.append(myDataList[2])
curatedList.append(myDataList[14])
curatedList.append(myDataList[22])
curatedList.append(myDataList[29])
curatedList.append(myDataList[78])

MakePlot(curatedList,"Freds_Curated_List")
