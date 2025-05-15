# Adapt the code to an el9 architecture (releases >CMSSW_14_X_X)

`export SCRAM_ARCH=el9_amd64_gcc12`

`cmsrel CMSSW_14_0_0`

`cd CMSSW_14_0_0/src`

`cmsenv`

### then clone the branch 140X out of the release and write the following commands:

`cd EgRegresTrainerLegacy`

`gmake RegressionTrainerExe -j 8`

`gmake RegressionApplierExe -j 8`

`export PATH=$PATH:./bin/$SCRAM_ARCH  #check that PATH ends with arch. name el9_amd64_gcc12`

`export PYTHON27PATH=$PYTHON27PATH:python #(could be PYTHONPATH instead of PYTHON27)`

### Convert the scripts to python3 syntax
`2to3 -w scripts/runEleRegTrainings.py` 
`2to3 -w python`

At the top of scripts/runEleRegTrainings.py change #!/usr/bin/env python with #!/usr/bin/env python3

Now open python/regtools.py and change the architecture name to el9_amd64_gcc12 do the same for  scripts/runEleRegTrainings.py 

## Run the script with:
`python3 scripts/runEleRegTrainings.py --era 2018 `


