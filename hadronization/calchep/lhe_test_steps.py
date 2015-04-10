#!/bin/env python

import subprocess
import multiprocessing
import time
import os

Target = '/disk1/erdweg/MC_production/results/'
N_events = 90 # 90

file_list_0 = [
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl200.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl300.lhe'
]

file_list_1 = [
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl200.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl300.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl400.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl600.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl700.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl800.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl900.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl1000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl1200.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl1400.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl1600.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl1800.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl2000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl2500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl3000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE01_LQD01-MSnl3000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl3500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE01_LQD01-MSnl3500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl4000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE01_LQD01-MSnl4000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl4500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl5000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl5500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl6000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE001_LQD001-MSnl6500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE02_LQD02-MSnl4000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE02_LQD02-MSnl4500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE02_LQD02-MSnl5000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE02_LQD02-MSnl5500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE02_LQD02-MSnl6000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE02_LQD02-MSnl6500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE005_LQD005-MSnl2000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE005_LQD005-MSnl2500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE005_LQD005-MSnl3000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE05_LQD05-MSnl4000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE05_LQD05-MSnl4500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE05_LQD05-MSnl5000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE05_LQD05-MSnl5500.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE05_LQD05-MSnl6000.lhe',
'lhes/emu/xsec_emu_ddbar_resonance_LLE05_LQD05-MSnl6500.lhe'
]

file_list_2 = [
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL500.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL1000.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL1500.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL2000.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL2500.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL3000.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL3500.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL4000.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL4500.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL5000.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL5500.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL6000.lhe',
'lhes/QBH_emu/CalcHEP_n_0_PDG/QBH_n0_ADD_Mth-MPL6500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL1000.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL1500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL2000.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL2500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL3000.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL3500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL4000.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL4500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL5000.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL5500.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL6000.lhe',
'lhes/QBH_emu/CalcHEP_n_1_RS/QBH_n1_RS_Mth-MPL6500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL1000.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL1500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL2000.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL2500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL3000.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL3500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL4000.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL4500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL5000.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL5500.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL6000.lhe',
'lhes/QBH_emu/CalcHEP_n_4_PDG/QBH_n4_ADD_Mth-MPL6500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL1000.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL1500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL2000.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL2500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL3000.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL3500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL4000.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL4500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL5000.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL5500.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL6000.lhe',
'lhes/QBH_emu/CalcHEP_n_5_PDG/QBH_n5_ADD_Mth-MPL6500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL1000.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL1500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL2000.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL2500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL3000.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL3500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL4000.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL4500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL5000.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL5500.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL6000.lhe',
'lhes/QBH_emu/CalcHEP_n_6_PDG/QBH_n6_ADD_Mth-MPL6500.lhe'
]

def run_lhe_test_job(number):
    print('starting with number %s'%number)

    number = number.replace('.lhe','')

    cmd = 'cmsDriver.py step1 --filein file:%s.lhe --fileout file:step0_%s.root --mc --eventcontent LHE --datatier GEN --conditions PHYS14_25_V1 --step NONE --python_filename step0_%s_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10000'%(number,number.replace('/',''),number.replace('/',''))

    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    cmd = 'cmsRun -e -j step0_%s.xml step0_%s_cfg.py'%(number.replace('/',''),number.replace('/',''))

    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    step_0_cpu = 0.
    step_0_siz = 0.

    for line in open("step0_%s.xml"%number.replace('/','')):
        if "AvgEventCPU" in line:
            step_0_cpu = float(line.split('\"')[3])
        if "Timing-tstoragefile-write-totalMegabytes" in line:
            step_0_siz = float(line.split('\"')[3])/10000*1000

    cmd = 'cmsDriver.py Configuration/GenProduction/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py --filein file:step0_%s.root --fileout file:step1_%s.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions PHYS14_25_V1 --step GEN,SIM --python_filename step1_%s_cfg.py --magField 38T_PostLS1 --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --no_exec -n %i'%(number.replace('/',''),number.replace('/',''),number.replace('/',''),N_events)

    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    cmd = 'cmsRun -e -j step1_%s.xml step1_%s_cfg.py'%(number.replace('/',''),number.replace('/',''))

    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    step_1_cpu = 0.
    step_1_siz = 0.

    for line in open("step1_%s.xml"%number.replace('/','')):
        if "AvgEventCPU" in line:
            step_1_cpu = float(line.split('\"')[3])
        if "Timing-tstoragefile-write-totalMegabytes" in line:
            step_1_siz = float(line.split('\"')[3])/N_events*1000

    print('done with number %s'%number)
    print('AvgCPU step0 : %f s/Evt'%step_0_cpu)
    print('AvgSiz step0 : %f kB/Evt'%step_0_siz)
    print('AvgCPU step1 : %f s/Evt'%step_1_cpu)
    print('AvgSiz step1 : %f kB/Evt'%step_1_siz)

    ofile = open('out_numbers_%s.txt'%number.replace('/',''),'w')
    ofile.write('%f %f %f %f'%(step_0_cpu, step_0_siz, step_1_cpu, step_1_siz))
    ofile.close()

def collect_infos_from_txt_file(file_list, ofile_name):
    step_0_cpu = []
    step_0_siz = []
    step_1_cpu = []
    step_1_siz = []
    file_names = []

    for item in file_list:
        item = item.replace('.lhe','')
        for line in open("out_numbers_%s.txt"%item.replace('/','')):
            dummy = line.split(' ')
            step_0_cpu.append(float(dummy[0]))
            step_0_siz.append(float(dummy[1]))
            step_1_cpu.append(float(dummy[2]))
            step_1_siz.append(float(dummy[3]))
            file_names.append(item.replace('/',''))

    ofile = open(ofile_name,'w')
    ofile.write('sample  AvgCPU / Evt (s)  AvgSize / Evt (kB)\n')
    for i in range(len(file_names)):
        ofile.write('%s: %f %f\n'%(file_names[i], step_0_cpu[i] + step_1_cpu[i], step_0_siz[i] + step_1_siz[i]))
    ofile.close()

# for item in file_list_0:
    # run_lhe_test_job(item)
    # raw_input('bla')

pool = multiprocessing.Pool(5)
pool.map_async(run_lhe_test_job, file_list_1)
while True:
    time.sleep(1)
    if not pool._cache: break
pool.close()
pool.join()

collect_infos_from_txt_file(file_list_1,'emu_res.txt')

pool = multiprocessing.Pool(5)
pool.map_async(run_lhe_test_job, file_list_2)
while True:
    time.sleep(1)
    if not pool._cache: break
pool.close()
pool.join()

collect_infos_from_txt_file(file_list_2,'QBH_res.txt')

print('everything done')
