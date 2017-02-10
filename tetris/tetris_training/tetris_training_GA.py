# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 07:05:08 2016

@author: cyber
"""

from tetris.tetris_AI import *
from pybrain.optimization.populationbased.ga import GA,GA_new
from scipy import randn
from numpy import array

def evaluz(param):
    return Tetris_evalu_z().evalu(bot,param)[0]
    
def evaluz_v(cols,rows):
    def evaluz_s(param):
        return Tetris_evalu_z(cols,rows).evalu(bot,param)[0]
    return evaluz_s

def evaluz_simple_bot(cols,rows):
    def evaluz_s(param):
        return Tetris_evalu_z(cols,rows).evalu(bot_simple_scorer,param)[0]
    return evaluz_s

#w=GA(evaluz_v(10,10),z.currentpop[0],populationSize = 20,topProportion = 0.4, mutationProb = 0.2)

# first example, trained by evaluz_v 10*22
x_5 = [ 5.11945522, -8.11517994,  8.2630125 , -5.156103  ,  6.63298312,
        3.02755139, -6.64815699, -9.7539148 ,  2.14473348, -6.7011111 ]

# exemple avec la fonction evaluz_v pour une grille de taille 10*10
# problème: instable, un résultat qui est étrangement bon nous empêche d'évoluer    
x_11 =[ 4.57189583, -6.13417336, -1.18827035, -0.68341413, -3.33502137,
       -3.08996605, -6.06791127, -3.74761228, -9.81072795, -5.63638325]
       
x_20 =[ 4.53279808, -0.03244652, -0.97898235, -1.38107701, -4.87915211,
       -3.67842296, -6.03888138, -4.07315681, -8.55634865, -5.3660044 ]
       
x_20_2 =[ 5.0000591 , -3.03715001, -1.32919909, -1.13163989, -5.79923644,
         -4.31894638, -6.84322888, -4.78816293, -8.32534843, -4.17302502]
         
x_adjuste =array([ -3. , -10. , 30. , -20. , -3.78658488,
                  -12.8250096 , -11.19805964, -17.41286747, -12.11259768,  -7.])