###################################################################################################
#   cicada_histos_script.py                                                                       #
#   Description: process cicada-triggered events and save relevant observables in histograms      #
#   Authors: Elliott Kauffman                                                                     #
###################################################################################################

###################################################################################################
# IMPORTS

# library imports
import awkward as ak
from collections import defaultdict
import dask
from dask.distributed import Client
import dask_awkward as dak
import dill
import hist
import hist.dask as hda
import json
import numpy as np
import time
import vector
vector.register_awkward()

# coffea imports
from coffea.nanoevents.methods import vector
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import coffea.processor as processor
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)

NanoAODSchema.warn_missing_crossrefs = False

###################################################################################################
# PROCESSING OPTIONS

# json_filename = "2025_mc_filelist.json"                    # name of json file containing root file paths
json_filename = "2024_data_filelist.json"
# dataset_name = "TT_TuneCP5_13p6TeV_powheg-pythia8"         # name of key within json containing dataset
dataset_name = "Scouting_2024I"
n_files = -1                                               # number of files to process (-1 for all)
coffea_step_size = 15_000                                  # step size for coffea processor
coffea_files_per_batch = 1                                 # files per batch for coffea processor
files_per_chunk = 200                                       # number of files to process at a time
visualize = False

# which hists to save (comment out unwanted)
hist_selection = {
    "ttbar": [
        "trijet_mass",                      # trijet invariant mass
        "trijet_pt",                        # trijet pt
        "trijet_eta",                       # trijet eta
        "trijet_phi",                       # trijet phi
        "lead_jet_pt",
        "lead_jet_eta",
        "lead_jet_phi",
        "sublead_jet_pt",
        "sublead_jet_eta",
        "sublead_jet_phi",
        "subsublead_jet_pt",
        "subsublead_jet_eta",
        "subsublead_jet_phi",
    ]
}

# which branches to save (comment out unwanted)
branch_selection = {
    "ttbar": [
        # "trijet_mass",                      # trijet invariant mass
        # "trijet_pt",                        # trijet pt
        # "trijet_eta",                       # trijet eta
        # "trijet_phi",                       # trijet phi
    ]
}

# which triggers to save (comment out unwanted or add)
triggers = [
    # 'DST_PFScouting_AXOLoose', 
    # 'DST_PFScouting_AXONominal', 
    # 'DST_PFScouting_AXOTight', 
    # 'DST_PFScouting_AXOVLoose', 
    # 'DST_PFScouting_AXOVTight',
    # 'DST_PFScouting_CICADALoose', 
    'DST_PFScouting_CICADAMedium', 
    'DST_PFScouting_CICADATight', 
    # 'DST_PFScouting_CICADAVLoose', 
    'DST_PFScouting_CICADAVTight',
    # 'DST_PFScouting_DoubleMuon',
    # 'DST_PFScouting_JetHT',
    'DST_PFScouting_ZeroBias'
]

###################################################################################################
# DEFINE SCHEMA
class ScoutingNanoAODSchema(NanoAODSchema):
    """ScoutingNano schema builder

    ScoutingNano is a NanoAOD format that includes Scouting objects
    """

    mixins = {
        **NanoAODSchema.mixins,
        "ScoutingPFJet": "Jet",
        "ScoutingPFJetRecluster": "Jet",
        "ScoutingFatJet": "Jet",
        "ScoutingMuonNoVtxDisplacedVertex": "Vertex",
        "ScoutingMuonVtxDisplacedVertex": "Vertex",
        "ScoutingElectron": "Electron",
        "ScoutingPhoton": "Photon", 
        "ScoutingMuonNoVtx": "Muon",
        "ScoutingMuonVtx": "Muon"

    }
    all_cross_references = {
        **NanoAODSchema.all_cross_references
    }
  
###################################################################################################
# HELPER FUNCTIONS FOR PROCESSOR

def createHist_1d(
    hist_dict, dataset_axis, trigger_axis, observable_axis, hist_name 
):
    h = hda.hist.Hist(dataset_axis, trigger_axis, observable_axis, storage="weight", label="nEvents")
    hist_dict[f'{hist_name}'] = h
    
    return hist_dict

