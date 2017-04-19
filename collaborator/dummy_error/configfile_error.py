class ConfigfileError(Exception):
    """docstring for ConfigfileError."""
    def __init__(self, msg="Config file is not well formatted"):
        self.__msg = msg

    def __str__(self):
        return self.__msg
