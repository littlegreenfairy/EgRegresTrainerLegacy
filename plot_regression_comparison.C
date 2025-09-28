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
    TCanvas* c1 = new TCanvas("c1", "Regression Comparison", 1200, 600);
    c1->Divide(2, 1);
    
    // Define the event selection cut (evt.eventnr%5>2)
    TCut eventCut = "evt.eventnr%5>2";
    
    // Create histograms
    TH1F* h1 = new TH1F("h1", "Ideal Regression Normalized Residual;(1/regIdealInvTar - regRealMean)/regRealSigma;Events", 100, -5, 5);
    TH1F* h2 = new TH1F("h2", "Real Regression Normalized Residual;(1/regRealInvTar - regRealMean)/regRealSigma;Events", 100, -5, 5);
    
    // Set histogram styles
    h1->SetLineColor(kBlue);
    h1->SetFillColor(kBlue);
    h1->SetFillStyle(3004);
    h1->SetLineWidth(2);
    
    h2->SetLineColor(kRed);
    h2->SetFillColor(kRed);
    h2->SetFillStyle(3005);
    h2->SetLineWidth(2);
    
    // Plot first histogram: (1/regIdealInvTar - regRealMean)/regRealSigma
    c1->cd(1);
    tree->Draw("(1/regIdealInvTar - regRealMean)/regRealSigma>>h1", eventCut, "");
    h1->GetXaxis()->SetTitle("(1/regIdealInvTar - regRealMean)/regRealSigma");
    h1->GetYaxis()->SetTitle("Events");
    h1->SetTitle("Ideal Regression Normalized Residual");
    
    // Add statistics
    gPad->Update();
    TPaveStats* st1 = (TPaveStats*)h1->FindObject("stats");
    if (st1) {
        st1->SetX1NDC(0.65);
        st1->SetX2NDC(0.95);
        st1->SetY1NDC(0.7);
        st1->SetY2NDC(0.95);
    }
    
    // Plot second histogram: (1/regRealInvTar - regRealMean)/regRealSigma
    c1->cd(2);
    tree->Draw("(1/regRealInvTar - regRealMean)/regRealSigma>>h2", eventCut, "");
    h2->GetXaxis()->SetTitle("(1/regRealInvTar - regRealMean)/regRealSigma");
    h2->GetYaxis()->SetTitle("Events");
    h2->SetTitle("Real Regression Normalized Residual");
    
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
    std::cout << "Ideal Regression:" << std::endl;
    std::cout << "  Mean: " << h1->GetMean() << std::endl;
    std::cout << "  RMS:  " << h1->GetRMS() << std::endl;
    std::cout << "  Entries: " << h1->GetEntries() << std::endl;
    
    std::cout << "\nReal Regression:" << std::endl;
    std::cout << "  Mean: " << h2->GetMean() << std::endl;
    std::cout << "  RMS:  " << h2->GetRMS() << std::endl;
    std::cout << "  Entries: " << h2->GetEntries() << std::endl;
    
    // Save the canvas to the specified directory
    c1->SaveAs(outputDir + "regression_comparison.png");
    c1->SaveAs(outputDir + "regression_comparison.pdf");
    
    // Keep the canvas open
    c1->Update();
    
    // Optional: Create an overlay plot
    TCanvas* c2 = new TCanvas("c2", "Regression Comparison Overlay", 800, 600);
    
    // Normalize histograms for comparison
    TH1F* h1_norm = (TH1F*)h1->Clone("h1_norm");
    TH1F* h2_norm = (TH1F*)h2->Clone("h2_norm");
    
    if (h1_norm->GetEntries() > 0) h1_norm->Scale(1.0/h1_norm->Integral());
    if (h2_norm->GetEntries() > 0) h2_norm->Scale(1.0/h2_norm->Integral());
    
    h1_norm->SetTitle("Regression Comparison (Normalized)");
    h1_norm->GetYaxis()->SetTitle("Normalized Events");
    
    h1_norm->Draw("HIST");
    h2_norm->Draw("HIST SAME");
    
    // Add legend
    TLegend* leg = new TLegend(0.15, 0.75, 0.45, 0.9);
    leg->AddEntry(h1_norm, "Ideal Regression", "f");
    leg->AddEntry(h2_norm, "Real Regression", "f");
    leg->SetBorderSize(0);
    leg->SetFillStyle(0);
    leg->Draw();
    
    c2->SaveAs(outputDir + "regression_comparison_overlay.png");
    c2->SaveAs(outputDir + "regression_comparison_overlay.pdf");
    
    std::cout << "\nPlots saved in " << outputDir << std::endl;
    std::cout << "Files: regression_comparison.png/pdf and regression_comparison_overlay.png/pdf" << std::endl;
}