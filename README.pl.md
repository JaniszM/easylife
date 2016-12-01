Przeczytaj w innym języku: [English](README.md), [Polski](README.pl.md).

Moduł grupujący różne użyteczne narzędzia/skrypty mające ułatwić Ci życie. Automatyzuje te same rzeczy, które wykonujesz każdego dnia.

Dostępne języki interfejsu użytkownika oraz całego narzędzia **easylife**:
- polski.

Wspierane systemy operacyjne:
- OSX
- Linux

TOC:

- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Uruchomienie](#uruchomienie)
- [Narzędzia i Skrypty](#narzędzia-i-skrypty)
    - [Przelewy](#przelewy)
        - [Wymagania](#wymagania)
        - [Konfiguracja](#konfiguracja)
        - [Uruchomienie](#uruchomienie)
        - [Użycie](#użycie)
        - [Wsparcie dla użytkownika](#wsparcie-dla-użytkownika)
- [Pomoc i Ulepszenia](#pomoc-i-ulepszenia)
    
# Wymagania

- Python 2.7
- geckodriver

# Instalacja

Jeżeli nie posiadasz Pythona zainstaluj: **https://www.python.org/downloads/**

Zainstalować paczkę:
```
pip install easylife
```

Jeżeli masz jakieś problemy z instalacją, upewnij się, że masz najnowszą wersje ```pip```. Jeżeli jej nie masz to uaktualnij według instrukcji ```pip```.

Potrzebujesz również geckodriver. Jeżeli masz już jeden to możesz spróbować go użyć, wystarczy, że będzie dodany do zmiennej systemowej PATH lub przeniesiony do:
`/usr/bin` dla systemów OSX i Linux.

Jeżeli nie masz geckodriver możesz spróbować doinstalować przez:
```
sudo easylife get-geckodriver
```
Wymagane są prawa admina ponieważ sterownik zostanie przeniesiony do katalogu `/usr/bin`, który zwykle nie daje dostępu z poziomu zwykłego użytkownika.

# Konfiguracja

Narzędzie korzysta z plików konfiguracji oraz różnych plików danych. Pierwsze uruchomienie spowoduje utworzenie pliku konfiguracji danego skryptu w katalogu, z którego został wywołany **easylife**.

Narazie nie ma możliwości skonfigurowania stałego katalogu dla **easylife**. *Prace w toku.*
Stwórz sobie jakiś katalog dla danych i odpalaj zawsze tam narzędzie.

# Uruchomienie

Poniżej przedstawiony jest sposób uruchomiania każdego z narzędzi/skryptów wbudowanych w **easylife**.

Po zainstalowaniu paczki zostanie dodany alias ```easylife``` do katalogu ```bin``` twojego interpretera Python. Alias powinien być dostępny z poziomu powłoki systemu. Jeżeli z jakiegoś powodu nie jest, upewnij się, że katalog ```bin``` twojego Pythona jest dodany to zmiennej systemowej ```PATH```.
Jeżeli ```PATH``` jest poprawnie skonfigurowany wywołaj:
```
easylife <narzędzie>

np.:
easylife przelewy
```

# Narzędzia i Skrypty

Poniżej znajduje się opis każdego z narzędzi/skryptów zaimplementowanych w **easylife**.

Obecnie dostępne:
- przelewy

## Przelewy

Bazuje na API **[selenium](http://docs.seleniumhq.org/)**. Oznacza to, że wykorzystuje strukturę strony HTTP hostowaną przez bank. W przypadku zmiany tej struktury przez bank *przelewy* mogą przestać odnajdywać właściwe elementy. **Jeżeli spotkasz się z tym problemem to załóż nowy 'issue'**.
Zmiana będzie wprowadzona tak szybko jak to tylko możliwe.

Posiada interfejs graficzny (GUI).
Wykonuje szereg przelewów zdefiniowanych przez użytkownika.
Waliduje wykonany przelew pod kątem kwoty oraz waluty. Jeżeli dane nie będą się zgadzać otrzymasz odpowiedni raport. Walidacja pozwala stwierdzić również obecność niektórych wirusów na twoim komputerze np.: podmieniających dane w formach danych strony banku na twojej przeglądarce.
Narzędzie wyposażone jest w **szczegółowe logi** oraz **zrzuty ekranów** dla każdej operacji. Więcej szczegółów tu [Wsparcie dla użytkownika](#wsparcie-dla-uzytkownika).

Obecnie zakłada się, że okresem rozliczeniowym jest dany miesiąc. Z każdym nowym miesiącem rozpoczyna się nowy okres.
Narzędzie **przelewy** nie wykona przelewu, który został już wykonany w danym okresie rozliczeniowym. Informacja o tym stanie podawana jest użytkownikowi.

**UWAGA:** Ze względów bezpieczeństwa narzędzie nie przechowuje żadnych wrażliwych danych jak hasła do banku.

Obecnie wspierane interfejsy banków:
- mbank \(wersja polska\) **https://www.mbank.pl/indywidualny/**

### Wymagania

1. Należy mieć zainstalowaną przynajmniej jedną z przeglądarek podanych niżej.

    Obecnie wspierane przeglądarki:
    - Firefox
    
    Przetestowane przeglądarki:
    - Firefox

2. Na stronie banku w książce adresowej muszą być zdefiniowani odbiorcy, do których chcesz rozesłać przelewy. Nazwa w książce musi się zgadzać z nazwami przelewów z pól "odbiorca" w pliku danych. Oczywiście w książce musi być zdefiniowany poprawny numer konta bankowego odbiorcy.

### Konfiguracja

Plik konfiguracji ```transfers_config```. W przypadku braku pliku zostanie utworzony nowy z domyślnymi wartościami.

Opcje:

- *web_timeout*: Definiuje czas oczekiwania (sekundy) skryptu na załadowanie strony.

    Domyślna wartość to 10.
    Jeżeli twoje połączenie jest wolne bądź dostajesz błędy o nie odnalezionych elementach strony spróbuj zwiększyć tę wartość.
    
- *user_timeout*: Definiuje czas oczekiwania (sekundy) skryptu na akcję użytkownika taką jak logowanie.

    Domyślna wartość to 90.
    
    Obecne akcje użytkownika:
    - logowanie do banku,
    - potwierdzenie przelewu kodem sms.
    
    Jeżeli z jakiegoś powodu nie nadążasz czegoś wykonać zwiększ tę wartość.
    
- *browser*: przeglądarka używana przez narzędzie.

    Domyślna wartość to "firefox".
    
- *payments*: Informacje na temat wykonany przelewów w danym okresie rozliczeniowym.
    **NIE MODYFIKOWAĆ!!!**
    
- *month*: miesięczny okres rozliczeniowy. Określa obecny miesiąc. W przypadku zmiany miesiąca rozpoczyna się nowy okres.
    **NIE MODYFIKOWAĆ!!!**

Plik danych ```my_transfers.json``` (Wymagany). Jest to plik, który definiuje dokładnie jakie przelewy i jak mają zostać wykonane. Jest zapisany w konwencji JSON oraz opisany przez schemę: **[user_data_schema.json](https://github.com/JaniszM/easylife/blob/master/easylife/transfers/user_data_schema.json)**. W przypadku niezgodności ze schemą ```przelewy``` nie włączą się oraz zostanie zalogowany błąd. W przypadku braku pliku lista przelewów do realizacji będzie pusta.
Obecnie nie ma jeszcze możliwości zmiany nazwy tego pliku.

Przykład pliku:
```
{
    "przelewy": [
        {
            "nazwa": "Do GetinBanku",
            "tytuł": "Transfer środków",
            "odbiorca": "Mój rachunek",
            "sms": false
        },
        {
            "nazwa": "Mieszkanie czynsz",
            "tytuł": "Czynsz za $MIESIAC_TERAZ",
            "odbiorca": "Jan Kowalski"
        },
        {
            "aktywny": false,
            "nazwa": "Mieszkanie pierwsze czynsz",
            "tytuł": "Czynsz za $MIESIAC_POPRZ",
            "odbiorca": "Marcin Nowak"
        }
    ]
}
```

- *nazwa*: (Wymagane) definiuje nazwę przelewu, wyświetlana w GUI.
- *tytuł*: (Wymagane) definiuje tytuł przelewu, wyświetlany w potwierdzeniu w GUI.
- *odbiorca*: (Wymagane) definiuje nazwę odbiorcy zdefiniowaną wcześniej w książce adresowej banku, wyświetlany w GUI.
- *aktywny*: (Domyślnie: true). Jeżeli ustawione na false to przelew ten nie jest brany pod uwagę. Można w ten sposób wyłączyć stare przelewy.
- *sms*: (Domyślnie: true). Jeżeli ustawione na false to narzędzie nie będzie czekać na potwierdzenie kodem sms przez użytkownika.

W polu *"tytuł"* istnieje możliwość użycia tak zwanych placeholderów. Obecnie dostępne:
- $MIESIAC_TERAZ: podstawi nazwę obecnego miesiąca.
- $MIESIAC_POPRZ: podstawi nazwę poprzedniego miesiąca.

### Uruchomienie

```
easylife przelewy
```

### Użycie

Po uruchomieniu i poprawnym skonfigurowaniu pojawi się ekran przelewów.

1. Użytkownik podaje kwoty przelewów.
2. Zatwierdza przyciskiem "Execute order 66".
3. Pojawia się okno potwierdzenia z informacjami o przelewach. Użytkownik czyta uważnie informacje i potwierdza bądź odrzuca.
4. Jeżeli w kroku 3 użytkownik potwierdził akcję, zostanie otworzona przeglądarka internetowa i przekierowanie do strony banku. Użytkownik loguje się do banku (akcja użytkownika).
5. a) Dla każdego z wybranych przelewów zostanie automatycznie wybrany odbiorca, wypełnione dane przelewu oraz wysłany przelew. Użytkownik potwierdza przelew kodem sms (akcja użytkownika), chyba, że przelew tego nie wymaga (patrz konfiguracja).

    b) Następuje walidacja przelewu.
6. Po wykonaniu wszystkich przelewów następuje automatyczne wylogowanie z banku oraz zamknięcie otwartego okna przeglądarki.

### Wsparcie dla użytkownika

Narzędzie wykonuje szczegółowe logi oraz zrzuty ekranów. Wszystko po to by mieć pewność, że przelew został wykonany jak trzeba.

Logi zapisywane są w pliku ```logs/easylife.log```.

Zrzuty ekranów w plikach ```reports/transfer_error_{datetime}``` oraz ```reports/transfer_success_{datetime}```.

W przypadku powodzenia zapisywany jest zrzut z ekranu potwierdzenia, w przypadku jakiegoś problemu zrzut ekranu z momentu, w którym problem wystąpił.

Obecnie katalogiem logów i raportów jest katalog, w którym skrypt został wywołany, jak w przypadku konfiguracji.

# Pomoc i Ulepszenia

Jeżeli znalazłeś jakieś błędy, coś nie działa jakbyś chciał, coś jest nie intuicyjne bądż brakuje ci czegoś co można dodać bądź chcesz rozwijać narzędzie to napisz do mnie: janiszewski.m.a@gmail.com.
Lub załóż 'issue' na GitHub.
Czasami rzadko sprawdzam mail, lecz raz na tydzień na pewno się to zdarza ;)

Planowane ulepszenia i poprawki:

1. Głowne narzędzie:

    - możliwość konfiguracji przez użytkownika ścieżki dla danych programu wraz z nazwą pliku danych,
    - konfiguracja ścieżki i nazwy pliku logów oraz zrzutów ekranu,
    - testy dla pythona 3.0.
    - unittesty i testy integracyjne.

2. Narzędzie *Przelewy*:

    - !! raport o okresie rozliczeniowy przy zmianie okresu. Informacja dla mega zapominalskich gdy przez cały miesiąc jednak nie wykonali przelewów,
    - możliwość konfiguracji długości i typu okresów rozliczeniowy dla każdego przelewu z osobna,
    - dodatkowa opcjonalna walidacja numeru konta odbiorcy z książki adresowej oraz pliku danych,
    - konfiguracja ścieżki i nazwy pliku logów oraz zrzutów ekranu,
    - walidacja pół kwot w GUI,
    - wsparcie dla chrome, opera i safari.
