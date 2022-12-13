from main.game import Game
from main.player import Player,AI
from main.trainer import Trainer

from main.player_collection import Economist
from main.exemple import BasicAI,UpgradedAI

#train / create your algorithms here !

trainer = Trainer(UpgradedAI)
trainer.train(1000)
trainer.evaluate_against(Economist)
trainer.evaluate_against(BasicAI)

