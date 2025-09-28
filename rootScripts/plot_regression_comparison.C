void plot_regression_comparison() {
    // Open the ROOT file
    TFile* file = TFile::Open("/eos/user/e/eldesant/results2022/regEleEcalTrk2022_RealIC_stdVar_stdCuts_ntrees1500_applied.root");
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Cannot open file!" << std::endl;
        return;
    }
    
    // Get the tree
    TTree* tree = (TTree*)file->Get("egRegTree");
    if (!tree) {
        std::cerr << "Error: Cannot find egRegTree!" << std::endl;
        file->Close();
        return;
    }
    
    // Define output directory
    TString outputDir = "/eos/user/e/eldesant/www/DarkPhotonGang/RegressionStep2/";
    
    // Create canvas
    TCanvas* c1 = new TCanvas("c1", "Regression Comparison", 800, 600);
    
    // Define the event selection cut (evt.eventnr%5>2)
    TCut eventCut = "evt.eventnr%5>2 && ele.et != 0";
    
    // Create histogram
    TH1F* h2 = new TH1F("h2", "Real Regression Normalized Residual;(1/regRealInvTar - regRealMean)/regRealSigma;Events", 100, -5, 5);
    
    // Set histogram style
    h2->SetLineColor(kRed);
    h2->SetFillColor(kRed);
    h2->SetFillStyle(3005);
    h2->SetLineWidth(2);
    
    // Plot histogram: (1/regRealInvTar - regRealMean)/regRealSigma
    tree->Draw("(1/regRealInvTar - regRealMean)/regRealSigma>>h2", eventCut, "");
    
    // Normalize the histogram
    if (h2->GetEntries() > 0) {
        h2->Scale(1.0 / h2->Integral());
    }
    
    h2->GetXaxis()->SetTitle("(1/regRealInvTar - regRealMean)/regRealSigma");
    h2->GetYaxis()->SetTitle("Normalized Events");
    h2->SetTitle("Real Regression Normalized Residual");

    // Fit the histogram with a Gaussian
    TF1* gaussFit = new TF1("gaussFit", "gaus", -5, 5);
    gaussFit->SetLineColor(kBlue);
    gaussFit->SetLineWidth(2);
    gaussFit->SetLineStyle(2); // dashed line
    
    // Perform the fit
    h2->Fit(gaussFit, "R");  // "R" uses the range specified in the function
    
    // Draw histogram and fit
    h2->Draw();
    gaussFit->Draw("same");
    
    // Add statistics
    gPad->Update();
    TPaveStats* st2 = (TPaveStats*)h2->FindObject("stats");
    if (st2) {
        st2->SetX1NDC(0.65);
        st2->SetX2NDC(0.95);
        st2->SetY1NDC(0.7);
        st2->SetY2NDC(0.95);
    }
    
    // Print some statistics
    std::cout << "\n=== Statistics for evt.eventnr%5>2 ===" << std::endl;
    std::cout << "Real Regression:" << std::endl;
    std::cout << "  Mean: " << h2->GetMean() << std::endl;
    std::cout << "  RMS:  " << h2->GetRMS() << std::endl;
    std::cout << "  Entries: " << h2->GetEntries() << std::endl;
    
    // Print Gaussian fit results
    std::cout << "\n=== Gaussian Fit Results ===" << std::endl;
    std::cout << "  Fit Mean: " << gaussFit->GetParameter(1) << " ± " << gaussFit->GetParError(1) << std::endl;
    std::cout << "  Fit Sigma: " << gaussFit->GetParameter(2) << " ± " << gaussFit->GetParError(2) << std::endl;
    std::cout << "  Chi2/NDF: " << gaussFit->GetChisquare() << "/" << gaussFit->GetNDF() 
              << " = " << gaussFit->GetChisquare()/gaussFit->GetNDF() << std::endl;
    
    // Save the canvas to the specified directory
    c1->SaveAs(outputDir + "real_regression_plot.png");
    c1->SaveAs(outputDir + "real_regression_plot.pdf");
    
    // Keep the canvas open
    c1->Update();
    
    // Create plots for events with (1/regRealInvTar - regRealMean)/regRealSigma < -2
    TCut outlierCut = eventCut && "(1/regRealInvTar - regRealMean)/regRealSigma < -2";
    
    // Create canvas for outlier analysis
    TCanvas* c3 = new TCanvas("c3", "Outlier Analysis", 1200, 400);
    c3->Divide(3, 1);
    
    // Create histograms for ele.et, ele.eta, ele.phi
    TH1F* h_et = new TH1F("h_et", "Electron E_{T} for Outliers;E_{T} [GeV];Events", 50, 0, 200);
    TH1F* h_eta = new TH1F("h_eta", "Electron #eta for Outliers;#eta;Events", 50, -3, 3);
    TH1F* h_phi = new TH1F("h_phi", "Electron #phi for Outliers;#phi [rad];Events", 50, -3.2, 3.2);
    
    // Set histogram styles
    h_et->SetLineColor(kBlue);
    h_et->SetFillColor(kBlue);
    h_et->SetFillStyle(3004);
    h_et->SetLineWidth(2);
    
    h_eta->SetLineColor(kGreen+2);
    h_eta->SetFillColor(kGreen+2);
    h_eta->SetFillStyle(3005);
    h_eta->SetLineWidth(2);
    
    h_phi->SetLineColor(kMagenta);
    h_phi->SetFillColor(kMagenta);
    h_phi->SetFillStyle(3006);
    h_phi->SetLineWidth(2);
    
    // Plot ele.et
    c3->cd(1);
    tree->Draw("ele.et>>h_et", outlierCut, "");
    h_et->GetXaxis()->SetTitle("E_{T} [GeV]");
    h_et->GetYaxis()->SetTitle("Events");
    h_et->SetTitle("Electron E_{T} for Outliers");
    
    // Plot ele.eta
    c3->cd(2);
    tree->Draw("ele.eta>>h_eta", outlierCut, "");
    h_eta->GetXaxis()->SetTitle("#eta");
    h_eta->GetYaxis()->SetTitle("Events");
    h_eta->SetTitle("Electron #eta for Outliers");
    
    // Plot ele.phi
    c3->cd(3);
    tree->Draw("ele.phi>>h_phi", outlierCut, "");
    h_phi->GetXaxis()->SetTitle("#phi [rad]");
    h_phi->GetYaxis()->SetTitle("Events");
    h_phi->SetTitle("Electron #phi for Outliers");
    
    // Print statistics for outlier events
    std::cout << "\n=== Statistics for Outlier Events ((1/regRealInvTar - regRealMean)/regRealSigma < -2) ===" << std::endl;
    std::cout << "Electron E_T:" << std::endl;
    std::cout << "  Mean: " << h_et->GetMean() << " GeV" << std::endl;
    std::cout << "  RMS:  " << h_et->GetRMS() << " GeV" << std::endl;
    std::cout << "  Entries: " << h_et->GetEntries() << std::endl;
    
    std::cout << "\nElectron eta:" << std::endl;
    std::cout << "  Mean: " << h_eta->GetMean() << std::endl;
    std::cout << "  RMS:  " << h_eta->GetRMS() << std::endl;
    std::cout << "  Entries: " << h_eta->GetEntries() << std::endl;
    
    std::cout << "\nElectron phi:" << std::endl;
    std::cout << "  Mean: " << h_phi->GetMean() << " rad" << std::endl;
    std::cout << "  RMS:  " << h_phi->GetRMS() << " rad" << std::endl;
    std::cout << "  Entries: " << h_phi->GetEntries() << std::endl;
    
    // Save outlier analysis plots
    c3->SaveAs(outputDir + "outlier_analysis.png");
    c3->SaveAs(outputDir + "outlier_analysis.pdf");
    c3->Update();
    
    std::cout << "\nPlots saved in " << outputDir << std::endl;
    std::cout << "Files: real_regression_plot.png/pdf and outlier_analysis.png/pdf" << std::endl;
}