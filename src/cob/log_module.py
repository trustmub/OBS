import logging
import os

LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
UPLOAD_FOLDER = os.path.abspath("logs//logs_file.log")
logging.basicConfig(filename=UPLOAD_FOLDER, level=logging.DEBUG, format=LOG_FORMAT)


class SystemOBS:
    """This is a logging class which takes in a messages where logging is required"""

    def __init__(self):
        self.logger = logging.getLogger()

    def start_logging(self, message):
        """
        THe start Logging function takes in one parameter, message, specifying specific thing to log like error
        messages on try catch blocks
        """
        self.logger.info(message)
