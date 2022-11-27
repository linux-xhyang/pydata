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
    debugger = 'vscode-gdb'
    host = '127.0.0.1'
    try:
        opts, args = getopt.getopt(argv, "hf:d:s:", ["file=","debugger="])
    except getopt.GetoptError:
        print('gdbclient -f <binary-file> -d <vscode-gdb/vscode-lldb> -s <device>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('gdbclient -f <binary-file> -d <vscode-gdb/vscode-lldb> -s <device>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-d", "--debugger"):
            debugger = arg
        elif opt in ("-s", "--serial"):
            host = arg

    if os.path.exists(file) == True:
        root = os.environ["ANDROID_BUILD_TOP"]
        sysroot = os.path.join(os.environ["ANDROID_PRODUCT_OUT"], "symbols")
        is64bit = False
        linker_search_dir = os.path.join(sysroot,"system/bin")
        if debugger == 'vscode-gdb':
            debugger_path = "arm-linux-gdb"
        else:
            debugger_path = "~/src/android/prebuilts/clang/host/linux-x86/clang-r450784d/bin/lldb.sh"
        port = 5039
        binary_file = open(file,"r")
        setup_commands = gdbclient.generate_setup_script(debugger_path,sysroot,linker_search_dir,binary_file,host,is64bit,port,debugger,connect_timeout=5)
        print("")
        print(setup_commands)
        print("")
    else:
        print("binary file not exists")

def main():
    main_impl(sys.argv[1:])

if __name__ == '__main__':
  sys.exit(main())
