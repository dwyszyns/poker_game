from random import randint, choice
from karty import Karty
from metody import kombinacje, mozliwe_kombinacje
import stale


class Uczestnik:
    """
    Class Uczestnik. Zawiera atrybyty:
    :param nazwa: nazwa uczestnika
    :typ nazwa: string

    :param pieniadze: pieniądze, które posiada uczestnik
    :typ pieniadze: float/int

    :param karty_w_dloni: lista kart w dłoni uczestnika
    :typ karty_w_dloni: lista
    """
    def __init__(self, nazwa, pieniadze):
        self.nazwa = nazwa
        self.pieniadze = pieniadze
        self.karty_w_dloni = Karty([])


class Gracz(Uczestnik):
    """ Class Gracz dziedziczy konstruktor od Uczestnika"""
    def __init__(self, nazwa, pieniadze):
        super().__init__(nazwa, pieniadze)

    def decyzja(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda pyta o decyzje uczestnika podczas rozgrywki
        """
        if stawka > self.pieniadze:
            opcje_va_banque = {"1": "pas", "2": "va banque"}
            dzialanie = input(f'Wybierz opcję: {opcje_va_banque} ')
            while dzialanie not in opcje_va_banque:
                dzialanie = input("Podaj poprawną opcję: ")
                print("")
            return opcje_va_banque[dzialanie]
        else:
            opcje = {"1": "pas", "2": "va banque", "3": "czekam", "4": "podbijam"}

            dzialanie = input(f'Wybierz opcję: {opcje} ')
            while dzialanie not in opcje:
                dzialanie = input("Podaj poprawną opcję: ")
            print("")
        return opcje[dzialanie]

    def dorownanie(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda pyta o decyzję o dalszym udziale, gdy ktoś inny gra va banque
        """
        if stawka > self.pieniadze:
            return "pas"
        opcje = {"1": "pas", "2": "dorównuję"}
        dzialanie = input(f'Wybierz opcję: {opcje} ')
        while dzialanie not in opcje:
            dzialanie = input("Podaj poprawną decyzję: ")
        print("")
        return opcje[dzialanie]

    def obstawianie(self, aktualna_stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda pyta o ilość podbijanej stawki podczas rozgrywki
        """
        while True:
            nowa_stawka = input(f'O ile podbijasz? Zakres 0-{self.pieniadze - aktualna_stawka} ')
            try:
                nowa_stawka = int(nowa_stawka)
                if nowa_stawka >= 0:
                    if nowa_stawka + aktualna_stawka <= self.pieniadze:
                        aktualna_stawka += nowa_stawka
                        print("")
                        return aktualna_stawka
            except Exception:
                print("Podaj poprawną stawkę!")
                self.obstawianie(aktualna_stawka)


class Bot(Uczestnik):
    """ Class Bot dziedziczy konstruktor od Uczestnika """
    def __init__(self, nazwa, pieniadze):
        super().__init__(nazwa, pieniadze)

    def decyzja(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda zwraca losową decyzję bota podczas rozgrywki
        """
        opcje = ["pas", "va banque", "czekam", "podbijam"]
        if stawka >= self.pieniadze:
            decyzja = choice(opcje[:-2])
        else:
            decyzja = choice(opcje)
        return decyzja

    def dorownanie(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda zwraca decyzję o grze, gdy ktoś inny gra va banque
        """
        if stawka > self.pieniadze:
            return "pas"
        opcje = ["pas", "dorownuję"]
        decyzja = choice(opcje)
        return decyzja

    def obstawianie(self, aktualna_stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda zwraca losową kwotę podbijanej stawki przez Bota
        """
        mozliwy_max = self.pieniadze - aktualna_stawka
        if mozliwy_max >= 0:
            nowa_stawka = randint(1, mozliwy_max+1)
            aktualna_stawka += nowa_stawka
        return aktualna_stawka


class Madry_Bot(Uczestnik):
    """ Class Madry_Bot dziedziczy konstruktor od Uczestnika"""
    def __init__(self, nazwa, pieniadze):
        super().__init__(nazwa, pieniadze)

    def _sprawdzenie(self):
        """
        Metoda sprawdza możliwe kombinacje wśród kart bota
        """
        ilosc_kart_w_dloni = len(self.karty_w_dloni.uklad_kart)
        if ilosc_kart_w_dloni == stale.KARTY_RIVER:
            self._sprawdzenie_ukladu_dla_7_kart()

        if len(self.karty_w_dloni.uklad_kart) <= stale.KARTY_TURN and len(self.karty_w_dloni.uklad_kart) > stale.KARTY_RUNDA_1:
            self._sprawdzenie_ukladu_dla_6_kart()

        if len(self.karty_w_dloni.uklad_kart) <= stale.KARTY_FLOP:
            lista = self.karty_w_dloni.uklad_kart.copy()
            mozliwe_kombinacje(lista, self)

    def _sprawdzenie_ukladu_dla_7_kart(self):
        """
        Metoda sprawdza możliwe kombinacje z 7 kart bota
        """
        uklad_w_dloni = self.karty_w_dloni.uklad_kart.copy()
        for k in range(len(uklad_w_dloni)-1):
            for j in range(k+1, len(uklad_w_dloni)):
                nowy_uklad = uklad_w_dloni.copy()
                nowy_uklad.remove(uklad_w_dloni[k])
                nowy_uklad.remove(uklad_w_dloni[j])
                mozliwe_kombinacje(nowy_uklad, self)

    def _sprawdzenie_ukladu_dla_6_kart(self):
        """
        Metoda sprawdza możliwe kombinacje z 6 kart bota
        """
        uklad_w_dloni = self.karty_w_dloni.uklad_kart.copy()
        for k in range(len(uklad_w_dloni)):
            nowy_uklad = uklad_w_dloni.copy()
            nowy_uklad.remove(uklad_w_dloni[k])
            mozliwe_kombinacje(nowy_uklad, self)

    def decyzja(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda zwraca decyzje uczestnika podczas rozgrywki
        """
        zlicz_kombinacje = 0
        najwyzsza_karta_ukladu = 0
        self._sprawdzenie()
        warte_uwagi = ["full", "kolor", "trojka", "2pary", "para", "kareta", "strit"]
        najlepsze = ["poker_krolewski", "poker", "kareta", "full"]
        for kombinacja in kombinacje:
            if len(kombinacje[kombinacja]) != 0:
                zlicz_kombinacje += 1
                if kombinacja in najlepsze and len(self.karty_w_dloni.uklad_kart) >= stale.KARTY_TURN and stawka >= self.pieniadze:
                    return "va banque"
                elif self.pieniadze < stale.MINIMALNA_NISKA_KWOTA:
                    return "va banque"
                elif kombinacja in warte_uwagi and stawka < self.pieniadze:
                    return "podbijam"
                elif self.pieniadze > stale.MINIMALNA_DUZA_KWOTA:
                    return "podbijam"
        if stawka >= self.pieniadze:
            return "pas"
        for karta in self.karty_w_dloni.uklad_kart:
            najwyzsza_karta_ukladu = max(najwyzsza_karta_ukladu, int(karta[:-1]))
        if zlicz_kombinacje == 1 and najwyzsza_karta_ukladu <= stale.MINIMALNA_NISKA_KARTA:
            return "pas"
        if najwyzsza_karta_ukladu <= stale.WARTOSC_AS and najwyzsza_karta_ukladu > stale.WARTOSC_JOKER and stawka < self.pieniadze:
            return "podbijam"
        return "czekam"

    def obstawianie(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda zwraca kwotę podbijanej stawki przez bota
        """
        zlicz_kombinacje = 0
        wynik = 0
        podbite_pieniadze = 0
        self._sprawdzenie()
        warte_uwagi = ["full", "kolor", "trojka", "2pary", "para"]
        for kombinacja in kombinacje:
            if len(kombinacje[kombinacja]) != 0:
                zlicz_kombinacje += 1
                if kombinacja in warte_uwagi and stawka < self.pieniadze:
                    podbite_pieniadze = self._obstawiana_wartosc("silna", stawka)
        for karta in self.karty_w_dloni.uklad_kart:
            wynik = max(wynik, int(karta[:-1]))
        if wynik <= stale.WARTOSC_AS and wynik > stale.WARTOSC_JOKER:
            podbite_pieniadze = self._obstawiana_wartosc("slaba", stawka)
        stawka += podbite_pieniadze
        if podbite_pieniadze == 0:
            stawka += 1
        return stawka

    def _obstawiana_wartosc(self, kombinacja, stawka):
        if kombinacja == "slaba":
            podbite_pieniadze = randint(0, (self.pieniadze-stawka)//stale.PODZIAL_SLABA_KOMBINACJA)
        else:
            podbite_pieniadze = randint(0, (self.pieniadze-stawka)//stale.PODZIAL_SILNA_KOMBINACJA)
        return podbite_pieniadze

    def dorownanie(self, stawka):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda zwraca decyzję o grze, gdy ktoś inny gra va banque
        """
        zlicz_kombinacje = 0
        najwyzsza_karta_ukladu = 0
        dobre_kombinacje = 0
        self._sprawdzenie()
        warte_uwagi = ["full", "kolor", "trojka", "2pary", "para", "strit"]
        for kombinacja in kombinacje:
            if len(kombinacje[kombinacja]) != 0:
                zlicz_kombinacje += 1
                if kombinacja in warte_uwagi:
                    dobre_kombinacje += 1
        if stawka > self.pieniadze:
            return "pas"
        if dobre_kombinacje > 1:
            return "dorównuję"
        for karta in self.karty_w_dloni.uklad_kart:
            najwyzsza_karta_ukladu = max(najwyzsza_karta_ukladu, int(karta[:-1]))
        if najwyzsza_karta_ukladu <= stale.WARTOSC_AS and najwyzsza_karta_ukladu > stale.WARTOSC_JOKER:
            if stawka <= self.pieniadze//stale.PODZIAL_SILNA_KOMBINACJA:
                return "dorównuję"
        return "pas"
