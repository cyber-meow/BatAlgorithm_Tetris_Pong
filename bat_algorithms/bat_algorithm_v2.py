# -*- coding: utf-8 -*-
"""
Created on Sun May 22 21:22:12 2016

@author: cyber
"""

"""
On considére ici la modification adoptée dans 
A Novel Adaptive Bat Algorithm to Control Explorations and Exploitations 
    for Continuous Optimization Problems
La partie 3.2
- Adaptive Mutation Step Size
- Rechenberg’s 1/5 mutation rule
"""

from bat_algorithms.bat_algorithm import BatAlgorithm2
from random import uniform, random, randint, gauss
from numpy import array, mean

class BA_v2(BatAlgorithm2):
    
    def init_optimize(self):
        super().init_optimize
        self.mutation = 0
        self.sigma = 1


    def optimize(self, number_of_iterations=1):
        
        self.init_optimize()        
        
        for it in range(number_of_iterations):
            
            self.aver_v = mean([bat.velocity for bat in self.bats_list])
            self.update_bats()
            self.average_loudness = mean([bat.loudness for bat in self.bats_list])

            for i,bat in enumerate(self.bats_list):
                
                if random() > bat.pulse_rate:
                    self.mutation += 1
                    choix = randint(0, int(self.population_size*self.best_proportion)-1)
                    target = self.bats_list[choix]
                    n_pos = self.localsearch(target)
                    if n_pos is not None:
                        bat.new_position = n_pos
                        
                if random() * self.max_loudness < bat.loudness:
                    newfitness = self.evaluator(bat.new_position)
                    if newfitness >= bat.fitness:
                        bat.position = bat.new_position
                        bat.fitness = newfitness
                        bat.update_loudness()        
            
            self.bats_list.sort(key = lambda bat: bat.fitness, reverse= True)
            
            if self.storeallbestfitness:
                self.bestfitnesses.append(self.epsilon*self.bats_list[0].fitness)            
            
            if self.mutation > (it+1)*self.population_size*0.2:
                for bat in self.bats_list:
                    bat.pulse_rate /= gauss(0.85,0.01)
                self.sigma -= 0.01
            
            elif self.mutation < (it+1)*self.population_size*0.2:
                for bat in self.bats_list:
                    bat.pulse_rate *= gauss(0.85,0.01)
                self.sigma += 0.01
                
        return self.bats_list[0].position, self.epsilon*self.bats_list[0].fitness
        
    '''
    def localsearch(self,target):
        decalage = array([
            self.average_loudness*gauss(0,self.sigma) for _ in range(self.dimension)])
        return target.position + decalage
       ''' 
        
    def update_velocity(self):
        for i,bat in enumerate(self.bats_list):
            new_velocity = uniform(0.1,1)*bat.velocity - (
                bat.position - (self.bats_list[0].position)) * self.bats_pulse_frequency[i]
            bat.velocity = new_velocity
            
            
"""
Contradictoirement, avec quelques expériences, on trouve que:
1. L'emploie de Rechenberg’s 1/5 mutation rule semble totalement indifférent 
    dans les résultats
2. Le nouveau local search détériore le performance
3. Par contre, l'idée d'ajouter le facteur uniform(0.1,1) avant bat.velocity
    dans update_velocity améliore beaucoup le performance,
    mais il faut pas non plus enlever complètement le terme bat.velocity
"""