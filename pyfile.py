#!/usr/bin/python

import sys, getopt,re
import pandas as pd
import json
import os

rules = {}
class rule:
    target = ''
    module = ''
    file = ''
    deps = ''
    command = ''
    def __init__(self,target,module,file,deps,command):
        self.target = target
        self.module = module
        self.file = file
        self.deps = deps
        self.command = command

    def tostring(self):
        return "module :" + self.module + '\n' + "deps :" + self.deps + '\n' + "file :" + self.file + '\n' +"command :" + self.command + '\n'
    def tojson(self):
        return json.dumps({"directory":os.getenv("PWD"),"command":self.command,"file":self.file},indent=True)

def file_process(src, dst):
    rfile = open(src, "r")
    wfile = open(dst, "w")
    alline = rfile.readlines()
    h = {}
    for i in alline:
        if not h.has_key(i):
            h[i] = 1
            wfile.write(i)
    wfile.close()

def rule_parser(src,dst):
    rfile = open(src, "r")
    wfile = open(dst, "w")

    rule_re = re.compile("rule rule[0-9]+")

    begin = False

    desc = None
    deps = None
    command = None

    line = rfile.readline()
    while line:
        if begin == True:
            if re.match(r" description = ",line):
                desc = re.split(r"=|:|<= ",line.strip('\n'))
            elif re.match(r" deps = ",line):
                deps = re.split(r" = ",line.strip('\n'))
            elif re.match(r" command = ",line):
                command = re.split(r" = ",line.strip('\n'))
                command = re.split("\"\(| \) ",command[1])

            if desc and deps and command:
                if deps[1] == "gcc" and len(desc) > 3 and len(command) > 1:
                    rules[desc[3]] = rule(desc[1],desc[2],desc[3],deps[1],command[1].replace("\$",""))
                    begin = False
                    desc = None
                    deps = None
                    command = None

        if re.match(rule_re,line):
            desc = None
            deps = None
            command = None
            begin = True
        line = rfile.readline()
    wfile.write("[\n")
    for key,value in rules.items():
        wfile.write(value.tojson())
        wfile.write(",\n")
    wfile.write("]")
    wfile.close()

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file_process is "', inputfile)
    print('Output file is "', outputfile)
    rule_parser(inputfile, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])
