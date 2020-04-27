import argparse
parser = argparse.ArgumentParser()
parser.add_argument("File", help='Input Location & Name')
args = parser.parse_args()

# outFile = file('output.csv','w')

infile = file(args.File,"r")

if not infile:
    print "No infile! Looked for {}".format(args.File)
    quit()

atResults = False

for line in infile:
    if atResults:
        if "minuit>" in line:
            quit()
        else:
            print line.rstrip()
    elif "STATUS=CONVERGED" in line:
        atResults = True
        print line.rstrip()
    else:
        continue
