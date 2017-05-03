from collections import OrderedDict
import collaborator.utils.utils as utils
import selenium
import threading
import random
import string
import time


class MuteWriteComponent(threading.Thread):
    """docstring for MuteWriteComponent."""
    def __init__(self, mute_collaborator, driver, splitter,  path_to_record,
                 writingSpeed=5):
        threading.Thread.__init__(self)
        self.__mute_collaborator = mute_collaborator
        self.__alive = False
        self.__driver = driver
        self.__splitter = splitter
        self.__path_to_record = path_to_record
        self.__word = ''.join(
            random.choice(string.ascii_uppercase) for _ in range(writingSpeed
                                                                 - 1))
        self.__records = OrderedDict()
        utils.clearFile(self.__path_to_record)
        utils.writeLine(self.__path_to_record, 'WRITER')

    def run(self):
        self.__alive = True
        count = 0
        word_to_type = self.__word + self.__splitter
        try:
            while self.__alive:
                word_to_type = utils.generateWord(count,
                                                  self.__word,
                                                  len(self.__word))
                timestamp = utils.getTime()
                self.__driver.execute_script("muteTest.insert(10, '%s')"
                                             % word_to_type)
                self.__records[timestamp] = ['+ ' + word_to_type[:-1]]
                count += 1
                time.sleep(1)

            utils.saveRecords(self.__path_to_record, self.__records)

            content = self.__driver.execute_script(
                "return muteTest.getText(0)")
            hash_content = utils.hashContent(content)

            utils.writeLine(self.__path_to_record, 'HASH %s' % hash_content)
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
                '[Mute-writer] Webdriver Error')
        finally:
            self.__driver.close()

    def kill(self):
        self.__alive = False
