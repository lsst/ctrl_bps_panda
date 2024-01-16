#!/usr/bin/python

# This file is part of ctrl_bps_panda.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Decode the command line string sent from the BPS
plugin -> PanDA -> Edge node cluster management
-> Edge node -> Container. This file is not a part
of the BPS but a part of the payload wrapper.
It decodes the hexified command line.
"""
import binascii
import json
import os
import re
import sys

from lsst.resources import ResourcePath


def replace_placeholders(cmd_line: str, tag: str, replacements: dict[str, str]) -> str:
    """Replace the placeholders.

    Parameters
    ----------
    cmd_line : `str`
        Command line.
    tag : `str`
        Tag to use for finding placeholders.
    replacements : `dict` [`str`, `str`]
        Replacements indexed by place holder string.

    Returns
    -------
    modified : `str`
        Processed command line.
    """
    occurrences_to_replace = re.findall(f"<{tag}:(.*?)>", cmd_line)
    for placeholder in occurrences_to_replace:
        if placeholder in replacements:
            cmd_line = cmd_line.replace(f"<{tag}:{placeholder}>", replacements[placeholder])
        else:
            raise ValueError(
                "ValueError exception thrown, because "
                f"{placeholder} is not found in the "
                "replacement values and could "
                "not be passed to the command line"
            )
    return cmd_line


def replace_environment_vars(cmd_line):
    """Replace placeholders to the actual environment variables.

    Parameters
    ----------
    cmd_line : `str`
        Command line.

    Returns
    -------
    cmdline: `str`
        Processed command line.
    """
    environment_vars = os.environ
    cmd_line = replace_placeholders(cmd_line, "ENV", environment_vars)
    return cmd_line


def replace_files_placeholders(cmd_line, files):
    """Replace placeholders for files.

    Parameters
    ----------
    cmd_line : `str`
        Command line.
    files : `str`
        String with key:value pairs separated by the '+' sign.
        Keys contain the file type (runQgraphFile,
        butlerConfig, ...).
        Values contains file names.

    Returns
    -------
    cmd_line: `str`
        Processed command line.
    """
    files_key_vals = files.split("+")
    files = {}
    for file in files_key_vals:
        file_name_placeholder, file_name = file.split(":")
        files[file_name_placeholder] = file_name
    cmd_line = replace_placeholders(cmd_line, "FILE", files)
    return cmd_line


def deliver_input_files(src_path, files, skip_copy):
    """Deliver input files needed for a job.

    Parameters
    ----------
    src_path : `str`
        URI for folder where the input files placed.
    files : `str`
        String with file names separated by the '+' sign.
    skip_copy : `str`
        String with file names separated by the '+' sign indicating which
        files in ``files`` should not be copied.

    Returns
    -------
    cmdline: `str`
        Processed command line.
    """
    files = files.split("+")
    src_uri = ResourcePath(src_path, forceDirectory=True)
    for file in files:
        file_name_placeholder, file_pfn = file.split(":")
        if file_name_placeholder not in skip_copy.split("+"):
            src = src_uri.join(file_pfn)
            base_dir = None
            if src.isdir():
                files_to_copy = ResourcePath.findFileResources([src])
                base_dir = file_pfn
            else:
                files_to_copy = [src]
            dest_base = ResourcePath("", forceAbsolute=True, forceDirectory=True)
            if base_dir:
                dest_base = dest_base.join(base_dir)
            for file_to_copy in files_to_copy:
                dest = dest_base.join(file_to_copy.basename())
                if file_name_placeholder == "orderIdMapFilename":
                    if not dest.exists():
                        dest.transfer_from(file_to_copy, transfer="copy")
                else:
                    dest.transfer_from(file_to_copy, transfer="copy")
                print(f"copied {file_to_copy.path} to {dest.path}", file=sys.stderr)
            if file_name_placeholder == "job_executable":
                os.chmod(dest.path, 0o777)


def replace_event_file(params, files):
    ret_status = True
    with_events = False
    files = files.split("+")
    file_map = {}
    for file in files:
        file_name_placeholder, file_pfn = file.split(":")
        file_map[file_name_placeholder] = file_pfn
    order_id_map_file = file_map.get("orderIdMapFilename", None)
    order_id_map = {}
    try:
        if order_id_map_file and os.path.exists(order_id_map_file):
            with open(order_id_map_file) as f:
                order_id_map = json.load(f)
    except Exception as ex:
        print("failed to load orderIdMapFilename: %s" % str(ex))

    params_map = {}
    params_list = params.split("+")
    for param in params_list:
        if "eventservice_" in param:
            with_events = True
            label, event = param.split(":")
            event_id = event.split("_")[1]
            event_base_id = event_id.split("^")[0]
            event_order = event_id.split("^")[1].split("^")[0]
            event_index = str(int(event_base_id) + int(event_order) - 1)
            if not order_id_map:
                ret_status = False

            if label not in order_id_map or event_index not in order_id_map[label]:
                ret_status = False

            params_map[param] = {"event_index": event_index, "order_id_map": order_id_map[label]}
    return ret_status, with_events, params_map


deliver_input_files(sys.argv[3], sys.argv[4], sys.argv[5])
cmd_line = str(binascii.unhexlify(sys.argv[1]).decode())
# data_params = sys.argv[2].split("+")
data_params = sys.argv[2]
cmd_line = replace_environment_vars(cmd_line)

ret_event_status, with_events, event_params_map = replace_event_file(data_params, sys.argv[4])
print("ret_event_status: %s, with_events: %s" % (ret_event_status, with_events))
if not ret_event_status:
    print("failed to parse event to files")
    exit_code = 1
    sys.exit(exit_code)

for event_param in event_params_map:
    event_index = event_params_map[event_param]["event_index"]
    pseudo_file_name = event_params_map[event_param]["order_id_map"][event_index]
    print("replacing event %s with event_index %s to: %s" % (event_param, event_index, pseudo_file_name))
    cmd_line = cmd_line.replace(event_param, pseudo_file_name)
    data_params = data_params.replace(event_param, pseudo_file_name)

data_params = data_params.split("+")

"""Replace the pipetask command line placeholders
 with actual data provided in the script call
 in form placeholder1:file1+placeholder2:file2:...
"""
cmd_line = replace_files_placeholders(cmd_line, sys.argv[4])

for key_value_pair in data_params[1:]:
    (key, value) = key_value_pair.split(":")
    cmd_line = cmd_line.replace("{" + key + "}", value)

print("executable command line:")
print(cmd_line)

exit_status = os.system(cmd_line)
exit_code = 1
if os.WIFSIGNALED(exit_status):
    exit_code = os.WTERMSIG(exit_status) + 128
elif os.WIFEXITED(exit_status):
    exit_code = os.WEXITSTATUS(exit_status)
sys.exit(exit_code)
