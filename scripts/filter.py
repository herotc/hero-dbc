#!/usr/bin/env python3

import datetime
import json
import math
import subprocess
import os
from os import path, chdir, system, getcwd

filterStartTime = math.floor(datetime.datetime.now().timestamp())

# Use the actual script directory rather than calculating it
scriptsDirPath = os.path.dirname(os.path.abspath(__file__))

cdnDirPath = path.join(scriptsDirPath, 'CDN')
simcDirPath = path.normpath(path.join(os.path.dirname(scriptsDirPath), '..', 'simc'))

# Load tasks information (from hero-dbc/scripts/tasks.json)
tasksPath = path.join(scriptsDirPath, 'tasks.json')
with open(tasksPath) as tasksFile:
    tasks = json.load(tasksFile)

# Find the wow version (using hero-dbc/scripts/tools/wowVersion.py)
toolsPath = path.join(scriptsDirPath, 'tools')
chdir(toolsPath)

wowVersionCmd = f'python wowVersion.py --cdnDirPath={cdnDirPath}'
wowVersionProc = subprocess.Popen(wowVersionCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
version = wowVersionProc.communicate()[0].decode().rstrip()

# Parsers (using hero-dbc/scripts/filters)
filtersPath = path.join(scriptsDirPath, 'filters')
chdir(filtersPath)
print('Parsing client data from CSV...')
for filter in tasks['filters']:
    print(f'Filtering {filter}...')
    system(f'python {filter}.py')

# Update .lua meta info (using hero-dbc/scripts/tools/luaMeta.py)
chdir(toolsPath)
metaCmd = f'python luaMeta.py --mtime={filterStartTime} --version={version}'
system(metaCmd)
