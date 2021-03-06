# Browser and HTML parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common import exceptions
from lxml import html
import re

# Logging and Error
import logging
import logging.handlers
import errno

# OS
import os
from os import listdir
from os.path import isfile, join
import sys
import subprocess

#TODO: Documentation, verbose

class SeleniumClass:
    def __init__(self, browser="Firefox", headless=True):
        # profile = webdriver.FirefoxProfile()
        self._name = browser
        self._headless = headless
        self.set_browser()

    def use_chrome(self):
        self._browser = Chrome
        self._options = ChromeOptions()
        self._name = "Chrome"
    
    def use_firefox(self):
        self._browser = Firefox
        self._options = FirefoxOptions()
        self._name = "Firefox"

    def set_browser(self):
        if self._name.lower() == "chrome":
            self.setChrome()
        elif self._name.lower() == "firefox":
            self.setFirefox()
        else:
            print(f"'{self._name}' not recognized defaulted to Firefox")
            self.setFirefox()
    
    def open_browser(self):
        print("Opening Browser")
        return self._browser()

    @property
    def browser(self, browser):
        return self._browser

    @property
    def headless(self, headless):
        return self._headless
    
    #TODO: work on headless setter
    @headless.setter
    def headless(self, headless):
        print("Setting headless mode")
        assert type(headless) == bool
        self._options.headless = headless
        self._options.add_argument('--remote-debugging-port=9222') # Enable debugging on local host while running selenium headless --> http://localhost:9222

    def set_logging_params(self, path=None, filename="selenium_scraper.log", root_level="DEBUG",console_level="INFO", file_level="WARNING"):
        """This method set logging parameters
        
        Args:
            path (str, optional): The path to the folder where you want the log file to be written. Defaults to the root path of the class object.
            filename (str, optional): The name of the log file (including the extension). Defaults to "selenium_scraper.log".
            root_level (str, optional): The root level. Defaults to "DEBUG".
            console_level (str, optional): The console level. Defaults to "INFO".
            file_level (str, optional): The file level. Defaults to "WARNING".
        """
        
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        root_level = root_level.upper()
        console_level = console_level.upper()
        file_level = file_level.upper()
        if not path:
            path = self.root_path
        for level_name, level in {"root level":root_level, "console level":console_level, "file level":file_level}.items():
            if level not in levels:
                logging.error(f"logging setting {level} unavailable for {level_name}")
                logging.info(f"Only the following levels are available: {' '.join(levels)}")
                return
        if path:
            pass
        if filename:
            pass
        rootLogger = logging.getLogger()
        rootLogger.setLevel(getattr(logging, root_level))
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-4.4s]  %(message)s")

        fileHandler = logging.FileHandler(os.path.join(path, filename))
        fileHandler.setLevel(getattr(logging, file_level))
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(getattr(logging, console_level))
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    def make_sure_path_exists(self, path):
        """This method create a path and the corresponding folders if the path doesn't exists yet
        
        Args:
            path (str): The path you want to make sure exists
        """
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    
    def run_bash(self, command):
        """This method runs simple bash command from a string (doesn't allow substring, ex: echo 'this is an example' >> test.txt WONT WORK) 
        
        Args:
            command (str): The string corresponding to the command you want to run
        """
        if type(command) == str:
            command = command.split()
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                output = process.communicate()[0]
            except:
                logging.error(f"Unable to run bash command {command}")