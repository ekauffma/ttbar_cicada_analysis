import os
import json

datasets = {
    "TTbar": [
        "/hdfs/store/user/ekauffma/TT_TuneCP5_13p6TeV_powheg-pythia8/ScoutingNano_TTbar_20241217/241217_215742/"
    ],
}


def list_root_files(directory):
    root_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.root'):
                full_path = os.path.join(dirpath, filename)
                root_files.append(full_path)
    return root_files

filePaths = {}
for k,v in datasets.items():
    root_files = []
    for directory in v:
        root_files += list_root_files(directory)
    filePaths[k] = root_files

with open("filePaths.json", "w") as outfile:
    json.dump(filePaths, outfile, indent=4)


