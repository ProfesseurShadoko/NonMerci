
from main.player_collection import Human,Economist
from main.game import Game
from main.exemple import BasicAI



players = [
    Human(),
    BasicAI(),
    Economist()
]

game = Game()
game.add_player(*players)
game.run()