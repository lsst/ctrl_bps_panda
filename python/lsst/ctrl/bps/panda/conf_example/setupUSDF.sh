#!/bin/bash
# setup Rubin env
export LSST_VERSION=w_2025_07
source /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/${LSST_VERSION}/loadLSST.bash
setup lsst_distrib

# setup PanDA env. Will be a simple step when the deployment of PanDA is fully done.
export PANDA_CONFIG_ROOT=$HOME/.panda
export PANDA_URL_SSL=https://usdf-panda-server.slac.stanford.edu:8443/server/panda
export PANDA_URL=https://usdf-panda-server.slac.stanford.edu:8443/server/panda
export PANDACACHE_URL=$PANDA_URL_SSL
export PANDAMON_URL=https://usdf-panda-bigmon.slac.stanford.edu:8443/
export PANDA_AUTH=oidc
export PANDA_VERIFY_HOST=off
export PANDA_AUTH_VO=Rubin

export PANDA_BEHIND_REAL_LB=true


# IDDS_CONFIG path depends on the weekly version
export PANDA_SYS=$CONDA_PREFIX
export IDDS_CONFIG=${PANDA_SYS}/etc/idds/idds.cfg.client.template

export IDDS_MAX_NAME_LENGTH=30000

# WMS plugin
export BPS_WMS_SERVICE_CLASS=lsst.ctrl.bps.panda.PanDAService
