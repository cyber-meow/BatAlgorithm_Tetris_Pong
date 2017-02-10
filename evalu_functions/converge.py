# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 01:31:59 2016

@author: cyber
"""

from matplotlib import pyplot as plt
import time
import numpy as np

def trace_converge(f, algo, **kwargs):
    
    d, N = kwargs.get('d',10), kwargs.get('N',50)
    n, r = kwargs.get('n',1000), kwargs.get('r',1)
    const = kwargs.get('const',True)
    log = kwargs.get('log',True)
    second = kwargs.get('second',False)
    title, courbe = kwargs.get('title', None), kwargs.get('courbe',None)

    plt.xlabel("iteration", fontsize=12)
    plt.ylabel("fitness value", fontsize=12)
    if title is not None:
        plt.suptitle(title, fontsize=14)    
    
    t0 = time.time()
    al = algo(N,d,f,rayon=r,minimalize=True,storeallbestfitness=True, constraint=const)
    al.optimize(n)
    gene = list(range(n+1))
    if log:
        plt.yscale('log')
    plt.plot(gene,al.bestfitnesses, label = courbe)
    if second:
        plt.plot(gene,al.currentbf)
    if courbe is not None:        
        plt.legend()
    plt.show()
    return time.time() - t0
    
def trace_converge_ga(f, algo, **kwargs):
    
    d, N = kwargs.get('d',10), kwargs.get('N',50)
    n, r = kwargs.get('n',1000), kwargs.get('r',1)
    const = kwargs.get('const',True)
    log = kwargs.get('log',True)
    courbe = kwargs.get('courbe',None)
    
    t0 = time.time()
    al = algo(lambda x: -f(x), numParameters= d, populationSize= N, rayon= r, constraint=const)
    bestfounds = []
    for _ in range(n+1):
        bestfounds.append(-al.learn(0)[1])
    gene = list(range(n+1))
    if log:
        plt.yscale('log')
    plt.plot(gene,bestfounds,label = courbe)
    if courbe is not None:
        plt.legend()
    plt.show()
    return time.time() - t0
    