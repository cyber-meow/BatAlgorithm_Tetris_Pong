# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 18:46:45 2016

@author: cyber
"""

"""
Il y a trois modifications importantes
1. Cherche une nouvelle solution tant que random > max(0.1,self.loudness)
   (pour continuer à chercher des nouvelles solutions,
    mais ensuite greedy marche encore mieux)
2. L'emploie de mutation (c'est nécessaire, sinon le 1 ne sert pas forcément)
3. La nouvelle update_velocite s'inspirant de DE

NB: le 1 est maintenant aussi codé dans BA_DE

Les deux premières nous permettent de trouver la minima globale à une longue échelle
(environ 1250 générations à la place de 200 générations)
Surtout utiles pour Michalewicz, Rastrigin, Rosenbrock
Il ne nous reste que Griewank 
"""

from bat_algorithms.BA_DE import BA_DE, BA_DE_T, Boltzmann
import math
import time
from numpy import zeros,array,array_equal,isinf
from numpy.random import choice as nu_ch
from random import randint, sample, random, uniform, gauss, choice
from copy import copy


class BA_DE_T_v2(BA_DE_T):
    
    Cr = 0.9
    n = 2
    thetainit = 0.5
    max_loudness = 0.95
    c = 340

    
    def __init__(self, size, dimension, evaluator, **kwargs):
        super().__init__(size, dimension, evaluator, **kwargs)
        self.choisir_target = self.choisir_target_boltzmann


    '''
    Ca a effectivement un effet positif dans la plupart de cas
    (et pas négligeable)
    '''
    def update_velocity(self):
        
        for i,bat in enumerate(self.bats_list):
            
            if random() < self.theta1:
                bonne_position = self.best_evaluated
            else:
                bonne_position = self.choisir_target_gauss().position

            autre_position = self.choisir_target_gauss().position
            
            add_velocity = zeros(self.dimension)
            for j in range(self.dimension):
                if random()<self.theta1:
                    add_velocity[j] = bonne_position[j] - bat.position[j]
                else:
                    add_velocity[j] = autre_position[j] - bat.position[j]
            
            bat.velocity = self.w* bat.velocity + add_velocity*self.bats_pulse_frequency[i]

    '''
    Greedy converge plus rapidement (générations)
    Mais ça prend 4 fois plus de temps
    (Problème: pourqoui ne pas greedy depuis le début, 
     quel est le rôle de cette comparaison dans l'algorithme originel, 
     vois pas trop...)
    '''
    def update_condition(self,bat):
        return random() * self.max_loudness < max(0.1,bat.loudness)
        
        
    '''
    Le terme uniform(0.5,1)*(self.best_evaluated[j]-pc[j]) 
    augmente le vitess de convergence (utilisons simplement converge_trace pour voir)
    Et il ne se révele pas de conduire à une convergence prématurée (effet négligeable)
    '''
    def DE(self,bat):
        
        a,b,c = sample(self.bats_list,3)
        pa, pb, pc = a.position, b.position, c.position
        jr = randint(0,self.dimension-1)
        n_pos = zeros(self.dimension)
                
        for j in range(self.dimension):
            if random() < self.Cr or j == jr:
                n_pos[j] = pc[j] + uniform(0.5,1)*(pa[j]-pb[j]) +( 
                    uniform(0.5,1)*(self.best_evaluated[j]-pc[j]))
            else:
                n_pos[j] = bat.position[j]

        return n_pos
    
    
    # On introduit la mutation
    def change_bat(self,bat,n_pos):
        
        m = self.mutate(bat)
        newfit1 = self.evaluator(bat.new_position)
        newfit2 = -float("inf") if n_pos is None else self.evaluator(n_pos)
        newfit3 = -float("inf")
        newfit3 = self.evaluator(m)
        tmp = list(zip([bat.new_position,n_pos,m,bat.position],[newfit1,newfit2,newfit3,bat.fitness]))
        tmp.sort(key=lambda x: x[1], reverse = True)
        
        
        if not isinf(tmp[0][1]) and (tmp[0][1] > bat.fitness
            or random() < self.theta1/2):

            bat.position = tmp[0][0]
            bat.fitness = tmp[0][1]
            bat.update_loudness()
            bat.update_pulse_rate()
            self.has_changed = True

            if tmp[0][1] > self.best_evaluation:
                self.best_evaluation = tmp[0][1]
                self.best_evaluated = tmp[0][0]
    
    def mutate(self,bat):
        v = copy(bat.position)
        for i in range(self.dimension):
            if random() < 0.2:
                v[i] += gauss(0,0.5)
        return v
            
            

class BA_DE_T_greedy(BA_DE_T_v2):

    def update_condition(self,bat):
        return 1
        


'''
Voici la version finale, adapté pour l'entrainement des bots
Comme le fitness d'un individu peut varie beaucoup et depend fortement
de la chance, les fitness sont reévaluer à chaque fois
Ainsi on ne peut que prendre la meilleure solution à chaque instant
pour bien guider afin d'éviter d'être égaré par un candidat mal évalué
On imprime à chaque itération quelques informations nécessaire pour l'expérience
'''
class BA_DE_T_v3(BA_DE_T_v2):
    
    def __init__(self, size, dimension, evaluator, **kwargs):
        super().__init__(size, dimension, evaluator, **kwargs)
        self.t0 = time.time()
    
    def update_bats(self):
        self.update_frequency()
        self.update_velocity()
        self.update_position()    
        self.update_fitness()
    
    def init_iteration(self,it):
        super().init_iteration(it)
        print(it)
        print(time.time()-self.t0)
        print(self.best_evaluation,self.best_evaluated)
        self.t0 = time.time()
        self.best_evaluated = self.bats_list[0].position
        self.best_evaluation = self.bats_list[0].fitness