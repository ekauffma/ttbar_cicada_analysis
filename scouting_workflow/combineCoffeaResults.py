import awkward as ak
import dill
n_chunks = 10
#chunk_list = [155,156,157]#,158,159,160]

# dataset = "TT_TuneCP5_13p6TeV_powheg-pythia8"
dataset = "Scouting_2024I"

trigger_list = [
    "DST_PFScouting_CICADAMedium",
    "DST_PFScouting_CICADATight",
    "DST_PFScouting_CICADAVTight",
    "DST_PFScouting_ZeroBias"
]
branch_list = [
    "trijet_mass",
    "trijet_phi"
]
output_filename_pkl = f"hist_result_{dataset}_ttbar_inspection4.pkl"

hist_result_list = []
for i in range(n_chunks):
# for i in chunk_list:
    print(i)
    # Open existing pkl file
    with open(
        f'hist_result_{dataset}_ttbar_chunk{i}.pkl', 
        'rb'
    ) as file:
         hist_result_list.append(dill.load(file))
            
# with open(output_filename_pkl, 'rb') as file:
#     hist_result_list.append(dill.load(file))         
            
# print(hist_result_list[0][dataset].keys())
    
hist_result = {}
hist_result[dataset] = {}
hist_result[dataset]['hists'] = {}
hist_list = list(hist_result_list[0][dataset]['hists'].keys())
for hist_name in hist_list:
    print(hist_name)
    hist_result[dataset]['hists'][hist_name] = sum(
        [hist_result_list[i][dataset]['hists'][hist_name] for i in range(len(hist_result_list))]
    )
    
# branches = {}
# for trigger in trigger_list:
#     for branch in branch_list:
#         branches[f"{branch}_{trigger}"] = 
    
# for trigger in trigger_list:
#     print(trigger)
#     for branch in branch_list:
#         print("    ", branch)
#         hist_result[dataset][f"{branch}_{trigger}"] = []
#         for hist_name in hist_list:
#             for i in range(len(hist_result_list)):
#                 hist_result[dataset][f"{branch}_{trigger}"] += ak.to_list(hist_result_list[i][dataset][f"{branch}_{trigger}"]) 

with open(output_filename_pkl, 'wb') as file:
    dill.dump(hist_result, file)
