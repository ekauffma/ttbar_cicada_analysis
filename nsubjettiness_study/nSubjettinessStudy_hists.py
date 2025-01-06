import ROOT
import argparse
import awkward as ak
import json
import numpy as np
import datetime
from sampleBuilder_nano import samples

def main(dataset, out_dir):

    # get dataframe from samples
    print("Getting dataframes")
    df = samples[dataset].getNewDataframe()

    # save dataframe to root file
    todaysDate = datetime.date.today().strftime('%Y%m%d')

    # create output ROOT file
    print("Creating output ROOT file")
    fileName = f'{out_dir}/hists_nsubjettiness_{dataset}_{todaysDate}.root'
    output_file = ROOT.TFile(
        fileName,
        'RECREATE'
    )

    # cut on fat jet pt
    df = df.Define("goodFatJet_pt", "ScoutingFatJet_pt[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_eta", "ScoutingFatJet_eta[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_phi", "ScoutingFatJet_phi[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_mass", "ScoutingFatJet_mass[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_tau1", "ScoutingFatJet_tau1[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_tau2", "ScoutingFatJet_tau2[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_tau3", "ScoutingFatJet_tau3[ScoutingFatJet_pt>30]")
    df = df.Define("goodFatJet_tau32", "goodFatJet_tau3/goodFatJet_tau2")
    df = df.Define("goodFatJet_tau21", "goodFatJet_tau2/goodFatJet_tau1")


    print("Creating and writing histogram for jet mass and nsubjettiness tau3/tau2")
    histModel = ROOT.RDF.TH2DModel(
        "JetMassTau32",
        "JetMassTau32",
        400,
        0,
        1000,
        100,
        0,
        1,
    )
    hist = df.Histo2D(
        histModel,
        "goodFatJet_mass",
        "goodFatJet_tau32"
    )
    hist.Write()

    print("Creating and writing histogram for jet mass and nsubjettiness tau2/tau1")
    histModel = ROOT.RDF.TH2DModel(
        "JetMassTau21",
        "JetMassTau21",
        200,
        0,
        1000,
        100,
        0,
        1,
    )
    hist = df.Histo2D(
        histModel,
        "goodFatJet_mass",
        "goodFatJet_tau21"
    )
    hist.Write()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program creates histograms of fat jet mass vs nsubjettiness variables"
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
