import json
import os
import re
import subprocess
import sys

back_list_projects = ["/common"]


class Project:
    def __init__(self, dir):
        self.root = dir
        self.items = []

    def add_file(self, item):
        #print("root ",self.root,",add file ",item['file'])
        self.items.append(item)

    def compdb_write(self):
        wf = os.path.join(self.root, "compile_commands.json")

        with open(wf, 'w') as f:
            f.write("[\n")
            first = True
            for entry in self.items:
                if first:
                    first = False
                else:
                    f.write(",\n")
                f.write(json.dumps(entry, indent=1))

            print("file count :", len(self.items))

            f.write("\n]")


def find_vcs_root(test, dirs=(".git", ), default=None):
    import os
    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.isdir(os.path.join(test, d)) for d in dirs):
            return test
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return default


def reserve_cmd(dir, cmd, debug):
    cmd = cmd.lstrip()
    reserves = re.findall('\$\(cat (.*?)\)', cmd)
    includes = " "

    for file in reserves:
        rf = os.path.join(dir, file)
        if debug:
            print(rf)

        try:
            with open(rf, "r") as f:
                includes = includes + " " + (f.read().replace('\n', ' '))
        except FileNotFoundError:
            None

    cmd = re.sub('(\$\(cat .*?\))', includes, cmd)

    return cmd


def is_blacklist_project(name):
    cur_dir = os.getcwd()
    for project in back_list_projects:
        if (name.replace(cur_dir, "") == project):
            return True
    return False


def compdb_parser(dir, file):
    rfile = open(file, "r")
    projects = {}

    os.chdir(dir)
    command = [
        os.path.join(os.path.dirname(__file__), "ninja"), '-f', file, '-t',
        'compdb'
    ]

    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = proc.stdout.read()
    json_data = json.loads(output, strict=False)
    r1 = re.compile(r"\.cpp$|\.c$|\.cxx$|\.cc$")

    for item in json_data:
        if item.__contains__('file'):
            if r1.search(item['file']):
                directory = item['directory']
                build_cmd = item['command']
                if build_cmd.__contains__('PWD=/proc/self/cwd '):
                    build_cmd = re.split(r"PWD=\/proc\/self\/cwd ", build_cmd)
                else:
                    build_cmd = re.split(r"\/bin\/bash -c \"\(| \) &&",
                                         build_cmd)

                if (len(build_cmd) > 1) and str.lstrip(
                        build_cmd[1]).startswith('prebuilts'):
                    build_cmd = build_cmd[1]
                    build_cmd = build_cmd.replace("\t", "")
                    build_cmd = build_cmd.replace("((packed))", "")
                    build_cmd = build_cmd.replace("\$(cat", "$(cat")
                    build_cmd = build_cmd.strip('"')
                    quote = re.compile('\\\\+\"')
                    build_cmd = re.sub(quote, r'\\"', build_cmd)

                    root = find_vcs_root(item['file'])
                    if root:
                        item['command'] = reserve_cmd(item['directory'],
                                                      build_cmd, False)

                        project = projects.get(root)
                        if project is None:
                            projects[root] = Project(root)
                            project = projects[root]
                        project.add_file(item)
    #now write
    print("project count ", len(projects))
    for name in projects.keys():
        print("project ", name)
        if is_blacklist_project(name):
            print(name + " is black list project")
        else:
            projects[name].compdb_write()
