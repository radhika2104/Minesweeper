import random
class Player:
    def __init__(self):
        player_name = input("pls enter player's name: ")
        self.player = player_name

    def get_move(self,game):
        pass

class Human(Player):
    def __init__(self):
        super().__init__()

    def get_move(self,game):
        valid_square = False
        #we want the Player to be able to get its next move in the game
        while not valid_square:
            print()
            move = input('Enter a valid move: ')
            try:
                move = int(move)
                if move not in game.available_moves():
                    raise ValueError
                valid_square = True
                #print('\n','User selected move:',move)
            except ValueError:
                print('invalid move. pls try again.')
        return move

class RandomComputer(Player):
    def __init__(self):
        self.player = 'Random Computer'
        print('User name:',self.player)

    def get_move(self,game):
        move = random.choice(game.available_moves())
        print('\n','User selected move:',move)
        return move

class GeniusComputer(Player):
    def __init__(self):
        self.player = 'Genius Computer'
        print('User name:',self.player)

    def get_move(self,game): #function incomplete
        if game.user_guide_board==None:
            move = random.choice(game.available_moves())

            #print('\n','User selected move:',move)
        return move
