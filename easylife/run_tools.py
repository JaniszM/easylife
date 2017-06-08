# coding=utf-8

import sys
import os
import requests
import tarfile

from easylife import VERSION, GECKO_DIR
from easylife.transfers.run_tool import main as transfers_main
from easylife.photo_organizer.run_photo_organizer import organize_photos

GECKO_URL = "https://github.com/mozilla/geckodriver/releases/download/{0}"


def get_newest_gecko_version():
    return requests.get("https://github.com/mozilla/geckodriver/releases/latest").url.rsplit('/', 1)[-1]


def _get_geckodriver():
    gecko_v = get_newest_gecko_version()
    gecko_url = GECKO_URL.format(gecko_v)
    if os.name in ["posix"]:
        # OSX
        gecko_path = GECKO_DIR
        url = os.path.join(gecko_url, "geckodriver-{0}-macos.tar.gz".format(gecko_v))
        # elif os.name in ['nt']:
        # windows
    else:
        print("Nie rozpoznano systemu, zainstaluj geckodriver manualnie.")
        return

    gecko_filepath = os.path.join(gecko_path, "geckodriver-{0}-macos.tar.gz".format(gecko_v))

    print("Pobieranie geckodriver z {0} do {1}".format(url, gecko_path))
    with open(gecko_filepath, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print("Wystąpił problem z pobieraniem pliku: {0}".format(response))

        for block in response.iter_content(1024):
            handle.write(block)

    print("Pobrano.\nRozpakowywanie...")
    gecko_file = tarfile.open(gecko_filepath, 'r:gz')
    try:
        gecko_file.extractall(gecko_path)
    finally:
        gecko_file.close()

    print("Rozpakowano.\nPorządkowanie plików.")
    os.remove(gecko_filepath)
    # os.rename(os.path.join(gecko_path, "geckodriver"), "/usr/bin/geckodriver")

    print("Geckodriver gotowy do użycia.")


def main():
    if len(sys.argv) < 2:
        print("\nZa mało argumentów. Sprawdź 'easylife help'.\n")
        exit(1)

    tool = sys.argv[1]

    if tool in ["przelewy", "transfers"]:
        transfers_main()
    elif tool in ["photo", "zdjecia"]:
        if len(sys.argv) < 5:
            print("\nZa mało argumentów. Sprawdź 'easylife help'.\n")
            exit(1)
        params = {
            'source_dir': sys.argv[2],
            'destination': sys.argv[3],
            'template': sys.argv[4]
        }
        try:
            params['remove_source'] = bool(sys.argv[5])
        except IndexError:
            pass
        try:
            params['override_existing'] = bool(sys.argv[6])
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
              "\t\tsyntax: photo [source_dir][destination][template]([remove-source][override-existing]).\n")
    elif tool == "version":
        print("\neasylife v{0}\nCopyright 2016 by Marcin Janiszewski, janiszewski.m.a@gmail.com\n".format(VERSION))
    elif tool == "get-geckodriver":
        _get_geckodriver()
    else:
        print("Wybrano nieznane narzędzie. Wpisz 'easylife help' by zobaczyć dostępne opcje i narzędzia.")
        exit(1)

    exit(0)


if __name__ == '__main__':
    main()
