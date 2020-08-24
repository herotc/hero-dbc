# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv
import json
from collections import OrderedDict

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', 'hero-dbc'))

## Mapping
#Covenant.id = Soulbind.id_covenant


# Get every spell id associated to an item effect
Covenants = []
with open(os.path.join(generatedDir, 'Covenant.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        covenant = {
            'covenantId': int(row['id']),
            'covenantName': row['name'],
            'soulbinds': []
        }
        Covenants.append(covenant)
    


with open(os.path.join(generatedDir, 'Soulbind.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    Soulbinds = []
    for row in reader:
        soulbind = {
            'soulbindId': int(row['id']),
            'soulbindName': row['name']
        }
        for index in range(len(Covenants)):
            if Covenants[index]["covenantId"] == int(row['id_covenant']):
                Covenants[index]["soulbinds"].append(soulbind)

# Full output
with open(os.path.join(parsedDir, 'Soulbinds.json'), 'w') as jsonFile:
    json.dump(Covenants, jsonFile, indent=4, sort_keys=True)