import sys, re
import json
import os
import subprocess
import re


def compdb_parser(dir, file):
    rfile = open(file, "r")
    wf = os.path.join(dir, "compile_commands.json")

    os.chdir(dir)
    command = [
        os.path.join(os.path.dirname(__file__), "ninja"), '-f', file, '-t',
        'compdb', 'all'
    ]

    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    output = proc.stdout.read()
    json_data = json.loads(output, strict=False)

    with open(wf, 'w') as f:
        r1 = re.compile(r"\.cpp$|\.c$|\.cxx$")
        f.write("[\n")
        file_count = 0

        first = True
        for item in json_data:
            if item.__contains__('file'):
                if r1.search(item['file']):
                    file_count += 1
                    build_cmd = item['command']
                    build_cmd = re.split(r"PWD=\/proc\/self\/cwd ", build_cmd)
                    if (len(build_cmd) > 1):
                        build_cmd = build_cmd[1]
                        build_cmd = build_cmd.replace("\t", "")
                        build_cmd = build_cmd.strip('"')
                        build_cmd = build_cmd.replace("\\", "")

                        item['command'] = build_cmd
                        if first == False:
                            f.write(",\n")
                        else:
                            first = False

                        f.write(json.dumps(item, indent=1))

        print("file count :", file_count)

        f.write("\n]")
