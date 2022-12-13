

#shadok imports
from shadok.abstract import ABC, abstractmethod
from shadok.network import Network,Population
from shadok.memory import Memory

#local imports
from main.exceptions import OutOfCoins


class Player(ABC):
    """A Player is an entity that allows you to make choices given an instance of game.
    It is an abstract class, so you need to inherit from it and define the function :
    
    def brain_response(self, card, coin_stack, other_players):
        *** determine if you should return 1 or 0 ***
        return 1 or 0
    
    With the arguments:
        - card = int = value of the card that is presented to you (1 means take the card, 0 means refuse and pay 1 coin)
        - coin_stack = number of coins on the card
        - other_players = list of the players you play against (player.coin = how many coins they have left / player.cards[n-3] = True if the player has the card n or not, else False)
    
    Once you've done it, you can call YourPlayer() to create an instance of the player.
    """
    
    id=1
    
    def __init__(self):
        self.cards=[False for i in range(3,36)]
        self.coins=0
        self.id = Player.id
        Player.id+=1
        
    
    def __str__(self):
        return f"{type(self).__name__} : {self.coins}$ || "+" ".join([str(card) for card in self.get_cards()])

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.id==__o.id
    
    def reset(self):
        self.cards=[False for i in range(3,36)]
        self.coins=0
    
    def get_response(self,card:int,coin_stack:int,other_players:list)->int:
        if self.coins==0:
            return 1
        else:
            return self.brain_response(
                card,
                coin_stack,
                other_players
            )
    
    def take_card(self,card:int,coin_stack:int)->None:
        self.cards[card-3]=True
        self.coins+=coin_stack
    
    def refuse_card(self)->None:
        if self.coins <=0:
            raise OutOfCoins()
        else:
            self.coins-=1
    
    def get_score(self)->int:
        relevant_cards = [i+3 for i in range(len(self.cards)) if self.cards[i] and (i==0 or not self.cards[i-1])]
        return sum(relevant_cards) - self.coins
    
    def get_cards(self)->list:
        return [card for card in range(3,36) if self.cards[card-3]]
    
    def card(self,card:int)->bool:
        """
        Args:
            card (int): searched card

        Returns:
            bool: do I have this card ?
        """
        return self.cards[card-3]
    
    def calculate_cost(self,card:int)->int:
        """present = self.get_score()
        player takes card in his hand (without taking coins)
        future = self.get_score()
        return present-future (can be -1 if you have the card 24 and you consider the card 23)
        """
        current = self.get_score()
        self.cards[card-3] = True
        future = self.get_score()
        self.cards[card-3]=False
        return future-current
    
    @abstractmethod
    def brain_response(self,card:int,coin_stack:int,other_players:list)->int:
        pass

class AI(Player):
    """AI inherits from Player and fills the function brain_response with a network applied on a list (and that returns 1 or 0)
    In the module trainer you'll see how to train your AI (you have to train it before using it). Then you will be able to call YourAi() to create a player.
    
    In order to define your AI, you must define :
    
    - YourAI.input_size := integer (size of the list you want to put in input of the network)
    - YourAI.layer_structure := list_of_integers (list of sizes of intermediate layers)
    If AI.input_size = 10 and AI.layer_structure = [5,2] --> network = Layer(10 --> 5) + Layer(5 --> 2) + Layer(2 --> 1)
    
    - def transform_input(self,card,coin_stack,other_players):
        *** extract relevent informations and put it in your list ***
        return list_of_size(AI.input_size)
    
    Then you can call in the stadium :
    trainer = Trainer(YourAI)
    trainer.train()
    
    player = YourAI() (the AI is stored in memory, automatically accessed)
    
    If you want to reset the training and start over (for exemple if you have changed YourAI.inputsize or YourAI.layer_structre), call YourAI.reset_AI()
    """
    
    input_size:int=None
    layer_structure:list=None
    
    def __init__(self,network:Network=None):
        super().__init__()
        if type(self).input_size==None or type(self).layer_structure==None:
            raise Exception(f"Please make sure to define {type(self).__name__}.input_size and {type(self).__name__}.layer_structure")
        
        if network==None:
            try:
                network = type(self).load().network
            except Exception as e:
                print(e)
                raise Exception("Failed to load any existing model !")
            
        self.network = network
    
    def __repr__(self)->str:
        return f"AI of type {type(self).__name__} (id={self.id}) : network = {str(self.network)}"
    
    @abstractmethod
    def transform_input(self,card:int,coin_stack:int,other_players:list)->list:
        pass
    
    def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
        input = self.transform_input(card,coin_stack,other_players)
        return self.network(input)
    
    @classmethod
    def get_folder(cls:type)->str:
        return "AI_memory/"+cls.__name__
    
    @classmethod
    def load(cls:type,rank:int=0):
        population:Population = Memory(cls.get_folder()).load("population")
        network = population.network(rank)
        return cls(network)

    @classmethod
    def reset_AI(cls:type):
        Memory(cls.get_folder()).reset()

        