#!/usr/bin/env python3
import sys
import uproot

def check_branches(filename, vars_list):
    # open file and tree
    f = uproot.open(filename)
    if "Events" not in f:
        print(f"ERROR: 'Events' tree not found in {filename}")
        return
    tree = f["Events"]

    # get all branch names
    branches = set(tree.keys())

    # check each requested var
    missing = []
    for var in vars_list:
        if var not in branches:
            missing.append(var)

    # report
    print(f"\nChecked {len(vars_list)} variables against {len(branches)} branches in {filename!r}\n")
    if not missing:
        print("All variables are PRESENT!")
    else:
        print(" Missing variables:")
        for v in missing:
            print(f"   - {v}")
    print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_branches.py yourNtuple.root")
        sys.exit(1)

    # your EB and EE lists:
    var_eb = (
        "nrVert:sc.rawEnergy:sc.etaWidth:sc.phiWidth:"
        "ssFrac.e3x3/sc.rawEnergy:sc.seedClusEnergy/sc.rawEnergy:"
        "ssFrac.eMax/sc.rawEnergy:ssFrac.e2nd/sc.rawEnergy:"
        "ssFrac.eLeftRightDiffSumRatio:ssFrac.eTopBottomDiffSumRatio:"
        "ssFrac.sigmaIEtaIEta:ssFrac.sigmaIEtaIPhi:ssFrac.sigmaIPhiIPhi:"
        "sc.numberOfSubClusters:sc.clusterMaxDR:sc.clusterMaxDRDPhi:"
        "sc.clusterMaxDRDEta:sc.clusterMaxDRRawEnergy/sc.rawEnergy:"
        "clus1.clusterRawEnergy/sc.rawEnergy:clus2.clusterRawEnergy/sc.rawEnergy:"
        "clus3.clusterRawEnergy/sc.rawEnergy:clus1.clusterDPhiToSeed:"
        "clus2.clusterDPhiToSeed:clus3.clusterDPhiToSeed:"
        "clus1.clusterDEtaToSeed:clus2.clusterDEtaToSeed:clus3.clusterDEtaToSeed:"
        "sc.iEtaOrX:sc.iPhiOrY"
    )
    var_ee = (
        var_eb + ":sc.seedEta"
    )

    eb_vars = var_eb.split(":")
    ee_vars = var_ee.split(":")

    fname = sys.argv[1]
    print("=== EB variables ===")
    check_branches(fname, eb_vars)
    print("=== EE variables ===")
    check_branches(fname, ee_vars)

