import ROOT
import argparse
import json
import numpy as np
import datetime

from loess import loess

threshold_loose = 106.
threshold_medium = 110.
threshold_tight = 115.

todaysDate = datetime.date.today().strftime('%Y%m%d')

def drawComparisonPlot(hist_zerobias, hist_ttbar, cicada_threshold, x_axis_title, output_dir, output_name, norm=True):

    ROOT.gStyle.SetTitleSize(0.05, "X")
    ROOT.gStyle.SetTitleSize(0.05, "Y")
    ROOT.gStyle.SetLabelSize(0.05, "XY")

    bin_min = hist_zerobias.GetXaxis().FindBin(cicada_threshold)
    bin_max = hist_zerobias.GetXaxis().GetNbins()

    c = ROOT.TCanvas("c", "c", 1000, 600)

    hist_zerobias_projection = hist_zerobias.ProjectionY("hist_zerobias_projection", bin_min, bin_max)
    hist_zerobias_projection.Rebin(4);

    if norm:
        integral_zerobias = hist_zerobias_projection.Integral()
        if integral_zerobias > 0:
            hist_zerobias_projection.Scale(1.0 / integral_zerobias)

    # loess
    '''
    number_bins = hist_zerobias_projection.GetNbinsX()
    bin_values = np.zeros(number_bins)
    bin_centers = np.zeros(number_bins)
    bin_errors = np.zeros(number_bins)
    for i in range(number_bins):
        bin_centers[i] = hist_zerobias_projection.GetXaxis().GetBinCenter(i)
        bin_values[i] = hist_zerobias_projection.GetBinContent(i)
        bin_errors[i] = hist_zerobias_projection.GetBinError(i)

    y_pred, (y_dn, y_up), gcv = loess(
        x=bin_centers,
        y=bin_values,
        e=bin_errors,
        deg=2, # degree of polynomial
        alpha=0.5,#0.683, # confidence interval
        span=0.25, # fraction of points to include in fit
    )

    print("bin centers = ", bin_centers)
    print("bin values = ", bin_values)
    print("bin errors = ", bin_errors)
    print("y_pred = ", y_pred)
    '''

    hist_zerobias_projection.SetMarkerColor(2)
    hist_zerobias_projection.SetLineColor(2)
    hist_zerobias_projection.SetLineWidth(2)
    hist_zerobias_projection.SetMarkerStyle(20)
    hist_zerobias_projection.GetXaxis().SetTitle(x_axis_title)
    hist_zerobias_projection.GetXaxis().SetTitleSize(0.05)

    if norm:
        hist_zerobias_projection.GetYaxis().SetTitle("Frequency (Normalized to 1)")
    else:
        hist_zerobias_projection.GetYaxis().SetTitle("Events")

    hist_zerobias_projection.SetTitle(f"CICADA Threshold = {cicada_threshold}")
    hist_zerobias_projection.SetStats(0)
    hist_zerobias_max = hist_zerobias_projection.GetBinContent(hist_zerobias_projection.GetMaximumBin())

    hist_ttbar_projection = hist_ttbar.ProjectionY("hist_ttbar_projection", bin_min, bin_max)
    hist_ttbar_projection.Rebin(4)

    if norm:
        integral_ttbar = hist_ttbar_projection.Integral()
        if integral_zerobias > 0:
            hist_ttbar_projection.Scale(1.0 / integral_ttbar)

    hist_ttbar_projection.SetMarkerColor(4)
    hist_ttbar_projection.SetLineColor(4)
    hist_ttbar_projection.SetLineWidth(2)
    hist_ttbar_projection.SetMarkerStyle(21)
    hist_ttbar_max = hist_ttbar_projection.GetBinContent(hist_ttbar_projection.GetMaximumBin())
    y_max =  1.15*max(hist_ttbar_max, hist_zerobias_max)

    hist_zerobias_projection.GetYaxis().SetRangeUser(0, y_max)
    hist_zerobias_projection.GetXaxis().SetRangeUser(0,1000)

    hist_zerobias_projection.GetYaxis().SetTitleOffset(0.95)
    hist_zerobias_projection.GetXaxis().SetTitleOffset(0.85)

    hist_zerobias_projection.Draw("E1")
    hist_zerobias_projection.Draw("HIST SAME")
    hist_ttbar_projection.Draw("hist,c same")

    '''
    nBins = hist_ttbar_projection.GetNbinsX();
    graph = ROOT.TGraph(nBins);

    for i in range(nBins):
        graph.SetPoint(i-1, hist_ttbar_projection.GetBinCenter(i), hist_ttbar_projection.GetBinContent(i));

    graph.Draw("AC")
    '''

    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    legend.AddEntry(hist_zerobias_projection, "Zero Bias Data", "ep")
    legend.AddEntry(hist_ttbar_projection, "TTbar MC", "l")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.045)
    legend.Draw()

    c.Update()
    c.Draw()
    c.SaveAs(f"{output_dir}/{output_name}_threshold{str(int(cicada_threshold))}_{todaysDate}.png")
    c.Close()

    return

def main(file_zerobias, file_ttbar, output_dir):

    f_zerobias = ROOT.TFile(file_zerobias)
    f_ttbar = ROOT.TFile(file_ttbar)

    for cicada_threshold in [0, threshold_loose, threshold_medium, threshold_tight]:

        hist_jetpt_zerobias = f_zerobias.Get("TrijetMass")
        print("Zero Bias Entries: ", hist_jetpt_zerobias.GetEntries())
        hist_jetpt_ttbar = f_ttbar.Get("TrijetMass")
        drawComparisonPlot(hist_jetpt_zerobias, hist_jetpt_ttbar, cicada_threshold, r"m_{bjj} [GeV]", output_dir, "TrijetMassComparison")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program creates comparison plots between Zero Bias and TTbar MC sample")
    parser.add_argument("-z", "--file_zerobias", help="path to input ROOT file containing hists from ZeroBias")
    parser.add_argument("-t", "--file_ttbar", help="path to input ROOT file containing hists from TTbar")
    parser.add_argument("-o", "--output_dir", default='./', help="directory to save output plots")

    args = parser.parse_args()

    main(args.file_zerobias, args.file_ttbar, args.output_dir)
