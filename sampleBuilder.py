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
    'analysisObjectNtuplizer/PATObjects',
]
treeNames_tt= [
    'analysisObjectNtuplizer/PATObjects',
    'l1CaloSummaryEmuTree/L1CaloSummaryTree'
]

samples = {
    "ZeroBias": sample(listOfFiles = filePaths["ZeroBias"], treeNames = treeNames),
    "TTbar": sample(listOfFiles = filePaths["TTbar"], treeNames = treeNames_tt)
}

f.close()

