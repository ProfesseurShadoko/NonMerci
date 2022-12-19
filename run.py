
from main.player_collection import Human,Economist
from main.game import Game
from main.exemple import BasicAI

from players import *

"""
Here you can play against the players you have created (AIs must have been trained first). Reminder : AIs are trained for games with 4 players.
In order to play, run :

players = [
    player1,
    player2,
    player3,
    player4
] (I you want to play, use Human() as a player !)
game=Game()
game.add_player(*players)
game.run()
"""

players = [
    Human(),
    BasicAI(),
    Economist()
]

game = Game()
game.add_player(*players)
game.run()