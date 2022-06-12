from uczestnik import Gracz, Bot, Madry_Bot, Uczestnik
from karty import Karty
from io import StringIO


def test_uczestnik():
    uczestnik = Uczestnik("Maciek", 200)
    assert uczestnik.nazwa == "Maciek"
    assert uczestnik.pieniadze == 200
    assert uczestnik.karty_w_dloni.uklad_kart == []


def test_gracz_decyzja_za_duza_stawka(monkeypatch):
    uczestnik = Gracz("Maciek", 200)
    uczestnik.karty_w_dloni = Karty(["3x", "5x"])
    decyzja_input = StringIO("2")
    monkeypatch.setattr('sys.stdin', decyzja_input)
    assert uczestnik.decyzja(300) == "va banque"


def test_gracz_decyzja_pas(monkeypatch):
    uczestnik = Gracz("Maciek", 200)
    uczestnik.karty_w_dloni = Karty(["3x", "5x"])
    decyzja_input = StringIO("1")
    monkeypatch.setattr('sys.stdin', decyzja_input)
    assert uczestnik.decyzja(100) == "pas"


def test_gracz_decyzja_czekam(monkeypatch):
    uczestnik = Gracz("Maciek", 200)
    uczestnik.karty_w_dloni = Karty(["3x", "5x"])
    decyzja_input = StringIO("3")
    monkeypatch.setattr('sys.stdin', decyzja_input)
    assert uczestnik.decyzja(100) == "czekam"


def test_gracz_obstawianie(monkeypatch):
    uczestnik = Gracz("Maciek", 200)
    uczestnik.karty_w_dloni = Karty(["3x", "5x"])
    decyzja_input = StringIO("10")
    monkeypatch.setattr('sys.stdin', decyzja_input)
    assert uczestnik.obstawianie(100) == 110


def test_bot():
    bot = Bot("Dominika", 2000)
    assert bot.nazwa == "Dominika"
    assert bot.pieniadze == 2000
    assert bot.karty_w_dloni.uklad_kart == []


def test_bot_decyzja_za_malo_pieniedzy(monkeypatch):
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])

    def get_choice(a):
        return "pas"
    monkeypatch.setattr("uczestnik.choice", get_choice)
    assert bot.decyzja(3000) == "pas"


def test_bot_decyzja_random(monkeypatch):
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])

    def get_choice(a):
        return "obstawiam"
    monkeypatch.setattr("uczestnik.choice", get_choice)
    assert bot.decyzja(40) == "obstawiam"


def test_bot_dorownanie(monkeypatch):
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])

    def get_choice(a):
        return "dorównuję"
    monkeypatch.setattr("uczestnik.choice", get_choice)
    assert bot.dorownanie(40) == "dorównuję"


def test_bot_obstawianie(monkeypatch):
    bot = Bot("Dominika", 2000)
    bot.karty_w_dloni = Karty(["2x", "5y"])

    def get_randint(a, b):
        return 20
    monkeypatch.setattr("uczestnik.randint", get_randint)
    assert bot.obstawianie(40) == 60


def test_madry_bot_decyzja():
    bot = Madry_Bot("Hubert", 200)
    bot.karty_w_dloni = Karty(["2x", "2y", "7x", "7y", "9x"])
    assert bot.decyzja(20) == "podbijam"


def test_madry_bot_decyzja_gdy_duzo_pieniedzy():
    bot = Madry_Bot("Hubert", 20220)
    bot.karty_w_dloni = Karty(["2x", "3y", "7a", "8y", "9x"])
    assert bot.decyzja(20) == "podbijam"


def test_madry_bot_decyzja_z_slabymi_kartami():
    bot = Madry_Bot("Hubert", 220)
    bot.karty_w_dloni = Karty(["2x", "5y"])
    assert bot.decyzja(20) == "pas"


def test_madry_bot_obstawianie(monkeypatch):
    bot = Madry_Bot("Hubert", 2020)
    bot.karty_w_dloni = Karty(["2x", "3y", "7a", "8y", "9x"])

    def get_randint(a, b):
        return 1
    monkeypatch.setattr("uczestnik.randint", get_randint)
    assert bot.obstawianie(40) == 41
