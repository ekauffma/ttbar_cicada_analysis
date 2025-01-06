import ROOT
import argparse
import awkward as ak
import json
import numpy as np
import datetime
from sampleBuilder_nano import samples

def main(dataset, out_dir, trigger):

    # get dataframe from samples
    print("Getting dataframes")
    df = samples[dataset].getNewDataframe()

    # save dataframe to root file
    todaysDate = datetime.date.today().strftime('%Y%m%d')

    # create output ROOT file
    print("Creating output ROOT file")
    fileName = f'{out_dir}/hists_nsubjettiness_{dataset}_{trigger}_{todaysDate}.root'
    output_file = ROOT.TFile(
        fileName,
        'RECREATE'
    )

    # apply trigger
    if trigger!="None":
        df = df.Filter(trigger)

    if dataset=="TTbar":
        jetObjStr = "ScoutingFatJet"
    else:
        jetObjStr = "ScoutingFatPFJetRecluster"

    # cut on fat jet pt
    df = df.Define("goodFatJet_pt", f"{jetObjStr}_pt[{jetObjStr}_pt>30]")
    df = df.Define("goodFatJet_eta", f"{jetObjStr}_eta[{jetObjStr}_pt>30]")
    df = df.Define("goodFatJet_phi", f"{jetObjStr}_phi[{jetObjStr}_pt>30]")
    df = df.Define("goodFatJet_mass", f"{jetObjStr}_mass[{jetObjStr}_pt>30]")
    df = df.Define("goodFatJet_tau1", f"{jetObjStr}_tau1[{jetObjStr}_pt>30]")
    df = df.Define("goodFatJet_tau2", f"{jetObjStr}_tau2[{jetObjStr}_pt>30]")
    df = df.Define("goodFatJet_tau3", f"{jetObjStr}_tau3[{jetObjStr}_pt>30]")
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
    parser.add_argument(
        "-t",
        "--trigger",
        default = "None",
        help="which trigger to apply to dataset"
    )

    args = parser.parse_args()

    main(args.dataset, args.out_dir, args.trigger)
