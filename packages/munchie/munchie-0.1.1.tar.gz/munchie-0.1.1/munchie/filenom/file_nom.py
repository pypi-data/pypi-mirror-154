import os

from munchie import MunchieResponse
from munchie.constants import SUPPORTED_FILE_MODES, SUPPORTED_FILE_TYPES
from munchie.filenom import utils
from typing import Any, Dict, List


def create_new_directory(
    dir_path: str, dir_name: str = "", permissions: int = 744, exists_ok: bool = True
) -> MunchieResponse:
    """Create a new directory at the given dir_path.

    Args:
        dir_path (str): path to create the directory at

    Optional Args:
        dir_name (str): if no directory name is provided \
            then the dir_path will attempt to \
            be created as the directory
        permissions (int): set the permissions on the path \
            defaults to 744 (rwxr--r--)
        exists_ok (bool): do not error if the directory already exists. \
            defaults to False

    Returns:
        MunchieResponse: message is set to the dir_path if created successfully
    """

    response = MunchieResponse()

    response = utils._validate_path(path_obj=dir_path, response=response)
    response = utils._validate_path_permissions(
        permissions=permissions, response=response
    )

    if response.ok:
        # validate the directory path does not end with a file extension
        response = utils._validate_path_extension(
            path_obj=dir_path, path_type="directory", response=response
        )

        try:
            if dir_name:
                # validate the directory name is a string
                response = utils._validate_path(path_obj=dir_name, response=response)

                # validate the directory name does not end with a file extension
                response = utils._validate_path_extension(
                    path_obj=dir_name, path_type="directory", response=response
                )

                # append the dir_name to the dir_path
                dir_path = os.path.join(dir_path, dir_name)

                # make the directory
                os.makedirs(dir_path, exist_ok=exists_ok)

            else:
                # make the directory without appending the dir_name
                os.makedirs(dir_path, exist_ok=exists_ok)

            # update the path to the specified permissions
            os.chmod(dir_path, int(str(permissions), base=8))

            response.message = f"Directory: '{dir_path}' has been successfully created"

        except FileExistsError as warning:
            response.ok, response.log_level = False, "warn"
            response.message = warning

    return response


def create_new_file(
    file_path: str, file_name: str = "", permissions: int = 744, exists_ok: bool = True
) -> MunchieResponse:
    """Create a new file at the given file_path.

    Args:
        file_path (str): path to create the new file

    Optional Args:
        file_name (str): if no file name is provided then \
            the file_path will attempt to be \
            created as the new file
        permissions (int): set the permissions on the path \
            defaults to 744 (rwxr--r--)
        exists_ok (bool): do not error if the file already exists. \
            defaults to True

    Returns:
        MunchieResponse: message is set to the file_path if created successfully
    """

    # Todo add logic to check if file exists

    response = MunchieResponse()

    response = utils._validate_path(path_obj=file_path, response=response)
    response = utils._validate_path_permissions(
        permissions=permissions, response=response
    )

    if response.ok:
        # validate the file path does not end with a file extension
        response = utils._validate_path_extension(
            path_obj=file_path, path_type="directory", response=response
        )

        if file_name:
            response = utils._validate_path(path_obj=file_name, response=response)
            response = utils._validate_path_extension(
                path_obj=file_name, path_type="file", response=response
            )

            # append the file_name to the file_path
            file_path = os.path.join(file_path, file_name)

            # check if the path already exists
            response = utils._validate_path_exists(
                path_obj=file_path, exists_ok=exists_ok, response=response
            )

            if response.ok:
                # make the file
                open(file_path, "a").close()

        else:
            # check if the path already exists
            response = utils._validate_path_exists(
                path_obj=file_path, exists_ok=exists_ok, response=response
            )

            if response.ok:
                # make the file without appending the file_name
                open(file_path, "a").close()

        if response.ok:
            # update the path to the specified permissions
            os.chmod(file_path, int(str(permissions), base=8))

            response.message = f"File: '{file_path}' has been successfully created"

    return response


