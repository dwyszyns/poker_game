from metody import kombinacje, mozliwe_kombinacje, sortowanie_ukladu_kart
from uczestnik import Uczestnik
from karty import Karty


def test_mozliwe_kombinacje_2_pary():
    uczestnik = Uczestnik("Jan", 100)
    uczestnik.karty_w_dloni = Karty(["3x", "3y", "5x", "5y", "14x"])
    mozliwe_kombinacje(uczestnik.karty_w_dloni.uklad_kart, uczestnik)
    slownik = {
        "poker_krolewski": [],
        "poker": [],
        "kareta": [],
        "full": [],
        "kolor": [],
        "strit": [],
        "trojka": [],
        "2pary": [((5, 3), [14, 5, 5, 3, 3], "Jan", uczestnik)],
        "para": [(5, [14, 5, 5, 3, 3], "Jan", uczestnik)],
        "karta": [(14, [14, 5, 5, 3, 3], "Jan", uczestnik)]
    }
    assert slownik == kombinacje


def test_mozliwe_kombinacje_kolor():
    uczestnik = Uczestnik("Jan", 100)
    uczestnik.karty_w_dloni = Karty(["8x", "10x", "11x", "12x", "13x"])
    mozliwe_kombinacje(uczestnik.karty_w_dloni.uklad_kart, uczestnik)
    slownik = {
        "poker_krolewski": [],
        "poker": [],
        "kareta": [],
        "full": [],
        "kolor": [(13, [13, 12, 11, 10, 8], "Jan", uczestnik)],
        "strit": [],
        "trojka": [],
        "2pary": [],
        "para": [],
        "karta": [(13, [13, 12, 11, 10, 8], "Jan", uczestnik)]
    }
    assert slownik == kombinacje


def test_mozliwe_kombinacje_2_graczy():
    uczestnik1 = Uczestnik("Jan", 100)
    uczestnik1.karty_w_dloni = Karty(["8x", "10x", "11x", "12x", "13x"])
    mozliwe_kombinacje(uczestnik1.karty_w_dloni.uklad_kart, uczestnik1)
    uczestnik2 = Uczestnik("Marek", 100)
    uczestnik2.karty_w_dloni = Karty(["3x", "4y", "5w", "6x", "7y"])
    mozliwe_kombinacje(uczestnik2.karty_w_dloni.uklad_kart, uczestnik2)
    slownik = {
        "poker_krolewski": [],
        "poker": [],
        "kareta": [],
        "full": [],
        "kolor": [(13, [13, 12, 11, 10, 8], "Jan", uczestnik1)],
        "strit": [(7, [7, 6, 5, 4, 3], "Marek", uczestnik2)],
        "trojka": [],
        "2pary": [],
        "para": [],
        "karta": [(13, [13, 12, 11, 10, 8], "Jan", uczestnik1), (7, [7, 6, 5, 4, 3], "Marek", uczestnik2)]
    }
    assert slownik == kombinacje


def test_sortowanie_ukladu_kart():
    uklad = ["11x", "12y", "3w", "3x", "3y"]
    karty, sortowane_pozycje_kart = sortowanie_ukladu_kart(uklad)
    assert karty.uklad_kart == ["3w", "3x", "3y", "11x", "12y"]
    assert sortowane_pozycje_kart == [12, 11, 3, 3, 3]
