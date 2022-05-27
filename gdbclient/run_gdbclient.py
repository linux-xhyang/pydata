#!/usr/bin/env python3

import sys, getopt
import optparse
import os
import time

_GDBCLIENT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))

from gdbclient import gdbclient

if _GDBCLIENT_DIR not in sys.path:
    sys.path.insert(0, _GDBCLIENT_DIR)

def main_impl(argv):
    file = ''

    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print('pyfile.py -f <build-file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pyfile.py -f <build-file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg

    if os.path.exists(file) == True:
        root = os.environ["ANDROID_BUILD_TOP"]
        sysroot = os.path.join(os.environ["ANDROID_PRODUCT_OUT"], "symbols")
        is64bit = False
        linker_search_dir = os.path.join(sysroot,"system/bin")
        debugger = "vscode-gdb"
        debugger_path = "arm-linux-gdb"
        port = 7777
        binary_file = open(file,"r")
        setup_commands = gdbclient.generate_setup_script(debugger_path,sysroot,linker_search_dir,binary_file,is64bit,port,debugger,connect_timeout=5)
        print("")
        print(setup_commands)
        print("")
    else:
        print("file not exists")

def main():
    main_impl(sys.argv[1:])

if __name__ == '__main__':
  sys.exit(main())
