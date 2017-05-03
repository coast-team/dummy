from collections import OrderedDict
import collaborator.utils.utils as utils
import selenium
import threading
import time
import hashlib
import difflib


class MuteReadComponent(threading.Thread):
    """docstring for MuteReadComponent."""
    def __init__(self, mute_collaborator, refresh_rate, driver, splitter,
                 path_to_record):
        threading.Thread.__init__(self)
        self.__mute_collaborator = mute_collaborator
        self.__refresh_rate = refresh_rate / 1000.0
        self.__driver = driver
        self.__splitter = splitter
        self.__path_to_record = path_to_record
        self.__alive = False
        self.__last_hash = ""
        self.__last_content = [""]
        self.__records = OrderedDict()
        utils.clearFile(self.__path_to_record)
        utils.writeLine(self.__path_to_record, 'READER')

    def run(self):
        self.__alive = True
        try:
            while self.__alive:
                content = self.__driver.execute_script(
                    "return muteTest.getText(0)")
                timestamp = str(utils.getTime())
                self.readContent(content, timestamp)
                time.sleep(self.__refresh_rate)

            utils.saveRecords(self.__path_to_record, self.__records)
            utils.writeLine(self.__path_to_record,
                            'HASH %s' % self.__last_hash)
            utils.saveLogs(self.__path_to_record,
                           'browser',
                           self.__driver.get_log('browser'))
            utils.saveLogs(self.__path_to_record,
                           'driver',
                           self.__driver.get_log('driver'))
            utils.saveLogs(self.__path_to_record,
                           'server',
                           self.__driver.get_log('server'))
        except selenium.common.exceptions.WebDriverException:
            self.__mute_collaborator.reportError(
                '[Mute-reader] Webdriver Error')
        finally:
            self.__driver.close()

    def kill(self):
        self.__alive = False

    def readContent(self, content, timestamp):
        hash_content = utils.hashContent(content)

        if self.__last_hash != hash_content:
            split_content = content.split(self.__splitter)
            split_content.reverse()

            diff = difflib.ndiff(self.__last_content, split_content)
            record = utils.basicShape(diff)
            print(str(timestamp) + ' ' + str(record))
            self.__records[timestamp] = record

            self.__last_hash = hash_content
            self.__last_content = split_content
