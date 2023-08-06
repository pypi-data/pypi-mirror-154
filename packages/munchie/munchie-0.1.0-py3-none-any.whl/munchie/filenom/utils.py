import csv
import json
import os
import shutil
import toml
import yaml

from munchie import MunchieResponse
from toml.decoder import TomlDecodeError
from typing import Any, Dict, List
from yaml.parser import ParserError


###################
# @ Validations @ #
###################


def _validate_path(path_obj: str, response: MunchieResponse) -> MunchieResponse:
    """Raise error if path object is a valid string.

    Args:
        path_obj (str): path to directory or file; or directory name or file_name

    Raises:
        TypeError:
        * if the directory or file path is not a string
        * if the directory or file name is not a string
    """

    if not isinstance(path_obj, str):
        response.ok, response.log_level = False, "error"
        response.message = TypeError(
            f"Given path '{path_obj}' is of type {type(path_obj)} and not a valid string"
        )

    return response


def _validate_path_exists(
    path_obj: str, exists_ok: bool, response: MunchieResponse
) -> MunchieResponse:
    """Check if the path_obj already exists.

    Args:
        path_obj (str): path to the directory or file
        exists_ok (bool): if False then check; else skip the skip

    Raises:
        FileExistsError: if the path already exists and exists_ok is False
    """

    if not exists_ok:
        if os.path.exists(path=path_obj):
            response.ok, response.log_level = False, "warn"
            response.message = FileExistsError(f"Path already exists: {path_obj}")

    return response


def _validate_path_extension(
    path_obj: str, path_type: str, response: MunchieResponse
) -> MunchieResponse:
    """Validate if the path_obj contains a file extension. If the path_type indicates
    that no extension should exist then an error will be thrown.

    Args:
        path_obj (str): path to directory or file; or directory name or file_name
        path_type (str): directory or file

    Raises:
        OSError: if the path_obj contains an extension that should not exist
        ValueError: if the path_type is not supported
    """

    if path_type == "directory":
        if all(os.path.splitext(path_obj)):
            response.ok, response.log_level = False, "warn"
            response.message = OSError(
                f"Directory name '{path_obj}' contains a file extension"
            )

    elif path_type == "file":
        if not os.path.splitext(path_obj)[1]:
            response.ok, response.log_level = False, "warn"
            response.message = OSError(
                f"File {path_obj} does not contain a file extension"
            )

    else:
        raise ValueError(f"Path type '{path_type}' is not supported")

    return response


def _validate_path_permissions(
    permissions: int, response: MunchieResponse
) -> MunchieResponse:
    """Validate directory or file permissions are within the allowed range.

    Args:
        permissions (int): octal permissions to apply to the path

    Raises:
        ValueError:
        * if the permissions are outside of the allowed range
    """

    if permissions not in range(000, 777):
        response.ok, response.log_level = False, "error"
        response.message = ValueError(
            f"Provided permissions: {permissions} are invalid"
        )

    return response


##################
# @ read files @ #
##################


def _read_csv_file(file_path: str, response: MunchieResponse) -> MunchieResponse:
    """Read in the contents of a CSV file.

    Args:
        file_path (str): path to the CSV file to read in
    """

    csv_contents = []

    with open(file_path, "r") as infile:
        for row in csv.DictReader(infile):
            csv_contents.append(row)

        infile.close()

    response.message = csv_contents
    return response


def _read_json_file(file_path: str, response: MunchieResponse) -> MunchieResponse:
    """Read in the contents of a JSON file.

    Args:
        file_path (str): path to the JSON file to read in

    Raises:
        JSONDecodeError: if the JSON file fails to be read
    """

    try:
        with open(file_path, "r") as infile:
            response.message = json.load(infile)
            infile.close()

    except json.JSONDecodeError as error:
        response.ok, response.log_level, response.message = False, "error", error

    return response


def _read_toml_file(file_path: str, response: MunchieResponse) -> MunchieResponse:
    """Read in the contents of a TOML file.

    Args:
        file_path (str): path to the JSON file to read in

    Raises:
        TomlDecodeError: if the TOML file fails to be read
    """

    try:
        response.message = toml.load(file_path)

    except TomlDecodeError as error:
        response.ok, response.log_level, response.message = False, "error", error

    return response


def _read_yaml_file(file_path: str, response: MunchieResponse) -> MunchieResponse:
    """Read in the contents of a YAML file.

    Args:
        file_path (str): path to the YAML file to read in

    Raises:
        TomlDecodeError: if the TOML file fails to be read
    """

    try:
        with open(file_path, "r") as infile:
            response.message = yaml.full_load(infile)
            infile.close()

    except ParserError as error:
        response.ok, response.log_level, response.message = False, "error", error

    return response


