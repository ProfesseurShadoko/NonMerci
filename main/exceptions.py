

class OutOfCoins(Exception):
    
    def __init__(self):
        super().__init__(f"Player out of coins ! Cannot refuse a card !")

class ExitGame(Exception):
    
    def __init__(self):
        super().__init__("Exiting Game !")