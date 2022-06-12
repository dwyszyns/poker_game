from karty import Karty
import pytest


def test_stworz_karty():
    lista = Karty([])
    assert lista.uklad_kart == []


def test_czy_poker_krolewski():
    lista1 = Karty(["3x", "4x", "5x", "6x", "7x"])
    assert lista1.czy_poker_krolewski() is False

    lista2 = Karty(["10x", "11x", "12x", "13x", "14x"])
    assert lista2.czy_poker_krolewski() is True

    lista3 = Karty(["10x", "11y", "12x", "13x", "14x"])
    assert lista3.czy_poker_krolewski() is False


def test_czy_poker():
    lista1 = Karty(["3x", "4x", "5x", "6x", "8x"])
    assert lista1.czy_poker() is False

    lista2 = Karty(["3x", "4x", "5x", "6x", "7x"])
    assert lista2.czy_poker() == 7


def test_czy_kareta():
    lista1 = Karty(["3x", "3y", "3k", "3g", "8x"])
    assert lista1.czy_kareta() == 3

    lista2 = Karty(["3x", "4x", "5x", "6x", "7x"])
    assert lista2.czy_kareta() is False

    lista1 = Karty(["3x", "3y", "3k", "3g", "11x", "11y", "11k", "11g"])
    assert lista1.czy_kareta() == 11


def test_czy_full():
    lista1 = Karty(["3x", "3y", "3k", "8g", "8x"])
    assert lista1.czy_full() == (3, 8)

    lista2 = Karty(["3g", "3y", "3x", "6x", "7y"])
    assert lista2.czy_full() is False

    lista1 = Karty(["3x", "3y", "3k", "11y", "11k", "11g"])
    assert lista1.czy_full() == (11, 3)


def test_czy_kolor():
    lista1 = Karty(["3x", "5x", "7x", "8x", "14x"])
    assert lista1.czy_kolor() == 14

    lista2 = Karty(["3x", "3x", "5y", "6x", "7x"])
    assert lista2.czy_kolor() is False


def test_czy_strit():
    lista1 = Karty(["3x", "4x", "5x", "6x", "8x"])
    assert lista1.czy_strit() is False

    lista2 = Karty(["3x", "4x", "5y", "6x", "7x"])
    assert lista2.czy_strit() == 7


def test_czy_para():
    lista1 = Karty(["3x", "4x", "5x", "6x", "8x"])
    assert lista1.czy_para() is False

    lista2 = Karty(["3x", "4x", "5y", "7y", "7x"])
    assert lista2.czy_para() == 7

    lista3 = Karty(["3x", "4x", "4y", "7y", "7x"])
    assert lista3.czy_para() == 7


def test_czy_trojka():
    lista1 = Karty(["3x", "4x", "5x", "6x", "8x"])
    assert lista1.czy_trojka() is False

    lista2 = Karty(["3x", "4x", "5y", "7y", "7x", "7g"])
    assert lista2.czy_trojka() == 7

    lista3 = Karty(["3x", "14x", "14y", "14g", "7y", "7x", "7g"])
    assert lista3.czy_trojka() == 14


def test_czy_2pary():
    lista1 = Karty(["3x", "4x", "5x", "6x", "8x"])
    assert lista1.czy_2_pary() is False

    lista2 = Karty(["3x", "4x", "5y", "5x", "7x", "7g"])
    assert lista2.czy_2_pary() == (7, 5)

    lista3 = Karty(["3x", "4x", "4y", "5y", "5x", "8x", "8g"])
    assert lista3.czy_2_pary() == (8, 5)


def test_wysoka_karta():
    lista1 = Karty(["3x", "4x", "5x", "6x", "8x"])
    assert lista1.wysoka_karta() == 8

    lista2 = Karty(["3x", "4x", "5y", "5x", "7x", "7g"])
    assert lista2.wysoka_karta() == 7


def test_rozdanie(monkeypatch):
    lista = Karty([])

    def get_shuffle(a):
        return ['2♠', '2✦']
    monkeypatch.setattr("karty.shuffle", get_shuffle)
    lista.rozdanie(2)
    assert lista.uklad_kart == ['2♠', '2✦']


def test_puste_karty():
    lista = Karty([])
    with pytest.raises(ValueError):
        lista.czy_poker_krolewski()


def test_opis_kart():
    karty = Karty(['2♠', '2✦'])
    assert karty.opis() == '2♠ 2✦ '
