
echo Copying pack...

user=$1
tag=$2
outfolderName=$3
file=$4
outfileName=${file/".lhe"/".root"}
echo $outfileName
echo $file

uberftp grid-ftp.physik.rwth-aachen.de "cd /pnfs/physik.rwth-aachen.de/cms/store/user/$user/MC/RPVresonantToEMu_M-4000_LLE_LQD_05_TuneCUETP8M1_13TeV-calchep-pythia8; get $file"

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
   echo Copying of pack file \'srmcp file:///`pwd`/miniAOD-prod_PAT.root srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/$user/MC/$outfolderName/$outfileName\' failed! 1>&2
fi

rm miniAOD-prod_PAT.root

