# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 00:33:15 2016

@author: cyber
"""

"""
DE/rand/1/bin

Reference:
Improved Hybridized Bat Algorithm for Global Numerical Optimization
DE
"""

from random import random,sample,uniform,randint
from numpy import array,zeros
from utilities import setAllArgs, modifyf



class DE(object):
    
    # Differential weight
    F = 0.8
    # Crossover probability
    Cr = 0.9    
    rayon = 1
        
    minimalize = False    
    storeallgenerations = False
    storeallbestfitness = False
    constraint = False
    
    
    def __init__(self, size, dimension, evaluator, **kwargs):
        
        self.population_size = size
        self.dimension = dimension
        setAllArgs(self, kwargs)
        self.epsilon = -1 if self.minimalize else 1
        if self.constraint:
            self.evaluator = modifyf(lambda x: self.epsilon*evaluator(x),self.rayon)
        else:
            self.evaluator = lambda x: self.epsilon*evaluator(x)
        
        self.currentpop = [array([uniform(-1,1)*self.rayon 
            for _ in range(self.dimension)]) for _ in range(self.population_size)]
        self.fitnesses = [self.evaluator(x) for x in self.currentpop]
        
        if self.storeallgenerations:
            self.generations = [self.currentpop]
        if self.storeallbestfitness:
            self.bestfitnesses = [self.epsilon*max(self.fitnesses)]
        
                
    def optimize(self, number_of_iterations=1):
        
        for _ in range(number_of_iterations):
            
            self.init_iter()            
            
            for (i,xi) in enumerate(self.currentpop):

                a,b,c = sample(range(self.population_size),3)
                xa, xb, xc = self.currentpop[a], self.currentpop[b], self.currentpop[c]
                jr = randint(0,self.dimension-1)
                v = zeros(self.dimension)

                for j in range(self.dimension):
                    if random() < self.Cr or j == jr:
                        v[j] = xc[j] + uniform(0.5,1)*(xa[j]-xb[j])
                    else:
                        v[j] = xi[j]

                newfitness = self.evaluator(v)
                if newfitness > self.fitnesses[i]:
                    self.currentpop[i] = v
                    self.fitnesses[i] = newfitness
                
            if self.storeallgenerations:
                self.generations.append(self.currentpop)
            if self.storeallbestfitness:
                self.bestfitnesses.append(self.epsilon*max(self.fitnesses))
                
        best_indice = max(list(range(self.population_size)), key= lambda i:self.fitnesses[i])
        best_value = self.epsilon * self.fitnesses[best_indice]
        
        return self.currentpop[best_indice], best_value
        
        
    def init_iter(self):
        pass
    

# adpaté pour l'entrainement des bots
class DE_adapte(DE):
    
    def init_iter(self):
        self.fitnesses = [self.evaluator(x) for x in self.currentpop]
        
        
        
        
        
        
        