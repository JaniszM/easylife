# coding=utf-8

import os
import datetime
import json
from copy import deepcopy
from Tkinter import Tk, Frame, BOTH, Button, Label, Entry, Toplevel, Message
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jsonschema import validate

from easylife import WORKING_DIR, MONTHS_TO_PL, MONTH, SCHEMA, get_logger, PLACEHOLDER_MONTH_NOW, \
    PLACEHOLDER_MONTH_PREV, REPORT_DIR, USER_ACTION_TIMEOUT, WEB_TIMEOUT, BROWSER, DEFAULT_USER_FILENAME

LOG = get_logger(__name__)

USER_DATA_FILE = os.path.join(WORKING_DIR, DEFAULT_USER_FILENAME)
CONFIG_FILE = os.path.join(WORKING_DIR, "bank_config")
OK_SHOT = os.path.join(REPORT_DIR, 'success_shot_' + datetime.datetime.now().isoformat() + ".jpg")
FAIL_SHOT = os.path.join(REPORT_DIR, 'exception_shot_' + datetime.datetime.now().isoformat() + ".jpg")


def _store_config(data):
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(data, outfile, encoding="utf-8")


def load_config():
    if not os.path.isfile(CONFIG_FILE):
        # first run
        _store_config({
            "user_timeout": USER_ACTION_TIMEOUT,
            "web_timeout": WEB_TIMEOUT,
            "browser": BROWSER,
            "user_data_filename": DEFAULT_USER_FILENAME
        })

    with open(CONFIG_FILE) as data_file:
        cfg = json.load(data_file, encoding="utf-8")

    try:
        month = cfg['month']
        if month != MONTH:
            # new month, reset payments
            for i in cfg['payments']:
                cfg['payments'][i] = False
            with open(CONFIG_FILE, 'w') as outfile:
                json.dump(cfg, outfile, encoding="utf-8")
    except KeyError:
        pass
    return cfg


# loads config
config = load_config()

# time that user needs to do some operations like logging in or providing sms code
try:
    USER_ACTION_TIMEOUT = config['user_timeout']
except KeyError:
    USER_ACTION_TIMEOUT = 90

# time before the most heave page should be loaded
try:
    WEB_TIMEOUT = config['web_timeout']
except KeyError:
    WEB_TIMEOUT = 10

# user browser
try:
    BROWSER = config['browser']
except KeyError:
    BROWSER = "firefox"

# user data file
try:
    DEFAULT_USER_FILENAME = config['user_data_filename']
except KeyError:
    pass


def load_user_transfers_data():
    if os.path.isfile(USER_DATA_FILE):
        with open(USER_DATA_FILE) as data_file:
            user_data = json.load(data_file, encoding="utf-8")
        validate(user_data, SCHEMA)
        return user_data
    else:
        LOG.warn("Nie znaleziono pliku danych użytkownika: " + USER_DATA_FILE)


def write_to_config(transfer_name, status):
    try:
        config['payments'][transfer_name] = status
    except KeyError:
        config['payments'] = {transfer_name: status}

    if config.get('month') != MONTH:
        config['month'] = MONTH
    _store_config(config)


