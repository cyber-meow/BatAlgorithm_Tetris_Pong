# -*- coding: utf-8 -*-
"""
Created on Tue May 17 04:32:25 2016

@author: cyber
"""

from random import randint
from utilities import setAllArgs


class pong(object):
    
    WIDTH = 600
    HEIGHT = 400
    BALL_RADIUS = 20
    PAD_WIDTH = 8
    
    
    def __init__(self, PAD_HEIGHT= 80, **kwargs): 
        self.PAD_HEIGHT = PAD_HEIGHT
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT / 2
        setAllArgs(self, kwargs)
        self.init_game()
        
    def init_game(self):
        self.score1, self.score2 = 0,0
        self.success_1, self.success_2 = 0,0
        self.restart()

        
    def init_ball(self,right,up):
        self.ball_pos = [self.WIDTH/2, self.HEIGHT/2]
        self.ball_vel = [randint(2,5) for _ in range(2)]
        self.directionx = 1 if right else -1
        self.directiony = 1 if up else -1
            
    def init_paddle(self):
        self.paddle1_vel = 5
        self.paddle2_vel = 5
        self.paddle1_pos = [0, self.HEIGHT/2-self.PAD_HEIGHT/2]
        self.paddle2_pos = [self.WIDTH-self.PAD_WIDTH, self.HEIGHT/2-self.PAD_HEIGHT/2]            
            
            
    def restart(self):
        self.init_paddle()        
        self.init_ball(randint(0,1),randint(0,1))

        
    
    def update_ball_pos(self):

        self.check_collision1()
        self.check_collision2()
        
        if self.ball_pos[1]>self.HEIGHT-self.BALL_RADIUS or (
            self.ball_pos[1] < self.BALL_RADIUS):
            self.directiony *= -1
        
        self.ball_pos[0] += self.ball_vel[0]*self.directionx
        self.ball_pos[1] += self.ball_vel[1]*self.directiony
        
        if self.ball_pos[0]<0:
            self.score2 +=1
            self.restart()
        elif self.ball_pos[0]>self.WIDTH:
            self.score1 +=1
            self.restart()
    
    
    def check_collision2(self):
        
        if self.ball_pos[0] > self.WIDTH - self.BALL_RADIUS - self.PAD_WIDTH and (
            abs((self.paddle2_pos[1]+self.HALF_PAD_HEIGHT)-self.ball_pos[1]) < (
            self.HALF_PAD_HEIGHT+self.BALL_RADIUS)):

            self.directionx *= -1 #change direction
            self.ball_vel[0] += 1 # speed up ball in x
            self.ball_vel[1] += 1 # speed up ball in y
            self.paddle1_vel += 1 # speed up paddle1 
            self.paddle2_vel += 1 # speed up paddle2
            self.success_2 += 1
    
    def check_collision1(self):
        
        if self.ball_pos[0] < self.BALL_RADIUS + self.PAD_WIDTH and (
            abs((self.paddle1_pos[1]+self.HALF_PAD_HEIGHT)-self.ball_pos[1]) < (
            self.HALF_PAD_HEIGHT+self.BALL_RADIUS)):

            self.directionx *= -1 #change direction
            self.ball_vel[0] += 1 # speed up ball in x
            self.ball_vel[1] += 1 # speed up ball in y
            self.paddle1_vel += 1 # speed up paddle1 
            self.paddle2_vel += 1 # speed up paddle2
            self.success_1 +=1
    
    
    def update_pos_paddle1(self,n):

        if n <= -0.5:
            self.paddle1_pos[1] += self.paddle1_vel
            if self.paddle1_pos[1] > self.HEIGHT-self.PAD_HEIGHT:
                self.paddle1_pos[1] = self.HEIGHT-self.PAD_HEIGHT
        if n >= 0.5:
            self.paddle1_pos[1] -= self.paddle1_vel
            if self.paddle1_pos[1] < 0:
                self.paddle1_pos[1] = 0
            
    def update_pos_paddle2(self,n):
        
        if n <= -0.5:
            self.paddle2_pos[1] += self.paddle2_vel
            if self.paddle2_pos[1] > self.HEIGHT-self.PAD_HEIGHT:
                self.paddle2_pos[1] = self.HEIGHT-self.PAD_HEIGHT
        if n >= 0.5:
            self.paddle2_pos[1] -= self.paddle2_vel
            if self.paddle2_pos[1] < 0:
                self.paddle2_pos[1] = 0
                
                

class pong_seul(pong):
    
    def check_collision2(self):
        
        if self.ball_pos[0] > self.WIDTH - self.BALL_RADIUS - self.PAD_WIDTH:

            self.directionx *= -1
            self.ball_vel[0] += 1
            self.ball_vel[1] += 1
            self.paddle1_vel += 1