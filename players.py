

from main.player import Player,AI

"""
Create your algorithms here !

If you want to simply create a player (without Artificial Intelligence and Training) :

    class YourPlayer(Player):
        def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
            #returns 1 or 0 (yes or no)
            ...
            return ?
    
       
If you want to use a Neural Network and train your AI (in stadium.py)

    class YourAI(AI):
        input_size:int=?
        layer_structure:list[int]=?
        
        def transform_input(self, card: int, coin_stack: int, other_players: list) -> list:
            return <list[int] of size 'input_size'>

See main.exemples or main.player_collections for more informations
"""