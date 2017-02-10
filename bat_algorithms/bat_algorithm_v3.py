# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 05:17:10 2016

@author: cyber
"""

"""
Reference:
A new modification approach on bat algorithm for solving optimization problems
"""

from bat_algorithms.bat_algorithm import BatAlgorithm
from random import random, randint, uniform, gauss
from numpy import array, mean
import math



class BA_v3(BatAlgorithm):
    
    n = 2
    thetainit = 0.6
    winit = 0.9
    wfin = 0.2
    smin = 0
    smax = 5
    sigfin = 0
    siginit = 1
    max_loudness = 0.95
    
   
    
    def optimize(self, number_of_iterations=1):
        
        self.init_optimize()
        
        for it in range(number_of_iterations):
            
            self.theta1 = 1+ (self.thetainit-1)* (1-it/number_of_iterations)**self.n
            self.theta2 = 1- self.theta1
            self.w = self.wfin+ (self.winit-self.wfin)* (1-it/number_of_iterations)**self.n
            self.sigma = self.sigfin+ (
                self.siginit-self.sigfin)* (1-it/number_of_iterations)**self.n
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


    
    # IS1, IS2
    def update_velocity(self):
        best_position = self.bats_list[0].position
        choix = int(min(abs(gauss(0,0.5)),0.9)*self.population_size)
        autre_position = self.bats_list[choix].position
        
        for i,bat in enumerate(self.bats_list):
            new_velocity = self.w* bat.velocity + (
                           self.theta1* (best_position-bat.position) +
                           self.theta2* (autre_position-bat.position))*(
                           self.bats_pulse_frequency[i])
            bat.velocity = new_velocity



    '''
    Il faut dire que dans la version précédente, en enlèvant localsearch,
    la fonction devient beaucoup moins efficace
    C'est moins vraie ici parce que update_velocity a été bcp améliorée
    Comme d'habitude, loudness joue un rôle important dans la capacité de localsearch
    '''

    # IS3
    
    def localsearch(self,target):

        best_fitness = self.bats_list[0].fitness
        worst_fitness = self.bats_list[-1].fitness
        if best_fitness == worst_fitness:
            return
        
        s = self.smin+ (self.smax-self.smin)*(
            (target.fitness-worst_fitness)/(best_fitness-worst_fitness))

        seeds = []
        for _ in range(int(s)):
            decalage = [self.average_loudness*gauss(0,self.sigma) for _ in range(self.dimension)]
            decalage = array(decalage)
            seed = target.position + decalage
            seeds.append(seed)
        if seeds != []:
            best_seed = max(seeds, key= lambda x: self.evaluator(x))
            return best_seed
            

        
class BA_explor(BA_v3):       
    def localsearch(self,target):
        pass
        
  

"""
Cette fois ci, les deux modifications se trouvent assez utiles
Et la solution est bcp améliorée
Mais pour la plupart des fonctions multimodales, 
comme Ackley([-32,32]), Griewank([-600,600]), Michalewicz([0,pi]),
ça reste peu satifisfaisant,
contrairement à ce qui est dit dans l'article
"""