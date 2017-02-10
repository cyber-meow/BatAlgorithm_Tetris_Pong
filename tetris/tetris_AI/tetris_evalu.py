from tetris.tetris_game.tetris_game_only import *
import pygame
import time
from random import randint

class Tetris_evalu(TetrisApp1):

    # 5 actions pour chaque drop    
    def evalu(self,bot,param):        
        key_actions = {
            'LEFT':	lambda:self.move(-1),
            'RIGHT':	lambda:self.move(+1),
            'DOWN':    self.drop,
           	 'UP':	self.rotate_stone,
             None:     lambda:None
        }
        
        bot0 = bot(param,(self.cols,self.rows))
        self.gameover = False
        self.init_game()
        cmp = 0
        play = True
        t = time.time()
        oldline = 0
        
        while not self.gameover:
            action = bot0.play(self.grille,self.stone,
                               self.stone_x,self.stone_y,self.next_stone,play)
            play = False
            if key_actions[action]():
                play = True
            if cmp%5 == 0:
                if self.drop():
                    play = True
            cmp += 1
            if self.lines%1000 == 0 and self.lines != oldline:
                print(self.lines,time.time()-t)
                oldline = self.lines
        return cmp,self.lines,time.time()-t
    

cell_size =	18
maxfps = 	30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35)]

class Tetris_display(TetrisApp1):
    
    def init_display(self):
        pygame.init()
        self.width = cell_size*(self.cols+6)
        self.height = cell_size*self.rows
        self.rlim = cell_size*self.cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(self.cols)] 
                                for y in range(self.rows)]
        self.default_font =  pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.pause = False
        
    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(line,False,(255,255,255),(0,0,0)),(x,y))
            y += 14

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x+x)*cell_size,
                            (off_y+y)*cell_size, cell_size, cell_size),0)

    def fpause(self):
        self.pause = not self.pause

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False    
    
    def display(self,bot,param):
        key_actions = {
            'LEFT':	lambda:self.move(-1),
            'RIGHT':	lambda:self.move(+1),
            'DOWN':    self.drop,
           	 'UP':	self.rotate_stone, 
             None:     lambda:None
        }

        self.init_display()
        self.init_game()
        self.gameover = False
        dont_burn_my_cpu = pygame.time.Clock()
        bot0 = bot(param,(self.cols,self.rows))
        cmp = 0
        done = False
        play = True

        while not done:

            if not self.gameover and not self.pause:
                self.screen.fill((0,0,0))
                pygame.draw.line(self.screen,
                    (255,255,255),(self.rlim+1, 0),(self.rlim+1, self.height-1))
                self.disp_msg("Next:", (self.rlim+cell_size,2))
                self.disp_msg("Lines: %d" % self.lines,(self.rlim+cell_size, cell_size*5))
                self.draw_matrix(self.bground_grid, (0,0))
                self.draw_matrix(self.grille.board, (0,0))
                self.draw_matrix(self.stone, (self.stone_x, self.stone_y))
                self.draw_matrix(self.next_stone, (self.cols+1,2))
                pygame.display.update()
                
                action = bot0.play(self.grille,self.stone,
                                   self.stone_x,self.stone_y,self.next_stone,play)
                play = False
                if key_actions[action]():
                    play = True
                if cmp%5 == 0:
                    if self.drop():
                        play = True
                cmp += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True 
                elif event.type == pygame.KEYDOWN:
                    if event.key == eval("pygame.K_SPACE"):
                        self.start_game()
                    if event.key == eval("pygame.K_p"):
                        self.fpause()
            dont_burn_my_cpu.tick(maxfps)
        
        pygame.display.quit()
        


class Tetris_evalu_z(TetrisApp_z,Tetris_evalu):
    pass
            
class Tetris_display_z(TetrisApp_z,Tetris_display):
    pass

class Tetris_display_z_ordre(TetrisApp_z_ordre,Tetris_display):
    pass

class Tetris_evalu_dans_lordre(TetrisApp_dans_lordre,Tetris_evalu):
    pass

class Tetris_display_dans_lordre(TetrisApp_dans_lordre,Tetris_display):
    pass
