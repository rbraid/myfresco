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

dataF = TFile.Open("~/nuclear/mine/rb/angulardistribution/angOutReal.root","read")
if not dataF:
  print "No dataF"
  quit()

tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_g2894_corrected_clean_drop_gam")#corresponds to 6263 2-
if not tmpPlot:
  print "No 2894"

outfile = open("twoMinus.search","w")
outfile.write("'transfer.in' 'transfer.frout'\n")#first line is the original fresco input file

outfile.write('1 ')#print number of variables
outfile.write('1\n')#number of experimental data sets.  ...

outfile.write(" &variable kind=2 name='2MinusSpecFactor' nafrac=3 afrac=.5/\n")
outfile.write(" &data idir=0 lab=F abserr=T idir=0 iscale=2 ic=2 ia=3/\n")
tmpPlot = ScaleTGraph(tmpPlot)
WriteGraph(tmpPlot)
outfile.write("&\n")
