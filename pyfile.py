#!/usr/bin/python

import sys, getopt

def file_process(src,dst):
    rfile = open(src, "r")
    wfile = open(dst, "w")
    alline = rfile.readlines()
    h = {}
    for i in alline:
        if not h.has_key(i):
            h[i] = 1
            wfile.write(i)
    wfile.close()

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts,args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file_process is "', inputfile
    print 'Output file is "', outputfile
    file_process(inputfile,outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