###################
# @ write files @ #
###################


def _write_csv_file(
    file_path: str,
    contents: Dict[str, Any] | List[Dict[str, Any]],
    mode: str,
    response: MunchieResponse,
) -> MunchieResponse:
    """Write dict or list contents to a file.

    Args:
        file_path (str): path to the CSV file to write
        contents (Dict[str, Any] | List[Dict[str, Any]]): data to write to the file
        mode (str): method used when opening a file
    """

    if isinstance(contents, dict):
        # if dict contents then wrap into a list
        contents = [contents]

    # check that all the records have the same keys
    unique_headers = []
    header_count = len(contents[0].keys())
    rebuild_headers = False

    for record in contents:
        if len(record.keys()) != header_count:
            rebuild_headers = True

        for key in record:
            if key not in unique_headers:
                unique_headers.append(key)

    # normalize the headers if needed
    if rebuild_headers:
        rebuilt_contents = []
        for record in contents:
            new_record = {}
            for header in unique_headers:
                new_record[header] = record.get(header, "-")

            rebuilt_contents.append(new_record)

        contents = rebuilt_contents  # reassign contents for writing

    with open(file_path, mode) as outfile:
        csv_writer = csv.writer(outfile)

        index = int(0)
        for record in contents:
            if index == 0:
                header = record.keys()
                csv_writer.writerow(header)
                index += 1

            csv_writer.writerow(record.values())

        outfile.close()

    return response


def _write_json_file(
    file_path: str,
    contents: Dict[str, Any] | List[Dict[str, Any]],
    mode: str,
    response: MunchieResponse,
) -> MunchieResponse:
    """Write dict contents to a file.

    Args:
        file_path (str): path to the JSON file to write
        contents (Dict[str, Any] | List[Dict[str, Any]]): data to write to the file
        mode (str): method used when opening a file
    """

    try:
        with open(file_path, mode) as outfile:
            json.dump(contents, outfile, indent=4)
            outfile.close()

    except json.JSONDecodeError as error:
        response.ok, response.log_level, response.message = False, "error", error

    return response


def _write_toml_file(
    file_path: str, contents: Dict[str, Any], mode: str, response: MunchieResponse
) -> MunchieResponse:
    """Write dict contents to a file.

    Args:
        file_path (str): path to the TOML file to write
        contents (Dict[str, Any]): data to write to the file
        mode (str): method used when opening a file
    """

    try:
        with open(file_path, mode) as outfile:
            toml.dump(contents, outfile)
            outfile.close()

    except TomlDecodeError as error:
        response.ok, response.log_level, response.message = False, "error", error

    return response


def _write_yaml_file(
    file_path: str,
    contents: Dict[str, Any] | List[Dict[str, Any]],
    mode: str,
    response: MunchieResponse,
) -> MunchieResponse:
    """Write dict contents to a file.

    Args:
        file_path (str): path to the YAML file to write
        contents (dict): data to write to the file
        mode (str): method used when opening a file
    """

    try:
        with open(file_path, mode) as outfile:
            yaml.dump(contents, outfile, indent=2)
            outfile.close()

    except ParserError as error:
        response.ok, response.log_level, response.message = False, "error", error

    return response


##############
# @ remove @ #
##############


def _delete_directory(dir_path: str, response: MunchieResponse) -> MunchieResponse:
    """Delete a directory and all of it's contents from the filesystem.

    Args:
        dir_path (str): path to the directory to be deleted
    """

    if not os.path.isdir(dir_path):
        response.ok, response.log_level = False, "error"
        response.message = TypeError(f"Path '{dir_path}' is not a directory")
        return response

    # remove the directory
    shutil.rmtree(dir_path, ignore_errors=False, onerror=None)
    response.message = f"Directory: '{dir_path}' has been successfully removed"

    return response


def _delete_file(file_path: str, response: MunchieResponse) -> MunchieResponse:
    """Delete a file from the filesystem.

    Args:
        file_path (str): path to the file to be deleted
    """

    if not os.path.exists(file_path):
        response.ok, response.log_level = False, "warn"
        response.message = FileNotFoundError(f"Path '{file_path}' does not exist")
        return response

    if not os.path.isfile(file_path):
        response.ok, response.log_level = False, "error"
        response.message = TypeError(f"Path '{file_path}' is not a file")
        return response

    # remove the file
    os.remove(file_path)
    response.message = f"File: '{file_path}' has been successfully removed"

    return response
