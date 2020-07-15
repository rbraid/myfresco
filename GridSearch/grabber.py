from ROOT import TFile, TGraph, TF1, TCanvas, TMultiGraph, TGraphErrors, TMath
import ROOT
import argparse
from array import array

def Average(g,low,high):
  npoints = 100
  irange = high-low
  rangeiter = irange/npoints

  isum = 0
  for n in range(npoints+1):
    tmp = g.Eval(low+n*rangeiter)
    isum += tmp
  return isum/npoints

def Blur(graph):
  ringFile = TFile.Open("~/nuclear/mine/analysis/inputRootFiles/DumbRings.root","read")
  if not ringFile:
    print "Can't open RingFile"
    return False
  if graph.GetN() < 20:
    print "Caution, graph has few points, maybe you are grabbing the data by mistake?"

  graphName = "COM_d1_s0_Be11"
  ringGraph = ringFile.Get(graphName)
  if not ringGraph:
    print "Did not find ring graph: {}".format(graphName)

  XArr = array('d')
  # XErrArr = array('d')
  YArr = array('d')
  # YErrArr = array('d')

  for point in range(ringGraph.GetN()):
    x = ringGraph.GetY()[point]
    xerr = (ringGraph.GetEYhigh()[point]+ringGraph.GetEYlow()[point])/2
    tmp = Average(graph,x-xerr,x+xerr)
    XArr.append(x)
    # XErrArr.append(xerr)
    YArr.append(tmp)
    # YErrArr.append(0)

  #outGraph = TGraphErrors(len(XArr),XArr,YArr,XErrArr,YErrArr)
  outGraph = TGraph(len(XArr),XArr,YArr)
  outGraph.SetName(graph.GetName()+"_blurred")
  outGraph.SetTitle(graph.GetTitle()+" blurred")
  return outGraph

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

def MovingAverageBlur(graph):
    debug = False
    # 2.937 for ring 1, 2.955 for ring 5, 3.18 for ring 10
    thetaRes = 3 #this is sigma
    nSigma = 1 #Gives 95.45%

    if debug:
        print graph.GetName()
        graph.Print()

    blurXArr = array('d')
    blurYArr = array('d')

    for centerPoint in range(graph.GetN()):
        centerTheta = graph.GetX()[centerPoint]
        lowerPoint = centerPoint - (thetaRes * nSigma)
        upperPoint = centerPoint + (thetaRes * nSigma)
        if debug:
            print "Points: {} - {} - {}".format(lowerPoint, centerPoint, upperPoint)

        if lowerPoint < 0:
            if debug:
                print "kill centerPoint: {} due to lowerPoint: {} min: 0".format(centerPoint, lowerPoint)
            continue
        elif upperPoint > 175:
            if debug:
                print "kill centerPoint: {} due to upperPoint: {} max: 175".format(centerPoint, upperPoint)
            continue

        sum = 0
        if debug:
            print "sub range {} to {} degrees".format(graph.GetX()[lowerPoint], graph.GetX()[upperPoint])
        for sumPoint in range(lowerPoint,upperPoint):
            sum += graph.GetY()[sumPoint]
        avg = sum / (upperPoint-lowerPoint)
        if debug:
            print "average for {} degrees: {}".format(centerTheta,avg)

        blurXArr.append(centerTheta)
        blurYArr.append(avg)

    retGraph = TGraph(len(blurXArr),blurXArr,blurYArr)
    retGraph.SetName("retGraph")
    if debug:
        print retGraph.GetName()
        retGraph.Print()
        print "\n"
    return retGraph

def graphFunc(x):
   return tmpHisto.Eval(x[0]);

def moveFunc(x):
   return tmpBlur.Eval(x[0]);

def TGraphToTF1(graph):
    xmin = graph.GetX()[0]
    xmax = graph.GetX()[graph.GetN()-1]
    if "_moving" in graph.GetName():
        f = TF1("f", moveFunc, xmin, xmax)
    else:
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
        if len(Zipper) == 1:
            color = ROOT.kBlack
        plot = bigInfo[-1]
        plot.SetMarkerColor(ROOT.kWhite)
        plot.SetLineColor(color)
        plot.SetFillColor(ROOT.kWhite)
        plot.SetLineWidth(2)
        if len(Zipper) > 1:
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


        if len(PlotList) < 4:
            blurPlot = bigInfo[-3]
            blurPlot.SetMarkerColor(color)
            blurPlot.SetLineColor(color)
            blurPlot.SetLineStyle(2)
            blurPlot.SetLineWidth(2)
            blurPlot.SetFillColor(ROOT.kWhite)        # print blurPlot.GetName()
            # blurPlot.Print()
            MG.Add(blurPlot,"L")
            legend.AddEntry(blurPlot,"Blurred Fresco Output")

    MG.Draw("AL")
    canvas.SetLogy()
    MG.GetXaxis().SetTitle("Center of Mass Angle in Degrees")
    MG.GetYaxis().SetTitle("Cross Section in mb/sr")
    MG.Draw()
    legend.Draw()

    outF.cd()
    MG.Write()

    canvas.SaveAs("pngs/{}.png".format(name))

