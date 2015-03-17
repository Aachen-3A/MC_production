#!/bin/env python

import sys
import os
import cesubmit
#from listFiles import getdcachelist
# import binConfig
import checkEnvironment
from datetime import datetime
import optparse,os,time,cPickle,subprocess,shutil,sys
import logging
log = logging.getLogger( 'remote' )
from terminalFunctions import update_progress



def makeExe():
    from string import Template
    exe="""
echo Copying pack...

user=$1
tag=$2
outfolderName=$3
file=$4
outfileName=${file/".lhe"/".root"}
echo $outfileName
echo $file

uberftp grid-ftp.physik.rwth-aachen.de "cd /pnfs/physik.rwth-aachen.de/cms/store/user/$user/MC; get $file"

ls -l

sed -i "s/File_NAME/$file/g" hadronizer_match_pu_2_cfg.py

cat hadronizer_match_pu_2_cfg.py
cmsRun hadronizer_match_pu_2_cfg.py

ls -l

cmsRun miniAOD-prod_PAT.py

ls -l

rm test.root

ls -l

#Try 10 times to copy the pack file with help of srmcp.
success=false
for i in {1..10}; do
   if srmcp -debug file:///`pwd`/miniAOD-prod_PAT.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/$user/MC/$outfolderName/$outfileName; then
      success=true
      break
   fi
done

if ! $success; then
   echo Copying of pack file \\\'srmcp file:///`pwd`/miniAOD-prod_PAT.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/$user/MC/$outfolderName/$outfileName\\\' failed! 1>&2
fi

rm miniAOD-prod_PAT.root

"""

    thisdir=os.getcwd()
    exeFile=open(thisdir+"/output/runtemp.sh","w+")
    exeFile.write(exe)
    exeFile.close()


def handle_LHEs(options, args):
    log.info('working with lhe file: %s'%args[0])

    if not os.path.exists('dummy_lhes/'):
        os.makedirs('dummy_lhes')

    cmd1 = "../../splitLHE.py"
    cmd2 = "--Nevents=%s"% (options.events)
    cmd3 = "%s"% (args[0])
    command = [cmd1,cmd2,cmd3]
    log.info( " ".join(command))
    subprocess.call(command)

    thisdir=os.getcwd()
    filelist = os.listdir(thisdir)
    lhe_file_list = []
    for item in filelist:
        if '.lhe' in item:
            lhe_file_list.append(item)
    for item in lhe_file_list:
        os.rename(item, 'dummy_lhes/'+item)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","rm /pnfs/physik.rwth-aachen.de/cms/store/user/%s/MC/*"%options.user]

    subprocess.call(mdir)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","rmdir /pnfs/physik.rwth-aachen.de/cms/store/user/%s/MC"%options.user]

    subprocess.call(mdir)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","mkdir /pnfs/physik.rwth-aachen.de/cms/store/user/%s/MC/"%options.user]

    subprocess.call(mdir)

    log.info( ' ' )
    log.info( ' Now starting to copy the LHEs to the dcache' )
    log.info( ' ' )

    update_progress(0)
    counter = 0
    for file in lhe_file_list:
        path = "srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/%s/MC/"%options.user
        cmd1 = "srmcp"
        cmd2 = "file:///%s/%s"% (thisdir+"/dummy_lhes",file)
        cmd3 = "%s%s"% (path,file)
        command = [cmd1,cmd2,cmd3]
        subprocess.call(command)
        counter += 1
        update_progress(float(counter)/float(len(lhe_file_list)))

    cmd1 = "rm"
    cmd2 = "-r"
    cmd3 = "dummy_lhes/"
    command = [cmd1,cmd2,cmd3]
    subprocess.call(command)

    log.info( ' ' )
    log.info( ' done with the moving' )
    log.info( ' ' )

    return lhe_file_list

def main():

    date_time = datetime.now()
    usage = '%prog [options] LHE_FILE HADRONIZER_FILE'
    parser = optparse.OptionParser( usage = usage )
    parser.add_option( '-u', '--user', default = os.getenv( 'LOGNAME' ),
                            help = 'which user on dcache [default = %s]'%(os.getenv( 'LOGNAME' )))
    parser.add_option( '-o', '--Output', default = 'test_run/',
                            help = 'Define the output directory. [default = %default]')
    parser.add_option( '-f', '--force', default = "force the output to overwrite", metavar = 'DIRECTORY',
                            help = 'Define the output directory. [default = %default]')
    parser.add_option( '--debug', metavar = 'LEVEL', default = 'INFO',
                       help= 'Set the debug level. Allowed values: ERROR, WARNING, INFO, DEBUG. [default = %default]' )
    parser.add_option( '--events', default = 100,
                       help = 'Number of events that should be hadronized per job. [default = %default]')
    parser.add_option( '-t', '--Tag', default = "%s-%s-%s"%(date_time.year,
                                                            date_time.month,
                                                            date_time.day), metavar = 'DIRECTORY',
                        help = 'Define a Tag for the output directory. [default = %default]' )

    ( options, args ) = parser.parse_args()
    if len( args ) != 2:
        parser.error( 'Exactly two CONFIG_FILE required!' )
        sys.exit(42)

    format = '%(levelname)s from %(name)s at %(asctime)s: %(message)s'
    date = '%F %H:%M:%S'
    logging.basicConfig( level = logging._levelNames[ options.debug ], format = format, datefmt = date )

    try:
       music_path, cmssw_version, cmssw_base, scram_arch = checkEnvironment.checkEnvironment()
    except EnvironmentError, err:
        log.error( err )
        log.info( 'Exiting...' )
        sys.exit( err.errno )

    lhe_file_list = handle_LHEs(options, args)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","mkdir /pnfs/physik.rwth-aachen.de/cms/store/user/%s/MC/%s"%(options.user,options.Output)]

    subprocess.call(mdir)

    thisdir=os.getcwd()

    if not os.path.exists(thisdir+'/output'):
        os.makedirs(thisdir+'/output')

    makeExe()

    task=cesubmit.Task('LHE_hadronization',scramArch=scram_arch, cmsswVersion=cmssw_version)

    task.executable=thisdir+"/output/runtemp.sh"
    task.inputfiles=[thisdir+"/hadronizer_match_pu_2_cfg.py", thisdir+"/miniAOD-prod_PAT.py"]

    standardArg=[options.user,options.Tag,options.Output]

    for f in lhe_file_list:
        job=cesubmit.Job()
        job.arguments=standardArg+[f]
        task.addJob(job)

    task.submit(6)

    log.info("Thanks for zapping in, bye bye")
    log.info("The out files will be in "+thisdir+'/output')

if __name__ == '__main__':
    main()
