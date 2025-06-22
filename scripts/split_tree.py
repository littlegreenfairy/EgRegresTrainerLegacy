#!/usr/bin/env python3
import sys
import argparse
import ROOT

def split_tree(input_file: str,
               tree_name: str,
               n_first: int,
               out1: str,
               out2: str) -> None:
    # Open input
    f_in = ROOT.TFile.Open(input_file, "READ")
    if not f_in or f_in.IsZombie():
        sys.exit(f"Error: cannot open '{input_file}'")
    tree = f_in.Get(tree_name)
    if not tree:
        sys.exit(f"Error: tree '{tree_name}' not found in '{input_file}'")

    total = tree.GetEntries()
    print(f"Total entries in '{tree_name}': {total}")

    # Part 1: first n_first entries
    n1 = min(n_first, total)
    f1 = ROOT.TFile.Open(out1, "RECREATE")
    t1 = tree.CloneTree(n1)               # clones entries [0..n1-1]
    f1.WriteTObject(t1, tree_name)
    f1.Close()
    print(f"Wrote {n1} entries to '{out1}'")

    # Part 2: the rest
    if total > n_first:
        remaining = total - n_first
        f2 = ROOT.TFile.Open(out2, "RECREATE")
        t2 = tree.CloneTree(0)            # same branches, 0 entries
        for idx in range(n_first, total):
            tree.GetEntry(idx)
            t2.Fill()
            if (idx - n_first + 1) % 1_000_000 == 0:
                done = idx - n_first + 1
                print(f"  filled {done}/{remaining} entries into '{out2}'")
        f2.WriteTObject(t2, tree_name)
        f2.Close()
        print(f"Wrote remaining {remaining} entries to '{out2}'")
    else:
        print("No remaining entries; skipped second file.")

    f_in.Close()


def main():
    p = argparse.ArgumentParser(
        description="Split a ROOT TTree into two files by entry count"
    )
    p.add_argument("--input",  "-i",
                   default="/eos/cms/store/group/phys_egamma/ReleaseInputsArchive/2018UL_ElePhoReg/input_trees/DoubleElectron_FlatPt-1To300_2018ConditionsFlatPU0to70ECALGT_105X_upgrade2018_realistic_IdealEcalIC_v4-v1_AODSIM_EgRegTreeV5Refined.root",
                   help="Input ROOT file (default: input.root)")
    p.add_argument("--tree",   "-t",
                   default="egRegTree",
                   help="Name of the TTree to split (default: egRegTree)")
    p.add_argument("--split",  "-n", type=int,
                   default=10_000_000,
                   help="Number of entries in the first output file (default: 10000000)")
    p.add_argument("--out1",   "-1",
                   default="/eos/user/e/eldesant/RegTrainingInput/train.root",
                   help="Filename for the first part (default: train.root)")
    p.add_argument("--out2",   "-2",
                   default="/eos/user/e/eldesant/RegTrainingInput/test.root",
                   help="Filename for the second part (default: test.root)")
    args = p.parse_args()

    split_tree(args.input, args.tree, args.split, args.out1, args.out2)


if __name__ == "__main__":
    main()