def CalcNorm(fg, dg):
  datY = dg.GetY()[0]
  datX = dg.GetX()[0]

  fresY = fg.Eval(datX)

  return fresY/datY

def MakeCSV(myList):
    csvOut = open("Sorted_Grid_Search.csv","w")
    csvOut.write("Item Number,Chi Square,rC,V,r0,a,W,rW,aW,vSO,rSO,aSO,Norm,BlurChiSquare\n")
    i = 0
    for item in myList:
        csvOut.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(i,item[0],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11], item[12], item[13]))
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

def sfrescoPrint(index):
    tmpItem = myDataList[index]
    # tmpList = [chiSquare, newName, deets[1],deets[2],deets[3],deets[4],deets[5],deets[6],deets[7],deets[8],deets[9],deets[10].replace('.root',''), tmpNorm, tmpScaledDataG, tmpHisto]
    print "elastic.search"
    print "set 1 {}".format(tmpItem[12])
    for i in range(10):
        print "set {} {}".format(i+2, tmpItem[i+2])

    print "fix 1"
    print "fix 2"
    print "fix 3"
    for i in range(9,12):
        print "fix {}".format(i)

    print "q"

    print "min"
    print "migrand"
    print "end"
    print "plot index_{}.plot".format(index)
    print "exit"
    print


def inputLoop():
    userInput = "default"
    while userInput != "quit":
        userInput = raw_input("Index to print, or quit: ")
        if userInput.lower() == "quit" or userInput.lower() == "q":
            userInput = "quit"
            continue
        sfrescoPrint(int(userInput))

def MakeSearchFile(myList):
        # tmpList = [chiSquare, newName, deets[1],deets[2],deets[3],deets[4],deets[5],deets[6],deets[7],deets[8],deets[9],deets[10].replace('.root',''), tmpNorm, tmpScaledDataG, tmpHisto]
    searchOut = open("search_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.search".format(myList[2], myList[3], myList[4],myList[5], myList[6], myList[7],myList[8], myList[9], myList[10], myList[11]), "w")
    searchOut.write("'input_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.in'".format(myList[2], myList[3], myList[4],myList[5], myList[6], myList[7],myList[8], myList[9], myList[10], myList[11]))
    searchOut.write(" 'output_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.out'\n".format(myList[2], myList[3], myList[4],myList[5], myList[6], myList[7],myList[8], myList[9], myList[10], myList[11]))
    searchOut.write("11 1\n")
    searchOut.write(" &variable kind=5 name='norm' dataset=1 datanorm= {}/\n".format(myList[-3]))
    searchOut.write(" &variable kind=1 name='r0C' kp=1 pline=1 col=3 potential={} step=.01/\n".format(myList[2]))
    searchOut.write(" &variable kind=1 name='V' kp=1 pline=2 col=1 potential={}  step=.1/\n".format(myList[3]))
    searchOut.write(" &variable kind=1 name='r0' kp=1 pline=2 col=2 potential={} step=.01/\n".format(myList[4]))
    searchOut.write(" &variable kind=1 name='a' kp=1 pline=2 col=3 potential={} step=.01/\n".format(myList[5]))
    searchOut.write(" &variable kind=1 name='W' kp=1 pline=3 col=4 potential={} step=.1/\n".format(myList[6]))
    searchOut.write(" &variable kind=1 name='rW' kp=1 pline=3 col=5 potential={} step=.01/\n".format(myList[7]))
    searchOut.write(" &variable kind=1 name='aW' kp=1 pline=3 col=6 potential={} step=.01/\n".format(myList[8]))
    searchOut.write(" &variable kind=1 name='Vso' kp=1 pline=4 col=1 potential={}  step=.02/\n".format(myList[9]))
    searchOut.write(" &variable kind=1 name='rso' kp=1 pline=4 col=2 potential={} step=.01/\n".format(myList[10]))
    searchOut.write(" &variable kind=1 name='aso' kp=1 pline=4 col=3 potential={}  step=.01/\n".format(myList[11]))
    searchOut.write(" &data idir=0 lab=F abserr=T iscale=-1 ic=1 ia=1/\n")
    searchOut.write(" 39.059150092  427143.002848  20628.3448026\n")
    searchOut.write(" 31.3199979321  1264600.60779  60618.4318559\n")
    searchOut.write(" 35.4667075188  555170.42659  23887.2534559\n")
    searchOut.write(" 41.2300474345  137036.652493  7433.19265619\n")
    searchOut.write(" 43.9678467908  168671.421207  7230.68806548\n")
    searchOut.write(" 48.189152681  55952.3841828  1876.98824895\n")
    searchOut.write(" 53.1417526255  46114.1973612  1754.08673178\n")
    searchOut.write(" 56.9049315953  20753.5074491  1165.30693998\n")
    searchOut.write(" 61.5991600461  7231.41158925  399.446429064\n")
    searchOut.write(" 66.4747692434  17803.9020474  1081.72089957\n")
    searchOut.write(" 69.4898614779  2681.64788421  438.702489556\n")
    searchOut.write("&\n")

