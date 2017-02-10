# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 22:25:00 2016

@author: cyber
"""

"""
Reference:

A comparison of feature functions for Tetris strategies
https://luckytoilet.wordpress.com/2011/05/27/coding-a-tetris-ai-using-a-genetic-algorithm/
https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
"""

from tetris.tetris_game.tetris_game_only import *

class boardscorer(object):
    
    def __init__(self,param,board,cleared,land_h):
        self.rows = len(board)-1
        self.cols = len(board[0])
        self.param = param
        self.board_nor = board
        self.board = self.transformer(board)
        self.set_height_colonne()
        self.clear_lines = cleared
        self.landing_height = land_h
            
    def transformer(self,board):
        bo_trans = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]
        return bo_trans

    def set_height_colonne(self):
        self.h_c = [self.rows]*self.cols
        for x,col in enumerate(self.board):
            y = 0
            while col[y] == 0:
                y += 1
                self.h_c[x] -= 1

    def calcul_some_values(self):
        self.bl = 0
        self.col_trans = 0
        self.rwh = set()
        self.holes = 0
        for x in range(self.cols):
            flag = False            
            col = self.board[x]
            for y in range(self.rows-1,self.rows-self.h_c[x]-1,-1):
                if col[y] == 0:
                    flag = True
                    self.holes += 1
                    self.rwh.add(y)
                elif flag:
                    self.bl += 1
                if col[y]^col[y-1]:
                    self.col_trans += 1
            self.col_trans -= 1
        
    def height(self):
        return max(self.h_c)
    
    def aggregate_height(self):
        return sum(self.h_c)
        
    def pseudo_holes(self):
        return self.holes
       
    def bumpiness(self):
        return sum([abs(self.h_c[i+1]-self.h_c[i]) for i in range(self.cols-1)])
        
    def blockade(self):
        return self.bl
        '''
        bl = 0
        for x in range(self.cols):
            flag = False            
            col = self.board[x]
            for y in range(self.rows-1,self.rows-self.h_c[x]-1,-1):
                if col[y] == 0:
                    flag = True
                elif flag:
                    bl += 1
        return bl
        '''
        
    def row_transitions(self):
        row_trans = 0
        for row in self.board_nor[:-1]:
            if row.count(0) < len(row):
                for x in range(self.cols-1):
                    if row[x]^row[x+1]:
                        row_trans += 1
                if row[0] == 0:
                    row_trans += 1
                if row[self.cols-1] == 0:
                    row_trans += 1
        return row_trans
        
    def colonne_transitions(self):
        return self.col_trans
        '''
        col_trans = 0
        for col in self.board:
            for i in range(self.rows):
                if col[i] ^ col[i+1]:
                    col_trans += 1
            col_trans -= 1
        return col_trans
        '''

    def rows_with_holes(self):
        return len(self.rwh)        
        '''
        rwh = set()
        for x in range(self.cols):
            for y in range(self.rows-1,self.rows-self.h_c[x]-1,-1):
                if self.board[x][y] == 0:
                    rwh.add(y)
        return len(rwh)
        ''' 
    
    def score(self):
        score = 0
        self.calcul_some_values()
        score += self.param[0]*self.height()
        score += self.param[1]*self.aggregate_height()
        score += self.param[2]*self.clear_lines
        score += self.param[3]*self.pseudo_holes()
        score += self.param[4]*self.bumpiness()
        score += self.param[5]*self.blockade()
        score += self.param[6]*self.landing_height
        score += self.param[7]*self.row_transitions()
        score += self.param[8]*self.colonne_transitions()
        score += self.param[9]*self.rows_with_holes()
        '''
        score += -abs(self.param[0]*self.height())
        score += -abs(self.param[1]*self.aggregate_height())
        score += abs(self.param[2]*self.clear_lines)
        score += -abs(self.param[3]*self.pseudo_holes())
        score += -abs(self.param[4]*self.bumpiness())
        score += -abs(self.param[5]*self.blockade())
        score += -abs(self.param[6]*self.landing_height)
        score += -abs(self.param[7]*self.row_transitions())
        score += -abs(self.param[8]*self.colonne_transitions())
        score += -abs(self.param[9]*self.rows_with_holes())
        '''
        return score
    

class scorer_simple(boardscorer):
    
    def pseudo_holes(self):
        return sum([self.h_c[i]-(self.rows-self.board[i].count(0)) for i in range(self.cols)])    
    
    def score(self):
        score = 0
        score += self.param[0]*self.height()
        score += self.param[1]*self.aggregate_height()
        score += self.param[2]*self.clear_lines
        score += self.param[3]*self.pseudo_holes()
        score += self.param[4]*self.bumpiness()
        score += self.param[5]*self.landing_height
        '''
        score += -abs(self.param[0])*self.height()
        score += -abs(self.param[1])*self.aggregate_height()
        score += abs(self.param[2])*self.clear_lines
        score += -abs(self.param[3])*self.pseudo_holes()
        score += -abs(self.param[4])*self.bumpiness()
        score += -abs(self.param[5])*self.landing_height
        '''
        return score
        
        
class scorer_4(boardscorer):

     def score(self):
        score = 0
        score += self.param[0]*self.aggregate_height()
        score += self.param[1]*self.clear_lines
        score += self.param[2]*self.pseudo_holes()
        score += self.param[3]*self.bumpiness()
        return score
        
test_param_4 = [-0.510066,0.760666,-0.35663,-0.184483]