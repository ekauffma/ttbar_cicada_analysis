import ROOT
import scipy
import cmsstyle as CMS
import numpy as np

def createLabel():
    latex = ROOT.TLatex()
    latex.SetTextSize(0.05)
    latex.SetNDC(True)
    latex.SetTextAlign(11)

    return latex

ROOT.gStyle.SetTitleSize(0.04, "X")
ROOT.gStyle.SetTitleSize(0.04, "Y")

cicada_thresholds = [0.0, 25.0, 50.0, 75.0, 100.0, 106.0, 110.0, 115.0, 120, 125.0, 150.0]
rebin_factor = 3

f_zb = ROOT.TFile.Open("hists_reconstruction_ZeroBias_20241101.root")
f_tt = ROOT.TFile.Open("hists_reconstruction_TTbar_20241101.root")

hist_zb = f_zb.Get("LeadJetPt")
bin_max_zb = hist_zb.GetXaxis().GetNbins()
hist_bkg = hist_zb.ProjectionY("hist_bkg", 0, bin_max_zb)
hist_bkg.Rebin(rebin_factor)

hist_tt = f_tt.Get("LeadJetPt")
bin_max_tt = hist_tt.GetXaxis().GetNbins()

# Define the observables
mass_top = ROOT.RooRealVar("mass_top", "Reconstructed Top Mass [GeV]", 0, 1000)
jet_pt = ROOT.RooRealVar("jet_pt", r"Leading Jet pT [GeV]", 0, 500)
jet_eta = ROOT.RooRealVar("jet_eta", "jet_eta", -2.4, 2.4)
jet_phi = ROOT.RooRealVar("jet_phi", "jet_eta", -3.14, 3.14)
njet = ROOT.RooRealVar("njet", "njet", 0, 25)
nlepton = ROOT.RooRealVar("nlepton", "nlepton", 0, 10)

hist_zb_njet = f_zb.Get("nJet")
bin_max_zb_njet = hist_zb_njet.GetXaxis().GetNbins()
hist_bkg_njet = hist_zb_njet.ProjectionY("hist_bkg_njet", 0, bin_max_zb_njet)
dh_bkg_njet = ROOT.RooDataHist("dh_bkg_njet", "Number of Jets Background", ROOT.RooArgList(njet), hist_bkg_njet)

hist_tt_njet = f_tt.Get("nJet")
bin_max_tt_njet = hist_tt_njet.GetXaxis().GetNbins()

hist_zb_nelectron = f_zb.Get("nElectron")
bin_max_zb_nelectron = hist_zb_nelectron.GetXaxis().GetNbins()
hist_bkg_nelectron = hist_zb_nelectron.ProjectionY("hist_bkg_nelectron", 0, bin_max_zb_nelectron)
dh_bkg_nelectron = ROOT.RooDataHist("dh_bkg_nelectron", "Number of Electrons Background", ROOT.RooArgList(nlepton), hist_bkg_nelectron)

hist_tt_nelectron = f_tt.Get("nElectron")
bin_max_tt_nelectron = hist_tt_nelectron.GetXaxis().GetNbins()

hist_zb_nmuon = f_zb.Get("nMuon")
bin_max_zb_nmuon = hist_zb_nmuon.GetXaxis().GetNbins()
hist_bkg_nmuon = hist_zb_nmuon.ProjectionY("hist_bkg_nmuon", 0, bin_max_zb_nmuon)
dh_bkg_nmuon = ROOT.RooDataHist("dh_bkg_nmuon", "Number of Muons Background", ROOT.RooArgList(nlepton), hist_bkg_nmuon)

hist_tt_nmuon = f_tt.Get("nMuon")
bin_max_tt_nmuon = hist_tt_nmuon.GetXaxis().GetNbins()

hist_zb_met = f_zb.Get("MET")
bin_max_zb_met = hist_zb_met.GetXaxis().GetNbins()
hist_bkg_met = hist_zb_met.ProjectionY("hist_bkg_met", 0, bin_max_zb_met)
dh_bkg_met = ROOT.RooDataHist("dh_bkg_met", "MET Background", ROOT.RooArgList(jet_pt), hist_bkg_met)

