import ROOT
import scipy
import numpy as np

import uproot
f = uproot.open("hists_reconstruction_TTbar_20241029.root")
print(f.keys())
f.close()

def createLabel():
    latex = ROOT.TLatex()
    latex.SetTextSize(0.05)
    latex.SetNDC(True)
    latex.SetTextAlign(11)

    return latex

ROOT.gStyle.SetTitleSize(0.05, "X")
ROOT.gStyle.SetTitleSize(0.05, "Y")

cicada_thresholds = [0.0, 25.0, 50.0, 75.0, 100.0, 106.0, 110.0, 115.0, 120, 125.0, 150.0]
rebin_factor = 7

f_zb = ROOT.TFile.Open("hists_reconstruction_ZeroBias_20241029.root")
f_tt = ROOT.TFile.Open("hists_reconstruction_TTbar_20241029.root")

hist_zb = f_zb.Get("TrijetMass")
bin_max_zb = hist_zb.GetXaxis().GetNbins()
hist_bkg = hist_zb.ProjectionY("hist_bkg", 0, bin_max_zb)
hist_bkg.Rebin(rebin_factor)

hist_tt = f_tt.Get("TrijetMass")
bin_max_tt = hist_tt.GetXaxis().GetNbins()

# Define the observables
mass_top = ROOT.RooRealVar("mass_top", "Reconstructed Top Mass [GeV]", 0, 1000)
jet_pt = ROOT.RooRealVar("jet_pt", "jet_pt", 0, 500)
jet_eta = ROOT.RooRealVar("jet_eta", "jet_eta", -2.4, 2.4)
jet_phi = ROOT.RooRealVar("jet_phi", "jet_eta", -3.14, 3.14)

hist_zb_leadjetpt = f_zb.Get("LeadJetPt")
bin_max_zb_leadjetpt = hist_zb_leadjetpt.GetXaxis().GetNbins()
hist_bkg_leadjetpt = hist_zb_leadjetpt.ProjectionY("hist_bkg_leadjetpt", 0, bin_max_zb_leadjetpt)
dh_bkg_leadjetpt = ROOT.RooDataHist("dh_bkg_leadjetpt", "Leading Jet pT Background", ROOT.RooArgList(jet_pt), hist_bkg_leadjetpt)

hist_tt_leadjetpt = f_tt.Get("LeadJetPt")
bin_max_tt_leadjetpt = hist_tt_leadjetpt.GetXaxis().GetNbins()

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

