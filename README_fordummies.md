export SCRAM_ARCH=el9_amd64_gcc12
cmsrel CMSSW_14_0_0
cd CMSSW_14_0_0/src
cmsenv

poi fuori dalla release clona il branch 140X della repo

cd EgRegresTrainerLegacy 
gmake RegressionTrainerExe -j 8
gmake RegressionApplierExe -j 8
export PATH=$PATH:./bin/$SCRAM_ARCH  #controllare che PATH finisca con il nome dell'architettura el9_amd64_gcc12
export PYTHON27PATH=$PYTHON27PATH:python (potrebbe essere PYTHONPATH invece di PYTHON27)

2to3 -w scripts/runEleRegTrainings.py 
2to3 -w python

All'inizio di scripts/runEleRegTrainings.py cambiare #!/usr/bin/env python con #!/usr/bin/env python3

Ora aprire python/regtools.py e cambiare il nome dell'architettura in el9_amd64_gcc12 (compare 3 volte), fare lo stesso per scripts/runEleRegTrainings.py 

eseguire lo script con:
python3 scripts/runEleRegTrainings.py --era 2018 


