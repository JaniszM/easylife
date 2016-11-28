# coding=utf-8

import sys

from easylife import VERSION
from easylife.transfers.run_tool import main as transfers_main


def main():
    if len(sys.argv) < 2:
        print("\nZa mało argumentów. Sprawdź 'easylife help'.\n")
        exit(1)

    tool = sys.argv[1]

    if tool in ["przelewy", "transfers"]:
        transfers_main()
    elif tool == "help":
        print("\nDostępne opcje:\n\thelp - wyświetla pomoc,\n\tversion - wyświetla wersję programu.\n\n"
              "Dostępne narzędzia:\n\tprzelewy - uruchamia narzędzie 'przelewy'.\n")
    elif tool == "version":
        print("\neasylife v{0}\nCopyright 2016 by Marcin Janiszewski, janiszewski.m.a@gmail.com\n".format(VERSION))
    else:
        print("Wybrano nieznane narzędzie. Wpisz 'easylife help' by zobaczyć dostępne opcje i narzędzia.")
        exit(1)

    exit(0)
