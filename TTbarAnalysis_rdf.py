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

def define_lead_jet_variables(df: ROOT.RDataFrame) -> ROOT.RDataFrame:

    df = df.Define("leadJetPt","jet_pt.empty()? 0.f : jet_pt[0]")
    df = df.Define("leadJetEta", "jet_eta.empty()? 0.f : jet_eta[0]")
    df = df.Define("leadJetPhi", "jet_phi.empty()? 0.f : jet_phi[0]")

    df = df.Define("subLeadJetPt","jet_pt.empty()? 0.f : jet_pt[1]")
    df = df.Define("subLeadJetEta", "jet_eta.empty()? 0.f : jet_eta[1]")
    df = df.Define("subLeadJetPhi", "jet_phi.empty()? 0.f : jet_phi[1]")

    df = df.Define("subSubLeadJetPt","jet_pt.empty()? 0.f : jet_pt[2]")
    df = df.Define("subSubLeadJetEta", "jet_eta.empty()? 0.f : jet_eta[2]")
    df = df.Define("subSubLeadJetPhi", "jet_phi.empty()? 0.f : jet_phi[2]")

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

    df = df.Filter("Sum(jet_mask) >= 3") # require at least four valid jets

    #df_tight = df.Filter("CICADAScore>=115")
    #df_nom = df.Filter("CICADAScore>=110")
    #df_loose = df.Filter("CICADAScore>=106")

    print("Number of Events After Filter = ", df.Count().GetValue())
    #print("Number of Events After Filter (Loose) = ", df_loose.Count().GetValue())
    #print("Number of Events After Filter (Med) = ", df_nom.Count().GetValue())
    #print("Number of Events After Filter (Tight) = ", df_tight.Count().GetValue())


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

    df = define_lead_jet_variables(df)

    print("Creating and writing histogram for leading jet pt")
    histModel = ROOT.RDF.TH2DModel("LeadJetPt", "LeadJetPt", 100, 0, 256, 100, 0, 500)
    hist = df.Histo2D(histModel, scoreStr, "leadJetPt")
    hist.Write()

    print("Creating and writing histogram for leading jet eta")
    histModel = ROOT.RDF.TH2DModel("LeadJetEta", "LeadJetEta", 100, 0, 256, 50, -2.4, 2.4)
    hist = df.Histo2D(histModel, scoreStr, "leadJetEta")
    hist.Write()

    print("Creating and writing histogram for leading jet phi")
    histModel = ROOT.RDF.TH2DModel("LeadJetPhi", "LeadJetPhi", 100, 0, 256, 50, -3.14, 3.14)
    hist = df.Histo2D( histModel, scoreStr, "leadJetPhi")
    hist.Write()

    print("Creating and writing histogram for subleading jet pt")
    histModel = ROOT.RDF.TH2DModel("SubLeadJetPt", "SubLeadJetPt", 100, 0, 256, 100, 0, 500)
    hist = df.Histo2D(histModel, scoreStr, "subLeadJetPt")
    hist.Write()

    print("Creating and writing histogram for subleading jet eta")
    histModel = ROOT.RDF.TH2DModel("SubLeadJetEta", "SubLeadJetEta", 100, 0, 256, 50, -2.4, 2.4)
    hist = df.Histo2D(histModel, scoreStr, "subLeadJetEta")
    hist.Write()

    print("Creating and writing histogram for subleading jet phi")
    histModel = ROOT.RDF.TH2DModel("SubLeadJetPhi", "SubLeadJetPhi", 100, 0, 256, 50, -3.14, 3.14)
    hist = df.Histo2D( histModel, scoreStr, "subLeadJetPhi")
    hist.Write()

    print("Creating and writing histogram for subsubleading jet pt")
    histModel = ROOT.RDF.TH2DModel("SubSubLeadJetPt", "SubSubLeadJetPt", 100, 0, 256, 100, 0, 500)
    hist = df.Histo2D(histModel, scoreStr, "subSubLeadJetPt")
    hist.Write()

    print("Creating and writing histogram for subsubleading jet eta")
    histModel = ROOT.RDF.TH2DModel("SubSubLeadJetEta", "SubSubLeadJetEta", 100, 0, 256, 50, -2.4, 2.4)
    hist = df.Histo2D(histModel, scoreStr, "subSubLeadJetEta")
    hist.Write()

    print("Creating and writing histogram for subsubleading jet phi")
    histModel = ROOT.RDF.TH2DModel("SubSubLeadJetPhi", "SubSubLeadJetPhi", 100, 0, 256, 50, -3.14, 3.14)
    hist = df.Histo2D( histModel, scoreStr, "subSubLeadJetPhi")
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
