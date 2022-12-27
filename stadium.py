from main.trainer import Trainer

from main.player_collection import Economist
from main.exemple import BasicAI,UpgradedAI,MyAI
from players import *

"""
here you can train your algorithms. In order to train a model (it must inherit from AI), run :

trainer = Trainer(YourAI)
trainer.train(1000)                                 --> everything will be saved on Keyboard Interrupt

trainer.evaluate_against(OtherPlayerClass)       --> test your model against an other model (creates 4 player games with two of each)


YourAI.reset_AI() #allows you to reset the training of your AI. You'll have to use it if you change network structure and input size.
"""

trained = UpgradedAI

opponents = [
    Economist,
    BasicAI,
    UpgradedAI,
]

trainer = Trainer(trained)
trainer.train(100)
for opponent in opponents:
    trainer.evaluate_against(opponent)

