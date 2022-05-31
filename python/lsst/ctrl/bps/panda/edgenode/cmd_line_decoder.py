#!/usr/bin/python
"""
This file is needed to decode the command line string sent from the BPS
plugin -> PanDA -> Edge node cluster management
-> Edge node -> Container. This file is not a part
of the BPS but a part of the payload wrapper.
It decodes the hexified command line.
"""
import binascii
import os
import re
import sys
import tarfile

from lsst.resources import ResourcePath


def replace_placeholders(cmd_line, tag, replancements):
    occurences_to_replace = re.findall(f"<{tag}:(.*?)>", cmd_line)
    for placeholder in occurences_to_replace:
        if placeholder in replancements:
            cmd_line = cmd_line.replace(f"<{tag}:{placeholder}>", replancements[placeholder])
        else:
            raise ValueError(
                f"ValueError exception thrown, because "
                f"{placeholder} is not found in the "
                f"replacement values and could "
                f"not be passed to the command line"
            )
    return cmd_line


def replace_environment_vars(cmd_line):
    """Replaces placeholders to the actual environment variables.

    Parameters
    ----------
    cmd_line : `str`
        Command line

    Returns
    -------
    cmdline: `str`
        Processed command line
    """
    environment_vars = os.environ
    cmd_line = replace_placeholders(cmd_line, "ENV", environment_vars)
    return cmd_line


def replace_files_placeholders(cmd_line, files):
    """Replaces placeholders for files.

    Parameters
    ----------
    cmd_line : `str`
        Command line
    files : `str`
        String with key:value pairs separated by the '+' sign.
        Keys contain the file type (runQgraphFile,
        butlerConfig, ...).
        Values contains file names.

    Returns
    -------
    cmd_line: `str`
        Processed command line
    """

    files_key_vals = files.split("+")
    files = {}
    for file in files_key_vals:
        file_name_placeholder, file_name = file.split(":")
        files[file_name_placeholder] = file_name
    cmd_line = replace_placeholders(cmd_line, "FILE", files)
    return cmd_line


def deliver_input_files_origin(src_path, files, skip_copy):
    """Delivers input files needed for a job

    Parameters
    ----------
    src_path : `str`
        URI for folder where the input files placed
    files : `str`
        String with file names separated by the '+' sign

    Returns
    -------
    cmdline: `str`
        Processed command line
        :param skip_copy:
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
                dest.transfer_from(file_to_copy, transfer="copy")
                print(f"copied {file_to_copy.path} " f"to {dest.path}", file=sys.stderr)


def deliver_input_files_pandacache(src_path, files, skip_copy):
    """Delivers input files needed for a job

    Parameters
    ----------
    src_path : `str`
        URI for folder where the input files placed
    files : `str`
        String with file names separated by the '+' sign

    Returns
    -------
    cmdline: `str`
        Processed command line
        :param skip_copy:
    """
    pos = files.index("+")
    archive_filename = files[:pos]
    archive_filename = archive_filename.replace("pandacache:", "")
    archive_basename = os.path.basename(archive_filename)
    target_dir = os.getcwd()
    full_output_filename = os.path.join(target_dir, archive_basename)
    if "PANDACACHE_URL" not in os.environ and "PANDA_URL_SSL" in os.environ:
        os.environ["PANDACACHE_URL"] = os.environ["PANDA_URL_SSL"]
    else:
        cache_dir = os.path.dirname(archive_filename)
        os.environ["PANDACACHE_URL"] = os.path.dirname(cache_dir)
    from pandaclient import Client
    status, output = Client.getFile(archive_basename, output_path=full_output_filename, verbose=False)
    print("Download archive file from pandacache status: %s, output: %s" % (status, output))
    if status != 0:
        raise RuntimeError("Failed to download archive file from pandacache")
    with tarfile.open(full_output_filename, 'r:gz') as f:
        f.extractall(target_dir)
    os.remove(full_output_filename)

    new_files = files[pos + 1:]

    files = new_files.split("+")
    dest_uri = ResourcePath(src_path, forceDirectory=True)
    for file in files:
        file_name_placeholder, file_pfn = file.split(":")
        src_base = ResourcePath("", forceAbsolute=True, forceDirectory=True)
        file_pfn = src_base.join(file_pfn)
        if file_pfn.isdir():
            files_to_copy = ResourcePath.findFileResources([file_pfn])
            dest_dir = dest_uri.join(file_pfn)
        else:
            files_to_copy = [file_pfn]
            dest_dir = dest_uri
        for file_to_copy in files_to_copy:
            dest = dest_dir.join(file_to_copy.basename())
            if not dest.exists():
                dest.transfer_from(file_to_copy, transfer="copy", overwrite=True)
                print(f"copied {file_to_copy.path} " f"to {dest.path}", file=sys.stderr)


def deliver_input_files(src_path, files, skip_copy):
    """Delivers input files needed for a job

    Parameters
    ----------
    src_path : `str`
        URI for folder where the input files placed
    files : `str`
        String with file names separated by the '+' sign

    Returns
    -------
    cmdline: `str`
        Processed command line
        :param skip_copy:
    """
    if files.startswith("pandacache:"):
        deliver_input_files_pandacache(src_path, files, skip_copy)
    else:
        deliver_input_files_origin(src_path, files, skip_copy)


def replace_pandacache_var(files):
    """Replaces pandacache to remove it.

    Parameters
    ----------
    files : `str`
        String with file names separated by the '+' sign

    Returns
    -------
    files: `str`
        Processed files by removing pandacache
    """
    if files.startswith("pandacache:"):
        pos = files.index("+")
        files = files[pos + 1:]

    return files


deliver_input_files(sys.argv[3], sys.argv[4], sys.argv[5])
sys.argv[4] = replace_pandacache_var(sys.argv[4])

cmd_line = str(binascii.unhexlify(sys.argv[1]).decode())
data_params = sys.argv[2].split("+")
cmd_line = replace_environment_vars(cmd_line)

"""This call replaces the pipetask command line placeholders
 with actual data provided in the script call
 in form placeholder1:file1+placeholder2:file2:...
"""
cmd_line = replace_files_placeholders(cmd_line, sys.argv[4])

for key_value_pair in data_params[1:]:
    (key, value) = key_value_pair.split(":")
    cmd_line = cmd_line.replace("{" + key + "}", value)

print(cmd_line)

exit_status = os.system(cmd_line)
exit_code = 1
if os.WIFSIGNALED(exit_status):
    exit_code = os.WTERMSIG(exit_status) + 128
elif os.WIFEXITED(exit_status):
    exit_code = os.WEXITSTATUS(exit_status)
sys.exit(exit_code)