def fillHist_1d(
    hist_dict, hist_name, dataset, observable, trigger_path, observable_name
):
    
    kwargs = {
        observable_name: observable,
        "dataset": dataset,
        "trigger": trigger_path
    }
    
    hist_dict[f'{hist_name}'].fill(**kwargs)
    
    return hist_dict

###################################################################################################
# DEFINE COFFEA PROCESSOR
class MakeAXOHists (processor.ProcessorABC):
    def __init__(
        self, 
        trigger_paths=[],
        hists_to_process={
            "ttbar": [],
        },
        branches_to_save={
            "ttbar": [],
        },
        extra_cut='', 
        object_dict=None
    ):
        the_object_dict =  {'ScoutingPFJetRecluster' :      {'cut' : [('pt', 30.)], 'label' : 'j'},
                            'ScoutingElectron' : {'cut' : [('pt', 10)], 'label' : 'e'},
                            'ScoutingMuonNoVtx' :     {'cut' : [('pt', 3)], 'label' : '\mu'},
                            'ScoutingPhoton' :     {'cut' : [('pt', 10)], 'label' : '\gamma'},
                            'L1Jet' :    {'cut' : [('pt', 0.1)], 'label' : 'L1j'},
                            'L1EG' :     {'cut' : [('pt', 0.1)], 'label' : 'L1e'},
                            'L1Mu' :     {'cut' : [('pt', 0.1)], 'label' : 'L1\mu'}
                            }
        
        self.run_dict = {
            'objects' : object_dict if object_dict is not None else the_object_dict
        }

        self.trigger_paths = trigger_paths
        self.extra_cut = extra_cut
        self.hists_to_process = hists_to_process
        self.branches_to_save = branches_to_save
        
        # define axes for histograms
        self.dataset_axis = hist.axis.StrCategory(
            [], growth=True, name="dataset", label="Primary dataset"
        )
        self.trigger_axis = hist.axis.StrCategory(
            [], growth=True, name="trigger", label="Trigger"
        )
        self.mult_axis = hist.axis.Regular(
            200, 0, 201, name="mult", label=r'$N_{obj}$'
        )
        self.pt_axis = hist.axis.Regular(
            500, 0, 5000, name="pt", label=r"$p_{T}$ [GeV]"
        )
        self.eta_axis = hist.axis.Regular(
            150, -5, 5, name="eta", label=r"$\eta$"
        )
        self.phi_axis = hist.axis.Regular(
            30, -4, 4, name="phi", label=r"$\phi$"
        )
        self.met_axis = hist.axis.Regular(
            250, 0, 2500, name="met", label=r"$p^{miss}_{T} [GeV]$"
        )
        self.ht_axis = hist.axis.Regular(
            100, 0, 2000, name="ht", label=r"$H_{T}$ [GeV]"
        )
        
        # invariant mass axes
        self.minv_axis = hist.axis.Regular(
            200, 0, 1000, name="minv", label=r"Invariant Mass [GeV]"
        )
        
    def process(self, events):
        dataset = events.metadata['dataset']
        cutflow = defaultdict(int)
        cutflow['start'] = dak.num(events.event, axis=0)
        hist_dict = {}
        return_dict = {}
               
        # Saturated-Jets event cut
        events = events[dak.all(events.L1Jet.pt<1000,axis=1)]
        # Saturated-MET event cut
        events = events[dak.flatten(events.L1EtSum.pt[(events.L1EtSum.etSumType==2) 
                                                      & (events.L1EtSum.bx==0)])<1040]
        
        # apply cuts to jets
        jet_mask = (
            (events.ScoutingPFJetRecluster.pt > 30) &             # jet pt requirement   
            (abs(events.ScoutingPFJetRecluster.eta) < 2.4) &      # remove forward jets
            (events.ScoutingPFJetRecluster.neHEF < 0.99) &        # neutral hadron fraction
            (events.ScoutingPFJetRecluster.neEmEF < 0.90) &       # neutral em fraction
            (events.ScoutingPFJetRecluster.nConstituents > 1) &   # number of constituents
            (events.ScoutingPFJetRecluster.muEF < 0.80) &         # muon fraction
            (events.ScoutingPFJetRecluster.chHEF > 0.01) &        # charged hadron fraction
            (events.ScoutingPFJetRecluster.nCh > 0) &             # charged multiplicity
            (events.ScoutingPFJetRecluster.chEmEF < 0.80)         # charged em fraction
        )
        selected_jets = events.ScoutingPFJetRecluster[jet_mask]
        
        # require at least 3 jets
        events = events[ak.num(selected_jets,axis=1)>=3]
        # events = events[ak.num(events.ScoutingPFJetRecluster,axis=1)>=3]
        
        # initialize histogams (filled for each trigger)
        if ("trijet_mass" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.minv_axis, 
                "trijet_mass"
            )
        if ("trijet_pt" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.pt_axis, 
                "trijet_pt"
            )
        if ("trijet_eta" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.eta_axis, 
                "trijet_eta"
            )
        if ("trijet_phi" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.phi_axis, 
                "trijet_phi"
            )
        if ("lead_jet_pt" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.pt_axis, 
                "lead_jet_pt"
            )
        if ("lead_jet_eta" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.eta_axis, 
                "lead_jet_eta"
            )
        if ("lead_jet_phi" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.phi_axis, 
                "lead_jet_phi"
            )
        if ("sublead_jet_pt" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.pt_axis, 
                "sublead_jet_pt"
            )
        if ("sublead_jet_eta" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.eta_axis, 
                "sublead_jet_eta"
            )
        if ("sublead_jet_phi" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.phi_axis, 
                "sublead_jet_phi"
            )
        if ("subsublead_jet_pt" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.pt_axis, 
                "subsublead_jet_pt"
            )
        if ("subsublead_jet_eta" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.eta_axis, 
                "subsublead_jet_eta"
            )
        if ("subsublead_jet_phi" in self.hists_to_process["ttbar"]):
            hist_dict = createHist_1d(
                hist_dict, 
                self.dataset_axis, 
                self.trigger_axis, 
                self.phi_axis, 
                "subsublead_jet_phi"
            )
            
        # loop over trigger paths
        for trigger_path in self.trigger_paths:
            trig_br = getattr(events,trigger_path.split('_')[0])
            trig_path = '_'.join(trigger_path.split('_')[1:])
            events_trig = events[getattr(trig_br,trig_path)]
            cutflow["trijet_mass"+trigger_path] = dak.num(events_trig.event, axis=0)
            
            obj = "ScoutingPFJetRecluster"
            obj_dict = self.run_dict['objects'][obj]
            cut_list = obj_dict['cut']
            label = obj_dict['label']
            isScoutingObj = 'Scouting' in obj
            br = getattr(events_trig, obj)
            
            jet_mask = (
                (events_trig.ScoutingPFJetRecluster.pt > 30) &             # jet pt requirement   
                (abs(events_trig.ScoutingPFJetRecluster.eta) < 2.4) &      # remove forward jets
                (events_trig.ScoutingPFJetRecluster.neHEF < 0.99) &        # neutral hadron fraction
                (events_trig.ScoutingPFJetRecluster.neEmEF < 0.90) &       # neutral em fraction
                (events_trig.ScoutingPFJetRecluster.nConstituents > 1) &   # number of constituents
                (events_trig.ScoutingPFJetRecluster.muEF < 0.80) &         # muon fraction
                (events_trig.ScoutingPFJetRecluster.chHEF > 0.01) &        # charged hadron fraction
                (events_trig.ScoutingPFJetRecluster.nCh > 0) &             # charged multiplicity
                (events_trig.ScoutingPFJetRecluster.chEmEF < 0.80)         # charged em fraction
            )
            
            selected_jets_trig = events_trig.ScoutingPFJetRecluster[jet_mask]
            
            # Apply list of cuts to relevant branches
            # for var, cut in cut_list:
            #     mask = (getattr(br,var) > cut)
            #     br = br[mask] 
                
            if ("lead_jet_pt" in self.hists_to_process["ttbar"]):
                lead_jet_pt = selected_jets_trig.pt[:, 0]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'lead_jet_pt', 
                    dataset, 
                    lead_jet_pt, 
                    trigger_path, 
                    "pt"
                )
            if ("lead_jet_eta" in self.hists_to_process["ttbar"]):
                lead_jet_eta = selected_jets_trig.eta[:, 0]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'lead_jet_eta', 
                    dataset, 
                    lead_jet_eta, 
                    trigger_path, 
                    "eta"
                )
            if ("lead_jet_phi" in self.hists_to_process["ttbar"]):
                lead_jet_phi = selected_jets_trig.phi[:, 0]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'lead_jet_phi', 
                    dataset, 
                    lead_jet_phi, 
                    trigger_path, 
                    "phi"
                )
            if ("sublead_jet_pt" in self.hists_to_process["ttbar"]):
                sublead_jet_pt = selected_jets_trig.pt[:, 1]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'sublead_jet_pt', 
                    dataset, 
                    sublead_jet_pt, 
                    trigger_path, 
                    "pt"
                )
            if ("sublead_jet_eta" in self.hists_to_process["ttbar"]):
                sublead_jet_eta = selected_jets_trig.eta[:, 1]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'sublead_jet_eta', 
                    dataset, 
                    sublead_jet_eta, 
                    trigger_path, 
                    "eta"
                )
            if ("sublead_jet_phi" in self.hists_to_process["ttbar"]):
                sublead_jet_phi = selected_jets_trig.phi[:, 1]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'sublead_jet_phi', 
                    dataset, 
                    sublead_jet_phi, 
                    trigger_path, 
                    "phi"
                )
            if ("subsublead_jet_pt" in self.hists_to_process["ttbar"]):
                subsublead_jet_pt = selected_jets_trig.pt[:, 2]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'subsublead_jet_pt', 
                    dataset, 
                    subsublead_jet_pt, 
                    trigger_path, 
                    "pt"
                )
            if ("subsublead_jet_eta" in self.hists_to_process["ttbar"]):
                subsublead_jet_eta = selected_jets_trig.eta[:, 2]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'subsublead_jet_eta', 
                    dataset, 
                    subsublead_jet_eta, 
                    trigger_path, 
                    "eta"
                )
            if ("subsublead_jet_phi" in self.hists_to_process["ttbar"]):
                subsublead_jet_phi = selected_jets_trig.phi[:, 2]
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'subsublead_jet_phi', 
                    dataset, 
                    subsublead_jet_phi, 
                    trigger_path, 
                    "phi"
                )
                
            
                
            trijet = dak.combinations(selected_jets_trig, 3, fields=["j1", "j2", "j3"])
            trijet["p4"] = trijet.j1 + trijet.j2 + trijet.j3
            trijet["max_btag"] = dak.max(
                dak.concatenate(
                    [trijet.j1.particleNet_prob_b[:, None], 
                     trijet.j2.particleNet_prob_b[:, None], 
                     trijet.j3.particleNet_prob_b[:, None]], 
                    axis=1
                ), 
                axis=1
            )
            #trijet = trijet[dak.any(trijet.max_btag > 0.1, axis=1)]
            selected_trijet = dak.argmax(trijet.p4.pt, axis=1, keepdims=True)
            trijet_mass = dak.flatten(trijet["p4"][selected_trijet].mass)
            trijet_pt = dak.flatten(trijet["p4"][selected_trijet].pt)
            trijet_eta = dak.flatten(trijet["p4"][selected_trijet].eta)
            trijet_phi = dak.flatten(trijet["p4"][selected_trijet].phi)
            
            if "trijet_mass" in self.branches_to_save["ttbar"]: 
                return_dict[f"trijet_mass_{trigger_path}"] = trijet_mass
            if "trijet_pt" in self.branches_to_save["ttbar"]: 
                return_dict[f"trijet_mass_{trigger_path}"] = trijet_pt
            if "trijet_eta" in self.branches_to_save["ttbar"]: 
                return_dict[f"trijet_mass_{trigger_path}"] = trijet_eta
            if "trijet_phi" in self.branches_to_save["ttbar"]: 
                return_dict[f"trijet_phi_{trigger_path}"] = trijet_phi
                
            if ("trijet_mass" in self.hists_to_process["ttbar"]):
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'trijet_mass', 
                    dataset, 
                    trijet_mass, 
                    trigger_path, 
                    "minv"
                )
            if ("trijet_pt" in self.hists_to_process["ttbar"]):
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'trijet_pt', 
                    dataset, 
                    trijet_pt, 
                    trigger_path, 
                    "pt"
                )
            if ("trijet_eta" in self.hists_to_process["ttbar"]):
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'trijet_eta', 
                    dataset, 
                    trijet_eta, 
                    trigger_path, 
                    "eta"
                )
            if ("trijet_phi" in self.hists_to_process["ttbar"]):
                hist_dict = fillHist_1d(
                    hist_dict, 
                    'trijet_phi', 
                    dataset, 
                    trijet_phi, 
                    trigger_path, 
                    "phi"
                )
            
        return_dict['cutflow'] = cutflow
        return_dict['hists'] = hist_dict
        return_dict['trigger'] = self.trigger_paths if len(self.trigger_paths)>0 else None
                
        return return_dict

    def postprocess(self, accumulator):
        return accumulator


