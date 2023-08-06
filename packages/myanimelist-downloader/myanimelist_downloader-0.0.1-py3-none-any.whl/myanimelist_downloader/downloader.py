# Typing.
from __future__ import annotations

# For downloading MAL list with selenium.
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

# For making storage directory.
from dir_handeler.dir import Dir

# Fro waiting for MAL list download.
from time import sleep

# For listing MAL list files.
from os import listdir, replace, rmdir

# For getting MAL credentials.
from password_credentials.credentials import Credentials

# Driver for browser.
from .driver import Driver

# For generating random string for TMP-directory.
from random import choices
from string import ascii_lowercase

# For defining list type manga|anime.
from .list import List


class Downloader:
    """Download MyAnimeList manga or anime lists."""

    # Download directory.
    __download_directory: Dir

    # MyAnimeList credentials.
    __credentials: Credentials

    def __init__(self: Downloader, credentials: Credentials, download_directory: Dir):
        """Init MyAnimeList list downloader.

        Args:
            credentials (Credentials): MyAnimeList credentials.
            download_directory (Dir): Download directory.
        """
        self.__credentials = credentials
        self.__download_directory = download_directory

    def download_list(self: Downloader, list: List) -> str:
        """Download anime or manga list from MyAnimeList.

        Args:
            list (List): Download anime or manga list?

        Returns:
            str: Downloaded filepath.
        """

        # Generate random TMP directory inside download directory.
        tmp_dir: Dir = Dir(
            name="tmp_{unique}".format(
                unique="".join(choices(population=ascii_lowercase, k=10))
            ),
            parent=self.__download_directory,
        )
        try:
            # Initialize driver.
            driver = Driver.Start(downloads_dir=tmp_dir.path)
            try:
                # Get export page.
                driver.get("https://myanimelist.net/panel.php?go=export")

                # Fill and submit login form.
                form = driver.element(By.NAME, "loginForm")
                form.find_element(By.NAME, "user_name").send_keys(
                    self.__credentials.username
                )
                form.find_element(By.NAME, "password").send_keys(
                    self.__credentials.password
                )
                form.submit()
                del form

                # Fill and submit download form.
                form = driver.element(
                    By.XPATH, "//form[@action='/panel.php?go=export2']"
                )
                Select(form.find_element(By.NAME, "type")).select_by_value(
                    str(list.value)
                )
                form.find_element(By.NAME, "subexport").click()
                del form

                # Accept alert dialog.
                Alert(driver).accept()

                # Get downloaded filename.
                loops = 0
                filename = None
                while filename is None:
                    # Get filenames.
                    filenames = listdir(tmp_dir.path)
                    # Get filenames count.
                    filename_count = len(filenames)
                    # If only one file.
                    if filename_count == 1:
                        # If filename is correct, set it.
                        if filenames[0].endswith(".xml.gz"):
                            filename = filenames[0]
                        # Still downloading so sleep.
                        else:
                            sleep(1)
                    # No files so sleep.
                    elif filename_count == 0:
                        sleep(1)
                    # Multiple files.
                    else:
                        raise Exception(
                            "Found {filename_count} files!".format(
                                filename_count=filename_count
                            )
                        )
                    del filenames, filename_count

                    # Increment and check loops.
                    loops += 1
                    if loops > 20:
                        raise Exception("Over 20 loops!")
                del loops
                to_filepath: str = self.__download_directory.file_path(
                    filename=filename
                )
                replace(src=tmp_dir.file_path(filename=filename), dst=to_filepath)
            finally:
                # Close driver.
                driver.close()
                del driver
        finally:
            # Delete temporary directory
            rmdir(tmp_dir.path)

        # Return path to downloaded file.
        return to_filepath
