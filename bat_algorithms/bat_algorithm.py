# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 00:38:46 2016

@author: cyber
"""

"""
Version originelle: 
BatAlgorithm version dans l'article
Mais BatAlgorithm2 semble plus logique
"""

from bat_algorithms.bat import Bat
from random import random, randint, uniform, gauss
from numpy import array, mean
from utilities import setAllArgs, modifyf
import math


class BatAlgorithm(object):

    min_frequency = 0
    max_frequency = 1
    
    # La précision du résultat depend largement de max_loudness
    max_loudness = 0.9
    gamma = 0.85
    rayon = 1

    best_proportion = 0.1
    
    storeallbestfitness = False
    constraint = False
    minimalize = False    


    def __init__(self, size, dimension, evaluator, **kwargs):
        
        self.population_size = size
        self.dimension = dimension
        setAllArgs(self, kwargs)
        self.epsilon = -1 if self.minimalize else 1
        if self.constraint:
            self.evaluator = modifyf(lambda x: self.epsilon*evaluator(x),self.rayon)
        else:
            self.evaluator = lambda x: self.epsilon*evaluator(x)
        self.init_bat()

    
    def init_bat(self):

        self.bats_list = [Bat(i, self.dimension, self.max_loudness, self.rayon)
                            for i in range(self.population_size)]
        self.bats_pulse_frequency = [0] * self.population_size
        self.update_fitness()
        if self.storeallbestfitness:
            self.bestfitnesses=[self.epsilon*self.bats_list[0].fitness]


    def init_optimize(self):
        for bat in self.bats_list:
            bat.loudness = self.max_loudness
            bat.pulse_rate = 0.85
            if mean(abs(bat.velocity)) < self.rayon/20:
                bat.velocity = array([v+gauss(0, self.rayon/2) for v in bat.velocity])



    def optimize(self, number_of_iterations=1):
        
        self.init_optimize()        
        
        for it in range(number_of_iterations):
            
            self.update_bats()
            self.average_loudness = mean([bat.loudness for bat in self.bats_list])

            for i,bat in enumerate(self.bats_list):

                if random() * self.max_loudness < bat.loudness:
                    
                    if random() > bat.pulse_rate:
                        choix = randint(0, int(self.population_size*self.best_proportion)-1)
                        target = self.bats_list[choix]
                        n_pos = self.localsearch(target)
                        if n_pos is not None:
                            bat.new_position = n_pos

                    newfitness = self.evaluator(bat.new_position)
                    if newfitness >= bat.fitness:
                        bat.position = bat.new_position
                        bat.fitness = newfitness
                        bat.update_loudness()
                        bat.pulse_rate = (1-math.exp(-self.gamma*it))*bat.pulse_rate0
            
            self.bats_list.sort(key = lambda bat: bat.fitness, reverse= True)
            
            if self.storeallbestfitness:
                self.bestfitnesses.append(self.epsilon*self.bats_list[0].fitness)
                
        return self.bats_list[0].position, self.epsilon*self.bats_list[0].fitness
        

    def localsearch(self,target):
        decalage = array([
            self.average_loudness*uniform(-0.5,0.5) for _ in range(self.dimension)])
        return target.position + decalage


    def update_bats(self):
        self.update_frequency()
        self.update_velocity()
        self.update_position()

    def update_fitness(self):
        for bat in self.bats_list:
            bat.getfitness(self.evaluator)
        self.bats_list.sort(key = lambda bat: bat.fitness, reverse= True)

    def update_frequency(self):
        for i in range(self.population_size):
            value = self.min_frequency + random()*(
                    self.max_frequency - self.min_frequency)
            self.bats_pulse_frequency[i] = value

    def update_velocity(self):
        for i,bat in enumerate(self.bats_list):
            new_velocity = bat.velocity + (
                bat.position - (self.bats_list[0].position)) * self.bats_pulse_frequency[i]
            bat.velocity = new_velocity

    def update_position(self):
        for bat in self.bats_list:
            bat.new_position = bat.position + bat.velocity


'''
Il semble beaucoup plus raisonable d'écrire update_velocity comme ça, 
effectivement ça marche mieux
'''

class BatAlgorithm2(BatAlgorithm):
    def update_velocity(self):
        for i,bat in enumerate(self.bats_list):
            new_velocity = bat.velocity - (
                bat.position - (self.bats_list[0].position)) * self.bats_pulse_frequency[i]
            bat.velocity = new_velocity
            

'''
Si on enlève directement update_bats (il ne reste que donc local_search)
Pour certain loudness les résultats restent indiférrent (0.1)
Pour d'autres ça change beaucoup (10,0.01)
Curieusement, même la première version marche mieux alors que 
les bats ne bougent dans la bonne direction
Raison possible: on a tout simplement un mouvement d'une échelle correcte
(quand loudness ~ 0.1, l'échelle de local_search fournit les bons résultats)
Et c'est encore mieux si on indique une direction qui est la bonne (version 2)
'''

class BatAlgorithm3(BatAlgorithm):
    def update_bats(self):
        pass
    
class BatAlgorithm4(BatAlgorithm2):
    def localsearch(self,target):
        pass

"""
Problème de l'algorithme, souvent difficile d'avoir une bonne précision de 
la solution, l'échelle de chaque pas est déterminée par le loudness
"""