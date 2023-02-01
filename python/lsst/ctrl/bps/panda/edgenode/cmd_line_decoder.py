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

from lsst.resources import ResourcePath


def replace_placeholders(cmd_line, tag, replancements):
    occurences_to_replace = re.findall(f"<{tag}:(.*?)>", cmd_line)
    for placeholder in occurences_to_replace:
        if placeholder in replancements:
            cmd_line = cmd_line.replace(f"<{tag}:{placeholder}>", replancements[placeholder])
        else:
            raise ValueError(
                "ValueError exception thrown, because "
                f"{placeholder} is not found in the "
                "replacement values and could "
                "not be passed to the command line"
            )
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


def deliver_input_files(files, skip_copy):
    """Delivers input files needed for a job.

    Parameters
    ----------
    file_params : `dict` [`str`, `str`]
        Mapping key to outside job URI (e.g. staging URI).
    skip_copy : `set `str`
        Keys for files that can be accessed in place.

    Returns
    -------
    file_placeholders: `dict` [`str`, `str`]
        Mapping file placeholder key to URIs to be used in job.
    """
    file_placeholders = {}
    for file_ in files:
        key, file_pfn = file_.split(":", 1)
        if key not in skip_copy:
            src = ResourcePath(file_pfn)
            base_dir = None
            if file_pfn.endswith("/"):
                base_dir = os.path.basename(file_pfn[:-1])
                files_to_copy = ResourcePath.findFileResources(src)
            else:
                files_to_copy = [src]

            dest_base = ResourcePath("", forceAbsolute=True, forceDirectory=True)
            if base_dir:
                dest_base = dest_base.join(base_dir)
            file_placeholders[key] = dest_base.join(src.basename())

            for file_to_copy in files_to_copy:
                dest = dest_base.join(file_to_copy.basename())
                dest.transfer_from(file_to_copy, transfer="copy")
                print(f"copied {file_to_copy.path} to {dest.path}", file=sys.stderr)

            if key == "job_executable":
                os.chmod(dest.path, 0o777)
        else:
            file_placeholders[key] = file_pfn
    return file_placeholders


def create_cmd_line(hex_cmd_line, data_params, file_placeholders):
    """Create payload job's command line.

    Parameters
    ----------
    hex_cmd_line : `str`
        Hex representation of payload job's command line pattern.
    data_params : `dict` [ `str`, `str` ]
        Mapping key to value for non-env and non-file data.
    file_placeholders : `dict` [ `str`, `str` ]
        Mapping key to inside job URI.

    Returns
    -------
    cmd_line : `str`
        Payload job's command line.
    """
    cmd_line = str(binascii.unhexlify(hex_cmd_line).decode())
    print(f"cmd_line: {cmd_line}")

    # Replace env variables in cmd_line
    cmd_line = replace_placeholders(cmd_line, "ENV", os.environ)
    print(f"ENV changes: {cmd_line}")

    # Replace file placeholders in command line with URI
    cmd_line = replace_placeholders(cmd_line, "FILE", file_placeholders)
    print(f"FILE changes: {cmd_line}")

    # Replace other value placeholders in command line with values
    for key_value_pair in data_params[1:]:
        (key, value) = key_value_pair.split(":")
        cmd_line = cmd_line.replace("{" + key + "}", value)
    print(f"OTHER changes: {cmd_line}")

    return cmd_line


def main(hex_cmd_line, data_params_str, file_params_str, direct_io_keys_str):
    """Compute job entry point.

    Parameters
    ----------
    hex_cmd_line : `str`
        Hex representation of payload job's command line pattern.
    data_params_str : `str`
        Mapping key to value for non-env and non-file data.
        (key:value pairs separated by "+")
        URI for folder where the input files placed
    file_params_str : `str`
        Mapping key to outside job URI (e.g. staging URI).
        (key:uri pairs separated by "+")
    direct_io_keys_str : `str`
        Keys for files that can be accessed in place.
        (Values separated by "+")

    Returns
    -------
    exit_code: `int`
        Status of executing compute job (0 for success).
    """
    print(f"main's args hex_cmd_line = {hex_cmd_line}")
    print(f"main's args data_params = {data_params_str}")
    print(f"main's args file_params = {file_params_str}")
    print(f"main's args direct_io_keys = {direct_io_keys_str}")

    file_params = file_params_str.split("+")
    direct_io_keys = direct_io_keys_str.split("+")
    data_params = data_params_str.split("+")

    file_placeholders = deliver_input_files(file_params, direct_io_keys)
    print(f"file_placeholders: {file_placeholders}")

    cmd_line = create_cmd_line(hex_cmd_line, data_params, file_placeholders)

    # Execute job command
    print(f"cmd to execute: {cmd_line}")
    exit_status = os.system(cmd_line)
    exit_code = 1
    if os.WIFSIGNALED(exit_status):
        exit_code = os.WTERMSIG(exit_status) + 128
    elif os.WIFEXITED(exit_status):
        exit_code = os.WEXITSTATUS(exit_status)
    return exit_code


if __name__ == "__main__":
    print(f"sys.argv: {sys.argv}")
    if len(sys.argv) != 5:
        print("Error: Invalid command line.")
        print(f"Usage: {sys.argv[0]} <data_params> <hex_cmd_line> <file_params> <direct_io_keys>")
        exit_code = 1
    else:
        exit_code = main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit(exit_code)
