from Hra import Game

game = Game()
#game.jo()
while game.run:
    game.jo()
    game.tohle_menu.ukazat_menu()
    game.loop()
