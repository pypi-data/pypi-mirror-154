# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## tracker.py
# ## 
# ##############################################################################
# =============================================================================>
# Definition

CHROME_UPDATE = True

# =============================================================================> 
# imports default
from xml.etree import ElementTree
import time
from abc import ABCMeta, abstractmethod
import warnings

# =============================================================================> 
# imports third party
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import chromedriver_binary
import chromedriver_autoinstaller as chromedriver

# =============================================================================> 
# imports local

# =============================================================================> 
# define local metod

# =============================================================================> 
# define class

class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class WebsiteAPI(webdriver.Chrome, Singleton):
    """WebsiteAPI

    Args:
        webdriver.Chrome (_type_): _description_
    References:
        - to solve `--headless timeout`
            https://stackoverflow.com/questions/67744514/timeout-exception-error-on-using-headless-chrome-webdriver
    """
    # =========================================================================>
    # Class attr
    silence = False

    # =========================================================================>
    # Default
    def __init__(self, *args, **kwargs):
        """ __init__ """
        Singleton.__init__(self)
        try:
            if CHROME_UPDATE:
                self._print_info("chromedriver auto install", mode = "p")
                chromedriver.install()
        except Exception as e:
            self._print_info(str(e), mode = "e")
        finally:
            self._print_info("", mode = "d")
        
        self._print_info("Initialize Chrome", mode = "p")
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--headless')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        webdriver.Chrome.__init__(self, *args, options = self.options, **kwargs)

        self.set_window_size("12000", "11000")
        self._print_info("", mode = "d")
    
    def __enter__(self):
        """ __enter__ """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ __exit__ """
        try:
            self.quit()
        except Exception as e:
            self._print_info("can not close", mode = "e")
    
    def __str__(self):
        """ __str__ """
        return "WebsiteAPI"
    
    # =========================================================================>
    # Class Method

    # =========================================================================>
    # SetGet
    @property
    def options(self):
        """ get options """
        return self.__options
    
    @options.setter
    def options(self, options):
        """ set options """
        if options is None:
            raise TypeError('invalid options')
        self.__options = options
    
    # =========================================================================>
    # Utils
    def _print_info(self, message, mode = "i"):
        """_print_info

        Args:
            message (str): printing message
            mode (str, optional): 'i' or 'w' or 'e' or 'p'. Defaults to 'i'.

        Raises:
            Exception: some of error
        """
        warnings.formatwarning = lambda message, category, *args, **kwargs: "WARN: %s ... %s" % (category.__name__, message)
        if not self.silence:
            if mode == "i":
                _message = "INFO: {:<50}".format(message)
                print(_message)
            elif mode == "w":
                warnings.warn(message, FutureWarning, stacklevel=4)
            elif mode == "e":
                _message = "ERRR: {:<50}".format(message) + " _____ errr"
                print(_message)
                raise Exception()
            elif mode == "p":
                _message = "_____ {:<50}".format(message)
                print(_message, end = " ")
            elif mode == "d":
                _message = "_____ done"
                print(_message)
    
    def wait_element(self, seconds, element_by = By.CLASS_NAME, target_string = "", timeout = 30):
        wait = WebDriverWait(self, timeout)
        element = wait.until(
            expected_conditions.presence_of_element_located(
                (element_by, target_string)
            )
        )
        time.sleep(seconds)
        return element
    
    def wait_element_clickable(self, seconds, element_by = By.CLASS_NAME, target_string = "", timeout = 30):
        wait = WebDriverWait(self, timeout)
        element = wait.until(
            expected_conditions.element_to_be_clickable(
                (element_by, target_string)
            )
        )
        time.sleep(seconds)
        return element


class TrackerWebsiteAPI(WebsiteAPI, metaclass = ABCMeta):
    """TrackerWebsiteAPI
    abstract class
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def get_match_summary(self, *args, **kwargs) -> dict:
        """get_match_summary
        Discription:
            get a list of game match summary
        Return:
            dict : game match summary
        """
        return {}

    @abstractmethod
    def get_pc_summary(self, *args, **kwargs) -> dict:
        """get_pc_summary
        Discription:
            get a list of game playable character summary
        Return:
            dict : game playable character summary
        """
        return {}

    @abstractmethod
    def get_match_url_list(self, *args, **kwargs) -> list:
        """get_match_url_list
        Discription:
            get a list of game match result url
        Return:
            list : game match result url
        """
        return []
    
    @abstractmethod
    def get_match_result(self, *args, **kwargs) -> dict:
        """get_match_result
        Discription:
            get a list of game match result
            1. call get_match_url_list
            2. get a results from url list
        Return:
            dict : game match result
        """
        return {}

    @abstractmethod
    def get_pc_url_list(self, *args, **kwargs) -> list:
        """get_pc_url_list
        Discription:
            get a list of game pc result url
        Return:
            list : game pc result url
        """
        return []
    
    @abstractmethod
    def get_pc_result(self, *args, **kwargs) -> dict:
        """get_pc_result
        Discription:
            get a list of game pc result
            1. call get_pc_url_list
            2. get a results from url list
        Return:
            dict : game pc result
        """
        return {}

# =============================================================================> 

if __name__ == "__main__":
    pass
