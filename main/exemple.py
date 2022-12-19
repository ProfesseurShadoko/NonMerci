
from main.player import AI
        
class BasicAI(AI):
    
    input_size:int=4
    layer_structure:list=[3]

    def transform_input(self, card: int, coin_stack: int, other_players: list) -> list:
        return [card,self.calculate_cost(card),coin_stack,self.coins]


class UpgradedAI(AI):
    
    input_size:int=6
    layer_structure:list=[4]
    
    def transform_input(self, card: int, coin_stack: int, other_players: list) -> list:
        return [card,self.calculate_cost(card),self.distance_up(card),self.distance_down(card),coin_stack,self.coins]
    
    def distance_up(self,card:int)->int:
        dist = 0
        for i in range(card+1,36):
            dist+=1
            if self.card(i):
                return dist
        return dist
    
    def distance_down(self,card:int)->int:
        dist = 0
        for i in range(card-1,2,-1):
            dist+=1
            if self.card(i):
                return dist
        return dist

class MyAI(UpgradedAI):
    
    input_size:int=13
    layer_structure:list=[7,3]
    
    def transform_input(self, card: int, coin_stack: int, other_players: list) -> list:
        card_status = self.card_status(other_players)
        return [
            card,
            self.calculate_cost(card),
            self.distance_up(card),
            self.distance_down(card),
            self.up_possibility(card,card_status),
            self.down_possibility(card,card_status),
            card_status.count(0)-9, #how many cards left ?
            coin_stack,
            min([player.coins for player in other_players]),
            other_players[0].calculate_cost(card),
            other_players[1].calculate_cost(card),
            other_players[2].calculate_cost(card),
            self.coins,
        ]
    
    def card_status(self,other_players:list)->list:
        out = [0 for i in range(3,36)]
        for card in range(3,36):
            for i,player in enumerate(other_players,start=1):
                if player.card(card):
                    out[card-3]=i
                    break
        return out
    
    def up_possibility(self,card:int,card_status:list)->int:
        for card in range(card+1,36):
            if self.card(card):
                return 1 #I am able to fill the gap between myself and the card
            if card_status[card-3] != 0:
                return 0 #someone has the card I want
        return 0 #I have no card above this card, there is no gap to fill
    
    def down_possibility(self,card:int,card_status:list)->int:
        for card in range(card-1,2,-1):
            if self.card(card):
                return 1
            if card_status[card-3]:
                return 0
        return 0


    

    
    