# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:51:07 2016

@author: cyber
"""

from pong.pong_game import *
import pygame


class pong_evalu_seul(pong_seul):
    
    def evalu(self,bot,interval= 1):
    
        cmp, cmp2, res = 0,0,0
        
        up = 250
        down = 150
        
        self.init_game()
        
        while max(self.score1,self.score2)<=5:
    
            posy = self.paddle1_pos[1]
            vel = self.ball_vel
            pos = self.ball_pos
            
            old_suc = self.success_1
            old_sc2 = self.score2
            self.update_ball_pos()
            if cmp % interval == 0:            
                res1 = bot(self)
                self.update_pos_paddle1(res1)
            cmp +=1
            
                    
            if down <= posy and posy <= up:
                cmp2 +=1
            else:
                cmp2 = 0
                up = posy + 50
                down = posy - 50
            
            if self.score2 == old_sc2+1:
                cmp2 = 0
            if self.success_1 == old_suc+1:
                res += cmp2
                cmp2 = 0
                    
        return cmp



class pong_display_seul(pong_seul):
    
    def display(self,bot,interval= 1):
        
        black = (0, 0, 0)
        white = (255, 255, 255)
        blue =  (0, 0, 255)
        
        size = [self.WIDTH, self.HEIGHT]
        screen = pygame.display.set_mode(size)
        
        pygame.display.set_caption('Test')
        
        clock = pygame.time.Clock()
        
        cmp = 0
        done = False
        self.init_game()
        
        while done == False:
        
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True 
        
            screen.fill(black)
        
            self.update_ball_pos()
            if cmp % interval == 0: 
                res1 = bot(self)
                self.update_pos_paddle1(res1)
            
            
            ball_x = int(self.ball_pos[0])
            ball_y = int(self.ball_pos[1])
            
            pygame.draw.circle(screen, white, [ball_x, ball_y], self.BALL_RADIUS)
            pygame.draw.rect(screen, blue, [self.paddle1_pos[0],self.paddle1_pos[1],
                                            self.PAD_WIDTH,self.PAD_HEIGHT])
            pygame.draw.rect(screen, blue, [self.paddle2_pos[0],0,
                                            self.PAD_WIDTH,self.HEIGHT])
                    
            pygame.display.flip()
            clock.tick(30)
            cmp += 1
        
        pygame.quit ()
