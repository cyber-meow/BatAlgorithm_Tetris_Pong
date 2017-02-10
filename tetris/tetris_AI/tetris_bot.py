# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:08:37 2016

@author: cyber
"""

from tetris.tetris_game.tetris_game_only import *
from tetris.tetris_AI.tetris_scorer import *

class bot(object):
    
    def __init__(self,param,taille):
        self.cols, self.rows = taille
        self.move = 0
        self.rotate = 0
        self.param = param
    
    def testdrop(self,grille0,stone,x):
        for y in range(self.rows+1):
            if grille0.check_collision(stone,(x,y)):
                if y == 0:
                    return False
                landing_h = self.rows-y-len(stone)+1
                grille0.board = join_matrixes(grille0.board,stone,(x,y))
                cleared_rows = []
                for i in range(self.rows):
                    row = grille0.board[i]
                    if 0 not in row:
                        cleared_rows.append(i)
                if cleared_rows != []:
                    has_cleared = grille0.remove_rows(cleared_rows)
                else:
                    has_cleared = []
                break
        def change_back():
            if has_cleared != []:
                grille0.add_rows(has_cleared)
            grille0.board = remove_matrixes(grille0.board,stone,(x,y))
        return grille0,len(cleared_rows),landing_h,change_back

    def scorer(self,board,clear,landing_h):
        sc = boardscorer(self.param,board,clear,landing_h)
        return sc.score()

    # pl est True quand un nouveau stone arrive
    def play(self,grille0,stone,x,y,ne,pl):
        if pl:
            maxscore = float("-inf")
            maxcouple = None
            for r in range(4):
                for c in range(self.cols):
                    res = self.testdrop(grille0,stone,c)
                    if res:
                        newscore = self.scorer(res[0].board,res[1],res[2])
                        if newscore > maxscore:
                            maxscore = newscore
                            maxcouple = (r,c)
                        res[3]()
                stone = rotate_clockwise(stone)
            self.rotate = maxcouple[0]
            self.move = maxcouple[1] - x
        if self.move < 0:
            self.move += 1
            return "LEFT"
        elif self.move >0 and (
             self.rotate == 0 or self.cols-x > max(len(stone[0]),len(stone))):
            self.move -= 1
            return "RIGHT"
        elif self.rotate != 0:
            self.rotate -= 1
            return "UP"
        else:
            return "DOWN"

class bot_simple_scorer(bot):
    def scorer(self,board,clear,landing_h):
        sc = scorer_simple(self.param,board,clear,landing_h)
        return sc.score()


class bot_2_pieces(bot):
    
    def play(self,grille0,stone,x,y,ne,pl):
        if pl:
            maxscore = float("-inf")
            maxcouple = None
            for r1 in range(4):
                for c1 in range(self.cols):
                    res = self.testdrop(grille0,stone,c1)
                    if res:
                        for r2 in range(4):
                            for c2 in range(self.cols):
                                res2 = self.testdrop(res[0],ne,c2)
                                if res2:
                                    newscore = self.scorer(res2[0].board,res[1]+res2[1],res[2])                     
                                    if newscore > maxscore:
                                        maxscore = newscore
                                        maxcouple = (r1,c1)
                                    res2[3]()
                            ne = rotate_clockwise(ne)
                        res[3]()                            
                stone = rotate_clockwise(stone)
            self.rotate = maxcouple[0]
            self.move = maxcouple[1] - x
        if self.move < 0:
            self.move += 1
            return "LEFT"
        elif self.move >0 and (
             self.rotate == 0 or self.cols-x > max(len(stone[0]),len(stone))):
            self.move -= 1
            return "RIGHT"
        elif self.rotate != 0:
            self.rotate -= 1
            return "UP"
        else:
            return "DOWN"
            
            
class bot_scorer_4(bot):
    def scorer(self,board,clear,landing_h):
        sc = scorer_4(self.param,board,clear,landing_h)
        return sc.score()