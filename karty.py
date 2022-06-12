from random import shuffle
kolor = {
    "karo": "✦",
    "pik": "♠",
    "trefl": "♣",
    "kier": "♥"
}

pozycje_kart_wiekszych_od_10 = {
    "11": "J",
    "12": "Q",
    "13": "K",
    "14": "A"
}

pozycje = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
talia_kart = []
for liczba in pozycje:
    for symbol in kolor:
        karta = liczba + kolor[symbol]
        talia_kart.append(karta)


class Karty:
    """
    Class Karty. Zawiera atrybyty:
    :param karty: lista kart w dłoni
    :typ karty: lista
    """

    def __init__(self, uklad_kart=None):
        self.uklad_kart = uklad_kart

    def _rozdanie_karty(self, nowa_karta):
        """
        Argumenty:
            nowa_karta(str): karta rozdana uczestnikowi

        Metoda usuwa kartę z talii i dodaje uczestnikowi do układu kart
        """
        talia_kart.remove(nowa_karta)
        self.uklad_kart.append(nowa_karta)

    def _wrzucenie_karty_na_koniec_talii(self, nowa_karta):
        """
        Argumenty:
            nowa_karta(str): karta rozdana uczestnikowi

        Metoda wrzuca wartość karty na koniec talii, aby ich ilość się zgadzała
        """
        talia_kart.append(nowa_karta)

    def rozdanie(self, ilosc_kart):
        """
        Argumenty:
            ilosc_kart(int): ilość kart w dłoni

        Metoda rozdaje karty uczestnikom, biorąc po kolei z talii
        """
        shuffle(talia_kart)
        for _ in range(ilosc_kart):
            nowa_karta = talia_kart[0]
            self._rozdanie_karty(nowa_karta)
            self._wrzucenie_karty_na_koniec_talii(nowa_karta)
        self.uklad_kart = sorted(self.uklad_kart)

    def opis(self):
        """ Wypisanie kart w dłoni """
        napis = ""
        for karta in self.uklad_kart[:2]:
            if karta[:-1] in pozycje_kart_wiekszych_od_10:
                napis += pozycje_kart_wiekszych_od_10[karta[:-1]]
                napis += karta[-1]
            else:
                napis += karta
            napis += " "
        return napis

    def _wyjatki(self):
        """ Metoda prywatna: sprawdza ilość kart w dłoni"""
        if len(self.uklad_kart) < 2:
            raise ValueError("Porównywać można min. 2 karty!")

    def czy_poker_krolewski(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają
        kombinacje pokera królewskiego

        Zwracanie:
        True jeśli spełni warunek pokera królewskiego,
        w innym przypadku False
        """
        self._wyjatki()
        poprzednia_karta = self.uklad_kart[0]
        if poprzednia_karta[:2] != "10":
            return False
        for karta in self.uklad_kart[1:]:
            if len(karta) != 3 or len(poprzednia_karta) != 3:
                return False
            nr_karty1 = int(poprzednia_karta[:2])
            nr_karty2 = int(karta[:2])
            if nr_karty1 + 1 != nr_karty2 or poprzednia_karta[2] != karta[2]:
                return False
            poprzednia_karta = karta
        return True

    def czy_poker(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        pokera (5 kolejnych kart w jednym kolorze)

        Zwracanie:
        Wartość najwyższej karty kombinacji pokera jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        poprzednia_karta = self.uklad_kart[0]
        for karta in self.uklad_kart[1:]:
            nr_karty1 = int(poprzednia_karta[:-1])
            nr_karty2 = int(karta[:-1])
            if nr_karty1 + 1 != nr_karty2 or poprzednia_karta[-1] != karta[-1]:
                return False
            poprzednia_karta = karta
        nr_karty2 = self.uklad_kart[-1]
        return int(nr_karty2[:-1])

    def czy_kareta(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        karety (4 karty o jednej wartości)

        Zwracanie:
        Wartość karty z kombinacji karety jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        zlicz_te_same = {}
        wynik = 0
        for karta in self.uklad_kart:
            if karta[:-1] in zlicz_te_same:
                zlicz_te_same[karta[:-1]] += 1
            else:
                zlicz_te_same[karta[:-1]] = 1
            if zlicz_te_same[karta[:-1]] == 4:
                wynik = max(wynik, int(karta[:-1]))
        if wynik == 0:
            return False
        return wynik

    def czy_full(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        fulla (para kart o jednej wartości i trojka kart o innej)

        Zwracanie:
        Wartość kart z trojki i pary jeśli spełni warunek kombinacji fulla,
        w innym przypadku False
        """
        self._wyjatki()
        zlicz_te_same = {}
        dwojka = 0
        trojka = 0
        for karta in self.uklad_kart:
            if karta[:-1] in zlicz_te_same:
                zlicz_te_same[karta[:-1]] += 1
            else:
                zlicz_te_same[karta[:-1]] = 1

        for numer in pozycje[::-1]:
            if numer in zlicz_te_same:
                if zlicz_te_same[numer] == 3:
                    if trojka == 0:
                        trojka = int(numer)
                    elif dwojka == 0:
                        dwojka = int(numer)
                if zlicz_te_same[numer] == 2 and dwojka == 0:
                    dwojka = int(numer)
        if dwojka == 0 or trojka == 0:
            return False
        return (trojka, dwojka)

    def czy_kolor(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        koloru (dowolne karty w tym samym kolorze)

        Zwracanie:
        Wartość najwyższej karty kombinacji koloru jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        poprzednia_karta = self.uklad_kart[0]
        for karta in self.uklad_kart[1:]:
            if karta[-1] != poprzednia_karta[-1]:
                return False
            poprzednia_karta = karta
        return int(poprzednia_karta[:-1])

    def czy_strit(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        strita (kolejne wartości kart w dowolnym kolorze)

        Zwracanie:
        Wartość najwyższej karty kombinacji strita jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        poprzednia_karta = self.uklad_kart[0]
        for karta in self.uklad_kart[1:]:
            nr_karty1 = int(poprzednia_karta[:-1])
            nr_karty2 = int(karta[:-1])
            if nr_karty1 + 1 != nr_karty2:
                return False
            poprzednia_karta = karta
        return int(poprzednia_karta[:-1])

    def czy_para(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        pary (dwie karty o tej samej wartości)

        Zwracanie:
        Wartość karty w kombinacji pary jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        zlicz_te_same = {}
        wynik = 0
        for karta in self.uklad_kart:
            if karta[:-1] in zlicz_te_same:
                zlicz_te_same[karta[:-1]] += 1
            else:
                zlicz_te_same[karta[:-1]] = 1
            if zlicz_te_same[karta[:-1]] == 2:
                wynik = max(wynik, int(karta[:-1]))
        if wynik == 0:
            return False
        return wynik

    def czy_2_pary(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        2 par (dwie różne pary kart)

        Zwracanie:
        Wartości wyższej i niższej pary w kombinacji 2par jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        zlicz_te_same = {}
        pary = 0
        wyzsza_para = 0
        nizsza_para = 0
        for karta in self.uklad_kart:
            if karta[:-1] in zlicz_te_same:
                zlicz_te_same[karta[:-1]] += 1
            else:
                zlicz_te_same[karta[:-1]] = 1
            if zlicz_te_same[karta[:-1]] == 2:
                pary += 1
                para_pomocnicza = wyzsza_para
                wyzsza_para = max(wyzsza_para, int(karta[:-1]))
                if wyzsza_para != int(karta[:-1]):
                    nizsza_para = max(nizsza_para, int(karta[:-1]))
                else:
                    nizsza_para = para_pomocnicza
        if pary >= 2:
            return (wyzsza_para, nizsza_para)
        return False

    def czy_trojka(self):
        """
        Metoda sprawdza, czy karty w dłoni spełniają kombinacje
        trójki (trzy karty o tej samej wartości)

        Zwracanie:
        Wartość karty w kombinacji trójki jeśli spełni warunek,
        w innym przypadku False
        """
        self._wyjatki()
        zlicz_te_same = {}
        wynik = 0
        for karta in self.uklad_kart:
            if karta[:-1] in zlicz_te_same:
                zlicz_te_same[karta[:-1]] += 1
            else:
                zlicz_te_same[karta[:-1]] = 1
            if zlicz_te_same[karta[:-1]] == 3:
                wynik = max(wynik, int(karta[:-1]))
        if wynik == 0:
            return False
        return wynik

    def wysoka_karta(self):
        """ Metoda zwraca wartosc najwyzszej karty z listy """
        self._wyjatki()
        wynik = 0
        for karta in self.uklad_kart:
            wynik = max(wynik, int(karta[:-1]))
        return wynik
