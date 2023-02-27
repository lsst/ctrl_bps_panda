#!/usr/bin/python
"""
This file is needed to decode the command line string sent from the BPS
plugin -> PanDA -> Edge node cluster management
-> Edge node -> Container. This file is not a part
of the BPS but a part of the payload wrapper.
It decodes the hexified command line.
"""
import os
import re
import sys

# import base64
import datetime
import tarfile

import logging

from lsst.utils.timer import time_this

from lsst.ctrl.bps.constants import DEFAULT_MEM_UNIT, DEFAULT_MEM_FMT

from lsst.resources import ResourcePath
from lsst.ctrl.bps.drivers import prepare_driver


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s\t%(threadName)s\t%(name)s\t%(levelname)s\t%(message)s')

_LOG = logging.getLogger(__name__)


def download_extract_archive(filename):
    archive_basename = os.path.basename(filename)
    target_dir = os.getcwd()
    full_output_filename = os.path.join(target_dir, archive_basename)

    if filename.startswith("https:"):
        panda_cache_url = os.path.dirname(os.path.dirname(filename))
        os.environ["PANDACACHE_URL"] = panda_cache_url
    elif "PANDACACHE_URL" not in os.environ and "PANDA_URL_SSL" in os.environ:
        os.environ["PANDACACHE_URL"] = os.environ["PANDA_URL_SSL"]
    print("PANDACACHE_URL: %s" % os.environ.get("PANDACACHE_URL", None))

    from pandaclient import Client
    # status, output = Client.getFile(archive_basename, output_path=full_output_filename, verbose=False)
    status, output = Client.getFile(archive_basename, output_path=full_output_filename, verbose=False)
    print("Download archive file from pandacache status: %s, output: %s" % (status, output))
    if status != 0:
        raise RuntimeError("Failed to download archive file from pandacache")
    with tarfile.open(full_output_filename, 'r:gz') as f:
        f.extractall(target_dir)
    print("Extract %s to %s" % (full_output_filename, target_dir))
    os.remove(full_output_filename)
    print("Remove %s" % full_output_filename)


# request_id and signature are added by iDDS for build task
request_id = os.environ.get("IDDS_BUILD_REQUEST_ID", None)
signature = os.environ.get("IDDS_BUIL_SIGNATURE", None)
job_archive = sys.argv[1]

if request_id is None:
    print("IDDS_BUILD_REQUEST_ID is not defined.")
    sys.exit(-1)
if signature is None:
    print("IDDS_BUIL_SIGNATURE is not defined")
    sys.exit(-1)

print("INFO: start {}".format(datetime.datetime.utcnow()))
print("INFO: job archive: {}".format(job_archive))

current_dir = os.getcwd()

download_extract_archive(job_archive)

print("INFO: current dir: %s" % current_dir)
