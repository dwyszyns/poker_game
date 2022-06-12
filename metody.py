from karty import Karty


kombinacje = {
    "poker_krolewski": [],
    "poker": [],
    "kareta": [],
    "full": [],
    "kolor": [],
    "strit": [],
    "trojka": [],
    "2pary": [],
    "para": [],
    "karta": []
}


def sortowanie_ukladu_kart(sprawdzane_karty):
    """
        Argumenty:
            sprawdzane_karty(lista): lista kart do porównania

        Metoda sortuje wczytane karty i tworzy z niej obiekt.
        Tworzy dodatkowo wysortowaną listę pozycji kart

        Zwracanie:
        obiekt karty oraz lista sortowanych pozycji kart
    """
    sortowane_pozycje_kart = sprawdzane_karty.copy()

    for i in range(len(sprawdzane_karty)):
        pozycja = int(sprawdzane_karty[i][:-1])
        kolor = sprawdzane_karty[i][-1]
        sprawdzane_karty[i] = (pozycja, kolor)
        sortowane_pozycje_kart[i] = sprawdzane_karty[i][0]

    sortowane_pozycje_kart = sorted(sortowane_pozycje_kart)[::-1]
    sprawdzane_karty = sorted(sprawdzane_karty)

    for i in range(len(sprawdzane_karty)):
        pozycja, kolor = sprawdzane_karty[i]
        sprawdzane_karty[i] = str(pozycja) + kolor

    karty = Karty(sprawdzane_karty)
    return (karty, sortowane_pozycje_kart)


def mozliwe_kombinacje(sprawdzane_karty, uczestnik):
    """
        Argumenty:
            sprawdzane_karty(lista): lista kart do porównania
            uczestnik(obiekt): obiekt Uczestnik lub klasy go dziedziczącej

        Metoda sprawdza w kartach możliwe kombinacje.
    """
    karty, sortowane_pozycje_kart = sortowanie_ukladu_kart(sprawdzane_karty)

    wynik = karty.czy_poker_krolewski()
    if wynik is not False:
        kombinacje["poker_krolewski"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_poker()
    if wynik is not False:
        kombinacje["poker"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_kareta()
    if wynik is not False:
        kombinacje["kareta"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_full()
    if wynik is not False:
        kombinacje["full"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_kolor()
    if wynik is not False:
        kombinacje["kolor"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_strit()
    if wynik is not False:
        kombinacje["strit"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_trojka()
    if wynik is not False:
        kombinacje["trojka"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_2_pary()
    if wynik is not False:
        kombinacje["2pary"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.czy_para()
    if wynik is not False:
        kombinacje["para"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))
    wynik = karty.wysoka_karta()
    if wynik is not False:
        kombinacje["karta"].append((wynik, sortowane_pozycje_kart, uczestnik.nazwa, uczestnik))

    for kombinacja in kombinacje:
        kombinacja = sorted(kombinacja)[::-1]
