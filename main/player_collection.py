

from main.player import Player

class Human(Player):
    
    def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
        response = input("Take the card ? (y/n or (1/0) : ")
        
        if not response in ["y","n","0","1"]:
            print("I am sorry, I didn't understand your answer.")
            return self.brain_response(card,coin_stack,other_players)
        
        return int(response=="y" or response=="1")


class NoMan(Player):
    
    def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
        return 0

class YesMan(Player):
    
    def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
        return 1

class FinanceGuy(Player):
    
    def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
        return int(coin_stack>=(card-1))

class Economist(Player):
    
    def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
        return(card/3<coin_stack or coin_stack>=self.calculate_cost(card))

