import ROOT
import argparse
import awkward as ak
import json
import numpy as np
import datetime
from sampleBuilder import samples

def load_cpp():
    """Load C++ helper functions."""
    cpp_source = "helpers.h"
    ROOT.gInterpreter.Declare(f'#include "{str(cpp_source)}"')

def define_trijet_combinations(df: ROOT.RDataFrame) -> ROOT.RDataFrame:

    # require at least two b-tagged jet
    df = df.Filter("Sum(jet_btagDeepCSV > 0.5) > 1")

    df = df.Define("jet_p4", "ConstructP4(jet_pt, jet_eta, jet_phi, jet_mass)")

    df = df.Define("Trijet_idx", "Combinations(jet_pt, 3)")

    df = df.Define(
        "Trijet_btag",
        """
            auto j1_btagDeepCSV = Take(jet_btagDeepCSV, Trijet_idx[0]);
            auto j2_btagDeepCSV = Take(jet_btagDeepCSV, Trijet_idx[1]);
            auto j3_btagDeepCSV = Take(jet_btagDeepCSV, Trijet_idx[2]);
            return j1_btagDeepCSV > 0.5 || j2_btagDeepCSV > 0.5 || j3_btagDeepCSV > 0.5;
            """,
    )

    df = df.Define(
        "Trijet_p4",
        """
        auto j1 = Take(jet_p4, Trijet_idx[0]);
        auto j2 = Take(jet_p4, Trijet_idx[1]);
        auto j3 = Take(jet_p4, Trijet_idx[2]);
        return (j1+j2+j3)[Trijet_btag];
        """,
    )

    df = df.Define(
        "Trijet_pt",
        "return Map(Trijet_p4, [](const ROOT::Math::PxPyPzMVector &v) { return v.Pt(); })",
    )

    return df


def define_trijet_mass(df: ROOT.RDataFrame) -> ROOT.RDataFrame:

    df = df.Define("Trijet_mass", "Trijet_p4[ArgMax(Trijet_pt)].M()")

    return df


def main(dataset, out_dir):

    if dataset=='ZeroBias':
        scoreStr = 'cicadaScore'
    else:
        scoreStr = 'CICADAScore'

    load_cpp()

    # get dataframe from samples
    print("Getting dataframes")
    df = samples[dataset].getNewDataframe()

    events_pre = df.Count().GetValue()
    print("Number of Events Before Filter = ", events_pre)

    ##### general event selection #####
    #df = df.Define("electron_mask", "electron_pt > 0") # apply electron selections here
    #df = df.Define("muon_mask", "muon_pt > 0") # apply muon selections here
    df = df.Define("jet_mask", "jet_pt > 20") # apply jet selections here
    #df = df.Filter("Sum(electron_mask) + Sum(muon_mask) == 1") # require exactly one valid electron or muon
    '''
    df_test = df.Filter("Sum(jet_mask) >= 1")
    events_1 = df_test.Count().GetValue()
    print("Number of Events with 1 Jet with pT>20 = ", events_1)
    print("Fraction of Events with 1 Jet with pT>20 = ", events_1/events_pre)
    df_test = df.Filter("Sum(jet_mask) >= 2")
    events_2 = df_test.Count().GetValue()
    print("Number of Events with 2 Jets with pT>20 = ", events_2)
    print("Fraction of Events with 2 Jet with pT>20 = ", events_2/events_pre)
    df_test = df.Filter("Sum(electron_mask) + Sum(muon_mask)>=1")
    events_lep = df_test.Count().GetValue()
    print("Number of Events with >=1 Lepton = ", events_lep)
    print("Fraction of Events with >=1 Lepton = ", events_lep/events_pre)
    df_test = df.Filter("(Sum(electron_mask) + Sum(muon_mask)>=1) && (Sum(jet_mask)>=1)")
    events_1_lep = df_test.Count().GetValue()
    print("Number of Events with >=1 Lepton and >1 Jet with pT>20 = ", events_1_lep)
    print("Fraction of Events with >=1 Lepton and >1 Jet with pT>20 = ", events_1_lep/events_pre)
    df_test = df.Filter("(Sum(electron_mask) + Sum(muon_mask)>=1) && (Sum(jet_mask)>=2)")
    events_2_lep = df_test.Count().GetValue()
    print("Number of Events with >=1 Lepton and >2 Jet with pT>20 = ", events_2_lep)
    print("Fraction of Events with >=1 Lepton and >2 Jet with pT>20 = ", events_2_lep/events_pre)
    '''


    df = df.Filter("Sum(jet_mask) >= 3") # require at least four valid jets

    df_tight = df.Filter("CICADAScore>=115")
    df_nom = df.Filter("CICADAScore>=110")
    df_loose = df.Filter("CICADAScore>=106")

    print("Number of Events After Filter = ", df.Count().GetValue())
    print("Number of Events After Filter (Loose) = ", df_loose.Count().GetValue())
    print("Number of Events After Filter (Med) = ", df_nom.Count().GetValue())
    print("Number of Events After Filter (Tight) = ", df_tight.Count().GetValue())


    # define trijet mass (top mass reconstruction)
    df = define_trijet_combinations(df)
    df = define_trijet_mass(df)

    todaysDate = datetime.date.today().strftime('%Y%m%d')

    # create output ROOT file
    print("Creating output ROOT file")
    fileName = f'{out_dir}/hists_reconstruction_{dataset}_{todaysDate}.root'
    output_file = ROOT.TFile(
        fileName,
        'RECREATE'
    )

    print("Creating and writing histogram for trijet mass")
    histModel = ROOT.RDF.TH2DModel(
        "TrijetMass",
        "TrijetMass",
        100,
        0,
        256,
        200,
        0,
        1000,
    )
    hist = df.Histo2D(
        histModel,
        scoreStr,
        "Trijet_mass"
    )
    hist.Write()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program creates histograms of reconstructed ttbar objects"
    )
    parser.add_argument(
        "-d",
        "--dataset",
        help="which dataset to create the histogram for"
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        default = ".",
        help="directory to save files to"
    )

    args = parser.parse_args()

    main(args.dataset, args.out_dir)
