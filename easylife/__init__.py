import os
import logging

VERSION = "0.2.0"

TOOL_DIR = os.path.join(os.getenv("HOME"), "easylife")
WORKING_DIR = ""
LOG_FILE = os.path.join(TOOL_DIR, "logs", "easylife.log")

if not os.path.exists(TOOL_DIR):
    os.makedirs(TOOL_DIR)


def get_logger(module_name, log_file=LOG_FILE, log_level=logging.DEBUG):
    log_file = os.path.join(TOOL_DIR, "logs", log_file)
    path = os.path.dirname(log_file)
    if not os.path.isdir(path):
        os.makedirs(path)

    # create logger
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)7s | %(name)-30s | %(message)s"))
    logger.addHandler(stream_handler)

    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)7s | %(name)-30s | %(message)s"))
    logger.addHandler(fh)

    return logger
