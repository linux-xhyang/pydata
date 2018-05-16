#!/usr/bin/env python

# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Android system-wide tracing utility.

This is a tool for capturing a trace that includes data from both userland and
the kernel.  It creates an HTML file for visualizing the trace.
"""

# Make sure we're using a new enough version of Python.
# The flags= parameter of re.sub() is new in Python 2.7. And Systrace does not
# support Python 3 yet.

import sys, getopt
import optparse
import os
import time
from compdb import compdb_parser

_COMPDB_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))

if _COMPDB_DIR not in sys.path:
    sys.path.insert(0, _COMPDB_DIR)


def main_impl(argv):
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
            print(directory)
        elif opt in ("-f", "--file"):
            file = arg

    if os.path.exists(directory) == True:
        directory = os.path.abspath(directory)
        file = os.path.join(directory, file)
        print('Directory is ', directory)
        print('File is ', file)

        if os.path.exists(file) == True:
            compdb_parser.compdb_parser(directory, file)
        else:
            print("compile_commands.json not exists")
    else:
        print("directory not exists:", directory)


def main():
    main_impl(sys.argv[1:])


if __name__ == '__main__' and __package__ is None:
    main_impl(sys.argv[1:])
