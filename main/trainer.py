
from main.exemple import AI,BasicAI

from main.utils.memory import Memory
from main.utils.style import Style
from main.utils.progress_bar import ProgressBar, ProgressIterator
from main.utils.population import Population
import sys

from main.game import Game

class Trainer:
    """Train your AI here.
        trainer = Trainer(YourAI)
        trainer.train(number_of_generations)
        trainer.evaluate_against(OtherPlayer) --> creates a game between 2 of your AIs and 2 OtherPlayer.
    """
    
    def __init__(self,cls:type,evolution_step:float=0.01):
        """
        Args:
            cls (type): YourAI (that you want to train) (if you train a trained AI, training is resumed)
            evolution_step (float, optional): range_of_values randomly added to all weights of the network. Defaults to 0.01.

        """
        self.cls = cls
        if not issubclass(cls,AI):
            raise Exception(f"Make sure you choose a class that inherits from AI, which is not the case for {cls.__name__} !")
        self.step=evolution_step
        self.load_population()        
    
    def load_population(self):
        try:
            self.population = Memory(self.cls.get_folder()).load("population")
            print(Style(text="green")(f"Successfully reloaded population  (generation n°{self.population.gen}) !"))
        except:
            print(Style(text="yellow")("Initializing new population..."))
            self.population = Population(input_size=self.cls.input_size, output_size=1,layer_structure=self.cls.layer_structure,population_size=61,evolution_step=self.step)
            self.population.gen=0
    
    def train(self,generations:int=100):
        """train your AI (see class description). Current progress is saved on keyboard interrupt (CTRL-C)

        Args:
            generations (int, optional): _description_. Defaults to 100.
        """
        bar = ProgressBar(generations*20*61)
        try:
            self.train_aux(generations,bar)
        except KeyboardInterrupt:
            bar.jammer.deactivate()
            print("\n")
            self.population.sort()
            Memory(self.cls.get_folder()).save(self.population,"population")
            print(Style(text="yellow")(f"KeyboardInterrupt --> progress successfully saved at generation n°{self.population.gen} !"))
            sys.exit(0)
            
    def train_aux(self,generations:int,bar:ProgressBar):
        
        for gen in range(generations):
            for ai1 in range(61):
                for group in range(20):
                    ai2 = (ai1+3*group+1)%61
                    ai3 = (ai1+3*group+2)%61
                    ai4 = (ai1+3*group+3)%61
                    
                    players=[
                        self.cls(self.population.network(ai1)),
                        self.cls(self.population.network(ai2)),
                        self.cls(self.population.network(ai3)),
                        self.cls(self.population.network(ai4)),
                    ]
                    indexes = [
                        ai1,
                        ai2,
                        ai3,
                        ai4,
                    ]
                    
                    game = Game(False)
                    game.add_player(
                        *players
                    )
                    
                    game.run()
                    bar.complete_task()
                    bar.update()
                    

                    for i in range(3):
                        ranked = game.players[i]
                        for j in range(4):
                            if ranked==players[j]:
                                self.population.reward(indexes[j],(3-i)**2)
            
            self.population.gen+=1
            if gen == generations-1: #in case of keyboard interrupt we save regularely
                self.population.sort()
                Memory(self.cls.get_folder()).save(self.population,"population")
            self.population.filter(0.3)
            
        

    def evaluate_against(self,cls:type):
        
        wins=0
        for _ in ProgressIterator(range(1000),"Testing reuslts..."):
            ai = self.cls()
            ai2 = self.cls()
            game = Game(False)
            game.add_player(
                ai,
                ai2,
                cls(),
                cls(),
            )
            game.shuffle()
            game.run()
            if ai==game.players[0] or ai2==game.players[0]:
                wins+=1
                
        print(f"Win rate againt {cls.__name__}() : {wins/1000:.1%}")
        


    
    
                