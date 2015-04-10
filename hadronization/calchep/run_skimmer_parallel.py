#!/bin/env python

import subprocess
import multiprocessing
import time
import os
import glob

Target = 'RPVresonantToEMu_M-6000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8'
User = 'serdweg'
DateTag = '2015-04-08'

def ls():
    liste = glob.glob(Target+'/*.py')
    return liste

def run_skimmer_job(cfg_name):
    job_number = int(cfg_name.split('_')[-2])

    print('starting with cfg number %i'%job_number)

    p = subprocess.Popen('cmsRun %s'%cfg_name,shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    thisdir=os.getcwd()

    file = 'RPVresonantToEMu_M-6000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8_%i.pxlio'%job_number

    path = "srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/%s/MUSiC/%s/%s/"%(User,DateTag,Target)
    cmd1 = "srmcp"
    cmd2 = "file:///%s/%s"% (thisdir,file)
    cmd3 = "%s%s"% (path,file)
    command = [cmd1,cmd2,cmd3]
    subprocess.call(command)

    p = subprocess.Popen('rm %s'%file,shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    print('done with number %i'%job_number)


liste = ls()

mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","mkdir /pnfs/physik.rwth-aachen.de/cms/store/user/%s/MUSiC/%s"%(User,DateTag)]

subprocess.call(mdir)

mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","mkdir /pnfs/physik.rwth-aachen.de/cms/store/user/%s/MUSiC/%s/%s"%(User,DateTag,Target)]

subprocess.call(mdir)

# for item in liste:
    # run_skimmer_job(item)

pool = multiprocessing.Pool(4)
pool.map_async(run_skimmer_job, liste)
while True:
    time.sleep(1)
    if not pool._cache: break
pool.close()
pool.join()

print('everything done')
