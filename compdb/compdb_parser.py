import json
import os
import re
import subprocess
import sys


def compdb_parser(dir, file):
    rfile = open(file, "r")
    wf = os.path.join(dir, "compile_commands.json")

    os.chdir(dir)
    command = [
        os.path.join(os.path.dirname(__file__), "ninja"), '-f', file, '-t',
        'compdb', 'all'
    ]

    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = proc.stdout.read()
    json_data = json.loads(output, strict=False)
    with open(wf, 'w') as f:
        r1 = re.compile(r"\.cpp$|\.c$|\.cxx$|\.cc$")
        f.write("[\n")
        file_count = 0

        first = True
        for item in json_data:
            if item.__contains__('file'):
                if r1.search(item['file']):
                    file_count += 1
                    build_cmd = item['command']
                    if build_cmd.__contains__('PWD=/proc/self/cwd  '):
                        build_cmd = re.split(r"PWD=\/proc\/self\/cwd  ",
                                             build_cmd)
                    else:
                        build_cmd = re.split(r"\/bin\/bash -c \"\(| \) &&",
                                             build_cmd)

                    if (len(build_cmd) >
                            1) and build_cmd[1].startswith('prebuilts'):
                        build_cmd = build_cmd[1]
                        build_cmd = build_cmd.replace("\t", "")
                        build_cmd = build_cmd.replace("((packed))", "")
                        build_cmd = build_cmd.replace("\$(cat", "$(cat")
                        build_cmd = build_cmd.strip('"')
                        quote = re.compile('\\\\+\"')
                        build_cmd = re.sub(quote, r'\\"', build_cmd)

                        item['command'] = build_cmd
                        if first == False:
                            f.write(",\n")
                        else:
                            first = False

                        f.write(json.dumps(item, indent=1))

        print("file count :", file_count)

        f.write("\n]")