def delete_directory(dir_path: str) -> MunchieResponse:
    """Recursively delete a directory.

    Args:
        dir_path (str): path to directory to delete

    Returns:
        MunchieResponse: ok is True if successful
    """

    response = MunchieResponse()

    response = utils._delete_directory(dir_path=dir_path, response=response)
    return response


def delete_file(file_path: str):
    """Delete a file.

    Args:
        file_path (str): path to the file to delete

    Returns:
        MunchieResponse: ok is True if successful
    """

    response = MunchieResponse()

    response = utils._delete_file(file_path=file_path, response=response)
    return response


def read_file(file_path: str, ext_override: str = "") -> MunchieResponse:
    """Read in the contents of a file.

    Args:
        file_path (str): path to file
        ext_override (str): type of file to read; \
            if provided the extension on the file will be ignored

    Returns:
        MunchieResponse: message is set to the contents of the file
    """

    response = MunchieResponse()

    extension = ""
    if ext_override:
        extension = ext_override

    else:
        _, extension = os.path.splitext(file_path)
        extension = extension.lstrip(".")

        if not extension:
            response.ok, response.log_level = False, "error"
            response.message = f"No file extension found for '{file_path}'"
            return response

    file_type = ""
    for key, values in SUPPORTED_FILE_TYPES.items():
        if extension in values:
            file_type = key
            break

    match file_type:
        case "csv":
            response = utils._read_csv_file(file_path=file_path, response=response)

        case "json":
            response = utils._read_json_file(file_path=file_path, response=response)

        case "toml":
            response = utils._read_toml_file(file_path=file_path, response=response)

        case "yaml":
            response = utils._read_yaml_file(file_path=file_path, response=response)

        case _:
            response.ok, response.log_level = False, "warn"
            response.message = ValueError(
                f"Extension '{extension}' not supported. No file has been read."
            )

    return response


def write_file(
    file_path: str,
    contents: Dict[str, Any] | List[Dict[str, Any]],
    mode: str = "w",
    ext_override: str = "",
) -> MunchieResponse:
    """Write contents to a file.

    Args:
        file_path (str): path to output file
        contents (Dict[str, Any] | List[Dict[str, Any]]): data to write to the file
        mode (str): method used when opening a file; \
            available modes: r, w, x, a, t, b, +; \
            defaults to write (w)
        ext_override (str): type of file to write; \
            if provided the extension on the file will be ignored

    Returns:
        MunchieResponse: ok is True if successful
    """

    response = MunchieResponse()

    if mode not in SUPPORTED_FILE_MODES:
        response.ok, response.log_level = False, "error"
        response.message = ValueError(f"File mode '{mode}' is not supported")

    extension = ""
    if ext_override:
        extension = ext_override

    else:
        _, extension = os.path.splitext(file_path)
        extension = extension.lstrip(".")

        if not extension:
            response.ok, response.log_level = False, "error"
            response.message = f"No file extension found for '{file_path}'"
            return response

    file_type = ""
    for key, values in SUPPORTED_FILE_TYPES.items():
        if extension in values:
            file_type = key
            break

    match file_type:
        case "csv":
            response = utils._write_csv_file(
                file_path=file_path, contents=contents, mode=mode, response=response
            )

        case "json":
            response = utils._write_json_file(
                file_path=file_path, contents=contents, mode=mode, response=response
            )

        case "toml":
            if isinstance(contents, dict):
                response = utils._write_toml_file(
                    file_path=file_path, contents=contents, mode=mode, response=response
                )

            else:
                response.ok, response.log_level = False, "warn"
                response.message = TypeError(
                    f"Contents of type {type(contents)} are not a valid dictionary"
                )

        case "yaml":
            response = utils._write_yaml_file(
                file_path=file_path, contents=contents, mode=mode, response=response
            )

        case _:
            response.ok, response.log_level = False, "warn"
            response.message = ValueError(
                f"Extension '{extension}' not supported. No file has been written."
            )

    if response.ok:
        response.message = f"File: '{file_path}' has been successfully written"

    return response
