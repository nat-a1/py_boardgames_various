import numpy as np
import os
from colorama import Fore,Back,Style


class Board:
    def __init__(self,w,h):
        self.board=np.zeros((w,h))
        self.width,self.height=w,h

        self.board[int(w/2),int(h/2)]=1
        self.board[int(w/2-1),int(h/2-1)]=1
        self.board[int(w/2-1),int(h/2)]=-1
        self.board[int(w/2),int(h/2-1)]=-1

    def get_possible_dirs(self,x,y):
        """
            returns a list of valid directions from one cell
        """
        dirs=[]
        if(x>0):
            dirs.append([-1,0])
            if(y>0):
                dirs.append([-1,-1])
            if(y<self.height-1):
                dirs.append([-1,1])
        if(x<self.width-1):
            dirs.append([1,0])
            if(y>0):
                dirs.append([1,-1])
            if(y<self.height-1):
                dirs.append([1,1])
        if(y>0):
            dirs.append([0,-1])
        if(y<self.height-1):
            dirs.append([0,1])
        print(x,y,dirs)
        return dirs

    def get_chain(self,x,y,color,direction,chain):
        """
            recursively computes the length of a line of pieces to flip
            there's definitely a better way to do this
        """
        dx, dy= direction
        print(x+dx,y+dy,direction)
        if(x+dx > 9 or y+dy > 9 or x+dx <0 or y+dy <0):
            chain=[]
            return 0

        if(self.board[x+dx,y+dy]==0):
            chain=[]
            return 0

        if(self.board[x+dx,y+dy]==color*-1):
            chain.append([x+dx,y+dy])
            return self.get_chain(x+dx,y+dy,color,direction,chain)

        if(self.board[x+dx,y+dy]==color):
            return len(chain)
   
    def put_tile(self,x,y,color):
        self.board[x,y]=color
        self.flip_tiles(x,y,color)
            
    def flip_tiles(self,x,y,color):
        dirs = self.get_possible_dirs(x,y)
        score=0  
        for d in dirs:
            chain=[]
            if(self.get_chain(x,y,color,d,chain)>0):
                for c in chain:
                    self.board[c[0],c[1]]=color

    def get_score(self,x,y,color):
        """
            returns a score for a move
        """
        dirs = self.get_possible_dirs(x,y)
        score=0  
        for d in dirs:
            chain=[]
            score+=self.get_chain(x,y,color,d,chain)
        return score
        
    def get_scores(self,color):
        """
            get all scores for all positions in the board
        """
        scores=np.zeros((self.width,self.height))
        for x in range(self.width):
            for y in range(self.height):
                if(self.board[x,y]==0):
                    scores[x,y]=self.get_score(x,y,color)
        return scores
    
    def get_possible_positions(self,color):
        """
            returns wa list of playable moves
        """
        scores = self.get_scores(color)
        pos = np.where(scores>0)
        return pos

    def get_best_pos(self,color):
        """
            returns the position that flips the most pieces
        """
        scores = self.get_scores(color)
        pos = np.where(scores==np.max(scores))
        bestpos=()
        if(len(pos[0])>0):
            bestpos = (pos[0][0],pos[1][0])
        return bestpos

    def colored_print(self):
        """
            void, prints the board with a color for each player 
        """
        os.system('clear')
        # print coordinates?
        for i in range(self.width):
            print(i,end=" ")
        print("")

        for y in range(self.height):
            for x in range(self.width):
                if(self.board[x,y]==0):           
                    print(Style.RESET_ALL+".",end=" ")
                if(self.board[x,y]==1):
                    print(Fore.GREEN+"*",end=" ")
                if(self.board[x,y]==-1):
                    print(Fore.YELLOW+"*",end=" ")
            print(y)

board = Board(10,10)

board.colored_print()

def read_player_move():
    moves = input("your move:").split()
    
    x,y = [int(m) for m in moves]

    if(board.get_score(x,y,-1)!=0):
        board.put_tile(x,y,-1)
        aix,aiy = board.get_best_pos(1)
        board.put_tile(aix,aiy,1)
        board.colored_print()
    else:
        print("you can't place here!")
    #print("an error occured")



while(True):
    read_player_move()
    
