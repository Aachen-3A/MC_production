#!/bin/env python

import subprocess
import multiprocessing
import time
import os

Target = '/disk1/erdweg/MC_production/results/'
N_events = 10000

def ls():
    p = subprocess.Popen('pwd',shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)

    p = subprocess.Popen('ls -l',shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)

def run_lhe_production_job(number):
    print('starting with number %i'%number)

    if not os.path.isdir( 'temp_%i'%number ):
        os.mkdir('temp_%i'%number)

    os.chdir('temp_%i'%number)

    ls()

    p = subprocess.Popen('tar xvzf /disk1/erdweg/MC_production/CMSSW_7_2_3_patch1/src/WW_llnunu_NNPDF30_13TeV_semi_tarball.tar.gz',shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    ls()

    seed = 52064 + number

    p = subprocess.Popen('./runcmsgrid.sh %i %i 1'%(N_events, seed),shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    ls()

    p = subprocess.Popen('mv cmsgrid_final.lhe %s/cmsgrid_final_%i.lhe'%(Target, number),shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    os.chdir('..')

    ls()

    p = subprocess.Popen('rm -rf temp_%i'%number,shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    print('done with number %i'%number)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31 ,32, 33,
           34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
           50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]

# for item in numbers:
    # run_lhe_production_job(item)

pool = multiprocessing.Pool(5)
pool.map_async(run_lhe_production_job, numbers)
while True:
    time.sleep(1)
    if not pool._cache: break
pool.close()
pool.join()

print('everything done')