class Transfer(object):
    # mbank locators
    LOCATOR_LOGIN = "//a[@class='button ind']"
    LOCATOR_LOGOUT = "//i[@class='icon-white-logout']"
    LOCATOR_ADD_BOOK = "//li[@data-id='AddressBook']/a[@href='#/AddressBook']"
    LOCATOR_RECORDS_LIST = "//ul[@id='records']"
    LOCATOR_RECORDS = LOCATOR_RECORDS_LIST + "/li[@id]/h3/strong[@class='name']"

    LOCATOR_TRANSFER_DO = "makeTransfer"
    LOCATOR_TRANSFER_AMOUNT = "amount"
    LOCATOR_TRANSFER_TITLE = "title"
    LOCATOR_TRANSFER_SUBMIT = "//a[contains(@id, 'submit') and @name='submit']"
    LOCATOR_TRANSFER_SEND = "//a[contains(@class, 'proceed-action') and @title='Wyślij przelew']"
    LOCATOR_TRANSFER_STATUS = "//div[contains(@class, 'box-status') and contains(@class, 'success')" \
                              " and contains(@class, 'transfer-summary')]"
    LOCATOR_TRANSFER_STATUS_OK = LOCATOR_TRANSFER_STATUS + "/h2"
    LOCATOR_TRANSFER_STATUS_AMOUNT = LOCATOR_TRANSFER_STATUS + "/ul/li/span[@class='amount']"
    LOCATOR_TRANSFER_STATUS_CURR = LOCATOR_TRANSFER_STATUS + "/ul/li/span[@class='currency']"

    def __init__(self):
        self.driver = webdriver.Firefox()

    def _dump_exception(self, error):
        LOG.error(error)
        self.driver.save_screenshot(FAIL_SHOT)

    def wait_for_element_and_get_it(self, locator, locator_type=By.XPATH, timeout=WEB_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((locator_type, locator)))

    def check_transfer_confirmation(self, amount_of_transfer, is_sms_confirmation=True):
        """
        Awaits for user action until he provides correct data.

        :param amount_of_transfer: the amount of money transfered and then should be same amount validated.
        :type amount_of_transfer: float
        :param is_sms_confirmation: if true then uses user timeout for validating mbank confirmation.
        :type is_sms_confirmation: bool
        """
        if is_sms_confirmation is True:
            timeout = USER_ACTION_TIMEOUT
        else:
            timeout = WEB_TIMEOUT

        LOG.info("Oczekiwanie na potwierdzenie przelewu.")
        try:
            status = self.wait_for_element_and_get_it(self.LOCATOR_TRANSFER_STATUS_OK, timeout=timeout).text

            LOG.info("Weryfikacja potwierdzenia...")
            if status != u"Przelew został zrealizowany":
                raise Exception(u"Błędny status przelewu: " + status)

            status = self.driver.find_element_by_xpath(self.LOCATOR_TRANSFER_STATUS_AMOUNT).text
            if unicode(amount_of_transfer) != status.replace(u",", u"."):
                raise Exception(u"Błędna kwota potwierdzenia przelewu: " + status)

            status = self.driver.find_element_by_xpath(self.LOCATOR_TRANSFER_STATUS_CURR).text
            if u"PLN" != status:
                raise Exception(u"Błędna waluta przelewu: " + status)

        except TimeoutException as err:
            self._dump_exception("Nie potwierdzono wykonania przelewu. Sprawdź dokładnie logi czy rzeczywiście"
                                 " nie zostął potwierdzony czy może mbnak zmienił frontend i nie znaleziono elementów.")
            LOG.error(err)
            raise err

        LOG.info("Potwierdzono.")

    def mbank_login(self):
        LOG.info("logowanie do mbanku...")

        if self.driver is None:
            self.__init__()

        self.driver.get("http://mbank.pl")
        self.driver.find_element_by_xpath(self.LOCATOR_LOGIN).click()

        # wait here until user gives credentials
        try:
            self.wait_for_element_and_get_it(self.LOCATOR_ADD_BOOK, timeout=USER_ACTION_TIMEOUT)
            LOG.info("... zalogowano.")
        except TimeoutException as err:
            self._dump_exception("Nie znaleziono elementow obecnych po zalogowaniu do mbanku."
                                 " Upewnij sie ze nastapilo poprawne logowanie.")
            self.driver.quit()
            self.driver = None
            raise err

    def mbank_logout(self):
        LOG.info("Wylogowywanie z mbanku, sprawdź logi ;)")
        self.driver.find_element_by_xpath(self.LOCATOR_LOGOUT)

    def do_transfer(self, data):
        """
        Do a transfer in mbank. Requires to login into account before.

        :param data: Data of the transfer.
        :type data: dict
        :return: Status of the operation. True if was found confirmation about transfer. Otherwise False.
        :rtype: bool
        """
        ok = False
        name = data['odbiorca']
        LOG.info(u"Wybieranie rachunku '{0}' z książki adresowej.".format(name))

        try:
            # open address book
            self.wait_for_element_and_get_it(self.LOCATOR_ADD_BOOK).click()
            # find correct record
            self.wait_for_element_and_get_it(self.LOCATOR_RECORDS_LIST)
            records = self.driver.find_elements(By.XPATH, self.LOCATOR_RECORDS)
            for record in records:
                if unicode(record.text) == name:
                    LOG.info(u"Odnaleziono odbiorcę '{0}' w książce adresowej.".format(name))
                    # load bookmark record
                    record.click()

                    # load transfer form
                    LOG.info("Ładowanie formularza.")
                    self.wait_for_element_and_get_it(self.LOCATOR_TRANSFER_DO, By.ID).click()

                    # enter data
                    LOG.info("Wypełnianie danych.")
                    web_el = self.wait_for_element_and_get_it(self.LOCATOR_TRANSFER_AMOUNT, By.ID)
                    web_el.clear()
                    web_el.send_keys(str(data['kwota']))
                    web_el = self.driver.find_element_by_id(self.LOCATOR_TRANSFER_TITLE)
                    web_el.clear()
                    web_el.send_keys(data[u'tytuł'])

                    # accept transfer operation
                    LOG.info("Zatwierdzanie tranzakcji.")
                    self.driver.find_element_by_xpath(self.LOCATOR_TRANSFER_SUBMIT).click()

                    # if sms confirmation code is disabled then send transfer instead of waiting for user action
                    sms = data.get('sms')
                    if sms is not None and not sms:
                        self.wait_for_element_and_get_it(self.LOCATOR_TRANSFER_SEND).click()
                    else:
                        sms = True

                    # validate confirmation
                    self.check_transfer_confirmation(data[u'kwota'], sms)
                    self.driver.save_screenshot(OK_SHOT)
                    return True
            LOG.error(u"Nie odnaleziono rachunku '{0}' w książce adresowej.".format(name))
        except TimeoutException as err:
            self._dump_exception("Nie odnaleziono jakiegoś elementu na stronie mbank :/")
            LOG.error(err)
            # self.mbank_logout()

        return ok

    def do_transfers(self, transfers):
        """
        Performs all transfers in mbank.

        ..note: Encoding data is UTF-8.

        :param transfers: List of the transfers to do.
                e.g.: {['UPC']: {"kwota": "23.5", "tytuł": "jakis badziew do zusu", 'odbiorca': "Stefan"},
                      ['Przedszkole']: {"kwota": "234", "tytuł": "kolejny rozbój", 'odbiorca': "Seba"}}
        :type transfers: dict
        """
        try:
            self.mbank_login()
            for key, val in transfers.iteritems():
                try:
                    status = self.do_transfer(val)
                    if not status:
                        LOG.warn(u"Kwota {0}zł na rachunek '{1}' nie zostala pomyslnie przelana."
                                 .format(val['kwota'], val['odbiorca']))
                    else:
                        LOG.info(u"Wykonano poprawnie przelew za '{0}'.".format(val['odbiorca']))
                    write_to_config(key, status)
                except Exception as err:
                    write_to_config(key, False)
                    raise err
        except Exception as err:
            # log all not caught exceptions
            self._dump_exception(err)
            raise err
        finally:
            self.mbank_logout()
            self.driver.quit()
            self.driver = None


