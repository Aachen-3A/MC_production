#!/bin/env python
from gridFunctions import getdcachelist
from string import Template
import shutil
import os


samples=[
"RPVresonantToEMu_M-6000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8"]

for sample in samples:

    os.makedirs(sample)

    folder="/serdweg/MC/RPVresonantToEMu_M-6000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8/"
    file_lists = getdcachelist( folder, sample,mem_limit = 500000000,fileXtension=".root" )
    print('creating ' + str(len(file_lists)) + ' cfg files')

    for j in range(len(file_lists)):
        print('cfg file ' + str(j) + ' will run over ' + str(len(file_lists[j])) + ' files')
        for i in range(len(file_lists[j])):
            file_lists[j][i]=file_lists[j][i].replace("dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms","")
        iutput=str(file_lists[j]).replace("[","").replace("]","")
        # print file_lists
        # print(sample)
        # raw_input("bla")

        d = dict(
            name='%s_%i'%(sample,j),
            datapath='pritvate',
            INPUT='%s'%(iutput),
        )

        file=open("mc_SP14_miniAOD_template_cfg.py","r")
        text=file.read()
        file.close()
        newText=Template(text).safe_substitute(d)
        fileNew=open("mc_SP14_miniAOD_%s_%i_cfg.py"%(sample,j),"w+")
        fileNew.write(newText)
        fileNew.close()

        shutil.move("mc_SP14_miniAOD_%s_%i_cfg.py"%(sample,j),sample+"/")