for threshold in cicada_thresholds:

    workspace = ROOT.RooWorkspace("w")

    ws_var = workspace.var("mass_top")

    ######## load bkg histograms into workspace
    getattr(workspace, "import")(dh_bkg_leadjetpt)
    getattr(workspace, "import")(dh_bkg_leadjeteta)
    getattr(workspace, "import")(dh_bkg_leadjetphi)
    getattr(workspace, "import")(dh_bkg_subleadjetpt)
    getattr(workspace, "import")(dh_bkg_subleadjeteta)
    getattr(workspace, "import")(dh_bkg_subleadjetphi)
    getattr(workspace, "import")(dh_bkg_subsubleadjetpt)
    getattr(workspace, "import")(dh_bkg_subsubleadjeteta)
    getattr(workspace, "import")(dh_bkg_subsubleadjetphi)

    bin_min_zb = hist_zb.GetXaxis().FindBin(threshold)
    bin_min_tt = hist_tt.GetXaxis().FindBin(threshold)

    hist_data = hist_zb.ProjectionY("hist_data", bin_min_zb, bin_max_zb)
    hist_data.Rebin(rebin_factor)
    print(f"Number of Events for Threshold={threshold} = ", hist_data.GetEntries())

    dh_data = ROOT.RooDataHist("dh_data", "Data", ROOT.RooArgList(mass_top), hist_data)
    getattr(workspace, "import")(dh_data)

    hist_sig = hist_tt.ProjectionY("hist_sig", bin_min_tt, bin_max_tt)
    hist_sig.Rebin(rebin_factor)


    ######## non-fit observables
    hist_data_leadjetpt = hist_zb_leadjetpt.ProjectionY("hist_data_leadjetpt", bin_min_zb, bin_max_zb)
    dh_data_leadjetpt = ROOT.RooDataHist("dh_data_leadjetpt", "Leading Jet pT Data", ROOT.RooArgList(jet_pt), hist_data_leadjetpt)
    getattr(workspace, "import")(dh_data_leadjetpt)
    hist_sig_leadjetpt = hist_zb_leadjetpt.ProjectionY("hist_sig_leadjetpt", bin_min_zb, bin_max_zb)
    dh_sig_leadjetpt = ROOT.RooDataHist("dh_sig_leadjetpt", "Leading Jet pT Signal", ROOT.RooArgList(jet_pt), hist_sig_leadjetpt)
    getattr(workspace, "import")(dh_sig_leadjetpt)
    hist_data_leadjeteta = hist_zb_leadjeteta.ProjectionY("hist_data_leadjeteta", bin_min_zb, bin_max_zb)
    dh_data_leadjeteta = ROOT.RooDataHist("dh_data_leadjeteta", "Leading Jet Eta Data", ROOT.RooArgList(jet_eta), hist_data_leadjeteta)
    getattr(workspace, "import")(dh_data_leadjeteta)
    hist_sig_leadjeteta = hist_zb_leadjeteta.ProjectionY("hist_sig_leadjeteta", bin_min_zb, bin_max_zb)
    dh_sig_leadjeteta = ROOT.RooDataHist("dh_sig_leadjeteta", "Leading Jet Eta Signal", ROOT.RooArgList(jet_eta), hist_sig_leadjeteta)
    getattr(workspace, "import")(dh_sig_leadjeteta)
    hist_data_leadjetphi = hist_zb_leadjetphi.ProjectionY("hist_data_leadjetphi", bin_min_zb, bin_max_zb)
    dh_data_leadjetphi = ROOT.RooDataHist("dh_data_leadjetphi", "Leading Jet Phi Data", ROOT.RooArgList(jet_phi), hist_data_leadjetphi)
    getattr(workspace, "import")(dh_data_leadjetphi)
    hist_sig_leadjetphi = hist_zb_leadjetphi.ProjectionY("hist_sig_leadjetphi", bin_min_zb, bin_max_zb)
    dh_sig_leadjetphi = ROOT.RooDataHist("dh_sig_leadjetphi", "Leading Jet Phi Signal", ROOT.RooArgList(jet_phi), hist_sig_leadjetphi)
    getattr(workspace, "import")(dh_sig_leadjetphi)
    hist_data_subleadjetpt = hist_zb_subleadjetpt.ProjectionY("hist_data_subleadjetpt", bin_min_zb, bin_max_zb)
    dh_data_subleadjetpt = ROOT.RooDataHist("dh_data_subleadjetpt", "Subleading Jet pT Data", ROOT.RooArgList(jet_pt), hist_data_subleadjetpt)
    getattr(workspace, "import")(dh_data_subleadjetpt)
    hist_sig_subleadjetpt = hist_zb_subleadjetpt.ProjectionY("hist_sig_subleadjetpt", bin_min_zb, bin_max_zb)
    dh_sig_subleadjetpt = ROOT.RooDataHist("dh_sig_subleadjetpt", "Subleading Jet pT Signal", ROOT.RooArgList(jet_pt), hist_sig_subleadjetpt)
    getattr(workspace, "import")(dh_sig_subleadjetpt)
    hist_data_subleadjeteta = hist_zb_subleadjeteta.ProjectionY("hist_data_subleadjeteta", bin_min_zb, bin_max_zb)
    dh_data_subleadjeteta = ROOT.RooDataHist("dh_data_subleadjeteta", "Subleading Jet Eta Data", ROOT.RooArgList(jet_eta), hist_data_subleadjeteta)
    getattr(workspace, "import")(dh_data_subleadjeteta)
    hist_sig_subleadjeteta = hist_zb_subleadjeteta.ProjectionY("hist_sig_subleadjeteta", bin_min_zb, bin_max_zb)
    dh_sig_subleadjeteta = ROOT.RooDataHist("dh_sig_subleadjeteta", "Subleading Jet Eta Signal", ROOT.RooArgList(jet_eta), hist_sig_subleadjeteta)
    getattr(workspace, "import")(dh_sig_subleadjeteta)
    hist_data_subleadjetphi = hist_zb_subleadjetphi.ProjectionY("hist_data_subleadjetphi", bin_min_zb, bin_max_zb)
    dh_data_subleadjetphi = ROOT.RooDataHist("dh_data_subleadjetphi", "Subleading Jet Phi Data", ROOT.RooArgList(jet_phi), hist_data_subleadjetphi)
    getattr(workspace, "import")(dh_data_subleadjetphi)
    hist_sig_subleadjetphi = hist_zb_subleadjetphi.ProjectionY("hist_sig_subleadjetphi", bin_min_zb, bin_max_zb)
    dh_sig_subleadjetphi = ROOT.RooDataHist("dh_sig_subleadjetphi", "Subleading Jet Phi Signal", ROOT.RooArgList(jet_phi), hist_sig_subleadjetphi)
    getattr(workspace, "import")(dh_sig_subleadjetphi)
    hist_data_subsubleadjetpt = hist_zb_subsubleadjetpt.ProjectionY("hist_data_subsubleadjetpt", bin_min_zb, bin_max_zb)
    dh_data_subsubleadjetpt = ROOT.RooDataHist("dh_data_subsubleadjetpt", "Subsubleading Jet pT Data", ROOT.RooArgList(jet_pt), hist_data_subsubleadjetpt)
    getattr(workspace, "import")(dh_data_subsubleadjetpt)
    hist_sig_subsubleadjetpt = hist_zb_subsubleadjetpt.ProjectionY("hist_sig_subsubleadjetpt", bin_min_zb, bin_max_zb)
    dh_sig_subsubleadjetpt = ROOT.RooDataHist("dh_sig_subsubleadjetpt", "Subsubleading Jet pT Signal", ROOT.RooArgList(jet_pt), hist_sig_subsubleadjetpt)
    getattr(workspace, "import")(dh_sig_subsubleadjetpt)
    hist_data_subsubleadjeteta = hist_zb_subsubleadjeteta.ProjectionY("hist_data_subsubleadjeteta", bin_min_zb, bin_max_zb)
    dh_data_subsubleadjeteta = ROOT.RooDataHist("dh_data_subsubleadjeteta", "Subsubleading Jet Eta Data", ROOT.RooArgList(jet_eta), hist_data_subsubleadjeteta)
    getattr(workspace, "import")(dh_data_subsubleadjeteta)
    hist_sig_subsubleadjeteta = hist_zb_subsubleadjeteta.ProjectionY("hist_sig_subsubleadjeteta", bin_min_zb, bin_max_zb)
    dh_sig_subsubleadjeteta = ROOT.RooDataHist("dh_sig_subsubleadjeteta", "Subsubleading Jet Eta Signal", ROOT.RooArgList(jet_eta), hist_sig_subsubleadjeteta)
    getattr(workspace, "import")(dh_sig_subsubleadjeteta)
    hist_data_subsubleadjetphi = hist_zb_subsubleadjetphi.ProjectionY("hist_data_subsubleadjetphi", bin_min_zb, bin_max_zb)
    dh_data_subsubleadjetphi = ROOT.RooDataHist("dh_data_subsubleadjetphi", "Subsubleading Jet Phi Data", ROOT.RooArgList(jet_phi), hist_data_subsubleadjetphi)
    getattr(workspace, "import")(dh_data_subsubleadjetphi)
    hist_sig_subsubleadjetphi = hist_zb_subsubleadjetphi.ProjectionY("hist_sig_subsubleadjetphi", bin_min_zb, bin_max_zb)
    dh_sig_subsubleadjetphi = ROOT.RooDataHist("dh_sig_subsubleadjetphi", "Subsubleading Jet Phi Signal", ROOT.RooArgList(jet_phi), hist_sig_subsubleadjetphi)
    getattr(workspace, "import")(dh_sig_subsubleadjetphi)


    ######## set up model

    data = ROOT.RooDataHist("data", "Data", ROOT.RooArgList(mass_top), hist_data)
    bkg = ROOT.RooDataHist("bkg", "Background", ROOT.RooArgList(mass_top), hist_bkg)
    sig = ROOT.RooDataHist("sig", "Signal", ROOT.RooArgList(mass_top), hist_sig)

    # Create RooHistPdf for background and signal
    bkg_pdf = ROOT.RooHistPdf("bkg_pdf", "Background PDF", ROOT.RooArgSet(mass_top), bkg)
    sig_pdf = ROOT.RooHistPdf("sig_pdf", "Signal PDF", ROOT.RooArgSet(mass_top), sig)

    # Create coefficients for the signal and background fractions
    n_sig = ROOT.RooRealVar(
        "n_sig",
        "Number of signal events",
        int(hist_data.GetEntries()/2),
        0,
        hist_data.GetEntries())
    poi1 = workspace.var("n_sig")

    n_bkg = ROOT.RooRealVar(
        "n_bkg",
        "Number of background events",
        int(hist_data.GetEntries()/2),
        0,
        hist_data.GetEntries())
    poi2 = workspace.var("n_bkg")


    # Create the combined model as a sum of signal and background PDFs
    model = ROOT.RooAddPdf("model", "Signal + Background", ROOT.RooArgList(sig_pdf, bkg_pdf), ROOT.RooArgList(n_sig, n_bkg))
    workspace.Import(model)

    # Perform the fit
    fit_result = model.fitTo(data, ROOT.RooFit.Save())
    fit_result.Write(f"fitResult_{str(int(threshold))}")
    fit_params = fit_result.floatParsFinal()

    getattr(workspace, "import")(fit_result)


    # Plot the data and the fit result
    canvas = ROOT.TCanvas("canvas", "Fit", 800, 600)
    #frame = mass_top.frame(ROOT.RooFit.Title(f'CICADA Threshold = {threshold}'))
    frame = mass_top.frame(ROOT.RooFit.Title("   "))
    frame.SetYTitle(r"Events / (35 GeV)")
    frame.GetYaxis().SetTitleOffset(1)
    frame.GetXaxis().SetTitleOffset(0.85)

    data.plotOn(frame)
    model.plotOn(frame)
    model.plotOn(frame, ROOT.RooFit.Components("bkg_pdf"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))  # Plot background
    model.plotOn(frame, ROOT.RooFit.Components("sig_pdf"), ROOT.RooFit.LineColor(ROOT.kGreen))  # Plot signal

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

    model_line = frame.getObject(int(frame.numItems()) - 3)
    signal_line = frame.getObject(int(frame.numItems()) - 1)
    background_line = frame.getObject(int(frame.numItems()) - 2)

    legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    legend.SetBorderSize(1)
    legend.SetTextSize(0.05)

    legend.AddEntry(data, "Data", "p")
    legend.AddEntry(model_line, "Model (S+B)", "l")
    legend.AddEntry(signal_line, "Signal", "l")
    legend.AddEntry(background_line, "Background", "l")

    # Draw the legend and the frame
    frame.Draw()
    legend.Draw()

    cmsLatex = createLabel()
    cmsLatex.DrawLatex(0.1,
                       0.93,
                       "#font[61]{CMS} #font[52]{Preliminary}")

    canvas.SaveAs(f"fit_result_{threshold}.png")


    model_config = ROOT.RooStats.ModelConfig("ModelConfig", workspace)
    model_config.SetPdf("model")
    #model_config.SetObservables(ROOT.RooArgSet(ws_var))
    model_config.SetParametersOfInterest(ROOT.RooArgSet(poi1, poi2))

    workspace.Import(model_config)
    workspace.writeToFile(f"workspace_threshold_{int(threshold)}.root")

file = ROOT.TFile("workspace_threshold_100.root")
workspace = file.Get("w")
workspace.Print("v")
