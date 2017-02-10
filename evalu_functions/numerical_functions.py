# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 04:46:45 2016

@author: cyber
"""

from numpy import mean, std
from math import *
import time


# U

def Sphere(arr):
    return sum([x**2 for x in arr])

def Zakharov(arr):
    square_sum = sum([x**2 for x in arr])
    ix_sum = sum([(i+1)*x for (i,x) in enumerate(arr)])
    return square_sum + (0.5*ix_sum)**2 + (0.5*ix_sum)**4

def Rosenbrock(arr):
    return sum([100*(arr[i+1]-arr[i]**2)**2 + (arr[i]-1)**2 for i in range(len(arr)-1)])


# M

def Ackley(arr):
    d = len(arr)
    square_sum = sum([x**2 for x in arr])
    cos_sum = sum([cos(2*pi*x) for x in arr])
    return -20*exp(-0.2*sqrt(square_sum/d))-exp(cos_sum/d)+20+exp(1)

def Griewank(arr):
    produit = 1
    for (i,x) in enumerate(arr):
        produit *= cos(x/sqrt(i+1))
    return sum([x**2 for x in arr])/4000 - produit + 1

def Rastrigin(arr):
    d = len(arr)
    return 10*d + sum([x**2-10*cos(2*pi*x) for x in arr])

def Schwefel(arr):
    d = len(arr)
    try:
        return 418.9829*d-sum([x*sin(sqrt(abs(x))) for x in arr])
    except ValueError:
        print(arr)
        
def Salomon(arr):
    square_sum = sum([x**2 for x in arr])
    return -cos(2*pi*sqrt(square_sum)) + 0.1*sqrt(square_sum) + 1

# Testé acec d= 2,5,10
def Michalewicz(arr):
    arr = [x+pi/2 for x in arr]
    penal = 0
    for x in arr:
        if x<0 or x>pi:
            penal += 20
    return -sum([sin(x)*(sin((i+1)*x**2/pi))**20 for (i,x) in enumerate(arr)]) + penal

# Testé avec d=2, +1 comparé avec le vesion normale
def Easom(arr):
    produit = 1
    for x in arr:
        produit *= cos(x)
    sq_sum = sum([(x-pi)**2 for x in arr])
    return -(-1)**len(arr)*produit*exp(-sq_sum)+1
    
# Testé avec d=2, +1 comparé avec le vesion normale
def Dropwave(arr):
    square_sum = sum([x**2 for x in arr])
    return -(1+cos(12*sqrt(square_sum)))/(square_sum/2+2)+1




'''
temps fixé
'''
def test(f, ba, **kwargs):
    d, N, t = kwargs.get('d',10), kwargs.get('N',50), kwargs.get('t',30)
    n, r = kwargs.get('n',1000), kwargs.get('r',1)
    const = kwargs.get('const',True)
    times = 0
    fits = []
    t0 = time.time()
    while time.time()-t0 < t:
        bat_a = ba(N,d,f, rayon= r, minimalize= True, constraint= const)
        fitness = bat_a.optimize(n)[1]
        fits.append(fitness)
        times += 1
    return min(fits),max(fits),mean(fits),std(fits),times



def test_ga(f, ga, **kwargs):
    d, N, t = kwargs.get('d',10), kwargs.get('N',50), kwargs.get('t',30)
    n, r = kwargs.get('n',1000), kwargs.get('r',1)
    const = kwargs.get('const',True)
    times = 0
    fits = []
    t0 = time.time()
    while time.time()-t0 < t:
        g = ga(lambda x: -f(x), numParameters= d, populationSize= N, rayon= r, constraint= const)
        fitness = -g.learn(n)[1]
        fits.append(fitness)
        times += 1
    return min(fits),max(fits),mean(fits),std(fits),times
    
    
'''
nombre de boucles exécutées fixé
'''
def test2(f, ba, **kwargs):
    d, N, times = kwargs.get('d',10), kwargs.get('N',50), kwargs.get('times',30)
    n, r = kwargs.get('n',1000), kwargs.get('r',1)
    const = kwargs.get('const',True)
    fits = []
    t0 = time.time()
    for _ in range(times):
        bat_a = ba(N,d,f, rayon= r, minimalize= True, constraint= const)
        fitness = bat_a.optimize(n)[1]
        fits.append(fitness)
    return min(fits),max(fits),mean(fits),std(fits),time.time()-t0



def test_ga2(f, ga, **kwargs):
    d, N, times = kwargs.get('d',10), kwargs.get('N',50), kwargs.get('times',30)
    n, r = kwargs.get('n',1000), kwargs.get('r',1)
    const = kwargs.get('const',True)
    fits = []
    t0 = time.time()
    for _ in range(times):
        g = ga(lambda x: -f(x), numParameters= d, populationSize= N, rayon= r, constraint= const)
        fitness = -g.learn(n)[1]
        fits.append(fitness)
    return min(fits),max(fits),mean(fits),std(fits),time.time()-t0



def t_value(x1,x2):
    m1, m2, sd1, sd2, n1, n2 = x1[2], x2[2], x1[3], x2[3], x1[4], x2[4]
    return (m1-m2)/sqrt(sd1**2/(n1-1)+sd2**2/(n2-1))