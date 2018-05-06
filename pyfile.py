#!/usr/bin/python

import sys, getopt, re
import json
import os

rules = {}
out_dir = ''


class rule:
    target = ''
    module = ''
    file = ''
    deps = ''
    command = ''

    def __init__(self, target, module, file, deps, command):
        self.target = target
        self.module = module
        self.file = file
        self.deps = deps
        self.command = command

    def tostring(self):
        return "module :" + self.module + '\n' + "deps :" + self.deps + '\n' + "file :" + self.file + '\n' + "command :" + self.command + '\n'

    def tojson(self):
        global out_dir
        return json.dumps(
            {
                "directory": out_dir,
                "command": self.command,
                "file": self.file
            },
            indent=True)


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


def rule_parser(dir, file):
    global out_dir
    out_dir = dir
    rfile = open(file, "r")
    wf = os.path.join(dir, "compile_commands.json")
    wfile = open(wf, "w")

    rule_re = re.compile("rule rule[0-9]+")

    begin = False

    desc = None
    deps = None
    command = None

    line = rfile.readline()
    while line:
        if begin == True:
            if re.match(r" description = ", line):
                desc = re.split(r"=|:|<= ", line.strip('\n'))
            elif re.match(r" deps = ", line):
                deps = re.split(r" = ", line.strip('\n'))
            elif re.match(r" command = ", line):
                command = re.split(r" = ", line.strip('\n'))
                command = re.split("\"\(| \) ", command[1])

            if desc and deps and command:
                if deps[1] == "gcc" and len(desc) > 3 and len(command) > 1:
                    rules[desc[3]] = rule(desc[1], desc[2], desc[3], deps[1],
                                          command[1].replace("\$", ""))
                    begin = False
                    desc = None
                    deps = None
                    command = None

        if re.match(rule_re, line):
            desc = None
            deps = None
            command = None
            begin = True
        line = rfile.readline()
    wfile.write("[\n")
    for key, value in rules.items():
        wfile.write(value.tojson())
        wfile.write(",\n")
    wfile.write("]")
    wfile.close()


def main(argv):
    directory = ''
    file = ''

    try:
        opts, args = getopt.getopt(argv, "hd:f:", ["dir=", "file="])
    except getopt.GetoptError:
        print('pyfile.py -d <directory> -f <build-file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pyfile.py -d <directory> -f <build-file>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            directory = arg
        elif opt in ("-f", "--file"):
            file = arg

    if os.path.exists(directory) == True:
        directory = os.path.abspath(directory)
        file = os.path.join(directory, file)
        print('Directory is ', directory)
        print('File is ', file)

        if os.path.exists(file) == True:
            rule_parser(directory, file)
        else:
            print("compile_commands.json not exists")
    else:
        print("directory not exists")


if __name__ == "__main__":
    main(sys.argv[1:])

#~/src/pydata/pyfile.py -d . -f out/build-anglee.ninja
