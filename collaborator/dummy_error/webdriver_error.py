class WebdriverError(Exception):
    """docstring for WebdriverError."""
    def __init__(self, msg="Config file is not well formatted"):
        self.__msg = msg

    def __str__(self):
        return self.__msg
