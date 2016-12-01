# coding=utf-8

import sys
import os
import requests
import tarfile

from easylife import VERSION
from easylife.transfers.run_tool import main as transfers_main

GECKO_VER = "0.11.1"
GECKO_URL = "https://github.com/mozilla/geckodriver/releases/download/v{0}".format(GECKO_VER)


def _get_geckodriver():
    if os.name in ["posix"]:
        # OSX
        gecko_path = "/usr/bin"
        url = os.path.join(GECKO_URL, "geckodriver-v{0}-macos.tar.gz".format(GECKO_VER))
        # elif os.name in ['nt']:
        # windows
    else:
        print("Nie rozpoznano systemu, zainstaluj geckodriver manualnie.")
        return

    gecko_filepath = os.path.join(gecko_path, "geckodriver-v{0}-macos.tar.gz".format(GECKO_VER))

    print("Pobieranie geckodriver z {0}...".format(url))
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
    os.rename(os.path.join(gecko_path, "geckodriver"), "/usr/bin/geckodriver")

    print("Geckodriver gotowy do użycia.")


def main():
    if len(sys.argv) < 2:
        print("\nZa mało argumentów. Sprawdź 'easylife help'.\n")
        exit(1)

    tool = sys.argv[1]

    if tool in ["przelewy", "transfers"]:
        transfers_main()
    elif tool == "help":
        print("\neasylife [opcja]|[narzędzie]:"
              "\nDostępne opcje:\n\thelp - wyświetla pomoc,\n\tversion - wyświetla wersję programu.\n\n"
              "Dostępne narzędzia:\n\tprzelewy - uruchamia narzędzie 'przelewy'.\n")
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
