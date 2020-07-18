from ROOT import TFile, TGraphErrors

def WriteGraph(graph):
  for i in range(graph.GetN()):
    outfile.write(" {}  {}  {}\n".format(graph.GetX()[i],graph.GetY()[i],graph.GetEY()[i]))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("Mode", help='Input Location & Name')
args = parser.parse_args()

# print "{} mode.".format(args.Mode)

if args.Mode != "oneMinus" and args.Mode != "twoPlus" and args.Mode != "twoMinus":
  print "Mode Unrecognized! Use 'oneMinus', 'twoPlus', or 'twoMinus'"
  quit()

dataF = TFile.Open("pureStates.root","read")
if not dataF:
  print "No dataF"
  quit()

dataPointer = -1

if args.Mode == "oneMinus":
  dataPointer = 3
elif args.Mode == "twoMinus":
  dataPointer = 4
elif args.Mode == "twoPlus":
  dataPointer = 2

dataPlot = dataF.Get(args.Mode+"Graph")
if not dataPlot:
  print "No angular distribution found!  Was looking for: {}".format(args.Mode+"Graph")

outfile = open("{}.search".format(args.Mode),"w")
outfile.write("'transfer.in' 'transfer.frout'\n")#first line is the original fresco input file

outfile.write('1 ')#print number of variables
outfile.write('1\n')#number of experimental data sets.  ...

#ia is the excitation pair number aka index of card 7.  card 7 is the states aka partition
#nfrac is the odrer of card 17.  Card 17 is the spectroscopic amplutudes aka my couplings

outfile.write(" &variable kind=2 name='{}SpecFactor' nafrac={} afrac=1/\n".format(args.Mode,dataPointer))
outfile.write(" &data idir=0 lab=F abserr=T iscale=2 ic=2 ia={}/\n".format(dataPointer))
# dataPlot = ScaleTGraph(dataPlot)
WriteGraph(dataPlot)
outfile.write("&\n")
