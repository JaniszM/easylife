Przeczytaj w innym języku: [English](README.md), [Polski](README.pl.md).

Moduł grupujący różne użyteczne narzędzia/skrypty mające ułatwić Ci życie. Automatyzuje te same rzeczy, które wykonujesz każdego dnia.

Dostępne języki interfejsu użytkownika oraz całego narzędzia **easylife**:
- polski.

Wspierane systemy operacyjne:
- OSX
- Linux
- Windows

TOC:

- [Dlaczego powinieneś używać tego narzędzia?](#dlaczego-powinieneś-używać-tego-narzędzia)
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
    - [Organizer zdjęć i filmów](#organizer-zdjęć-i-filmów)
        - [Uruchomienie i uźycie](#uruchomienie-i-użycie)
- [Pomoc i Ulepszenia](#pomoc-i-ulepszenia)
    
# Dlaczego powinieneś używać tego narzędzia?

Każdy wykonuje pewne czynności jak płacenie rachunków, segregowanie zdjęć zrobionych smartfonem, sprawdzanie kursów walut czy przeglądanie pewnych zbiorów danych w poszukiwaniu zmian. Przykładów może być nieskończenie wiele. Każda z nich zabiera Ci czas. Gdy czynność jest powtarzalna np. co tydzień a czas potrzebny do jej wykonania przekracza powiedzmy minutę to zautomatyzowanie takiej czynności zaczyna mieć sens. Easylife zamierza być właśnie zbiorem różnych takich zautomatyzowanych czynności.

Zadaniem easylife jest więc przede wszystkim **oszczędzać twój czas** oraz uwolnić Cię nie rzadko od nudnych zadań.

*Jeżeli masz pomysł na zautomatyzowanie jakieś czynności, która może przydać się również innym to napisz do mnie: janiszewski.m.a@gmail.com*.

# Znane problemy

**Przelewy:** Brak.

# Wymagania

- Python 2.7

# Instalacja

Jeżeli nie posiadasz Pythona zainstaluj: **https://www.python.org/downloads/**

Zainstalować paczkę:
```
pip install easylife
```

Jeżeli masz jakieś problemy z instalacją, upewnij się, że masz najnowszą wersje ```pip```. Jeżeli jej nie masz to uaktualnij według instrukcji ```pip```.

# Konfiguracja

Narzędzie korzysta z plików konfiguracji oraz różnych plików danych. Pierwsze uruchomienie spowoduje utworzenie pliku konfiguracji danego skryptu w katalogu **easylife**, który znajduje się w katalogu domowym użytkownika.

W chwili obecnej nie ma możliwości skonfigurowania stałego katalogu dla **easylife**. *Prace w toku.*

# Uruchomienie

Poniżej przedstawiony jest sposób uruchomiania każdego z narzędzi/skryptów wbudowanych w **easylife**.

Po zainstalowaniu paczki zostanie dodany alias ```easylife``` do katalogu ```bin``` interpretera Python. Alias powinien być dostępny z poziomu powłoki systemu. Jeżeli z jakiegoś powodu nie jest, upewnij się, że katalog ```bin``` twojego Pythona jest dodany to zmiennej systemowej ```PATH```.
Jeżeli ```PATH``` jest poprawnie skonfigurowany wywołaj:
```
easylife <narzędzie>

np.:
easylife przelewy
```

Pomoc:
```
easylife help
```

Wersja programu i narzedzie:
```
easylife version
```

# Narzędzia i Skrypty

Poniżej znajduje się opis każdego z narzędzi/skryptów zaimplementowanych w **easylife**.

## Przelewy

*Cel narzędzia: zapłacić szereg różnych rachunków poprzez elektroniczne przelewy.*

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
2. Należy zainstalować odpowiedni sterownik dla przeglądarki, np. dla firefox sterownikiem jest geckodriver.

    - Instalacja GeckoDriver dla Firefox:
    
        Jeżeli nie masz geckodriver możesz spróbować doinstalować przez:
        ```
        easylife get-geckodriver
        ```
        Jeżeli posiadasz już jeden to możesz spróbować go użyć przenosząc lub linkując sterownik w subkatalogu **easylife** katalogu domowego.
        
        *Jeżeli zobaczysz błąd: **WebDriverException: Message: 'geckodriver' executable needs to be in PATH.** to znaczy, że geckodriver nie jest poprawnie skonfigurowany.*
3. Na stronie banku w książce adresowej muszą być zdefiniowani odbiorcy, do których zostaną rozesłane przelewy. Nazwa w książce musi się zgadzać z nazwami przelewów z pól "odbiorca" w pliku danych. Oczywiście w książce musi być zdefiniowany poprawny numer konta bankowego odbiorcy.

### Konfiguracja

Plik konfiguracji ```transfers_config```. W przypadku braku pliku zostanie utworzony nowy z domyślnymi wartościami. Pliki konfiguracyjne są tworzone w podkatalogu **easylife** katalogu domowego.

Opcje:

- *web_timeout*: Definiuje czas oczekiwania (sekundy) skryptu na załadowanie strony.

    Domyślna wartość to 30.
    Jeżeli twoje połączenie jest wolne bądź dostajesz błędy o nie odnalezionych elementach strony spróbuj zwiększyć tę wartość.
    
- *user_timeout*: Definiuje czas oczekiwania (sekundy) skryptu na akcję użytkownika taką jak logowanie.

    Domyślna wartość to 120.
    
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
            "odbiorca": "Jan Kowalski",
            "kwota": 1200
        },
        {
            "aktywny": false,
            "nazwa": "Mieszkanie pierwsze czynsz",
            "tytuł": "Czynsz za $MIESIAC_POPRZ",
            "odbiorca": "Marcin Nowak",
            "kwota": "1000"
        }
    ]
}
```

- *nazwa*: (Wymagane) definiuje nazwę przelewu, wyświetlana w GUI.
- *aktywny*: (Domyślnie: true). Jeżeli ustawione na false to przelew ten nie jest brany pod uwagę. Można w ten sposób wyłączyć stare przelewy.
- *tytuł*: (Wymagane) definiuje tytuł przelewu, wyświetlany w potwierdzeniu w GUI.
- *odbiorca*: (Wymagane) definiuje nazwę odbiorcy zdefiniowaną wcześniej w książce adresowej banku, wyświetlany w GUI.
- *sms*: (Domyślnie: true). Jeżeli ustawione na false to narzędzie nie będzie czekać na potwierdzenie kodem sms przez użytkownika.
- *kwota*: (Opcjonalne). Domyślna kwota przelewu. Wartość z tego pola zostanie przeniesiona do formularza na interfejsie użytkownika.

W polu *"tytuł"* istnieje możliwość użycia tak zwanych placeholderów. Obecnie dostępne:
- $MIESIAC_TERAZ: podstawi nazwę obecnego miesiąca.
- $MIESIAC_POPRZ: podstawi nazwę poprzedniego miesiąca.

### Uruchomienie

```
easylife przelewy
easylife transfers
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

Logi zapisywane są w katalogu domowym użytkownika w ```easylife/logs/easylife.log``` a zrzuty ekranów w ```easylife/reports/transfer_error_{datetime}``` oraz ```easylife/reports/transfer_success_{datetime}```.

W przypadku powodzenia zapisywany jest zrzut z ekranu potwierdzenia, w przypadku jakiegoś problemu zrzut ekranu z momentu, w którym problem wystąpił.

Pliki konfiguracyjne programu przechowywane są w katalogu, z którego skrypt został wywołany.

## Organizer zdjęć i filmów

*Cel narzędzia: uporządkować zasoby zdjęć i wideo, lub zarchivizować je.*

Narzędzie przeszukuje rekursywnie podaną ścieżkę dla plików graficznych i video a następnie przenosi je do wskazanego katalogu według zadanej struktury i nazewnictwa.
Wykorzystuje EXIF do ustalenia daty zdjęcia. Jeżeli brak EXIF próbuje odczytać date systemową utworzenia pliku.

Template według, którego znalezione pliki są rozrzycane po katalogu:
- YYYY: pozycja roku, zostanie zamienione na rok założenia pliku,
- MONTH lub MM: pozycja miesiąca,
- DD: pozycja dni,
- NAME: pozycja nazwy pliku przenoszonego,
- rozdzielacze, '-' i '/'.

Przetwarzane są jedynie pliki o znanych rozszerzeniach. Listę rozszerzeń można znaleźć w `easylife/photo_organizer/__init__.py`. 

Sprawdzono dla:
- OSX Yosemite,
- Windows 7.

### Uruchomienie i użycie

```
easylife zdjecia [params]
easylife photo [params]
```

Parametry:
- source_dir: katalog, w którym znajdują się pliki do przetworzenia,
- destination: katalog gdzie zostaną umieszczone pliki przetworzone,
- template: template według, którego segregować pliki,
- (OPCJONALNE) remove-source: jeżeli się pojawi to katalog źródłowy (source_dir) zostanie usunięty,
- (OPCJONALNE) overwrite-existing: jeżeli się pojawi to w przypadku kolizji plików te w *destination* zostaną zastąpione tymi z *source_dir*. 

**PRZYKŁADY**
```
# Backup zdjęć z karty telefonu do katalogów typu ./my_backup/photo/2017/05-21-DCIM0000001.jpg. Duplikaty w ./my_backup/photo nadpisane będą.
easylife zdjecia /my_phone_card/photo ./my_backup/photo /YYYY/MM-DD-NAME overwrite-existing

# Backup filmów z karty telefonu do katalogów typu ./my_backup/video/2017-03/funny1234.avi. Katalog końcowy /my_phone_card/video zostanie usunięty.
easylife zdjecia /my_phone_card/video ./my_backup/video /YYYY-MM/NAME remove source
```

# Pomoc i Ulepszenia

Jeżeli znalazłeś jakieś błędy, coś nie działa jakbyś chciał, coś jest nie intuicyjne bądż brakuje ci czegoś co można dodać bądź chcesz rozwijać narzędzie to napisz do mnie: janiszewski.m.a@gmail.com.
Lub załóż 'issue' na GitHub.
Czasami rzadko sprawdzam mail, lecz raz na tydzień na pewno się to zdarza ;)

