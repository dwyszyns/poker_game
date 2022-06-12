from karty import Karty, talia_kart
from random import shuffle
from metody import kombinacje, mozliwe_kombinacje
from time import sleep


zwyciezcy = []
gra = {}

pozycje_kart_wiekszych_od_10 = {
    "11": "J",
    "12": "Q",
    "13": "K",
    "14": "A"
}


class Rozgrywka:
    """
    Class Rozgrywka. Zawiera atrybyty:
    :param player: uczestnik, którym gramy
    :typ player: obiekt klasy Gracz

    :param bots: lista botów, które biorą udział w rozgrywce
    :typ bots: lista botów klasy Bot albo Madry_Bot

    :param uczestnicy: lista uczestników w rozgrywce
    :typ uczestnicy: lista uczestników klas dziedziczących Uczestnik

    :param karty_na_stole: lista kart wyłożonych na stole
    :typ karty_na_stole: lista
    """
    def __init__(self, player=None, bots=None):
        uczestnicy = []
        self._uczestnicy = uczestnicy
        self._player = player
        self._bots = bots
        karty_na_stole = []
        self._karty_na_stole = karty_na_stole
        uczestnicy.append(player)
        for bot in bots:
            uczestnicy.append(bot)

    def karty_na_stole(self):
        return self._karty_na_stole

    def uczestnicy(self):
        return self._uczestnicy

    def bots(self):
        return self._bots

    def _rozdanie_kart(self):
        """
        Metoda prywatna: rozdaje po 2 karty z talii uczestnikom
        """
        for uczestnik in self._uczestnicy:
            uczestnik.karty_w_dloni = Karty([])
            uczestnik.karty_w_dloni.rozdanie(2)

    def sprawdzenie_kombinacji(self):
        """
        Metoda sprawdza kombinacje wśród kart uczestnika i na stole
        """
        for kombinacja in kombinacje:
            kombinacje[kombinacja] = []
        for uczestnik in self._uczestnicy:
            if gra[uczestnik][0] != "pas":
                self._sprawdzenie_ukladu_dla_kart(uczestnik)

    def _sprawdzenie_ukladu_dla_kart(self, uczestnik):
        """
        Metoda sprawdza możliwe kombinacje z ukladu
        """
        uklad_w_dloni = uczestnik.karty_w_dloni.uklad_kart.copy()
        for k in range(len(uklad_w_dloni)-1):
            for j in range(k+1, len(uklad_w_dloni)):
                nowy_uklad = uklad_w_dloni.copy()
                if len(nowy_uklad) == 7:
                    nowy_uklad.remove(uklad_w_dloni[k])
                    nowy_uklad.remove(uklad_w_dloni[j])
                mozliwe_kombinacje(nowy_uklad, uczestnik)

    def zwyciezca(self):
        """
        Metoda wyszukuje wśród uczestników tych, którzy mają
        najlepszą kombinację kart i zwraca jej nazwę
        """
        for kombinacja in kombinacje:
            if len(kombinacje[kombinacja]) > 0:
                lista = kombinacje[kombinacja].copy()
                self._porownanie_graczy(lista)
                return kombinacja

    def _porownanie_graczy(self, lista):
        """
        Argumenty:
            lista(list): wygrana kombinacja kart

        Metoda prywatna: znajduje wszystkich graczy,
        którzy mają wygraną kombinacje
        """
        lista = sorted(lista)[::-1]
        wynik_wygrywajacy = 0
        mozliwi_zwyciezcy = []
        wynik_wygrywajacy = lista[0][0]
        for i in range(0, len(lista)):
            if wynik_wygrywajacy == lista[i][0]:
                mozliwi_zwyciezcy.append((lista[i][1], lista[i][2], lista[i][3]))
        mozliwi_zwyciezcy = sorted(mozliwi_zwyciezcy)[::-1]
        zwyciezcy.append(mozliwi_zwyciezcy[0][2])
        for i in range(1, len(mozliwi_zwyciezcy)):
            if mozliwi_zwyciezcy[0][0] == mozliwi_zwyciezcy[i][0]:
                zwyciezcy.append(mozliwi_zwyciezcy[i][2])
            else:
                break

    def kolejna_runda(self):
        """
        Metoda zeruje globalne zmienne oraz
        tasuje karty przed nową rundą
        """
        gra[self._uczestnicy[0]] = ("gra", 1)
        gra[self._uczestnicy[1]] = ("gra", 2)
        for uczestnik in self._uczestnicy[2:]:
            gra[uczestnik] = ("gra", 0)

        for kombinacja in kombinacje:
            kombinacje[kombinacja] = []
        shuffle(talia_kart)
        self._karty_na_stole = []

    def _decyzje_uczestnikow(self, stawka, osoby_w_grze):
        """
        Argumenty:
            stawka(int/float): aktualna stawka podczas rozgrywki
            osoby_w_grze(list): lista osób nadal biorących udział w rundzie

        Metoda sprawdza decyzje uczestników po rozdaniu kolejnych kart
        """
        ostatnia_podbijajaca_osoba = 0
        kolejnosc_graczy = 0
        ruch_osoby = 0
        for gracz in self._uczestnicy:
            czy_gra, kwota = gra[gracz]
            if czy_gra != "pas":
                czy_gra = gracz.decyzja(stawka)
                print(f'{gracz.nazwa}: {czy_gra}')
                if czy_gra == "pas":
                    osoby_w_grze -= 1
                else:
                    kwota = stawka
                if czy_gra == "va banque":
                    ruch_osoby = "va banque"
                    stawka = gracz.pieniadze
                    ostatnia_podbijajaca_osoba = kolejnosc_graczy
                    gra[gracz] = (czy_gra, stawka)
                    break
                if czy_gra == "podbijam" and ruch_osoby == 0:
                    stawka = gracz.obstawianie(stawka)
                    print(f'{gracz.nazwa} podbija do {stawka}$')
                    ostatnia_podbijajaca_osoba = kolejnosc_graczy
                    kwota = stawka
            gra[gracz] = (czy_gra, kwota)
            kolejnosc_graczy += 1
            if osoby_w_grze == 1:
                return osoby_w_grze
            sleep(1)

        if ruch_osoby == "va banque":
            for gracz in self._uczestnicy[(ostatnia_podbijajaca_osoba+1):]:
                czy_gra, kwota = gra[gracz]
                if czy_gra != "pas":
                    czy_gra = gracz.dorownanie(stawka)
                    print(f'{gracz.nazwa}: {czy_gra}')
                    if czy_gra == "pas":
                        osoby_w_grze -= 1
                    else:
                        kwota = stawka
                    gra[gracz] = (czy_gra, kwota)
                    if osoby_w_grze == 1:
                        return osoby_w_grze
                sleep(1)

        for gracz in self._uczestnicy[:ostatnia_podbijajaca_osoba]:
            czy_gra, kwota = gra[gracz]
            if czy_gra != "pas":
                czy_gra = gracz.dorownanie(stawka)
                print(f'{gracz.nazwa}: {czy_gra}')
                if czy_gra == "pas":
                    osoby_w_grze -= 1
                else:
                    kwota = stawka
                gra[gracz] = (czy_gra, kwota)
                if osoby_w_grze == 1:
                    return osoby_w_grze
            sleep(1)
        if ruch_osoby == "va banque":
            return "va banque"
        return osoby_w_grze

    def _suma_wygranej(self):
        """
        Metoda prywatna: zwraca sumę wszystkich obstawionych
        pieniędzy podczas rundy
        """
        suma = 0
        for uczestnik in self._uczestnicy:
            _, kwota = gra[uczestnik]
            uczestnik.pieniadze -= kwota
            suma += kwota
        return suma

    def nowe_karty(self, ilosc_kart):
        """
        Argumenty:
            ilosc_kart(int): ilość kart do wyłożenia na stół

        Metoda rozdaje karty na stół,
        """
        for _ in range(ilosc_kart):
            nowa_karta = talia_kart[0]
            self._rozdanie_karty_na_stol(nowa_karta)
            self._wrzucenie_karty_na_koniec_talii(nowa_karta)

    def _rozdanie_karty_na_stol(self, nowa_karta):
        """
        Argumenty:
            nowa_karta(str): karta wyłożona na stół

        Metoda usuwa kartę z talii i dodaje do kart na stole
        """
        talia_kart.remove(nowa_karta)
        self._karty_na_stole.append(nowa_karta)

    def _wrzucenie_karty_na_koniec_talii(self, nowa_karta):
        """
        Argumenty:
            nowa_karta(str): karta wyłożona na stół

        Metoda wrzuca wartość karty na koniec talii, aby ich ilość się zgadzała
        """
        talia_kart.append(nowa_karta)

    def player(self):
        return self._player

    def opis_kart_na_stole(self):
        """ Opis kart na stole """
        napis = "Karty na stole: "
        for karta in self._karty_na_stole:
            if karta[:-1] in pozycje_kart_wiekszych_od_10:
                napis += pozycje_kart_wiekszych_od_10[karta[:-1]]
                napis += karta[-1]
            else:
                napis += karta
            napis += " "
        return napis

    def _sprawdzenie_stawki(self):
        """
        Metoda zwraca aktualną stawkę podczas rozgrywki
        """
        stawka = 0
        for gracz in gra:
            stawka = max(stawka, gra[gracz][1])
        return stawka

    def _czesc_licytacji(self, osoby_w_grze):
        """
        CZĘŚĆ LICYTACJI: rozdanie kart uczestnikom i ich decyzje
        Argumenty:
            osoby_w_grze(int): ilość graczy w rundzie

        Metoda prywatna: zwraca ilość graczy biorących nadal udział w rundzie
        """
        print("Rozdanie kart uczestnikom:")
        self._rozdanie_kart()
        if self._player in self._uczestnicy:
            print(f'Twoje karty to: {self._player.karty_w_dloni.opis()}')
            print(f'Twoje pieniądze: {self._player.pieniadze}$')
        print("")
        stawka = 2
        osoby_w_grze = self._decyzje_uczestnikow(stawka, osoby_w_grze)
        return osoby_w_grze

    def _flop(self, stawka, osoby_w_grze):
        """
        CZĘŚĆ FLOP : wyłożenie 3 kart na stół i decyzje graczy
        Argumenty:
            osoby_w_grze(int): ilość graczy w rundzie
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda prywatna: zwraca ilość graczy biorących nadal udział w rundzie
        """
        if osoby_w_grze == "va banque":
            print('Wyłożenie 3 kart na stół')
            self.nowe_karty(3)
            for gracz in self._uczestnicy:
                for karta in self._karty_na_stole:
                    gracz.karty_w_dloni.uklad_kart.append(karta)
            print(self.opis_kart_na_stole())

        elif osoby_w_grze > 1:
            print('Wyłożenie 3 kart na stół')
            self.nowe_karty(3)
            for gracz in self._uczestnicy:
                for karta in self._karty_na_stole:
                    gracz.karty_w_dloni.uklad_kart.append(karta)
            print(self.opis_kart_na_stole())
            if self._player in self._uczestnicy:
                print(f'Twoje karty to: {self._player.karty_w_dloni.opis()}')
                print(f'Twoje pieniądze: {self._player.pieniadze}$')
                print("")
            osoby_w_grze = self._decyzje_uczestnikow(stawka, osoby_w_grze)
        return osoby_w_grze

    def _turn(self, stawka, osoby_w_grze):
        """
        CZĘŚĆ TURN : wyłożenie 4.karty na stół i decyzje graczy
        Argumenty:
            osoby_w_grze(int): ilość graczy w rundzie
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda prywatna: zwraca ilość graczy biorących nadal udział w rundzie
        """
        if osoby_w_grze == "va banque":
            print('Wyłożenie 1 karty na stół')
            self.nowe_karty(1)
            for gracz in self._uczestnicy:
                gracz.karty_w_dloni.uklad_kart.append(self._karty_na_stole[-1])
            print(self.opis_kart_na_stole())

        elif osoby_w_grze > 1:
            print('Wyłożenie 1 karty na stół')
            self.nowe_karty(1)
            for gracz in self._uczestnicy:
                gracz.karty_w_dloni.uklad_kart.append(self._karty_na_stole[-1])
            print(self.opis_kart_na_stole())
            if self._player in self._uczestnicy:
                print(f'Twoje karty to: {self._player.karty_w_dloni.opis()}')
                print(f'Twoje pieniądze: {self._player.pieniadze}$')
                print("")
            osoby_w_grze = self._decyzje_uczestnikow(stawka, osoby_w_grze)
        return osoby_w_grze

    def _river(self, stawka, osoby_w_grze):
        """
        CZĘŚĆ RIVER : wyłożenie 5.karty na stół i decyzje graczy
        Argumenty:
            osoby_w_grze(int): ilość graczy w rundzie
            stawka(int/float): aktualna stawka podczas rozgrywki

        Metoda prywatna: zwraca ilość graczy biorących nadal udział w rundzie
        """
        if osoby_w_grze == "va banque":
            print('Wyłożenie 1 karty na stół')
            self.nowe_karty(1)
            for gracz in self._uczestnicy:
                gracz.karty_w_dloni.uklad_kart.append(self._karty_na_stole[-1])
            print(self.opis_kart_na_stole())

        elif osoby_w_grze > 1:
            print('Wyłożenie 1 karty na stół')
            self.nowe_karty(1)
            for gracz in self._uczestnicy:
                gracz.karty_w_dloni.uklad_kart.append(self._karty_na_stole[-1])
            print(self.opis_kart_na_stole())
            if self._player in self._uczestnicy:
                print(f'Twoje karty to: {self._player.karty_w_dloni.opis()}')
                print(f'Twoje pieniądze: {self._player.pieniadze}$')
                print("")
            osoby_w_grze = self._decyzje_uczestnikow(stawka, osoby_w_grze)
        return osoby_w_grze

    def play(self):
        """
        Metoda przeprowadza rozgrywkę, dopóki jest więcej niż 1 gracz
        """
        print('Gra się rozpoczyna...')
        runda = 0
        while True:
            runda += 1
            if not bool(self._uczestnicy):
                print("Brak uczestników do gry")
                break
            if len(self._uczestnicy) == 1:
                print("Gra wymaga co najmniej 2 graczy")
                break

            i = 0
            while(i < len(self._uczestnicy)):
                uczestnik = self._uczestnicy[i]
                if uczestnik.pieniadze <= 0:
                    self._uczestnicy.remove(uczestnik)
                    i -= 1
                    gra[uczestnik] = ("pas", 0)
                    print(f'Z gry odpada {uczestnik.nazwa}.')
                i += 1
            if len(self._uczestnicy) == 1:
                print(f'Grę wygrał/a {self._uczestnicy[0].nazwa}')
                return
            osoby_w_grze = len(self._uczestnicy)

            print("---------------------------------")
            print(f'Runda {runda}:')
            uczestnicy = "W grze są: "
            uczestnicy += " ".join(str(gracz.nazwa) for gracz in self._uczestnicy)
            print(uczestnicy)
            sleep(1)
            print(f'Small blind to: {self._uczestnicy[0].nazwa}.')
            sleep(1)
            print(f'Big blind to: {self._uczestnicy[1].nazwa}.')
            self.kolejna_runda()
            sleep(1)

            osoby_w_grze = self._czesc_licytacji(osoby_w_grze)
            stawka = self._sprawdzenie_stawki()
            sleep(1)

            osoby_w_grze = self._flop(stawka, osoby_w_grze)
            stawka = self._sprawdzenie_stawki()
            sleep(1)

            osoby_w_grze = self._turn(stawka, osoby_w_grze)
            stawka = self._sprawdzenie_stawki()
            sleep(1)

            osoby_w_grze = self._river(stawka, osoby_w_grze)

            wygrana = self._suma_wygranej()
            if osoby_w_grze == 1:
                for gracz in gra:
                    if gra[gracz][0] != "pas":
                        print(f'{gracz.nazwa} wygrywa {wygrana}$.')
                        gracz.pieniadze += wygrana
                        break
            else:
                self.sprawdzenie_kombinacji()
                wygrana_kombinacja = self.zwyciezca()
                niepowtarzalni_zwyciezcy = list(set(zwyciezcy.copy()))
                wygrana = wygrana / len(niepowtarzalni_zwyciezcy)
                for gracz in niepowtarzalni_zwyciezcy:
                    gracz.pieniadze += wygrana
                print("Sprawdzenie:")
                for uczestnik in self._uczestnicy:
                    print(f'{uczestnik.nazwa}: {uczestnik.karty_w_dloni.opis()}')
                    sleep(1)
                print(self.opis_kart_na_stole())
                if len(niepowtarzalni_zwyciezcy) == 1:
                    print(f'{niepowtarzalni_zwyciezcy[0].nazwa} wygrywa {wygrana}$ z {wygrana_kombinacja}!')
                else:
                    wygrani = " ".join(str(gracz.nazwa) for gracz in niepowtarzalni_zwyciezcy)
                    print(f'{wygrani} wygrywają po {wygrana}$ z {wygrana_kombinacja}')
            self._zmiana_kolejnosci_graczy()
            zwyciezcy.clear()
            sleep(2)

    def _zmiana_kolejnosci_graczy(self):
        small_blind = self._uczestnicy[0]
        self._uczestnicy.remove(small_blind)
        self._uczestnicy.append(small_blind)
