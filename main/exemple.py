

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


    

    
    