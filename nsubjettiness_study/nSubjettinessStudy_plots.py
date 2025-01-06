import ROOT
import argparse
import json
import numpy as np
import datetime

thresholds = np.linspace(0.1,1,20)
colors = [ROOT.kRed+3, ROOT.kRed+1, ROOT.kRed-4, ROOT.kOrange+8, ROOT.kOrange+1, ROOT.kOrange, ROOT.kYellow-3, ROOT.kSpring+5, ROOT.kGreen, ROOT.kGreen+2, ROOT.kGreen+3, ROOT.kTeal+3, ROOT.kTeal, ROOT.kCyan+2, ROOT.kCyan+3, ROOT.kAzure+7, ROOT.kBlue, ROOT.kViolet+8, ROOT.kMagenta+1, ROOT.kPink+6]

todaysDate = datetime.date.today().strftime('%Y%m%d')

def drawComparisonPlot(hist, hist_name, x_axis_title, output_dir, norm=True):

    # root style options
    ROOT.gStyle.SetTitleSize(0.05, "X")
    ROOT.gStyle.SetTitleSize(0.05, "Y")
    ROOT.gStyle.SetLabelSize(0.05, "XY")

    # set up canvas and legend
    c = ROOT.TCanvas("c", "c", 1000, 600)
    legend = ROOT.TLegend(0.75, 0.3, 0.9, 0.88)
    
    # set max y value
    y_max = 1
    
    # keep track of whether we are on first histogram
    first = True
    
    # keep track of histograms
    histograms = []
    
    for i in range(len(thresholds)):
    
        # get current values
        threshold = thresholds[i]
        color = colors[i]
        
        # locate bins for projection
        bin_min = 1
        bin_max = hist.GetYaxis().FindBin(threshold)
        
        # get histogram projection
        histograms.append(hist.ProjectionX(f"hist_projection_{i}", bin_min, bin_max))
        # histograms[-1].Rebin(4);

        if norm:
            integral = histograms[-1].Integral()
            if integral > 0:
                histograms[-1].Scale(1.0 / integral)

        # histogram styling options
        histograms[-1].SetMarkerColor(color)
        histograms[-1].SetLineColor(color)
        histograms[-1].SetLineWidth(2)
        histograms[-1].SetMarkerStyle(20)

        # update legend
        legend.AddEntry(histograms[-1], f"{hist_name} < {np.round(threshold,decimals=2)}", "l")
        
        # set axis titles and ranges for first histogram
        if first:
            histograms[-1].SetStats(0)
            histograms[-1].SetTitle("")
            histograms[-1].GetXaxis().SetTitle(x_axis_title)
            histograms[-1].GetXaxis().SetTitleSize(0.05)
            if norm:
                histograms[-1].GetYaxis().SetTitle("Frequency (Normalized to 1)")
            else:
                histograms[-1].GetYaxis().SetTitle("Events")
            histograms[-1].GetYaxis().SetRangeUser(0.0001, 1.15 * y_max)
            histograms[-1].GetXaxis().SetRangeUser(100, 250)
            histograms[-1].GetYaxis().SetTitleOffset(0.95)
            histograms[-1].GetXaxis().SetTitleOffset(0.85)
            histograms[-1].Draw("hist")
        else:
            histograms[-1].Draw("hist same")
        
        first = False
        
    # draw legend
    legend.SetBorderSize(0)
    #legend.SetFillStyle(0)
    legend.SetTextSize(0.025)
    legend.Draw()

    # draw and save canvas
    c.SetLogy()
    c.Update()
    c.Draw()
    c.SaveAs(f"{output_dir}/{hist_name}_{todaysDate}.png")
    c.Close()

    return

def main(input_file, output_dir):

    # open root file
    f = ROOT.TFile(input_file)
    
    # get histogram and create plot for tau21
    hist_tau21 = f.Get("JetMassTau21")
    drawComparisonPlot(hist_tau21, "tau21", "Jet Mass", output_dir)
    
    # get histogram and create plot for tau32
    hist_tau32 = f.Get("JetMassTau32")
    drawComparisonPlot(hist_tau32, "tau32", "Jet Mass", output_dir)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program creates comparison plots for different nsubjettiness thresholds")
    parser.add_argument("-i", "--input_file", help="path to input ROOT file containing hists")
    parser.add_argument("-o", "--output_dir", default='./', help="directory to save output plots")

    args = parser.parse_args()

    main(args.input_file, args.output_dir)
