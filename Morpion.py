import numpy as np
from scipy.signal import convolve2d

"""
    tic tac toe
    players in this code are represented by numbers (-1 and 1)
    (this is for matrix convenience)
"""

class Morpion:
    def __init__(self):
        self.board = np.zeros((3,3))                # game board
        self.player_symbol = {0:" ",1:"X",-1:"O"}   # players symbols
        self.player = 1                             # current player

    def print_board(self):

        horizontal_line = " + - + - + - +\n"
        print("\n===============\n")
        for i in range(3):
            print(horizontal_line,*[self.player_symbol[b] for b in self.board.T[i]],sep=" | ",end=" |\n")
        print(horizontal_line)

    def play(self,x,y,player):                      # tries to place, and returns true has move has been successfully played

        if(x>2 or y > 2 or x<0 or y<0 or self.board[x,y]!= 0 ):
            print("invalid move!")
            return False
        self.board[x,y]= player
        return True

    def win(self,player):                           # win check?!

        identity, row = np.identity(3), np.ones((1,3))
        kernels = [ row, row.T, identity, np.flip(identity,1) ]

        for k in kernels:
            if(3 in convolve2d(self.board,k*player)):
                return True
        return False
    
    def cur_player_symbol(self):
        return self.player_symbol[self.player]


def game_loop():
    print("\n\n##### WELCOME #####\n","this is tic-tac-toe.\n","may the game begin!",sep="\n")

    game = Morpion()

    while(True):

        game.print_board()

        if(game.win(game.player)):
            print("yeyyy!","player "+game.cur_player_symbol()+" won!!!")
            break
        
        game.player *=-1
        valid_move = False

        while(not valid_move): # as long as there is no valid move

            try:               # ask for an input
                coords_str = input("player "+game.cur_player_symbol()+", please enter coordinates. (in the format: x y)\n>").split(" ")
                coords_int = int(coords_str[0]),int(coords_str[1])
            except:
                print("hmmm, invalid input.\n please, try again.\n")
                continue
            
            valid_move = game.play(coords_int[0],coords_int[1],game.player)
    

if __name__ == "__main__":
    game_loop()
