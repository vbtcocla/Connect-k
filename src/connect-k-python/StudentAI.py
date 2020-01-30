from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
#Start our own AI
class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.board = Board(col,row,k,g)
        self.player = 0

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

        #todo: Greedy best-first search
        return Move(0,0)
    
    def evaluate(self):
        #h(n) = the max number of consecutive moves by us - the max number of consecutive moves by our opponent
        steps = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self_max = 0
        opponent_max = 0

        #brute force solution to count the max number of consecutive moves at every position
        for i in range(self.row):
            for j in range(self.col):
                player = self.board.board[i][j]
                if(player != 0):
                    curr_max = 1
                    for step in steps:
                        temp_i = i
                        temp_j = j
                        for k in range(self.k-1):
                            temp_i+=step[0]
                            temp_j+=step[1]
                            if(self.board.board[i][j] != player):
                                break
                            else:
                                curr_max+=1
                    if(player == self.player):
                        self_max = max(curr_max, self_max)
                    else:
                        opponent_max = max(opponent_max, self_max)
        return self_max-opponent_max
