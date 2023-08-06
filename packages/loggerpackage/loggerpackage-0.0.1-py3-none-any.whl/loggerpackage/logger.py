import logging
import sys


def init_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    MSG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=MSG_FORMAT, datefmt=DATETIME_FORMAT)
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root

logger = init_logger()
