#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"

void compareMeanSigma(const char* origPath, const char* friendPath) {
  // 1) Open files and retrieve trees
  TFile *fOrig   = TFile::Open(origPath,   "READ");
  TFile *fFriend = TFile::Open(friendPath, "READ");
  if (!fOrig || !fOrig->IsOpen() || !fFriend || !fFriend->IsOpen()) {
    printf("Error opening files\n");
    return;
  }
  TTree *tOrig   = (TTree*)fOrig->Get("egRegTree");
  TTree *tFriend = (TTree*)fFriend->Get("egRegTreeFriend");
  if (!tOrig || !tFriend) {
    printf("Error retrieving trees\n");
    return;
  }

  // 2) Book histograms
  const Int_t nBinsMean = 100;
  const Double_t minMean = 0, maxMean = 3;
  TH1F *hOrigMean   = new TH1F("hOrigMean",   "Original vs New Mean;Mean;Density",   nBinsMean, minMean, maxMean);
  TH1F *hFriendMean = new TH1F("hFriendMean", ";Mean;Density",                          nBinsMean, minMean, maxMean);

  const Int_t nBinsSigma = 100;
  const Double_t minSigma = 0, maxSigma = 1;
  TH1F *hOrigSigma   = new TH1F("hOrigSigma",   "Original vs New Sigma;Sigma;Density",   nBinsSigma, minSigma, maxSigma);
  TH1F *hFriendSigma = new TH1F("hFriendSigma", ";Sigma;Density",                         nBinsSigma, minSigma, maxSigma);

  // 3) Fill histograms (use "goff" to suppress canvas)
  tOrig->Draw("(mc.energy/(sc.rawEnergy))>>hOrigMean",   "", "goff");
  tFriend->Draw("mean>>hFriendMean",       "", "goff");
  tOrig->Draw("ele.corrSigma>>hOrigSigma", "", "goff");
  tFriend->Draw("sigma>>hFriendSigma",     "", "goff");

  // 4) Normalize to unit area (density)
  if (hOrigMean->GetEntries() > 0)   hOrigMean->Scale(1.0 / hOrigMean->Integral("width"));
  if (hFriendMean->GetEntries() > 0) hFriendMean->Scale(1.0 / hFriendMean->Integral("width"));
  if (hOrigSigma->GetEntries() > 0)  hOrigSigma->Scale(1.0 / hOrigSigma->Integral("width"));
  if (hFriendSigma->GetEntries() > 0)hFriendSigma->Scale(1.0 / hFriendSigma->Integral("width"));

  // 5) Draw means on one canvas
  TCanvas *c1 = new TCanvas("c1","Mean Comparison",800,600);
  hOrigMean->SetLineColor(kRed);
  hFriendMean->SetLineColor(kBlue);
  hFriendMean->Draw("HIST");
  hOrigMean->Draw("HIST SAME");
  TLegend *leg1 = new TLegend(0.6,0.7,0.88,0.88);
  leg1->AddEntry(hOrigMean,   "ele.corrMean (orig)",   "l");
  leg1->AddEntry(hFriendMean, "mean (new)",            "l");
  leg1->Draw();

  // 6) Draw sigmas on another canvas
  TCanvas *c2 = new TCanvas("c2","Sigma Comparison",800,600);
  hOrigSigma->SetLineColor(kRed);
  hFriendSigma->SetLineColor(kBlue);
  hOrigSigma->Draw("HIST");
  hFriendSigma->Draw("HIST SAME");
  TLegend *leg2 = new TLegend(0.6,0.7,0.88,0.88);
  leg2->AddEntry(hOrigSigma,   "ele.corrSigma (orig)", "l");
  leg2->AddEntry(hFriendSigma, "sigma (new)",          "l");
  leg2->Draw();

  // 7) Keep canvases open
  c1->Update();
  c2->Update();
    // Save canvases to PNG
  c1->SaveAs("/eos/user/e/eldesant/www/DarkPhotonGang/mean_comparison.png");
 // c2->SaveAs("/eos/user/e/eldesant/www/DarkPhotonGang/sigma_comparison.png");
}