hist_tt_met = f_tt.Get("MET")
bin_max_tt_met = hist_tt_met.GetXaxis().GetNbins()

hist_zb_topmass = f_zb.Get("TrijetMass")
bin_max_zb_topmass = hist_zb_topmass.GetXaxis().GetNbins()
hist_bkg_topmass = hist_zb_topmass.ProjectionY("hist_bkg_topmass", 0, bin_max_zb_topmass)
dh_bkg_topmass = ROOT.RooDataHist("dh_bkg_topmass", "Trijet Mass [GeV]", ROOT.RooArgList(mass_top), hist_bkg_topmass)

hist_tt_topmass = f_tt.Get("TrijetMass")
bin_max_tt_topmass = hist_tt_topmass.GetXaxis().GetNbins()

hist_zb_leadjeteta = f_zb.Get("LeadJetEta")
bin_max_zb_leadjeteta = hist_zb_leadjeteta.GetXaxis().GetNbins()
hist_bkg_leadjeteta = hist_zb_leadjeteta.ProjectionY("hist_bkg_leadjeteta", 0, bin_max_zb_leadjeteta)
dh_bkg_leadjeteta = ROOT.RooDataHist("dh_bkg_leadjeteta", "Leading Jet Eta Background", ROOT.RooArgList(jet_eta), hist_bkg_leadjeteta)

hist_tt_leadjeteta = f_tt.Get("LeadJetEta")
bin_max_tt_leadjeteta = hist_tt_leadjeteta.GetXaxis().GetNbins()

hist_zb_leadjetphi = f_zb.Get("LeadJetPhi")
bin_max_zb_leadjetphi = hist_zb_leadjetphi.GetXaxis().GetNbins()
hist_bkg_leadjetphi = hist_zb_leadjetphi.ProjectionY("hist_bkg_leadjetphi", 0, bin_max_zb_leadjetphi)
dh_bkg_leadjetphi = ROOT.RooDataHist("dh_bkg_leadjetphi", "Leading Jet Phi Background", ROOT.RooArgList(jet_phi), hist_bkg_leadjetphi)

hist_tt_leadjetphi = f_tt.Get("LeadJetPhi")
bin_max_tt_leadjetphi = hist_tt_leadjetphi.GetXaxis().GetNbins()

hist_zb_subleadjetpt = f_zb.Get("SubLeadJetPt")
bin_max_zb_subleadjetpt = hist_zb_subleadjetpt.GetXaxis().GetNbins()
hist_bkg_subleadjetpt = hist_zb_subleadjetpt.ProjectionY("hist_bkg_subleadjetpt", 0, bin_max_zb_subleadjetpt)
dh_bkg_subleadjetpt = ROOT.RooDataHist("dh_bkg_subleadjetpt", "Subleading Jet pT Background", ROOT.RooArgList(jet_pt), hist_bkg_subleadjetpt)

hist_tt_subleadjetpt = f_tt.Get("SubLeadJetPt")
bin_max_tt_subleadjetpt = hist_tt_subleadjetpt.GetXaxis().GetNbins()

hist_zb_subleadjeteta = f_zb.Get("SubLeadJetEta")
bin_max_zb_subleadjeteta = hist_zb_subleadjeteta.GetXaxis().GetNbins()
hist_bkg_subleadjeteta = hist_zb_subleadjeteta.ProjectionY("hist_bkg_subleadjeteta", 0, bin_max_zb_subleadjeteta)
dh_bkg_subleadjeteta = ROOT.RooDataHist("dh_bkg_subleadjeteta", "Subleading Jet Eta Background", ROOT.RooArgList(jet_eta), hist_bkg_subleadjeteta)

hist_tt_subleadjeteta = f_tt.Get("SubLeadJetEta")
bin_max_tt_subleadjeteta = hist_tt_leadjeteta.GetXaxis().GetNbins()

hist_zb_subleadjetphi = f_zb.Get("SubLeadJetPhi")
bin_max_zb_subleadjetphi = hist_zb_subleadjetphi.GetXaxis().GetNbins()
hist_bkg_subleadjetphi = hist_zb_subleadjetphi.ProjectionY("hist_bkg_subleadjetphi", 0, bin_max_zb_subleadjetphi)
dh_bkg_subleadjetphi = ROOT.RooDataHist("dh_bkg_subleadjetphi", "Subleading Jet Phi Background", ROOT.RooArgList(jet_phi), hist_bkg_subleadjetphi)

