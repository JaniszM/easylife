# coding=utf-8

import sys
import os
import requests
import tarfile

from easylife import VERSION, TOOL_DIR, get_logger
from easylife.transfers import VERSION as VERSION_TRASFER
from easylife.transfers.run_tool import main as transfers_main
from easylife.photo_organizer import VERSION as VERSION_PHOTO
from easylife.photo_organizer.run_photo_organizer import organize_photos

LOG = get_logger(__name__)

GECKO_URL = "https://github.com/mozilla/geckodriver/releases/download/{0}"


def get_newest_gecko_version():
    return requests.get("https://github.com/mozilla/geckodriver/releases/latest").url.rsplit('/', 1)[-1]


def _get_geckodriver():
    gecko_v = get_newest_gecko_version()
    gecko_url = GECKO_URL.format(gecko_v)
    if os.name in ["posix"]:
        # OSX
        gecko_path = TOOL_DIR
        url = os.path.join(gecko_url, "geckodriver-{0}-macos.tar.gz".format(gecko_v))
        # elif os.name in ['nt']:
        # windows
    else:
        LOG.error("Nie rozpoznano systemu, zainstaluj geckodriver manualnie.")
        return

    gecko_filepath = os.path.join(gecko_path, "geckodriver-{0}-macos.tar.gz".format(gecko_v))

    LOG.info("Pobieranie geckodriver z {0} do {1}".format(url, gecko_path))
    with open(gecko_filepath, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            LOG.error("Wystąpił problem z pobieraniem pliku: {0}".format(response))

        for block in response.iter_content(1024):
            handle.write(block)

    LOG.info("Pobrano. Rozpakowywanie...")
    gecko_file = tarfile.open(gecko_filepath, 'r:gz')
    try:
        gecko_file.extractall(gecko_path)
    finally:
        gecko_file.close()

    LOG.info("Rozpakowano. Porządkowanie plików...")
    os.remove(gecko_filepath)
    # os.rename(os.path.join(gecko_path, "geckodriver"), "/usr/bin/geckodriver")

    LOG.info("Geckodriver gotowy do użycia.")


def main():
    if len(sys.argv) < 2:
        print("\nZa mało argumentów. Sprawdź 'easylife help'.\n")
        exit(1)

    tool = sys.argv[1]

    if tool in ["przelewy", "transfers"]:
        transfers_main()
    elif tool in ["photo", "zdjecia"]:

        def check_opt(arg):
            if arg == 'remove-source':
                params['remove_source'] = True
            elif arg == 'overwrite-existing':
                params['overwrite_existing'] = True

        if len(sys.argv) < 5:
            print("\nZa mało argumentów. Sprawdź 'easylife help'.\n")
            exit(1)
        params = {
            'source_dir': os.path.expanduser(sys.argv[2]),
            'destination': os.path.expanduser(sys.argv[3]),
            'template': sys.argv[4]
        }
        try:
            check_opt(sys.argv[5])
            check_opt(sys.argv[6])
        except IndexError:
            pass

        organize_photos(**params)
    elif tool == "help":
        print("\neasylife [opcja]|[narzędzie]:"
              "\nDostępne opcje:"
              "\n\thelp - wyświetla pomoc,"
              "\n\tversion - wyświetla wersję programu."
              "\n\tget-geckodriver - pobiera i przygotowuje geckodriver do użycia.\n\n"
              "Dostępne narzędzia:"
              "\n\tprzelewy - uruchamia narzędzie 'przelewy'.\n"
              "\n\tphoto - organizer zdjęć:"
              "\t\tsyntax: photo [source_dir][destination][template]([remove-source][overwrite-existing]).\n")
    elif tool == "version":
        print("\neasylife v{0}\ntransfers v{1}\nphoto v{2}\nCopyright 2017 by Marcin Janiszewski,"
              " janiszewski.m.a@gmail.com\n".format(VERSION, VERSION_TRASFER, VERSION_PHOTO))
    elif tool == "get-geckodriver":
        _get_geckodriver()
    else:
        print("Wybrano nieznane narzędzie. Wpisz 'easylife help' by zobaczyć dostępne opcje i narzędzia.")
        exit(1)

    exit(0)


if __name__ == '__main__':
    main()
