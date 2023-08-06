# Typing.
from __future__ import annotations
from typing import Union

# For downloading MAL list with selenium.
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

# For downloading Chrmoe webdriver.
from webdriver_manager.chrome import ChromeDriverManager

# For  getting env values.
from os import getenv

# For setting log level.
from logging import ERROR


class Driver(Chrome):
    """Overwrite default Chrome web driver."""

    __wait: WebDriverWait

    @classmethod
    def Start(cls, downloads_dir: Union[str, None]) -> Driver:
        """Start Chrome driver.

        Args:
            downloads_dir (Union[str, None]): Download directory.

        Returns:
            Driver: Started driver.
        """

        # Generate browser options.
        options = Options()

        # If debug set.
        if str(getenv("SELENIUM_DEBUG", False)).lower() in ("true", "1"):
            # Set to not work as headless.
            options.headless = False
            # Do not close browser.
            options.add_experimental_option("detach", True)
        else:
            # Set to work as headless.
            options.headless = True

        # Set downloads directory.
        if downloads_dir:
            options.add_experimental_option(
                "prefs", {"download.default_directory": downloads_dir}
            )

        # Initialize driver.
        driver = cls(
            service=Service(ChromeDriverManager(log_level=ERROR).install()),
            options=options,
        )
        del options

        # Initalize wait.
        driver.__wait = WebDriverWait(driver, getenv("SELENIUM_TIMEOUT", 10))

        # Return created driver.
        return driver

    def element(self, by: By, value: str) -> WebElement:
        """Get element.

        Args:
            by (By): Search by this attribute.
            value (str): Search with this value.

        Returns:
            WebElement: Found element.
        """

        return self.__wait.until(
            expected_conditions.presence_of_element_located((by, value))
        )