###################################################################################################
# DEFINE MAIN FUNCTION
def main():
    client = Client("tls://localhost:8786")
    
    with open(json_filename) as json_file:
        dataset = json.load(json_file)
    
    dataset_skimmed = {dataset_name: {'files': {}}}
    i = 0
    for key, value in dataset[dataset_name]['files'].items():
        if ((i<n_files) or (n_files==-1)):
            dataset_skimmed[dataset_name]['files'][key] = value
        i+=1
         
    number_of_files = n_files
    if n_files==-1: number_of_files = i
    print(f"Processing {number_of_files} files")
    
    # calculate chunks
    if number_of_files > files_per_chunk:
        chunks_left = np.arange(0,number_of_files,files_per_chunk,dtype=int)
        print(chunks_left)
        chunks_right = np.arange(files_per_chunk-1,number_of_files,files_per_chunk,dtype=int)
        chunks_right = np.append(chunks_right, number_of_files)
        print(chunks_right)
    else:
        chunks_left = [0]
        chunks_right = [number_of_files]
        
    print("Number of chunks = ", len(chunks_left))
    
    # iterate over chunks and run coffea processor
    for j in range(len(chunks_left)):
        print("Current chunk = ", j)
        
        dataset_reskimmed = {dataset_name: {'files': {}}}
        i = 0
        for key, value in dataset_skimmed[dataset_name]['files'].items():
            if (i>=chunks_left[j]) and (i<=chunks_right[j]):
                dataset_reskimmed[dataset_name]['files'][key] = value
            i+=1
        
        print("Number of Files to Process This Chunk = ", len(dataset_reskimmed[dataset_name]['files']))
        
        dataset_runnable, dataset_updated = preprocess(
            dataset_reskimmed,
            align_clusters=False,
            step_size=coffea_step_size,
            files_per_batch=coffea_files_per_batch,
            skip_bad_files=True,
            save_form=False,
        )

        tstart = time.time()
    
        to_compute = apply_to_fileset(
            MakeAXOHists(trigger_paths=triggers, 
                         hists_to_process=hist_selection,
                         branches_to_save=branch_selection),
            max_chunks(dataset_runnable, 300000),
            schemaclass=ScoutingNanoAODSchema,
            uproot_options={"allow_read_errors_with_report": (OSError, TypeError, KeyError)}
        )
    
        if visualize:
            dask.optimize(to_compute)
            dask.visualize(to_compute, filename="dask_coffea_graph_ttbar", format="pdf")
        
        (hist_result,) = dask.compute(to_compute)
        print(f'Chunk took {time.time()-tstart:.1f}s to process')
        hist_result = hist_result[0]

        #Save file 
        with open(f'hist_result_{dataset_name}_ttbar_chunk{j}.pkl', 'wb') as file:
                # dump information to that file
                dill.dump(hist_result, file)
    

###################################################################################################
# RUN SCRIPT
if __name__=="__main__":
    main()