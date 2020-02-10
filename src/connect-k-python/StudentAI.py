from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy

from GameLogic import *
import sys
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0
    cutoff = 0

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.board = Board(col,row,k,g)
        self.player = 0
        self.cutoff = self.col + self.row

    def get_move(self,move):
        # if self.g == 0:
        #     return Move(randint(0,self.col-1),randint(0,self.row-1))
        # else:
        #     return Move(randint(0,self.col-1),0)
        
        #Identify our player number
        if(self.player == 0):
            if(move.row == -1 & move.col == -1):
                self.player = 1
            else:
                self.player = 2
        #update board
        if(move.row != -1 or move.col != -1):
            self.board = self.board.make_move(move, self.player % 2 + 1)
        

        #Greedy best-first search
        best = -self.row - self.col
        best_move = Move(-1,-1)
        for j in range(self.col):
            if(self.g == 0):
                for i in range(self.row):
                    #make a move on a temp board and evaluate the move
                    if(self.board.board[i][j] == 0):
                        temp_board = copy.deepcopy(self.board.board)
                        temp_board[i][j] = self.player
                        score = self.evaluate(temp_board)
                        if(score > best):
                            best = score
                            best_move = Move(j, i)
            else:
                #make a move on a temp board and evaluate the move
                i = self.space_on_column(j)
                if(i != -1):
                    temp_board = copy.deepcopy(self.board.board)
                    temp_board[i][j] = self.player
                    score = self.evaluate(temp_board)
                    if(score > best):
                        best = score
                        best_move = Move(j, 0)
                    if(score == self.cutoff):
                        break
        self.board = self.board.make_move(best_move,self.player)
        return best_move
    
    #determine the first space on a column
    def space_on_column(self, col):
        for i in range(self.row-1, -1, -1):
            if(self.board.board[i][col] == 0):
                return i
        return -1

    def evaluate(self,temp_board):
        #h(n) = the max number of consecutive moves by us - the max number of consecutive moves by our opponent
        steps = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self_max = 0
        opponent_max = 0

        #brute force solution to count the max number of consecutive moves at every position
        for i in range(self.row):
            for j in range(self.col):
                player = temp_board[i][j]
                if(player != 0):
                    for step in steps:
                        isPotential = False
                        curr_max = 1
                        temp_i = i
                        temp_j = j
                        for k in range(1, self.k):
                            temp_i+=step[0]
                            temp_j+=step[1]

                            #if current line can't win, abandon it
                            if(temp_i < 0 or temp_j < 0 or temp_i >= self.row 
                            or temp_j >= self.col or temp_board[temp_i][temp_j] == player % 2 + 1):
                                curr_max = 0
                                break

                            elif(temp_board[temp_i][temp_j] == 0):
                                #if there is a move after '0', 
                                #see it as a potential consecutive line and continue
                                if(temp_i+step[0] >= 0 and temp_j+step[1] >= 0 and temp_i+step[0] < self.row 
                            and temp_j+step[1] < self.col and temp_board[temp_i+step[0]][temp_j+step[1]] == player):
                                    isPotential = True

                                else:
                                    break

                            #if current line already wins, make it the next move
                            elif(player == self.player and curr_max == self.k-1):
                                return self.cutoff

                            #if opponent is winning, try to stop it
                            elif(player != self.player and (curr_max == self.k-2
                            or (curr_max == self.k-3 and i-step[0] >= 0 and i-step[0] < self.row
                            and j-step[1] >= 0 and j-step[1] < self.col and temp_board[i-step[0]][j-step[1]] == 0))):
                                curr_max = self.cutoff
                                if(isPotential):
                                    break
                            
                            else:
                                curr_max+=1
                        if(player == self.player):
                            self_max = max(curr_max, self_max)
                        else:
                            opponent_max = max(curr_max, opponent_max)
        return self_max-opponent_max

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('Invalid Parameters')
        sys.exit(-1)
    col = int(sys.argv[1])
    row = int(sys.argv[2])
    k = int(sys.argv[3])
    g = int(sys.argv[4])
    mode = sys.argv[5]
    main = GameLogic(col,row,k,g,mode,debug=True)
    main.Run()