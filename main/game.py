from main.player import Player
from main.player_collection import Human,Economist

from main.utils.style import Style
import numpy.random as rd
import time

class Game:
    """allows to simulate games between various players. To run a game, proceed as follows:
            game=Game()
            game.add_player(
                player_one, #inherits from Player
                player_two,
                ...
            )
            game.run()
            
            --> use player.get_score() to get the results, when execution is completed, game.players is sorted by score.
        
    The rules of the game are the following.
    1. The purpous of the game is to have the least points possible
    2. Cards count as positive points (so you don't want to collect them) and coins as negative
    3. Cards are all te integers between 3 and 35 (included), but 9 of them are randomly removed at the begining
    4. To start the game, give each player 11 coins and draw a first card. The players, one after another, have the following choice :
        - refuse the card an put a coin on the card (so you lose 1 pt)
        - take the card (so you lose the value of the card) and take all the coins on the card
    5. When you take a card, you draw the next card and take it or pay and the game continues.
    6. If you have no coins left, you are forced to take the card (by doing this you get some coins and you are able to say no again)
    7. When there are no cards left, the game ends and each player counts their points :
        - each coin you have left counts as -1
        - the card n counts as +n points only if you don't have the card n-1. If you have the card n-1, the card n counts as 0.
    
    For exemple if a players has:
        - 5 coins
        - the cards 3 8 19 20 21 35
    he has a score of (3+8+19+0+0+35) - 5 = 60
    
    WARNING : when using trained AI, the number of players is 4.

    """
    
    def __init__(self,show:bool = True):
        """
        Args:
            show (bool, optional): displays necessary infos to follow the game. When training, put this to False, and nothing will be printed. Defaults to True.
        """
        self.deck = [i for i in range(3,36)]
        rd.shuffle(self.deck)
        
        for i in range(9):
            self.deck.pop()
        
        self.card=None
        self.coin_stack = 0
        self.players=[]
        self.turn=0
        self.show = show
    
    def __repr__(self)->str:
        return f"{Style(text='green')(self.card)} : {Style(text='yellow')(str(self.coin_stack)+'$')}  -  ({len(self.deck)} cards left)"
    
    def add_player(self,*args:Player)->None:
        for player in args:
            self.players.append(player)
    
    def shuffle(self)->None:
        """shuffles the order of the players"""
        rd.shuffle(self.players)
    
    def get_player(self,i:int=None)->Player:
        """returns requested player

        Args:
            i (int, optional): Returns the player corresponding to the index i%len(players). Defaults to None, is that case player who has to play is returned.
        """
        if i==None:
            i=self.turn
        return self.players[i%len(self.players)]
    
    def parse_response(self,response:int)->None:
        """updates game and players depending on the response of the player

        Args:
            response (int): take card (1) or pay (0)
        """
        player = self.get_player()
        
        if response==0:
            player.refuse_card()
            self.coin_stack+=1
        else:
            player.take_card(self.card,self.coin_stack)
            self.card=None
            self.coin_stack = 0
    
    def ask(self)->None:
        """ask player for his decision an makes all the changes necessary
        """
        player = self.get_player()
        if self.card==None:
            raise Exception("self.current_card shouldn't be None when you ask someone if he wants to take it")
        other_players=[self.get_player(self.turn+i) for i in range(1,len(self.players))]
        res = player.get_response(self.card,self.coin_stack,other_players)
        self.parse_response(res)
    
    def run(self):
        """main loop"""
        self.turn=0
        for player in self.players:
            player.reset()
            player.coins=11
            
        while self.deck:
            
            #do we need to draw a card ?
            if self.card==None:
                self.card=self.deck.pop()
            
            player = self.get_player()
            if self.show:
                print("\n")
                print(self.__repr__())
                print(player)
                time.sleep(1)
            self.ask()
            
            if self.show:
                if self.card==None:
                    print(f"{player} says {Style(text='green')('YES')}")
                else:
                    print(f"{player} says {Style(text='red')('NO')}")
                time.sleep(1)
            
            if self.card!=None:
                self.turn+=1
                
        self.players.sort(key=lambda x:x.get_score())
        if self.show:
            print("\n\n\nRESULTS :")
            for i,player in enumerate(self.players,start=1):
                print(f"{i}. {player} --> score:{player.get_score()}")


            