hist_tt_subleadjetphi = f_tt.Get("SubLeadJetPhi")
bin_max_tt_subleadjetphi = hist_tt_subleadjetphi.GetXaxis().GetNbins()

hist_zb_subsubleadjetpt = f_zb.Get("SubSubLeadJetPt")
bin_max_zb_subsubleadjetpt = hist_zb_subsubleadjetpt.GetXaxis().GetNbins()
hist_bkg_subsubleadjetpt = hist_zb_subsubleadjetpt.ProjectionY("hist_bkg_subsubleadjetpt", 0, bin_max_zb_subsubleadjetpt)
dh_bkg_subsubleadjetpt = ROOT.RooDataHist("dh_bkg_subsubleadjetpt", "Subsubleading Jet pT Background", ROOT.RooArgList(jet_pt), hist_bkg_subsubleadjetpt)

hist_tt_subsubleadjetpt = f_tt.Get("SubSubLeadJetPt")
bin_max_tt_subsubleadjetpt = hist_tt_subsubleadjetpt.GetXaxis().GetNbins()

hist_zb_subsubleadjeteta = f_zb.Get("SubSubLeadJetEta")
bin_max_zb_subsubleadjeteta = hist_zb_subsubleadjeteta.GetXaxis().GetNbins()
hist_bkg_subsubleadjeteta = hist_zb_subsubleadjeteta.ProjectionY("hist_bkg_subsubleadjeteta", 0, bin_max_zb_subsubleadjeteta)
dh_bkg_subsubleadjeteta = ROOT.RooDataHist("dh_bkg_subsubleadjeteta", "Subsubleading Jet Eta Background", ROOT.RooArgList(jet_eta), hist_bkg_subsubleadjeteta)

hist_tt_subsubleadjeteta = f_tt.Get("SubSubLeadJetEta")
bin_max_tt_subsubleadjeteta = hist_tt_subsubleadjeteta.GetXaxis().GetNbins()

hist_zb_subsubleadjetphi = f_zb.Get("SubSubLeadJetPhi")
bin_max_zb_subsubleadjetphi = hist_zb_subsubleadjetphi.GetXaxis().GetNbins()
hist_bkg_subsubleadjetphi = hist_zb_subsubleadjetphi.ProjectionY("hist_bkg_subsubleadjetphi", 0, bin_max_zb_subsubleadjetphi)
dh_bkg_subsubleadjetphi = ROOT.RooDataHist("dh_bkg_subsubleadjetphi", "Subsubleading Jet Phi Background", ROOT.RooArgList(jet_phi), hist_bkg_subsubleadjetphi)

hist_tt_subsubleadjetphi = f_tt.Get("SubSubLeadJetPhi")
bin_max_tt_subsubleadjetphi = hist_tt_subsubleadjetphi.GetXaxis().GetNbins()

scale_factors = {}

