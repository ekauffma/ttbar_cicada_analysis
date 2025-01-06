import sys
import os
import json

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from sample import sample

f = open("filePaths.json")
filePaths = json.load(f)

treeNames = [
    'Events',
]

samples = {
    "TTbar": sample(listOfFiles = filePaths["TTbar"], treeNames = treeNames),
    "Scouting2024I": sample(listOfFiles = filePaths["Scouting2024I"], treeNames = treeNames)
}

f.close()

