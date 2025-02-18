#!/bin/bash
# To setup PanDA at USDF: source setup_lsst_panda.sh w_2023_38
# If using PanDA at CERN: source setup_lsst_panda.sh w_2023_38 cern

latest=$(ls -td /cvmfs/sw.lsst.eu/almalinux-x86_64/panda_env/v* | head -1)

weekly=$1
panda_ins=$2

if [ "$panda_ins" == "cern" ]; then
   setupScript=${latest}/setup_panda_cern.sh
   echo "Submission to PanDA at: " $panda_ins
else
   setupScript=${latest}/setup_panda_usdf.sh
fi

source ${latest}/setup_lsst.sh $weekly
echo "setup from:" $setupScript
source $setupScript
