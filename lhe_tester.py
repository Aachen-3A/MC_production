#!/bin/env python

from lheanalyzer import *
from rootpy.plotting import Hist

# lhe_file = LHEAnalysis('/disk1/erdweg/MC_production/results/merged.lhe')
# lhe_file = LHEAnalysis('/disk1/erdweg/MC_production/results/cmsgrid_final_0.lhe')
lhe_file = LHEAnalysis('/disk1/erdweg/MC_production/WW_powheg_leptonic/merged.lhe')

for item in lhe_file.processes:
    print('process:')
    print(item.id)
    print('cross section:')
    print(str(item.crossSection) + ' +- ' + str(item.crossSectionUncertainty))

print(' ')

w_plus_hist_pT = Hist(1000, 0, 200, name = 'w_plus_hist_pT')
w_plus_hist_phi = Hist(65, -3.5, 3.5, name = 'w_plus_hist_phi')
w_plus_hist_eta = Hist(100, -5, 5, name = 'w_plus_hist_eta')
w_plus_hist_decays = Hist(4, 0, 4, name = 'w_plus_hist_decays')

w_minus_hist_pT = Hist(1000, 0, 200, name = 'w_minus_hist_pT')
w_minus_hist_phi = Hist(65, -3.5, 3.5, name = 'w_minus_hist_phi')
w_minus_hist_eta = Hist(100, -5, 5, name = 'w_minus_hist_eta')
w_minus_hist_decays = Hist(4, 0, 4, name = 'w_minus_hist_decays')

while(True):
    try:
        event = lhe_file.next()
    except(StopIteration):
        break
    plus_number = -1
    minus_number = -1
    counter = 1
    # print(10*'-')
    for part in event.particles:
        # print(counter, part.pdgId, part.mother[0], part.mother[1])
        if(part.pdgId == 24):
            w_plus_hist_pT.Fill(part.pt)
            w_plus_hist_phi.Fill(part.phi)
            w_plus_hist_eta.Fill(part.eta)
            plus_number = counter
            # print(plus_number)
        if(part.mother[0] == plus_number):
            # print('found plus')
            if(part.pdgId == 11 or part.pdgId == -11):
                w_plus_hist_decays.Fill(0.5)
            elif(part.pdgId == 13 or part.pdgId == -13):
                w_plus_hist_decays.Fill(1.5)
            elif(part.pdgId == 15 or part.pdgId == -15):
                w_plus_hist_decays.Fill(2.5)
            elif(part.pdgId == 12 or part.pdgId == -12 or part.pdgId == 14 or part.pdgId == -14 or part.pdgId == 16 or part.pdgId == -16):
                continue
            else:
                print(counter, part.pdgId, part.mother[0], part.mother[1])
                w_plus_hist_decays.Fill(3.5)
        if(part.pdgId == -24):
            w_minus_hist_pT.Fill(part.pt)
            w_minus_hist_phi.Fill(part.phi)
            w_minus_hist_eta.Fill(part.eta)
            minus_number = counter
            # print(minus_number)
        if(part.mother[0] == minus_number):
            # print('found minus')
            if(part.pdgId == 11 or part.pdgId == -11):
                w_minus_hist_decays.Fill(0.5)
            elif(part.pdgId == 13 or part.pdgId == -13):
                w_minus_hist_decays.Fill(1.5)
            elif(part.pdgId == 15 or part.pdgId == -15):
                w_minus_hist_decays.Fill(2.5)
            elif(part.pdgId == 12 or part.pdgId == -12 or part.pdgId == 14 or part.pdgId == -14 or part.pdgId == 16 or part.pdgId == -16):
                continue
            else:
                print(counter, part.pdgId, part.mother[0], part.mother[1])
                w_minus_hist_decays.Fill(3.5)
        counter += 1

hist_list = [w_plus_hist_pT, w_plus_hist_phi, w_plus_hist_eta, w_plus_hist_decays, w_minus_hist_pT, w_minus_hist_phi, w_minus_hist_eta, w_minus_hist_decays]

from DukePlotALot import *

for hist in hist_list:
    hist_style = sc.style_container(style = 'CMS', useRoot = False, cms=13, lumi=19700)
    hist_style.Set_additional_text('Powheg simulation')

    hist.SetFillColor('y')
    hist.SetFillStyle('solid')

    test = plotter(sig=[hist],style=hist_style)
    test.Set_axis(ymin=1e2,ymax=1e6)
    test.make_plot('plots/%s.pdf'%hist.GetName())
    
