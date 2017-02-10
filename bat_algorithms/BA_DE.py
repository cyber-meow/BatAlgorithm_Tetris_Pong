# -*- coding: utf-8 -*-
"""
Created on Sun May  1 00:55:58 2016

@author: cyber
"""

"""
Reference:

A Novel Bat Algorithm Based on Differential Operator and
Lévy Flights Trajectory
Simulated Annealing Optimization Bat Algorithm in Service
Migration Joining the Gauss Perturbation
"""

from bat_algorithms.bat_algorithm_v3 import BA_v3
import math
from numpy import zeros,array,mean,seterr,isinf
from numpy.random import choice as nu_ch
from random import randint, sample, random, uniform, gauss




class BA_DE(BA_v3):
    
    Cr = 0.9
    n = 2
    thetainit = 0.5
    winit = 0.9
    wfin = 0.2
    smin = 0
    smax = 5
    sigfin = 0
    siginit = 1
    max_loudness = 0.95
    
    
    def __init__(self, size, dimension, evaluator, **kwargs):
        super().__init__(size, dimension, evaluator, **kwargs)
        self.choisir_target = self.choisir_target_rand
    
    '''
    On stocke désormais la meilleure solution jamais rencontrée car on accepte
    maintenant éventuellement les solutions moins bonnes (voir change_bat)
    '''
    def init_bat(self):
        super().init_bat()
        if self.storeallbestfitness:
            self.currentbf=[self.epsilon*self.bats_list[0].fitness]
        self.best_evaluated = self.bats_list[0].position
        self.best_evaluation = self.bats_list[0].fitness

    
    # Changement principal: l'ajoute de l'opérateur de DE
    def optimize(self, number_of_iterations=1):
        
        self.init_optimize()
        self.n_it = number_of_iterations
        
        for it in range(self.n_it):
            
            self.init_iteration(it)
            self.update_bats()
            self.has_changed = False


            for i,bat in enumerate(self.bats_list):


                if self.update_condition(bat):

                    if random() > bat.pulse_rate:
                        target = self.choisir_target()
                        n_pos = self.localsearch(bat,target)                
                    else:
                        n_pos = self.DE(bat)
                    
                    self.change_bat(bat,n_pos)
            
            self.bats_list.sort(key = lambda bat: bat.fitness, reverse= True)

            if self.storeallbestfitness:
                self.bestfitnesses.append(self.epsilon*self.best_evaluation)
                self.currentbf.append(self.epsilon*self.bats_list[0].fitness)

            
        return self.best_evaluated, self.epsilon*self.best_evaluation, self.epsilon*self.bats_list[0].fitness
        
        
    # Inchangé
    def update_velocity(self):
    
        autre_position = self.choisir_target_gauss().position
        
        for i,bat in enumerate(self.bats_list):
            new_velocity = self.w* bat.velocity + (
                           self.theta1* (self.best_evaluated-bat.position) +
                           self.theta2* (autre_position-bat.position))*(
                           self.bats_pulse_frequency[i])
            bat.velocity = new_velocity
        

    # On remarque que theta1 varie de 0.5 à 0.8
    def init_iteration(self,it):
        
        self.theta1 = 0.8+ (self.thetainit-0.8)* (1-it/self.n_it)**self.n
        self.theta2 = 1- self.theta1
        self.w = self.wfin+ (self.winit-self.wfin)* (1-it/self.n_it)**self.n
        self.sigma = self.sigfin+ (
            self.siginit-self.sigfin)* (1-it/self.n_it)**self.n
        self.average_loudness = mean([bat.loudness for bat in self.bats_list])

    # NB: avec au moin une probabilité de 0.1 pour chercher les nouvelles solutions
    def update_condition(self,bat):
        return random() * self.max_loudness < max(0.1,bat.loudness)

    
    def choisir_target_rand(self):
        choix = randint(0, int(self.population_size*self.best_proportion)-1)
        target = self.bats_list[choix]
        return target

    def choisir_target_gauss(self):
        choix = int(min(abs(gauss(0,0.5)),0.9)*self.population_size)
        target = self.bats_list[choix]
        return target
    
    # Inchangé
    def localsearch(self,bat,target):
        return super().localsearch(target)


    # DE/rand/1/bin
    def DE(self,bat):
        
        a,b,c = sample(self.bats_list,3)
        pa, pb, pc = a.position, b.position, c.position
        jr = randint(0,self.dimension-1)
        n_pos = zeros(self.dimension)
                
        for j in range(self.dimension):
            if random() < self.Cr or j == jr:
                n_pos[j] = pc[j] + uniform(0.5,1)*(pa[j]-pb[j])
            else:
                n_pos[j] = bat.position[j]
        
        return n_pos


    '''
    Pour ne pas être piégé dans une extréma locale,
    on accepte aussi de temps en temps une solution qui n'est pas meilleure
    La mise à jour de pluse rate est aussi légèrement modifiée
    '''    
    def change_bat(self,bat,n_pos):
        
        newfit1 = self.evaluator(bat.new_position)
        newfit2 = -float("inf") if n_pos is None else self.evaluator(n_pos)
        tmp = list(zip([bat.new_position,n_pos],[newfit1,newfit2]))                    
        tmp.sort(key=lambda x: x[1], reverse = True)
                  
        if not isinf(tmp[0][1]) and (tmp[0][1] > bat.fitness 
            or random() * self.max_loudness < bat.loudness*0.5):
                        
            bat.position = tmp[0][0]
            bat.fitness = tmp[0][1]
            bat.update_loudness()
            bat.update_pulse_rate()
            self.has_changed = True

            if tmp[0][1] > self.best_evaluation:
                self.best_evaluation = tmp[0][1]
                self.best_evaluated = tmp[0][0]
        



def around(x):
    return x if x > 1e-299 else 0 

def Boltzmann(energies,T):
    
    energies -= energies[0]
    prob = array([around(math.exp(-E/T)) for E in energies])
    Z = sum(prob)
    ans = prob/Z
    return ans
    
    


'''
Pour la température
                  Ackley   Griewank   Rosenbrock   Michalewicz  Zakharov
fixé                 X        O           @            X            @
croissante           O        O           @            O            @
décroissante         O        X           @            O            @
'''

class BA_DE_T(BA_DE):
    
    
    def __init__(self, size, dimension, evaluator, **kwargs):
        super().__init__(size, dimension, evaluator, **kwargs)
        self.choisir_target = self.choisir_target_boltzmann
    
    
    def init_optimize(self):
        
        for bat in self.bats_list:
            bat.loudness = self.max_loudness
            bat.pulse_rate = 0.85
        
        self.T0 = abs(self.best_evaluation)
        self.has_changed = True
    
    
    def init_iteration(self,it):
        
        super().init_iteration(it)
        self.T = self.T0 * ((it+1)/self.n_it)**self.n
        #self.T = self.T0 * 1.2**it
        #self.T = self.T0 *0.9**it
        if self.has_changed:
            self.energies = array([-b.fitness+self.best_evaluation for b in self.bats_list])
            self.prob_vect = Boltzmann(self.energies,self.T)
        
        
    def choisir_target_boltzmann(self):
        pv = self.prob_vect if random()<self.theta1 else None
        target = nu_ch(self.bats_list, p=pv)
        return target
        

"""
De façon générale, cette version de l'algorithme batte toutes les versions précédentes

Dans BA_DE_T
Le choix de choisir_target_boltzmann à la place de choisir_target_gauss
peut être favorable (Ackley), mais en fait le plus souvent indéffirent
"""
                     