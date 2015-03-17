#!/usr/bin/env python

## @package music_crab3
# MUSiC wrapper for crab3
#
# music_crab is a wrapper script that has been developed
# to submit the large number of tasks (more or less) automatically, 
# needed to get all data and MC. The script automatically creates CRAB 
# config files according to the dataset file provided. 
# crab3 rebuilds the previous crab2 functionality and relies on the work
# in the previous version
# @author Tobias Pook

import datetime
import os, csv
import sys
import time
import re
import logging
import optparse
import glob
import subprocess
import imp
import pickle
import fnmatch
import argparse

#custom libs
import aix3adb
from  aix3adb import Aix3adbException
#~ import dbutilscms

parser = argparse.ArgumentParser(description='Submit sample & skim info from csv to aix3adb')
msg = 'CSV file which contains the sample & skim information'
parser.add_argument('csvfile', help=msg)
msg = 'The user name under which the task is stored on SE (e.g. DCache) '
parser.add_argument('--user', default = None , help=msg)
args = parser.parse_args()

if args.user is None:
    import crabFunctions
    con = crabFunctions.CrabControllercontroller()
    user = con.checkusername()
else:
    user = args.user

# some general definitions
COMMENT_CHAR = '#'
log_choices = [ 'ERROR', 'WARNING', 'INFO', 'DEBUG' ]
date = '%F %H:%M:%S'

# Write everything into a log file in the directory you are submitting from.
log = logging.getLogger( 'csv2aix3adb' )

def createDBlink():
    
    # Create a database object.
    dblink = aix3adb.aix3adb()

    # Authorize to database.
    log.info( "Connecting to database: 'http://cern.ch/aix3adb'" )
    dblink.authorize(username = user)
    log.info( 'Authorized to database.' )
    return dblink

def main():
    
    dblink = createDBlink()
    
    runOnMC = True
    runOnData = False
    outdict = {}
    playlistdict = {}
    scalesdict = {}
    with open( args.csvfile , 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        for ind, row in enumerate(spamreader):
            if ind < 1:
                continue
            samplename, datasetpath, generator, xs, filter_effi, filter_effi_ref, kfactor, kfactor_ref, energy, globalTag, CMSSW_Version, numEvents = row
            log.info( 'Adding sample ' + samplename + ' to aix3adb')
            # check which kind of sample to submit  
            if runOnMC:
                newSample = False
                # try to get sample db entry and create it otherwise
                try:
                    dbSample = dblink.getMCSample( samplename )
                except Aix3adbException:
                    dbSample = aix3adb.MCSample()
                    newSample = True

                dbSample.datasetpath = datasetpath 
                dbSample.name = samplename 
                dbSample.datasetpath= datasetpath 
                dbSample.generator = generator
                dbSample.crosssection = float( xs )
                dbSample.filterefficiency = float(filter_effi)
                dbSample.filterefficiency_reference = filter_effi_ref
                dbSample.kfactor = kfactor
                dbSample.kfactor_reference  = kfactor_ref
                dbSample.crosssection_reference = 'McM'
                dbSample.energy = energy
                # change sample on
                if newSample:
                    dbSample = dblink.insertMCSample(dbSample)
                else:
                    dblink.editMCSample( dbSample)
                # create a new McSkim object
                mcSkim = aix3adb.MCSkim()
                # create relation to dbsample object
                mcSkim.sampleid = dbSample.id
                mcSkim.owner = user
                mcSkim.is_created = 1
                mcSkim.datasetpath= datasetpath 
                now = datetime.datetime.now()
                mcSkim.created_at = now.strftime( "%Y-%m-%d %H:%M:%S" )
                # where to get the skimmer name ??? MUSiCSkimmer fixed
                mcSkim.skimmer_name = "MUSiCSkimmer"
                mcSkim.skimmer_cmssw = CMSSW_Version
                mcSkim.skimmer_globaltag = globalTag
                mcSkim.nevents = numEvents
                dblink.insertMCSkim( mcSkim )
        
if __name__ == '__main__':
    main()


