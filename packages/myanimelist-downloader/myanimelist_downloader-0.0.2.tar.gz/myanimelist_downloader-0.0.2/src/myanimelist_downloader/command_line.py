# Argument parsing.
from argparse import (
    ArgumentParser,
    Namespace,
    BooleanOptionalAction,
)

# Union from typing to allow two type variables.
from typing import Union

# From os.path get directory and file check and path joiner.
from os.path import isdir, isfile, join

# Get current working directory for default arguments.
from os import getcwd

# Credentials from password-credentials.
from password_credentials.credentials import Credentials

# Directory handeler.
from dir_handeler.dir import Dir

# For loading .env files.
from dotenv import load_dotenv

# For downloading MyAnimeList manga and/or anime lists.
from .downloader import Downloader

# For manga and anime list types.
from .list import List


def dir_path(string: str) -> str:
    """Check if given string argument is directory path.

    Args:
        string (str): Argument to check.

    Raises:
        NotADirectoryError: If was not directory path.

    Returns:
        str: Given argument.
    """

    if isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def file_path(string: str) -> str:
    """Check if given string argument is file path.

    Args:
        string (str): Argument to check.

    Raises:
        FileNotFoundError: If was not file path.

    Returns:
        str: Given argument.
    """
    if isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def main():
    """Handle anime/manga list downloading from MyAnimeList."""

    # Init argument parser.
    parser: ArgumentParser = ArgumentParser()
    # Working directory.
    working_directory: str = getcwd()
    # Default .evn file.
    default_env: str = join(working_directory, ".env")
    # Add arguments to parser.
    parser.add_argument(
        "-u",
        "--username",
        dest="username",
        type=str,
        default=None,
        help="MyAnimeList username",
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        type=str,
        default=None,
        help="MyAnimeList password",
    )
    parser.add_argument(
        "-d",
        "--download-directory",
        dest="download_directory",
        type=dir_path,
        default=working_directory,
        help="Download directory",
    )
    del working_directory
    parser.add_argument(
        "-e",
        "--env-file",
        dest="env_file",
        type=file_path,
        default=default_env,
        help="Enviroment file",
    )
    del default_env
    parser.add_argument(
        "-a",
        "--anime",
        dest="anime",
        action=BooleanOptionalAction,
        help="Download mangalist.",
        default=False,
    )
    parser.add_argument(
        "-m",
        "--manga",
        dest="manga",
        action=BooleanOptionalAction,
        help="Download mangalist.",
        default=False,
    )

    # Parse arguments.
    args: Namespace = parser.parse_args()

    # Get arguments to variables.
    username: Union[str, None] = args.username
    password: Union[str, None] = args.password
    download_directory: Union[str, None] = args.download_directory
    env_file: str = args.env_file
    lists: list = []
    if args.anime:
        lists.append(List.ANIME)
    if args.manga:
        lists.append(List.MANGA)
    if not lists:
        parser.error(message="--anime and/or --manga must be given!")
    del parser, args

    # Load enviroment.
    load_dotenv(dotenv_path=(env_file if isfile(env_file) else None))
    del env_file

    # Init downloader.
    downloader = Downloader(
        Credentials.get(service="MAL", username=username, password=password),
        Dir(download_directory),
    )
    del username, password, download_directory

    # Download lists.
    for list in lists:
        downloader.download_list(list=list)
        del list
    del lists, downloader