def FindCorrPoint(g, val):
    for testPoint in range(g.GetN()):
        if int(g.GetX()[testPoint]*1000) == int(val*1000):
            return testPoint
    return False

def GraphsChiSquare(dataG, frescoG):
    chiSquare = 0
    for point in range(dataG.GetN()):
        corrPoint = FindCorrPoint(frescoG, dataG.GetX()[point])
        if not corrPoint:
            print "Didn't find a correlated point for dataG X: {}".format(dataG.GetX()[point])
            continue
        Obs = dataG.GetY()[point]
        Exp = frescoG.GetY()[corrPoint]
        chiSquare += TMath.Power( Obs - Exp , 2.)/Exp

    return chiSquare


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

    # print int(float(deets[1])*100)

    if int(float(deets[1])*100) != 63:
        continue

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
    newName = "rC({})_V({})_r({})_a({})_W({})_rW({})_aW({})".format(deets[1],deets[2],deets[3],deets[4],deets[5],deets[6],deets[7])

    tmpHisto.SetName(newName)
    outF.cd()

    tmpHisto.Write()

    tmpBlur = MovingAverageBlur(tmpHisto)
    tmpBlur.SetName(newName+"_moving")
    tmpBlur.Write()

    tmpNorm = CalcNorm(tmpHisto,dataG)
    tmpDataG = dataG.Clone("tmpDataG")
    tmpScaledDataG = ScaleTGraph(tmpDataG,tmpNorm)
    tmpScaledDataG.SetName(newName+"_data")
    outF.cd()

    tmpScaledDataG.Write()

    # blurG = Blur(tmpHisto)
    # outF.cd()
    # blurG.Write()

    func = TGraphToTF1(tmpHisto)
    chiSquare = tmpScaledDataG.Chisquare(func)

    funcBlur = TGraphToTF1(tmpBlur)
    noErrScaledGraph = killXErr(tmpScaledDataG)
    newChiSquare = noErrScaledGraph.Chisquare(funcBlur)

    # newChiSquare = GraphsChiSquare(tmpScaledDataG, blurG)

    tmpList = [chiSquare, newName, deets[1],deets[2],deets[3],deets[4],deets[5],deets[6],deets[7],deets[8],deets[9],deets[10].replace('.root',''), tmpNorm, newChiSquare,  tmpBlur, tmpScaledDataG, tmpHisto]
    myDataList.append(tmpList)

myDataList.sort(key=lambda x: x[13])
# print "Read in {} files successfully.".format(len(myDataList))
if len(myDataList) == 0:
    quit()

MakeCSV(myDataList)

# MakeCorrGraphs(myDataList)
# MakePlot(myDataList,"First_Five")
#

IndexList = [356] #range(0,40)
curatedList = []

for index in IndexList:
    tmpList = []
    tmpList.append(myDataList[index])
    curatedList.append(myDataList[index])
    MakePlot(tmpList,"Index_{}".format(index))

    # sfrescoPrint(index)

# MakePlot(curatedList,"All_3")

# for item in curatedList:
#     MakeSearchFile(item)

# inputLoop()
