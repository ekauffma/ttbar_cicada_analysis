import os
import json

datasets = {
    "TTbar": [
        "/eos/cms/store/group/phys_exotica/axol1tl/MC_ScoutingNano_withAXOscore/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/ScoutingNano_TTto2L2Nu_withAXOscore_20241024/"
    ],
    "Scouting2024I": [
        "/eos/cms/store/group/phys_exotica/axol1tl/Data_ScoutingNano_withAXOscore/2024I/"
    ]
}


def list_root_files(directory, n_files=-1):
    root_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.root'):
                full_path = os.path.join(dirpath, filename)
                root_files.append(full_path)
            if (len(root_files)>n_files) and (n_files!=-1): break
        if (len(root_files)>n_files) and (n_files!=-1): break
    return root_files

filePaths = {}
for k,v in datasets.items():
    root_files = []
    for directory in v:
        if k=="TTbar":
            root_files += list_root_files(directory)
        else:
            root_files += list_root_files(directory, n_files=500)
    filePaths[k] = root_files

with open("filePaths.json", "w") as outfile:
    json.dump(filePaths, outfile, indent=4)


