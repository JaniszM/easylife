# coding=utf-8

import os
import datetime
import json

from easylife import TOOL_DIR

VERSION = '0.1.7'
REPORT_DIR = os.path.join(TOOL_DIR, "report")
LOG_FILE = "easylife-transfers.log"

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

PLACEHOLDER_MONTH_NOW = u"$MIESIAC_TERAZ"
PLACEHOLDER_MONTH_PREV = u"$MIESIAC_POPRZ"

MONTH = datetime.datetime.now().strftime("%B")

USER_ACTION_TIMEOUT = 120
WEB_TIMEOUT = 30
BROWSER = "firefox"

# make dirs
if not os.path.isdir(REPORT_DIR):
    os.makedirs(REPORT_DIR)


def get_schema():
    with open(SCHEMA_FILE) as data_file:
        data = json.load(data_file)
    return data
