# Non Merci

*Non Merci* (*No Thanks! in english*) is a game that I enjoy a lot. The idea of the game is very simple, I'll explain the rules down below.
Anyway, I was wondering what the best strategy was, what was the right decision to make and when. 
So I decided to implement the game in python to test it out. I implemented the rules, created players,
and created a structure to make the construction of AIs, trained by reinforcement (they are playing against themselves), 
very easy. And this is what I created:

## Rules
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
 
Then he has a score of (3+8+19+0+0+35) - 5 = 60

Simple, right? For each move, you have one decision to make, whether you should take the card or not. 
Now, it's time to build algorithms!

## How to use this project?
What do we do with this project? The goal is to create players, train them, and play against them. So let's do it!

### Installation
You can install this project wherever you want, either by downloading it or by runnning:

```bash
  git clone https://github.com/ProfesseurShadoko/shadok.git
```

### Creating a Player
Player are not AIs, they cannot be trained. You can create them by modifying players.py:
 
 ```python
class YourPlayer(Player):
  def brain_response(self, card: int, coin_stack: int, other_players: list) -> int:
      #returns 1 or 0 (yes or no)
      ...
      return ?
 ```
 For exemple, the method brain_response from the class **Human**, that you can find in main/player_collection.py,
 just asks you in the console what you want to do.
 
 ### Creating and AI
 AIs are a bit different. The brain_response is alredy implemented, by calling the method transform_input(...)
 that returns a list, and feeding the Neural Network with this list and returning 1 or 0, depending
 on what the AI has answered. You also need to define the structure of the Network. So let's modify
 players.py again:
 
```python
class YourAI(AI):
  input_size:int=?
  layer_structure:list[int]=?

  def transform_input(self, card: int, coin_stack: int, other_players: list) -> list:
      return <list[int] of size 'input_size'>
 ```
 
 You can find exemples at main/exemples.py
 
 ### Training an AI
 This time, go to stadium.py:
 
 ```python
trainer = Trainer(YourAI)
trainer.train()
trainer.evaluate_against(YourPlayer)
 ```
 
 And that's it!
 
 ### Playing against your AI
 Finally, you can go to run.py if you want to play, or see your AIs play together. You just need to run:
 
```python
players = [
    Human(),
    YourAI(),
    YourPlayer()
]

game = Game()
game.add_player(*players)
game.run()
 ```
 
 Game on! You'll see, your AIs become quickly better than you!
 
 ***
 
 Have fun! 😄

 
 