class ShowStuff(Frame):
    """
    Very simple GUI to have info about at least few data transfers.
    """
    makeTransfer = None

    def __init__(self, parent):

        def make_good_caption(name):
            try:
                status = config['payments'][name]
            except KeyError:
                status = None

            if status is True:
                return {
                    'text': u"Zapłacono :)",
                    'fg': "#006600"
                }
            else:
                return {
                    'text': u"Nie zapłaciłeś w tym miesiącu!!!",
                    'fg': "#cc0000"
                }

        Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.parent.title(u"Zapłać cholerne rachunki!")
        self.pack(fill=BOTH, expand=1)
        self.center(self.parent)
        self.parent.focus()

        y_pos = 10
        label_info = Label(self, text="Kwota")
        label_info.place(x=160, y=y_pos + 2)
        # label_info.pack()

        self.widgets = dict()

        self.user_data = load_user_transfers_data()

        # make widget groups for each transfer data
        try:
            for val in self.user_data['przelewy']:
                # skip transfer if is disabled
                try:
                    if val['aktywny'] is False:
                        continue
                except KeyError:
                    pass
                y_pos += 30
                label1 = Label(self, text=val['nazwa'])
                label1.place(x=5, y=y_pos + 2)
                entry = Entry(self, width=10)
                entry.place(x=160, y=y_pos)
                label2 = Label(self, **make_good_caption(val['nazwa']))
                label2.place(x=245, y=y_pos + 2)
                self.widgets[val['nazwa']] = {
                    'label1': label1,
                    'entry': entry,
                    'label2': label2
                }
        except TypeError:
            # if self.user_data['przelewy'] not found
            pass

        y_pos += 30
        quit_button = Button(self, text="Execute Order 66", command=self.execute_order_66)
        quit_button.place(x=5, y=y_pos)

        author = Label(self, text="Copyright by Janiszewski Marcin: janiszewski.m.a@gmail.com", fg="#003399")
        author.place(x=120, y=425)

    @staticmethod
    def center(handle, w=500, h=450):
        """
        Centers given handle window.
        """
        sw = handle.winfo_screenwidth()
        sh = handle.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        handle.geometry('%dx%d+%d+%d' % (w, h, x, y))
        handle.focus()

    def execute_order_66(self):
        """
        Reads data from input widgets and builds up list of the transfers to perform by Transfer class.
        """
        if self.user_data is None or self.user_data['przelewy'] is None:
            return

        date_now = datetime.datetime.now()
        month_now = MONTHS_TO_PL[date_now.strftime("%B")]
        month_previous = MONTHS_TO_PL[(date_now.replace(day=1) - datetime.timedelta(days=1)).strftime("%B")]
        transfers = dict()
        try:
            # check all user transfers to process
            for transfer in self.user_data['przelewy']:
                # skip transfer if is disabled
                try:
                    if transfer['aktywny'] is False:
                        continue
                except KeyError:
                    pass
                # get name of transfer
                name = transfer['nazwa']
                try:
                    # get cost of transfer from GUI widget, if not exist them must be inactive
                    amount = self.widgets[name]['entry'].get()
                    if amount:
                        amount = float(amount)
                    else:
                        amount = 0
                except KeyError:
                    continue
                # get info about payment did for current transfer
                try:
                    is_payed = config['payments'][name]
                except KeyError:
                    is_payed = False

                # if there is something to transfer and it wasn't transfered yet, do it
                if amount > 0 and is_payed is not True:
                    # copy user transfer data and extend it by GUI set up
                    transfers[name] = deepcopy(transfer)
                    transfers[name]['kwota'] = amount
                    # replace placeholders
                    transfers[name][u'tytuł'] = transfers[name][u'tytuł'] \
                        .replace(PLACEHOLDER_MONTH_PREV, month_previous).replace(PLACEHOLDER_MONTH_NOW, month_now)

        except ValueError as err:
            LOG.error(err)
            raise err

        if len(transfers) > 0:
            # create new window with summary and confirmation for operations
            confirm = Toplevel()
            confirm.title("Potwierdzenie danych")
            size = (len(transfers) * 50) + 80
            self.center(confirm, 450, size)

            info = ""
            for key, val in transfers.iteritems():
                info += u"Zamierzasz zaplacic {0}zł za '{1}', tytułem:\n{2}\n\n".format(unicode(val['kwota']),
                                                                                        key,
                                                                                        val[u'tytuł'])

            msg = Message(confirm, text=info, width=440)
            msg.pack()

            btn_confirm = Button(confirm, text="Idź do banku", command=lambda: self.go(transfers, confirm))
            btn_cancel = Button(confirm, text="Nie chcę!!!", command=confirm.destroy)
            btn_confirm.pack()
            btn_cancel.pack()

    def go(self, rachunki, cb):
        cb.destroy()
        if self.makeTransfer is None:
            self.makeTransfer = Transfer()
        self.makeTransfer.do_transfers(rachunki)


def main():
    # run GUI
    try:
        root = Tk()
        ShowStuff(root)
        root.mainloop()
    except Exception as err:
        # log all not caught exceptions
        LOG.error(err)
        raise err