Planowane ulepszenia i poprawki:

1. Głowne narzędzie:

    - wersja angielska.
    - możliwość konfiguracji przez użytkownika ścieżki dla danych programu wraz z nazwą pliku danych,
    - konfiguracja ścieżki i nazwy pliku logów oraz zrzutów ekranu,
    - testy dla pythona 3.x.
    - unittesty i testy integracyjne.
    - ulepszone narzedzie help

2. Narzędzie *Przelewy*:

    - !! raport o okresie rozliczeniowy przy zmianie okresu. Informacja dla mega zapominalskich gdy przez cały miesiąc jednak nie wykonali przelewów,
    - możliwość konfiguracji długości i typu okresów rozliczeniowy dla każdego przelewu z osobna,
    - dodatkowa opcjonalna walidacja numeru konta odbiorcy z książki adresowej oraz pliku danych,
    - konfiguracja ścieżki i nazwy pliku logów oraz zrzutów ekranu,
    - walidacja pół kwot w GUI,
    - wsparcie dla chrome, opera i safari.
    - możliwość oznaczenia w GUI, że przelew został wykonany (wykonano ręcznie bądź z jakiegoś powodu nie został oznaczony przez skrypt).
    - profile użytkownika pozwalające używać więcej niż jeden plik konfiguracji.
