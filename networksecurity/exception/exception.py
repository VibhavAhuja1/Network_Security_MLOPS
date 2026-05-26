import sys
from networksecurity.logging.logger import get_logger

logger = get_logger(__name__)

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message

        _, _, exc_tb = error_details.exc_info()

        if exc_tb is None:
            self.lineno = "N/A"
            self.file_name = "N/A"
        else:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occurred in script [{self.file_name}] "
            f"line [{self.lineno}] "
            f"message [{self.error_message}]"
        )


if __name__ == '__main__':
    try:
        logger.info("Entered the try block")
        a = 1 / 0
    except Exception as e:
        exc = NetworkSecurityException(e, sys)
        logger.error(str(exc))