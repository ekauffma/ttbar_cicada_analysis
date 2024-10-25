import os
import json

datasets = {
    "TTbar": [
        #"/hdfs/store/user/ekauffma/TT_TuneCP5_13p6TeV_powheg-pythia8/CICADAAnalysis_TTbar_Run3Winter24Digi_20240901/"
        "/hdfs/store/user/ekauffma/TTbarAnalysisFiles/TTbar/"
    ],
    "ZeroBias": [
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20240927/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241001/241001_144625/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241003/241004_001642/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241006/241006_200947/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241010/241010_163200/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241011/241011_160909/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241013/241013_183202/",
        "/hdfs/store/user/ekauffma/ZeroBias/CICADAAnalysis_ZeroBias_2024G_20241015/241016_025534/"
    ]
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
    #outfile.write(json.dumps(json.loads(filePaths), indent=4, sort_keys=True))
    #json.dump(filePaths, outfile)
    json.dump(filePaths, outfile, indent=4)


