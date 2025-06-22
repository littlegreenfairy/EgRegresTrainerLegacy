"""
regtools is a python module to collect various functions for running the regression
"""
import os
import subprocess
import math 

def delta_phi(phi1, phi2):
    """
    Compute Δφ = φ1 - φ2, wrapped into [-π, +π].
    """
    dphi = phi1 - phi2
    # Wrap into [-π, π]
    while dphi > math.pi:
        dphi -= 2 * math.pi
    while dphi < -math.pi:
        dphi += 2 * math.pi
    return dphi

def genpart_energy(pt, eta):
    return pt * math.cosh(eta)

class RegArgs:
    def set_defaults(self):
        self.base_name = "reg_sc"
        self.cuts_name = "stdCuts"
        self.vars_name = "stdVar"  
        self.cfg_dir = "configs"
        self.out_dir = "results" 
        self.tree_name = "Events"
        #indices for the first and second genmatched electrons
        self.idx1 = "Sum$(Iteration$*(Electron_genPartIdx==0))"
        self.idx2 = "Sum$(Iteration$*(Electron_genPartIdx==1))"
        self.write_full_tree = "0"
        self.reg_out_tag = ""
        self.min_events = 300
        self.shrinkage = 0.15
        self.min_significance = 5.0
        self.event_weight = 1.
        self.mean_min = 0.2
        self.mean_max = 2.0
        self.fix_mean = False
        self.input_testing = "test.root"
        self.input_training = "train.root"
        self.target = f"genpart_energy(GenPart_pt[0], GenPart_eta[0])/(Electron_preRegEnergy[{self.idx1}] + Electron_SCrawESenergy[{self.idx1}])"
        self.var_eb = f"PV_npvs:Electron_preRegEnergy[{self.idx1}]:Electron_scletawidth[{self.idx1}]:Electron_sclphiwidth[{self.idx1}]:Electron_e3x3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_seedEnergy[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_eMax[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_e2nd[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:(Electron_eLeft[{self.idx1}] - Electron_eRight[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:(Electron_eTop[{self.idx1}]  - Electron_eBottom[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:Electron_sigmaietaieta[{self.idx1}]:Electron_sigmaietaiphi[{self.idx1}]:Electron_sigmaiphiiphi[{self.idx1}]:Electron_SCclustersSize[{self.idx1}]:Electron_clusterMaxDR[{self.idx1}]:Electron_clusterMaxDRDEta[{self.idx1}]:Electron_clusterMaxDRDPhi[{self.idx1}]:Electron_subClusterEnergy1[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy2[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:delta_phi(Electron_subClusterPhi1[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi2[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi3[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):Electron_subClusterEta1[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta2[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta3[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_iEtaOrX[{self.idx1}]:Electron_iPhiOrY[{self.idx1}]"  
        self.var_ee = f"PV_npvs:Electron_preRegEnergy[{self.idx1}]:Electron_scletawidth[{self.idx1}]:Electron_sclphiwidth[{self.idx1}]:Electron_e3x3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_seedEnergy[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_eMax[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_e2nd[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:(Electron_eLeft[{self.idx1}] - Electron_eRight[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:(Electron_eTop[{self.idx1}]  - Electron_eBottom[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:Electron_sigmaietaieta[{self.idx1}]:Electron_sigmaietaiphi[{self.idx1}]:Electron_sigmaiphiiphi[{self.idx1}]:Electron_SCclustersSize[{self.idx1}]:Electron_clusterMaxDR[{self.idx1}]:Electron_clusterMaxDRDEta[{self.idx1}]:Electron_clusterMaxDRDPhi[{self.idx1}]:Electron_subClusterEnergy1[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy2[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:delta_phi(Electron_subClusterPhi1[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi2[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi3[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):Electron_subClusterEta1[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta2[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta3[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_iEtaOrX[{self.idx1}]:Electron_iPhiOrY[{self.idx1}]:Electron_etaCrySeed[{self.idx1}]"
        self.cuts_base = "(genpart_energy(GenPart_pt[0], GenPart_eta[0])>0 && Electron_sigmaietaieta[{self.idx1}]>0 && Electron_sigmaiphiiphi[{self.idx1}]>0 && event%2==0)"
        self.ntrees = 1500
        self.do_eb = True

    def __init__(self):
        self.set_defaults()

    def name(self):
        if self.do_eb: region = "EB"
        else: region = "EE"
        return "{args.base_name}_{args.vars_name}_{args.cuts_name}_{region}_ntrees{args.ntrees}".format(args=self,region=region)

    def applied_name(self):
        return "{args.out_dir}/{args.base_name}_{args.vars_name}_{args.cuts_name}_ntrees{args.ntrees}_applied.root".format(args=self)
    
    def cfg_name(self):
        return "{}/{}.config".format(self.cfg_dir,self.name())

    def output_name(self):
        return "{}/{}_results.root".format(self.out_dir,self.name())


    def set_sc_default(self):
        self.target = f"genpart_energy(GenPart_pt[0], GenPart_eta[0])/(Electron_preRegEnergy[{self.idx1}])"
        self.var_eb = f"PV_npvs:Electron_preRegEnergy[{self.idx1}]:Electron_scletawidth[{self.idx1}]:Electron_sclphiwidth[{self.idx1}]:Electron_e3x3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_seedEnergy[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_eMax[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_e2nd[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:(Electron_eLeft[{self.idx1}] - Electron_eRight[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:(Electron_eTop[{self.idx1}]  - Electron_eBottom[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:Electron_sigmaietaieta[{self.idx1}]:Electron_sigmaietaiphi[{self.idx1}]:Electron_sigmaiphiiphi[{self.idx1}]:Electron_SCclustersSize[{self.idx1}]:Electron_clusterMaxDR[{self.idx1}]:Electron_clusterMaxDRDEta[{self.idx1}]:Electron_clusterMaxDRDPhi[{self.idx1}]:Electron_subClusterEnergy1[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy2[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:delta_phi(Electron_subClusterPhi1[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi2[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi3[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):Electron_subClusterEta1[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta2[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta3[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_iEtaOrX[{self.idx1}]:Electron_iPhiOrY[{self.idx1}]"
    
        self.var_ee = f"PV_npvs:Electron_preRegEnergy[{self.idx1}]:Electron_scletawidth[{self.idx1}]:Electron_sclphiwidth[{self.idx1}]:Electron_e3x3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_seedEnergy[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_eMax[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_e2nd[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:(Electron_eLeft[{self.idx1}] - Electron_eRight[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:(Electron_eTop[{self.idx1}]  - Electron_eBottom[{self.idx1}]) / Electron_preRegEnergy[{self.idx1}]:Electron_sigmaietaieta[{self.idx1}]:Electron_sigmaietaiphi[{self.idx1}]:Electron_sigmaiphiiphi[{self.idx1}]:Electron_SCclustersSize[{self.idx1}]:Electron_clusterMaxDR[{self.idx1}]:Electron_clusterMaxDRDEta[{self.idx1}]:Electron_clusterMaxDRDPhi[{self.idx1}]:Electron_subClusterEnergy1[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy2[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:Electron_subClusterEnergy3[{self.idx1}] / Electron_preRegEnergy[{self.idx1}]:delta_phi(Electron_subClusterPhi1[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi2[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):delta_phi(Electron_subClusterPhi3[{self.idx1}],  Electron_scseedPhi[{self.idx1}]):Electron_subClusterEta1[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta2[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_subClusterEta3[{self.idx1}] - Electron_scseedEta[{self.idx1}]:Electron_iEtaOrX[{self.idx1}]:Electron_iPhiOrY[{self.idx1}]:Electron_etaCrySeed[{self.idx1}]"
        self.cuts_base = "(genpart_energy(GenPart_pt[0], GenPart_eta[0])>0 && Electron_sigmaietaieta[{self.idx1}]>0 && Electron_sigmaiphiiphi[{self.idx1}]>0 && event%2==0)"
        self.ntrees = 1500
        self.do_eb = True

    def set_ecal_default(self):
        self.target = f"genpart_energy(GenPart_pt[0], GenPart_eta[0])/(Electron_preRegEnergy[{self.idx1}] + Electron_SCrawESenergy[{self.idx1}])"
    
        self.var_eb = ':'.join([
            f"Electron_preRegEnergy[{self.idx1}]",                      # sc.rawEnergy
            f"Electron_scletawidth[{self.idx1}]",                       # sc.etaWidth
            f"Electron_sclphiwidth[{self.idx1}]",                       # sc.phiWidth
            f"Electron_seedEnergy[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",  # sc.seedClusEnergy/sc.rawEnergy
            f"Electron_e5x5[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",        # ssFull.e5x5/sc.rawEnergy
            f"Electron_hoe[{self.idx1}]",                               # ele.hademTow
            "PV_npvs",                                                  # rho (missing direct equivalent)
            f"Electron_deltaEtaSC[{self.idx1}]",                        # sc.dEtaSeedSC
            f"Electron_deltaPhiSC[{self.idx1}]",                        # sc.dPhiSeedSC
            f"Electron_e3x3[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",        # ssFull.e3x3/sc.rawEnergy
            f"Electron_sigmaietaieta[{self.idx1}]",                     # ssFull.sigmaIEtaIEta
            f"Electron_sigmaietaiphi[{self.idx1}]",                     # ssFull.sigmaIEtaIPhi
            f"Electron_sigmaiphiiphi[{self.idx1}]",                     # ssFull.sigmaIPhiIPhi
            f"Electron_eMax[{self.idx1}]/Electron_e5x5[{self.idx1}]",   # ssFull.eMax/ssFull.e5x5
            f"Electron_e2nd[{self.idx1}]/Electron_e5x5[{self.idx1}]",   # ssFull.e2nd/ssFull.e5x5
            f"Electron_eTop[{self.idx1}]/Electron_e5x5[{self.idx1}]",   # ssFull.eTop/ssFull.e5x5
            f"Electron_eBottom[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.eBottom/ssFull.e5x5
            f"Electron_eLeft[{self.idx1}]/Electron_e5x5[{self.idx1}]",  # ssFull.eLeft/ssFull.e5x5
            f"Electron_eRight[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.eRight/ssFull.e5x5
            f"Electron_e2x5Max[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Max/ssFull.e5x5
            f"Electron_e2x5Left[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Left/ssFull.e5x5
            f"Electron_e2x5Right[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Right/ssFull.e5x5
            f"Electron_e2x5Top[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Top/ssFull.e5x5
            f"Electron_e2x5Bottom[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Bottom/ssFull.e5x5
            f"Electron_nrSatCrys[{self.idx1}]",                         # ele.nrSatCrys
            f"Electron_SCclustersSize[{self.idx1}]",                    # sc.numberOfClusters
            f"Electron_iEtaOrX[{self.idx1}]",                           # sc.iEtaOrX
            f"Electron_iPhiOrY[{self.idx1}]",                           # sc.iPhiOrY
            f"Electron_iEtaMod5[{self.idx1}]",                          # sc.iEtaMod5
            f"Electron_iPhiMod2[{self.idx1}]",                          # sc.iPhiMod2
            f"Electron_iEtaMod20[{self.idx1}]",                         # sc.iEtaMod20
            f"Electron_iPhiMod20[{self.idx1}]"                          # sc.iPhiMod20
        ])

        self.var_ee = ':'.join([
            f"Electron_preRegEnergy[{self.idx1}]",                      # sc.rawEnergy
            f"Electron_scletawidth[{self.idx1}]",                       # sc.etaWidth
            f"Electron_sclphiwidth[{self.idx1}]",                       # sc.phiWidth
            f"Electron_seedEnergy[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",  # sc.seedClusEnergy/sc.rawEnergy
            f"Electron_e5x5[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",        # ssFull.e5x5/sc.rawEnergy
            f"Electron_hoe[{self.idx1}]",                               # ele.hademTow
            "PV_npvs",                                                  # rho (missing direct equivalent)
            f"Electron_deltaEtaSC[{self.idx1}]",                        # sc.dEtaSeedSC
            f"Electron_deltaPhiSC[{self.idx1}]",                        # sc.dPhiSeedSC
            f"Electron_e3x3[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",        # ssFull.e3x3/sc.rawEnergy
            f"Electron_sigmaietaieta[{self.idx1}]",                     # ssFull.sigmaIEtaIEta
            f"Electron_sigmaietaiphi[{self.idx1}]",                     # ssFull.sigmaIEtaIPhi
            f"Electron_sigmaiphiiphi[{self.idx1}]",                     # ssFull.sigmaIPhiIPhi
            f"Electron_eMax[{self.idx1}]/Electron_e5x5[{self.idx1}]",   # ssFull.eMax/ssFull.e5x5
            f"Electron_e2nd[{self.idx1}]/Electron_e5x5[{self.idx1}]",   # ssFull.e2nd/ssFull.e5x5
            f"Electron_eTop[{self.idx1}]/Electron_e5x5[{self.idx1}]",   # ssFull.eTop/ssFull.e5x5
            f"Electron_eBottom[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.eBottom/ssFull.e5x5
            f"Electron_eLeft[{self.idx1}]/Electron_e5x5[{self.idx1}]",  # ssFull.eLeft/ssFull.e5x5
            f"Electron_eRight[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.eRight/ssFull.e5x5
            f"Electron_e2x5Max[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Max/ssFull.e5x5
            f"Electron_e2x5Left[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Left/ssFull.e5x5
            f"Electron_e2x5Right[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Right/ssFull.e5x5
            f"Electron_e2x5Top[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Top/ssFull.e5x5
            f"Electron_e2x5Bottom[{self.idx1}]/Electron_e5x5[{self.idx1}]", # ssFull.e2x5Bottom/ssFull.e5x5
            f"Electron_nrSatCrys[{self.idx1}]",                         # ele.nrSatCrys
            f"Electron_SCclustersSize[{self.idx1}]",                    # sc.numberOfClusters
            f"Electron_iEtaOrX[{self.idx1}]",                           # sc.iEtaOrX
            f"Electron_iPhiOrY[{self.idx1}]",                           # sc.iPhiOrY
            f"Electron_iEtaMod5[{self.idx1}]",                          # sc.iEtaMod5
            f"Electron_iPhiMod2[{self.idx1}]",                          # sc.iPhiMod2
            f"Electron_iEtaMod20[{self.idx1}]",                         # sc.iEtaMod20
            f"Electron_iPhiMod20[{self.idx1}]",                         # sc.iPhiMod20
            f"Electron_SCrawESenergy[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]" # sc.rawESEnergy/sc.rawEnergy
        ])
        
    def set_phoecal_default(self):
        """Configure for photon ECAL energy regression with NanoAOD variables"""
    
        self.target = f"genpart_energy(GenPart_pt[0], GenPart_eta[0])/(Photon_preRegEnergy[{self.idx1}] + Photon_SCrawESenergy[{self.idx1}])"
        
        self.var_eb = ':'.join([
            f"Photon_preRegEnergy[{self.idx1}]",                       # sc.rawEnergy
            f"Photon_scletawidth[{self.idx1}]",                        # sc.etaWidth
            f"Photon_sclphiwidth[{self.idx1}]",                        # sc.phiWidth
            f"Photon_seedEnergy[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]",  # sc.seedClusEnergy/sc.rawEnergy
            f"Photon_e5x5[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]",       # ssFull.e5x5/sc.rawEnergy
            f"Photon_hoe[{self.idx1}]",                                # pho.hademCone
            "PV_npvs",                                                 # rho (missing direct equivalent)
            f"Photon_deltaEtaSC[{self.idx1}]",                         # sc.dEtaSeedSC
            f"Photon_deltaPhiSC[{self.idx1}]",                         # sc.dPhiSeedSC
            f"Photon_e3x3[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]",       # ssFull.e3x3/sc.rawEnergy
            f"Photon_sigmaietaieta[{self.idx1}]",                      # ssFull.sigmaIEtaIEta
            f"Photon_sigmaietaiphi[{self.idx1}]",                      # phoSSFull.sigmaIEtaIPhi 
            f"Photon_sigmaiphiiphi[{self.idx1}]",                      # ssFull.sigmaIPhiIPhi
            f"Photon_eMax[{self.idx1}]/Photon_e5x5[{self.idx1}]",      # ssFull.eMax/ssFull.e5x5
            f"Photon_e2nd[{self.idx1}]/Photon_e5x5[{self.idx1}]",      # ssFull.e2nd/ssFull.e5x5
            f"Photon_eTop[{self.idx1}]/Photon_e5x5[{self.idx1}]",      # ssFull.eTop/ssFull.e5x5
            f"Photon_eBottom[{self.idx1}]/Photon_e5x5[{self.idx1}]",   # ssFull.eBottom/ssFull.e5x5
            f"Photon_eLeft[{self.idx1}]/Photon_e5x5[{self.idx1}]",     # ssFull.eLeft/ssFull.e5x5
            f"Photon_eRight[{self.idx1}]/Photon_e5x5[{self.idx1}]",    # ssFull.eRight/ssFull.e5x5
            f"Photon_e2x5Max[{self.idx1}]/Photon_e5x5[{self.idx1}]",   # ssFull.e2x5Max/ssFull.e5x5
            f"Photon_e2x5Left[{self.idx1}]/Photon_e5x5[{self.idx1}]",  # ssFull.e2x5Left/ssFull.e5x5
            f"Photon_e2x5Right[{self.idx1}]/Photon_e5x5[{self.idx1}]", # ssFull.e2x5Right/ssFull.e5x5
            f"Photon_e2x5Top[{self.idx1}]/Photon_e5x5[{self.idx1}]",   # ssFull.e2x5Top/ssFull.e5x5
            f"Photon_e2x5Bottom[{self.idx1}]/Photon_e5x5[{self.idx1}]", # ssFull.e2x5Bottom/ssFull.e5x5
            f"Photon_nrSatCrys[{self.idx1}]",                          # pho.nrSatCrys
            f"Photon_SCclustersSize[{self.idx1}]",                     # sc.numberOfClusters
            f"Photon_iEtaOrX[{self.idx1}]",                            # sc.iEtaOrX
            f"Photon_iPhiOrY[{self.idx1}]",                            # sc.iPhiOrY
            f"Photon_iEtaMod5[{self.idx1}]",                           # sc.iEtaMod5
            f"Photon_iPhiMod2[{self.idx1}]",                           # sc.iPhiMod2
            f"Photon_iEtaMod20[{self.idx1}]",                          # sc.iEtaMod20
            f"Photon_iPhiMod20[{self.idx1}]"                           # sc.iPhiMod20
        ])

        self.var_ee = ':'.join([
            f"Photon_preRegEnergy[{self.idx1}]",                       # sc.rawEnergy
            f"Photon_scletawidth[{self.idx1}]",                        # sc.etaWidth
            f"Photon_sclphiwidth[{self.idx1}]",                        # sc.phiWidth
            f"Photon_seedEnergy[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]",  # sc.seedClusEnergy/sc.rawEnergy
            f"Photon_e5x5[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]",       # ssFull.e5x5/sc.rawEnergy
            f"Photon_hoe[{self.idx1}]",                                # pho.hademCone
            "PV_npvs",                                                 # rho (missing direct equivalent)
            f"Photon_deltaEtaSC[{self.idx1}]",                         # sc.dEtaSeedSC
            f"Photon_deltaPhiSC[{self.idx1}]",                         # sc.dPhiSeedSC
            f"Photon_e3x3[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]",       # ssFull.e3x3/sc.rawEnergy
            f"Photon_sigmaietaieta[{self.idx1}]",                      # ssFull.sigmaIEtaIEta
            f"Photon_sigmaietaiphi[{self.idx1}]",                      # phoSSFull.sigmaIEtaIPhi 
            f"Photon_sigmaiphiiphi[{self.idx1}]",                      # ssFull.sigmaIPhiIPhi
            f"Photon_eMax[{self.idx1}]/Photon_e5x5[{self.idx1}]",      # ssFull.eMax/ssFull.e5x5
            f"Photon_e2nd[{self.idx1}]/Photon_e5x5[{self.idx1}]",      # ssFull.e2nd/ssFull.e5x5
            f"Photon_eTop[{self.idx1}]/Photon_e5x5[{self.idx1}]",      # ssFull.eTop/ssFull.e5x5
            f"Photon_eBottom[{self.idx1}]/Photon_e5x5[{self.idx1}]",   # ssFull.eBottom/ssFull.e5x5
            f"Photon_eLeft[{self.idx1}]/Photon_e5x5[{self.idx1}]",     # ssFull.eLeft/ssFull.e5x5
            f"Photon_eRight[{self.idx1}]/Photon_e5x5[{self.idx1}]",    # ssFull.eRight/ssFull.e5x5
            f"Photon_e2x5Max[{self.idx1}]/Photon_e5x5[{self.idx1}]",   # ssFull.e2x5Max/ssFull.e5x5
            f"Photon_e2x5Left[{self.idx1}]/Photon_e5x5[{self.idx1}]",  # ssFull.e2x5Left/ssFull.e5x5
            f"Photon_e2x5Right[{self.idx1}]/Photon_e5x5[{self.idx1}]", # ssFull.e2x5Right/ssFull.e5x5
            f"Photon_e2x5Top[{self.idx1}]/Photon_e5x5[{self.idx1}]",   # ssFull.e2x5Top/ssFull.e5x5
            f"Photon_e2x5Bottom[{self.idx1}]/Photon_e5x5[{self.idx1}]", # ssFull.e2x5Bottom/ssFull.e5x5
            f"Photon_nrSatCrys[{self.idx1}]",                          # pho.nrSatCrys
            f"Photon_SCclustersSize[{self.idx1}]",                     # sc.numberOfClusters
            f"Photon_iEtaOrX[{self.idx1}]",                            # sc.iEtaOrX
            f"Photon_iPhiOrY[{self.idx1}]",                            # sc.iPhiOrY
            f"Photon_iEtaMod5[{self.idx1}]",                           # sc.iEtaMod5
            f"Photon_iPhiMod2[{self.idx1}]",                           # sc.iPhiMod2
            f"Photon_iEtaMod20[{self.idx1}]",                          # sc.iEtaMod20
            f"Photon_iPhiMod20[{self.idx1}]",                          # sc.iPhiMod20
            f"Photon_SCrawESenergy[{self.idx1}]/Photon_preRegEnergy[{self.idx1}]" # sc.rawESEnergy/sc.rawEnergy
        ])
        
    def set_elecomb_default(self):
        """Configure for electron combined ECAL+tracker energy regression with NanoAOD variables"""
        # Note: This uses regression output variables which may need special handling
    
        self.var_eb = ":".join([
            f"(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalMean",  # (sc.rawEnergy+sc.rawESEnergy)*regEcalMean
            "regEcalSigma/regEcalMean",                               # regEcalSigma/regEcalMean
            f"Electron_trkPModeErr[{self.idx1}]/Electron_trkPMode[{self.idx1}]",  # ele.trkPModeErr/ele.trkPMode
            f"(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalMean/Electron_trkPMode[{self.idx1}]",  # (sc.rawEnergy+sc.rawESEnergy)*regEcalMean/ele.trkPMode
            f"Electron_ecalDrivenSeed[{self.idx1}]",                  # ele.ecalDrivenSeed
            f"Electron_e3x3[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",  # ssFull.e3x3/sc.rawEnergy
            f"Electron_fbrem[{self.idx1}]",                           # ele.fbrem
            f"Electron_trkEtaMode[{self.idx1}]",                      # ele.trkEtaMode
            f"Electron_trkPhiMode[{self.idx1}]"                       # ele.trkPhiMode
        ])
        
        self.var_ee = ":".join([
            f"(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalMean",  # (sc.rawEnergy+sc.rawESEnergy)*regEcalMean
            "regEcalSigma/regEcalMean",                               # regEcalSigma/regEcalMean
            f"Electron_trkPModeErr[{self.idx1}]/Electron_trkPMode[{self.idx1}]",  # ele.trkPModeErr/ele.trkPMode
            f"(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalMean/Electron_trkPMode[{self.idx1}]",  # (sc.rawEnergy+sc.rawESEnergy)*regEcalMean/ele.trkPMode
            f"Electron_ecalDrivenSeed[{self.idx1}]",                  # ele.ecalDrivenSeed
            f"Electron_e3x3[{self.idx1}]/Electron_preRegEnergy[{self.idx1}]",  # ssFull.e3x3/sc.rawEnergy
            f"Electron_fbrem[{self.idx1}]",                           # ele.fbrem
            f"Electron_trkEtaMode[{self.idx1}]",                      # ele.trkEtaMode
            f"Electron_trkPhiMode[{self.idx1}]"                       # ele.trkPhiMode
        ])
        
        # Complex target expression for combined energy estimation
        self.target = f"(genpart_energy(GenPart_pt[0], GenPart_eta[0]) * (Electron_trkPModeErr[{self.idx1}]*Electron_trkPModeErr[{self.idx1}] + (Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalSigma*regEcalSigma) / ( (Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalMean*Electron_trkPModeErr[{self.idx1}]*Electron_trkPModeErr[{self.idx1}] + Electron_trkPMode[{self.idx1}]*(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*(Electron_preRegEnergy[{self.idx1}]+Electron_SCrawESenergy[{self.idx1}])*regEcalSigma*regEcalSigma ))"
    def make_cfg(self):
        base_cfg = """
Trainer: GBRLikelihoodTrain
NumberOfRegressions: 1
TMVAFactoryOptions: !V:!Silent:!Color:!DrawProgressBar
OutputDirectory: {args.out_dir}
Regression.1.Name: {name}
Regression.1.InputFiles: {args.input_training}
Regression.1.Tree: {args.tree_name}
Regression.1.trainingOptions: SplitMode=random:!V
Regression.1.Options: MinEvents={args.min_events}:Shrinkage={args.shrinkage}:NTrees={args.ntrees}:MinSignificance={args.min_significance}:EventWeight={args.event_weight}
Regression.1.DoCombine: False
Regression.1.DoEB: {args.do_eb}
Regression.1.VariablesEB: {args.var_eb}
Regression.1.VariablesEE: {args.var_ee}
Regression.1.Target: {args.target}
Regression.1.CutBase: {args.cuts_base} 
Regression.1.CutEB: sc.isEB
Regression.1.CutEE: !sc.isEB
Regression.1.MeanMin: {args.mean_min}
Regression.1.MeanMax: {args.mean_max}
Regression.1.FixMean: {args.fix_mean}

""".format(args=self,name=self.name())
        if not os.path.isdir(self.cfg_dir):
            os.mkdir(self.cfg_dir)
        with open(self.cfg_name(),"w") as f:
            f.write(base_cfg)

    def run_eb_and_ee(self):  

        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)

        self.do_eb = True
        self.make_cfg()
        print("starting: {}".format(self.name()))
        subprocess.Popen(["bin/el9_amd64_gcc12/RegressionTrainerExe",self.cfg_name()]).communicate()
        forest_eb_file = self.output_name()
        print("Expected EB output:", forest_eb_file)
    
        self.do_eb = False
        self.make_cfg()
        print("starting: {}".format(self.name()))
        subprocess.Popen(["bin/el9_amd64_gcc12/RegressionTrainerExe",self.cfg_name()]).communicate()
        forest_ee_file = self.output_name()
        print("Expected EE output:", forest_ee_file)
        
        subprocess.Popen(["bin/el9_amd64_gcc12/RegressionApplierExe",self.input_testing,self.applied_name(),"--gbrForestFileEE",forest_ee_file,"--gbrForestFileEB",forest_eb_file,"--nrThreads","4","--treeName",self.tree_name,"--writeFullTree",self.write_full_tree,"--regOutTag",self.reg_out_tag]).communicate()

        print("made ",self.applied_name())


    def forest_filenames(self):
        do_eb_org = self.do_eb
        self.do_eb = True
        forest_eb_file = self.output_name()
        self.do_eb = False
        forest_ee_file = self.output_name()
        self.do_eb = do_eb_org
        return forest_eb_file,forest_ee_file
