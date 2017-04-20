from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collaborator.collaborator_config_loader import CollaboratorConfigLoader
from collaborator.dummy_error.configfile_error import ConfigfileError
import threading
import time


class Collaborator(threading.Thread):
    """docstring for Collaborator."""
    def __init__(self, id, path_to_config):
        threading.Thread.__init__(self)
        self._id = id
        self._configurationLoader = CollaboratorConfigLoader(path_to_config)
        self._config = self._configurationLoader.getCollaboratorConfig()

    def getDriver(self):
        driver = None

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = self._config['chromeLocation']

        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {"driver": "ALL", "server": "ALL",
                             "browser": "ALL"}

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
        return config
