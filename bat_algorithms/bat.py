# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 00:41:19 2016

@author: cyber
"""

from numpy import array
from random import random,uniform
import math

class Bat(object):
    
    def __init__(self, idd, dimension, max_loudness= 1, r= 1):
        self.id = idd
        self.rayon = r
        self.position = array([self.rayon*uniform(-1,1) for _ in range(dimension)])
        self.new_position = array([self.rayon*random() for _ in range(dimension)])
        self.velocity = array([self.rayon*random() for _ in range(dimension)])
        self.pulse_rate0 = 0.85
        self.pulse_rate = 0.85
        self.loudness = max_loudness
        self.times = 0
        
    def getfitness(self, evaluator):
        self.fitness = evaluator(self.position)
        return self.fitness

    def update_loudness(self):
        alpha = 0.95
        self.loudness *= alpha
        
    def update_pulse_rate(self):
        gamma = 0.85
        self.times += 1
        self.pulse_rate = (1-math.exp(-gamma*self.times))*self.pulse_rate0
        
    def update_pulse_rate2(self,itera,n):
        self.pulse_rate = self.pulse_rate0 * (itera/n)**3

    def __repr__(self):
        s = "Bat number: " + str(self.id) + (
            "\nBat current position: " + str(self.position) +            
            "\nBat current vilocity: " + str(self.velocity) +
            "\nBat current fitness: " + str(self.fitness))
        return s
        