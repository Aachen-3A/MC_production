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



def makeExe(user):
    from string import Template
    exe="""
echo Copying pack...

mkdir -p CMSSW_7_0_6_patch1/src/A/A/data/

name=$1
file=$2
echo $name
echo $file

sed -i "s/PROC_NAME/$name/g" Wprime-Phys14DR_cfg.py
sed -i "s/File_NAME/$file/g" Wprime-Phys14DR_cfg.py

cat Wprime-Phys14DR_cfg.py
cmsRun Wprime-Phys14DR_cfg.py


outfileName="$file"


uberftp grid-ftp.physik.rwth-aachen.de mkdir "/pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName"

#uberftp grid-ftp.physik.rwth-aachen.de rm /pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName
#lcg-cp file:///`pwd`/DM_out.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName
uberftp grid-ftp.physik.rwth-aachen.de "mkdir /pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName"

#uberftp grid-ftp.physik.rwth-aachen.de rm /pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName
#lcg-cp file:///`pwd`/DM_out.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName


uberftp grid-ftp.physik.rwth-aachen.de "rm /pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName"
#Try 10 times to copy the pack file with help of srmcp.
success=false
for i in {1..10}; do
   if lcg-cp file:///`pwd`/DM_out.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName; then
      success=true
      break
   fi
done
if ! $success; then
   echo Copying of pack file \\\'lcg-cp file:///`pwd`/test.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/padeken/MC/miniAOD/$name/$outfileName\\\' failed! 1>&2
   echo Did you forget to \\\'remix --copy\\\'? 1>&2
fi


"""

    exeFile=open("runtemp.sh","w+")
    exeFile.write(exe)
    exeFile.close()

def handle_LHEs(options, args):
    print('working with lhe file: %s'%args[0])

    if not os.path.exists('dummy_lhes/'):
        os.makedirs('dummy_lhes')

    cmd1 = "../../splitLHE.py"
    cmd2 = "--Nevents=%s"% (options.events)
    cmd3 = "%s"% (args[0])
    command = [cmd1,cmd2,cmd3]
    print " ".join(command)
    subprocess.call(command)

    thisdir=os.getcwd()
    filelist = os.listdir(thisdir)
    lhe_file_list = []
    for item in filelist:
        if '.lhe' in item:
            lhe_file_list.append(item)
    for item in lhe_file_list:
        os.rename(item, 'dummy_lhes/'+item)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","rm /pnfs/physik.rwth-aachen.de/cms/store/user/serdweg/MC/*"]

    subprocess.call(mdir)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","rmdir /pnfs/physik.rwth-aachen.de/cms/store/user/serdweg/MC"]

    subprocess.call(mdir)

    mdir=["uberftp","grid-ftp.physik.rwth-aachen.de","mkdir /pnfs/physik.rwth-aachen.de/cms/store/user/serdweg/MC/"]

    subprocess.call(mdir)

    update_progress(0)
    counter = 0
    for file in lhe_file_list:
        path = "srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/serdweg/MC/"
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

    return lhe_file_list

def main():

    date_time = datetime.now()
    usage = '%prog [options] LHE_FILE HADRONIZER_FILE'
    parser = optparse.OptionParser( usage = usage )
    parser.add_option( '-u', '--user', default = os.getenv( 'LOGNAME' ),
                            help = 'which user on dcache [default = %s]'%(os.getenv( 'LOGNAME' )))
    parser.add_option( '-o', '--Output', default = 'output/',
                            help = 'Define the output directory. [default = %default]')
    parser.add_option( '-f', '--force', default = "force the output to overwrite", metavar = 'DIRECTORY',
                            help = 'Define the output directory. [default = %default]')
    parser.add_option( '--debug', metavar = 'LEVEL', default = 'INFO',
                       help= 'Set the debug level. Allowed values: ERROR, WARNING, INFO, DEBUG. [default = %default]' )
    parser.add_option( '--events', default = 100,
                       help = 'Number of events that should be hadronized per job. [default = %default]')

    ( options, args ) = parser.parse_args()
    if len( args ) != 2:
        parser.error( 'Exactly two CONFIG_FILE required!' )
        sys.exit(42)

    format = '%(levelname)s from %(name)s at %(asctime)s: %(message)s'
    date = '%F %H:%M:%S'
    logging.basicConfig( level = logging._levelNames[ options.debug ], format = format, datefmt = date )

    try:
       cmssw_version, cmssw_base, scram_arch, music_path = checkEnvironment.checkEnvironment()
       print(cmssw_version, cmssw_base, scram_arch, music_path)
    except EnvironmentError, err:
        log.error( err )
        log.info( 'Exiting...' )
        sys.exit( err.errno )

    lhe_file_list = handle_LHEs(options, args)

    # makeExe(options.user)
# 
    # thisdir=os.getcwd()
    # if os.path.exists(options.Output) or not options.force:
        # log.error("The outpath "+options.Output+" already exists pick a new one or use --force")
        # sys.exit(3)
    # else:
        # os.makedirs(options.Output)
    # shutil.copyfile(thisdir+"/runtemp.sh",options.Output+"/runtemp.sh")
    # os.remove(thisdir+"/runtemp.sh")
# 
    # for sample in sampleList:
        # task=cesubmit.Task(sample,options.Output+"/"+sample,scramArch=scram_arch, cmsswVersion=cmssw_version)
# 
        # task.executable=options.Output+"/runtemp.sh"
        # task.inputfiles=[thisdir+"/Wprime-Phys14DR_cfg.py"]
        # #task.outputfiles=[""]
# 
# 
        # standardArg=[sample]
# 
        # for f in sampleList[sample]:
            # job=cesubmit.Job()
            # job.arguments=standardArg+[f]
            # task.addJob(job)
        # log.info("start submitting "+sample)
        # task.submit(6)


    log.info("Thanks for zapping in, bye bye")
    log.info("The out files will be in "+options.Output)



if __name__ == '__main__':
    main()
    