for threshold in cicada_thresholds:

    bin_min_zb = hist_zb.GetXaxis().FindBin(threshold)
    bin_min_tt = hist_tt.GetXaxis().FindBin(threshold)

    hist_data = hist_zb.ProjectionY("hist_data", bin_min_zb, bin_max_zb)
    hist_data.Rebin(rebin_factor)
    hist_data.SetMarkerStyle(20)
    binWidth = hist_data.GetBinWidth(1)
    print(f"Number of Events for Threshold={threshold} = ", hist_data.GetEntries())

    dh_data = ROOT.RooDataHist("dh_data", "Data", ROOT.RooArgList(jet_pt), hist_data)

    hist_sig = hist_tt.ProjectionY("hist_sig", bin_min_tt, bin_max_tt)
    hist_sig.Rebin(rebin_factor)

    ######## set up model

    data = ROOT.RooDataHist("data", "Data", ROOT.RooArgList(jet_pt), hist_data)
    bkg = ROOT.RooDataHist("bkg", "Background", ROOT.RooArgList(jet_pt), hist_bkg)
    integral_bkg_prefit = bkg.sumEntries()
    sig = ROOT.RooDataHist("sig", "Signal", ROOT.RooArgList(jet_pt), hist_sig)
    integral_sig_prefit = sig.sumEntries()

    # Create RooHistPdf for background and signal
    bkg_pdf = ROOT.RooHistPdf("bkg_pdf", "Background PDF", ROOT.RooArgSet(jet_pt), bkg)
    sig_pdf = ROOT.RooHistPdf("sig_pdf", "Signal PDF", ROOT.RooArgSet(jet_pt), sig)

    # Create coefficients for the signal and background fractions
    n_sig = ROOT.RooRealVar(
        "n_sig",
        "Number of signal events",
        int(hist_data.GetEntries()/2),
        0,
        hist_data.GetEntries())

    n_bkg = ROOT.RooRealVar(
        "n_bkg",
        "Number of background events",
        int(hist_data.GetEntries()/2),
        0,
        hist_data.GetEntries())


    # Create the combined model as a sum of signal and background PDFs
    model = ROOT.RooAddPdf("model", "Signal + Background", ROOT.RooArgList(sig_pdf, bkg_pdf), ROOT.RooArgList(n_sig, n_bkg))

    # Perform the fit
    fit_result = model.fitTo(data, ROOT.RooFit.Save())
    fit_result.Write(f"fitResult_{str(int(threshold))}")
    fit_params = fit_result.floatParsFinal()

    # Plot the data and the fit result
    canvas = ROOT.TCanvas("canvas", "Fit", 800, 600)
    canvas.SetTopMargin(0.06)
    canvas.SetTicks(1, 1)
    frame = jet_pt.frame(ROOT.RooFit.Title("   "))
    frame.SetYTitle(f"Events / ({int(binWidth)} GeV)")
    frame.GetYaxis().SetTitleOffset(1.3)
    frame.GetXaxis().SetTitleOffset(1.05)

    data_max = hist_data.GetBinContent(hist_data.GetMaximumBin())
    frame.GetYaxis().SetRangeUser(0, 1.7*data_max)
    data.plotOn(frame)
    model.plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor("#964A8B")))
    model.plotOn(frame, ROOT.RooFit.Components("bkg_pdf"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.TColor.GetColor("#F89C20")))  # Plot background
    model.plotOn(frame, ROOT.RooFit.Components("sig_pdf"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor("#5790FC")))  # Plot signal

    n_params = fit_result.floatParsFinal().getSize()  # Number of free parameters
    n_bins = data.numEntries()
    dof = n_bins - n_params
    chi2 = frame.chiSquare(n_params)

    ratio = fit_params[1].getVal() / fit_params[0].getVal()
    ratio_unc = ratio*np.sqrt((fit_params[1].getError()/fit_params[1].getVal())**2 + (fit_params[0].getError()/fit_params[0].getVal())**2)

    print(f'Final Fit Results for CICADA Threshold {threshold}')
    for param in fit_params:
        print(f'    {param.GetName()} = {param.getVal()} +/- {param.getError()}')
    print("    chi2 / dof = ", chi2)
    print("    signal / background = ", ratio, " +/- ", ratio_unc)
    print()
    integral_bkg_postfit = fit_params[0].getVal()
    integral_sig_postfit = fit_params[1].getVal()
    scale_factors[threshold] = {}
    scale_factors[threshold]["bkg"] = integral_bkg_postfit / integral_bkg_prefit
    scale_factors[threshold]["sig"] = integral_sig_postfit / integral_sig_prefit

    model_line = frame.getObject(int(frame.numItems()) - 3)
    signal_line = frame.getObject(int(frame.numItems()) - 1)
    background_line = frame.getObject(int(frame.numItems()) - 2)

    legend = ROOT.TLegend(0.63, 0.7, 0.85, 0.9)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)

    legend.AddEntry(hist_data, "Data", "pe")
    legend.AddEntry(model_line, "Model (S+B)", "l")
    legend.AddEntry(signal_line, "Signal", "l")
    legend.AddEntry(background_line, "Background", "l")

    # Draw the legend and the frame
    frame.Draw()
    legend.Draw()

    cmsLatex = createLabel()
    cmsLatex.DrawLatex(0.13,
                       0.85,
                       "#splitline{#font[61]{CMS}}{#font[52]{Preliminary}}")
    lumiLatex = createLabel()
    lumiLatex.DrawLatex(0.62,
                        0.95,
                        "#font[42]{31.4 fb^{-1} (13.6 TeV)}")

    canvas.SaveAs(f"plots/fit_result_jetpt_{threshold}.png")

    def postfit_plots(hist_zb, hist_tt, hist_bkg, scale_factors, cicada_thresholds, varname, varnameprint, rebin_factor = 1):

    bin_max_zb = hist_zb.GetXaxis().GetNbins()

    for threshold in cicada_thresholds:

        bin_min_zb = hist_zb.GetXaxis().FindBin(threshold)

        # leading jet pt
        hist_data = hist_zb.ProjectionY(f"hist_data_{varname}", bin_min_zb, bin_max_zb)
        hist_data.Rebin(rebin_factor)
        hist_sig = hist_tt.ProjectionY(f"hist_sig_{varname}", bin_min_zb, bin_max_zb)
        hist_sig_postfit = hist_sig.Clone()
        hist_sig_postfit.Scale(scale_factors[threshold]["sig"])
        hist_sig_postfit.Rebin(rebin_factor)
        hist_bkg_postfit = hist_bkg.Clone()
        hist_bkg_postfit.Scale(scale_factors[threshold]["bkg"])
        hist_bkg_postfit.Rebin(rebin_factor)

        c1 = ROOT.TCanvas("canvas", "Fit", 800, 600)

        hist_data.SetMarkerColor(1)
        hist_data.SetLineColor(1)
        hist_data.SetMarkerStyle(20)
        hist_data.SetStats(0)
        hist_data.SetTitle(" ")
        hist_data.GetYaxis().SetTitle("Events")
        hist_data.GetXaxis().SetTitle(varnameprint)
        hist_data_max = hist_data.GetBinContent(hist_data.GetMaximumBin())

        hist_sig_postfit.SetMarkerColor(ROOT.TColor.GetColor("#5790FC"))
        hist_sig_postfit.SetLineColor(ROOT.TColor.GetColor("#5790FC"))
        hist_sig_postfit.SetStats(0)

        hist_bkg_postfit.SetMarkerColor(ROOT.TColor.GetColor("#F89C20"))
        hist_bkg_postfit.SetLineColor(ROOT.TColor.GetColor("#F89C20"))
        hist_bkg_postfit.SetStats(0)

        hist_model_postfit = hist_bkg_postfit.Clone()
        hist_model_postfit.Add(hist_sig_postfit)
        hist_model_postfit.SetMarkerColor(ROOT.TColor.GetColor("#964A8B"))
        hist_model_postfit.SetLineColor(ROOT.TColor.GetColor("#964A8B"))
        hist_model_postfit.SetStats(0)
        hist_model_max = hist_model_postfit.GetBinContent(hist_model_postfit.GetMaximumBin())

        plot_y_max = max(hist_model_max, hist_data_max)
        hist_data.GetYaxis().SetRangeUser(0, 1.7*plot_y_max)
        hist_data.Draw("E1")
        hist_sig_postfit.Draw("HIST SAME")
        hist_bkg_postfit.Draw("HIST SAME")
        hist_model_postfit.Draw("HIST SAME")

        legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.85)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.04)
        legend.AddEntry(hist_data, "Data", "l")
        legend.AddEntry(hist_model_postfit, "Model (S+B)", "l")
        legend.AddEntry(hist_sig_postfit, "Signal", "l")
        legend.AddEntry(hist_bkg_postfit, "Background", "l")
        legend.Draw()


        c1.Update()
        c1.Draw()
        c1.SaveAs(f"plots/postfit_jetpt_{varname}_threshold{str(int(threshold))}.png")
        c1.Close()

postfit_plots(hist_zb_topmass, hist_tt_topmass, hist_bkg_topmass,
              scale_factors, cicada_thresholds,
              "topmass", r"Reconstructed Top Mass [GeV]", rebin_factor = 7)

