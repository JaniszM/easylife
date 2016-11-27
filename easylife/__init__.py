# coding=utf-8

import os
import logging
import datetime
import json

WORKING_DIR = ""

LOG_DIR = os.path.join(WORKING_DIR, "logs")
REPORT_DIR = os.path.join(WORKING_DIR, "report")

LOG_FILE = os.path.join(LOG_DIR, "bank_transfers.log")
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data_schema.json")
DEFAULT_USER_FILENAME = "my_transfers.json"

MONTHS_TO_PL = {
    'January': u"Styczeń",
    'February': u"Luty",
    'March': u"Marzec",
    'April': u"Kwiecień",
    'May': u"Maj",
    'June': u"Czerwiec",
    'July': u"Lipiec",
    "August": u"Sierpień",
    "September": u"Wrzesień",
    "October": u"Październik",
    "November": u"Listopad",
    "December": u"Grudzień"
}

PLACEHOLDER_MONTH_NOW = u"$MIESIAC_POPRZ"
PLACEHOLDER_MONTH_PREV = u"$MIESIAC_TERAZ"

MONTH = datetime.datetime.now().strftime("%B")

USER_ACTION_TIMEOUT = 90
WEB_TIMEOUT = 10
BROWSER = "firefox"

with open(SCHEMA_FILE) as data_file:
    data = json.load(data_file)
SCHEMA = data

# make dirs
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.isdir(REPORT_DIR):
    os.makedirs(REPORT_DIR)


def get_logger(module_name):
    # create logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)7s | %(name)-30s | %(message)s"))
    logger.addHandler(stream_handler)

    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)7s | %(name)-30s | %(message)s"))
    logger.addHandler(fh)

    return logger
