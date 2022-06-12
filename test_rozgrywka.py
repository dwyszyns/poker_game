from rozgrywka import Rozgrywka, gra, kombinacje
from uczestnik import Bot, Gracz
from karty import Karty


def test_rozgrywka():
    bot = Bot("Dominika", 2000)
    player = Gracz("Maciek", 200)
    gra = Rozgrywka(player, [bot])
    assert gra.bots() == [bot]
    assert gra.player() == player
    assert gra.karty_na_stole() == []


def test_zwyciezca_kolor():
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])
    player = Gracz("Maciek", 200)
    player.karty_w_dloni = Karty(["3x", "5x"])
    gra = Rozgrywka(player, [bot])
    gra.kolejna_runda()
    gra.sprawdzenie_kombinacji()
    assert gra.zwyciezca() == "kolor"


def test_zwyciezca_2_pary():
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "2y", "3x", "3y", "5y"])
    player = Gracz("Maciek", 200)
    player.karty_w_dloni = Karty(["3w", "4x", "4y", "5x", "5w"])
    gra = Rozgrywka(player, [bot])
    gra.kolejna_runda()
    gra.sprawdzenie_kombinacji()
    assert gra.zwyciezca() == "2pary"


def test_nowe_karty():
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])
    player = Gracz("Maciek", 200)
    player.karty_w_dloni = Karty(["3x", "5x"])
    gra = Rozgrywka(player, [bot])
    gra.nowe_karty(1)
    assert gra.opis_kart_na_stole() == "Karty na stole: 2✦ "


def test_kolejna_runda():
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])
    player = Gracz("Maciek", 200)
    player.karty_w_dloni = Karty(["3x", "5x"])
    rozgrywka = Rozgrywka(player, [bot])
    rozgrywka.kolejna_runda()
    sprawdz_gre = {player: ("gra", 1), bot: ("gra", 2)}
    assert gra == sprawdz_gre
    sprawdz_kombinacje = {
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
    assert sprawdz_kombinacje == kombinacje
    assert rozgrywka.karty_na_stole() == []


def test_sprawdzenie_kombinacji():
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])
    player = Gracz("Maciej", 200)
    player.karty_w_dloni = Karty(["3x", "5x"])
    rozgrywka = Rozgrywka(player, [bot])
    rozgrywka.kolejna_runda()
    rozgrywka.sprawdzenie_kombinacji()
    sprawdz_kombinacje = {
        'poker_krolewski': [],
        'poker': [],
        'kareta': [],
        'full': [],
        'kolor': [(5, [5, 3], 'Maciej', player)],
        'strit': [],
        'trojka': [],
        '2pary': [],
        'para': [],
        'karta': [(5, [5, 3], 'Maciej', player), (5, [5, 2], 'Dominika', bot)]
    }
    assert sprawdz_kombinacje == kombinacje
