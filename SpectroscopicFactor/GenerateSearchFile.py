from ROOT import TFile, TGraphErrors

scalefactor = 0.77214E-04

def ScaleTGraph(graph):
  for i in range(graph.GetN()):
    graph.GetY()[i] *= scalefactor;
    graph.GetEY()[i] *= scalefactor

  return graph

def WriteGraph(graph):
  for i in range(graph.GetN()):
    outfile.write(" {}  {}  {}\n".format(graph.GetX()[i],graph.GetY()[i],graph.GetEY()[i]))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("Mode", help='Input Location & Name')
args = parser.parse_args()

print "{} mode.".format(args.Mode)

if args.Mode != "1-" and args.Mode != "2+" and args.Mode != "2-":
  print "Mode Unrecognized! Use '1-', '2+', or '2-'"
  quit()

dataF = TFile.Open("pureStates.root","read")
if not dataF:
  print "No dataF"
  quit()

dataStr = "default"
dataPointer = -1

if args.Mode == "1-":
  dataStr = "oneMinus"
  dataPointer = 2
elif args.Mode == "2-":
  dataStr = "twoMinus"
  dataPointer = 3
elif args.Mode == "2+":
  dataStr = "twoPlus"
  dataPointer = 4 

dataPlot = dataF.Get(dataStr+"Graph")
if not dataPlot:
  print "No angular distribution found!  Was looking for: {}".format(dataStr+"Graph")

outfile = open("{}.search".format(dataStr),"w")
outfile.write("'transfer.in' 'transfer.frout'\n")#first line is the original fresco input file

outfile.write('1 ')#print number of variables
outfile.write('1\n')#number of experimental data sets.  ...

outfile.write(" &variable kind=2 name='{}SpecFactor' nafrac={} afrac=.5/\n".format(dataStr,dataPointer))
outfile.write(" &data idir=0 lab=F abserr=T idir=0 iscale=2 ic=2 ia={}/\n".format(dataPointer))
# dataPlot = ScaleTGraph(dataPlot)
WriteGraph(dataPlot)
outfile.write("&\n")
