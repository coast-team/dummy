from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collaborator.config_loader import ConfigLoader
from collaborator.dummy_error.configfile_error import ConfigfileError
from pyvirtualdisplay import Display
from easyprocess import EasyProcessCheckInstalledError
import threading
import time


class Collaborator(threading.Thread):
    """docstring for Collaborator."""
    def __init__(self, id, path_to_config):
        threading.Thread.__init__(self)
        self._id = id
        self._configurationLoader = ConfigLoader(path_to_config)
        self._config = self._configurationLoader.getCollaboratorConfig()
        self.__display = None
        self._errors = []
        if self._config['noDisplay']:
            try:
                self.__display = Display(visible=0, size=(800, 600))
                self.__display.start()
            except EasyProcessCheckInstalledError:
                self.__display = None
                self.reportError('Xvfb is not installed')
                print("L'environnement Xvfb n'est pas installé")

    def getDriver(self):
        driver = None

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = self._config['chromeLocation']

        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {"driver": "ALL", "browser": "ALL"}

        service_args = ["--verbose"]
        driver = webdriver.Chrome(
            self._config['chromeDriverLocation'],
            chrome_options=chrome_options,
            desired_capabilities=d,
            service_args=service_args)
        driver.get(self._config['url'])
        time.sleep(self._config['loadingTime'])

        return driver

    def getConfig(self):
        config = {}
        config['status'] = 'RUNNING'
        config['url_targeted'] = self._config['url']
        config['errors'] = self._errors
        return config

    def reportError(self, msg):
        self._errors.append(msg)

    def getErrors(self):
        return self._errors

    def stopDisplay(self):
        print("ert")
        self.__display.stop()

    def killReader(self):
        pass
    
    def killWriter(self):
        pass
