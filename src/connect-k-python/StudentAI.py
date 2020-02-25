from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy

import time

from GameLogic import *
import sys
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class MyBoard(Board):
    def get_moves(self):
        moves = []
        if(self.g == 0):
            for j in range(self.col):
                for i in range(self.row):
                    if(self.is_valid_move(j,i)):
                        moves.append(Move(j,i))
        else:
            for j in range(self.col):
                if(self.is_valid_move(j)):
                        moves.append(Move(j,0))
        return moves

    def is_valid_move(self,col,row=-1,check_space=True):
        if(self.g == 1):
            for i in range(self.row-1,-1,-1):
                if  self.board[i][col] == 0:
                    row = i
                    break
        if col < 0 or col >= self.col:
            return False
        if row < 0 or row >= self.row:
            return False
        if (check_space and self.board[row][col] != 0):
            return False
        return True

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
        self.board = MyBoard(col,row,k,g)
        self.player = 0
        self.cutoff = 10 * (self.col + self.row)
        self.time_limit = 5.0

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

        best_score = -self.cutoff - 1
        best_move = Move(-1,-1)

        #Greedy best-first search
        # for j in range(self.col):
        #     if(self.g == 0):
        #         for i in range(self.row):
        #             #make a move on a temp board and evaluate the move
        #             if(self.board.is_valid_move(j, i)):
        #                 next_move = Move(j, i)
        #                 temp_board = self.board.make_move(next_move,self.player)
        #                 score = self.evaluate(temp_board.board)
        #                 if(score > best):
        #                     best = score
        #                     best_move = Move(j, i)
        #                 if(score == self.cutoff):
        #                     break
        #     else:
        #         #make a move on a temp board and evaluate the move
        #         if(self.board.is_valid_move(j)):
        #             next_move = Move(j, 0)
        #             temp_board = self.board.make_move(next_move,self.player)
        #             score = self.evaluate(temp_board.board)
        #             if(score > best):
        #                 best = score
        #                 best_move = Move(j, 0)
        #             if(score == self.cutoff):
        #                 break
        
        #IDS search with alpha-beta pruning
        moves = self.board.get_moves()
        search_time_limit = self.time_limit / len(moves)
        for move in moves:
            temp_board = self.board.make_move(move,self.player)
            score = self.IDS(temp_board,search_time_limit)
            if(score > best_score):
                best_move = move
                best_score = score
            if(score >= self.cutoff):
                break

        self.board = self.board.make_move(best_move,self.player)
        return best_move

    def get_opponent_number(self,player_number):
        return player_number % 2 + 1

    def IDS(self,board,time_limit):
        end_time = time.time() + time_limit
        depth = 1
        score = 0
        while(time.time() < end_time):
            score = self.alpha_beta(board,self.get_opponent_number(self.player),
                -self.cutoff-1,self.cutoff+1,depth,end_time)
            if(score >= self.cutoff):
                return score
            depth += 1
        return score
    
    #alpha-beta prunning search
    def alpha_beta(self,board,player,alpha,beta,depth,end_time):
        moves = board.get_moves()
        current_score = self.evaluate(board.board)
        if(time.time() >= end_time or depth == 0 or current_score >= self.cutoff):
            return current_score
        if(player == self.player):
            #alpha
            for move in moves:
                temp_board = board.make_move(move,player)
                alpha = max(alpha,self.alpha_beta(temp_board,self.get_opponent_number(player),alpha,beta,depth-1,end_time))
                if(beta <= alpha):
                    break
            return alpha
        else:
            #beta
            for move in moves:
                temp_board = board.make_move(move,player)
                beta = min(beta,self.alpha_beta(temp_board,self.get_opponent_number(player),alpha,beta,depth-1,end_time))
                if(beta <= alpha):
                    break
            return beta

    def evaluate(self,temp_board):
        #h(n) = the number of possible winning lines - the number of opponent's possible winning lines
        steps = [(0,1),(1,0),(1,1),(-1,1)]
        winning_lines = 0
        losing_lines = 0
        for j in range(self.col):
            for i in range(self.row):
                if(temp_board[i][j] == 0 or temp_board[i][j] == self.player):
                    for step in steps:
                        consecutive_moves = 0
                        if(temp_board[i][j] == self.get_opponent_number(self.player)):
                            consecutive_moves += 1
                        curr_i = i
                        curr_j = j
                        winning_lines += 1
                        for k in range(self.k-1):
                            curr_i += step[0]
                            curr_j += step[1]
                            if(curr_i < 0 or curr_i >= self.row or curr_j >= self.col
                            or temp_board[curr_i][curr_j] == self.get_opponent_number(self.player)):
                                winning_lines -= 1
                                break
                            elif(temp_board[curr_i][curr_j] != 0):
                                consecutive_moves += 1
                        if(consecutive_moves >= self.k):
                            return self.cutoff
                if(temp_board[i][j] == 0 or temp_board[i][j] == self.get_opponent_number(self.player)):
                    for step in steps:
                        consecutive_moves = 0
                        if(temp_board[i][j] == self.get_opponent_number(self.player)):
                            consecutive_moves += 1
                        curr_i = i
                        curr_j = j
                        losing_lines += 1
                        for k in range(self.k-1):
                            curr_i += step[0]
                            curr_j += step[1]
                            if(curr_i < 0 or curr_i >= self.row or curr_j >= self.col
                            or temp_board[curr_i][curr_j] == self.player):
                                losing_lines -= 1
                                break
                            elif(temp_board[curr_i][curr_j] != 0):
                                consecutive_moves += 1
                        if(consecutive_moves >= self.k):
                            return -self.cutoff
        return winning_lines - losing_lines

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