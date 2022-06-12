from rozgrywka import Rozgrywka
from uczestnik import Madry_Bot, Gracz, Bot


bot = Madry_Bot("Patrycja", 50)
bot2 = Bot("Eryk", 50)
bot3 = Bot("Kinga", 50)
bot4 = Madry_Bot("Marcin", 50)
bot5 = Madry_Bot("Zdzisiek", 50)
bot6 = Madry_Bot("Anna", 50)
bot7 = Madry_Bot("Łukasz", 50)
player = Gracz("Dominika", 5)
game = Rozgrywka(player, [bot, bot2, bot3, bot4, bot5])
game.play()
