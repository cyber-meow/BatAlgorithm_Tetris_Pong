# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:27:37 2016

@author: cyber
"""

from pybrain.optimization.populationbased.ga import GA,GA_new
from differential_evolution.DE_rand_1_bin import DE_adapte
from bat_algorithms import *
from tetris.tetris_AI import *
from numpy import mean
import time

# training z, bot_simple, 15 fois puis moyenner, revoie cmp
def training1(cols,rows):
    def evaluz_s(param):
        res = [Tetris_evalu_z(cols,rows).evalu(bot_simple_scorer,param)[0] for _ in range(15)]
        return mean(res)
    return evaluz_s

# training normal, bot_simple
def training1_n(cols,rows):
    def evalu_s(param):
        res = [Tetris_evalu(cols,rows).evalu(bot_simple_scorer,param)[0] for _ in range(15)]
        return mean(res)
    return evalu_s
    

# training z, bot
def training2(cols,rows):
    def evaluz_s(param):
        res = [Tetris_evalu_z(cols,rows).evalu(bot,param)[0] for _ in range(15)]
        return mean(res)
    return evaluz_s

# training normal, bot
def training2_n(cols,rows):
    def evalu_s(param):
        res = [Tetris_evalu(cols,rows).evalu(bot,param)[0] for _ in range(8)]
        return mean(res)
    return evalu_s


'''
Pour obtenir quelques résultats
'''

'''
GAs = GA_new(training1(10,10), numParameters= 6, populationSize= 20, 
             mutationProb=0.2, elitism= True, _eliteSize= 1)

for i in range(31):
    t0 = time.time()
    print(i)
    print(GAs.learn(0))
    i = max(range(20), key= lambda j:GAs.fitnesses[j])
    print((GAs.currentpop[i],GAs.fitnesses[i]))    
    print(time.time()-t0)
'''

'''
GAl = GA_new(training2(10,10), numParameters= 10, populationSize= 20,
            mutationProb=0.2, elitism= True, _eliteSize= 1)

for i in range(31):
    t0 = time.time()
    print(i)
    print(GAl.learn(0))
    i = max(range(20), key= lambda j:GAl.fitnesses[j])
    print((GAl.currentpop[i],GAl.fitnesses[i]))    
    print(time.time()-t0)
'''

'''
DEs = DE_adapte(20,10,training2(10,10))

for i in range(31):
    t0 = time.time()
    print(i)
    print(DEs.optimize(1))
    print(time.time()-t0)
'''
    
'''
DEl = DE_adapte(20,6,training1(10,10))

for i in range(31):
    t0 = time.time()
    print(i)
    print(DEl.optimize(1))
    print(time.time()-t0)
'''



'''
BA=BA_DE_T_v3(20,6,training1(10,10))
BA.optimize(30)
'''

# 273.466666667 [ 0.4763844  -0.62627876  0.2253577  -0.48459688 -0.35362737 -0.74897456]    
res1 = [ 0.4763844,  -0.62627876,  0.2253577,  -0.48459688, -0.35362737, -0.74897456]
res2 = [ 0.4637336,  -0.63847381, -0.1592599,   0.02037212, -0.19534719, -0.39338208]


ga_30z = [ 2.39291753, -0.40274433,  0.67072424,  0.75410654, -0.60055218,
          -0.63424512, -1.38370884, -2.94481695, -1.32049929, -1.88529419]
         
ba_30z = [-1.09635548, -0.55998682, -2.1724755 ,  0.91319898,  0.69219992,
           0.7883684 , -4.44930571, -2.54551623, -6.13402177, -0.99799277]

# 5177.875       
ba_30 = array([ 2.94838774,  0.76801092,  1.57338983, -8.38505527, -2.00257298,
                -1.3398024 , -1.35541477, -2.48791813, -0.10383824, -7.88605585])

ba_50 = [ 2.98308146,  0.09425874 , 1.62948612 ,-3.43650894, -0.6761944 , -1.31124708,
 -1.59465976, -1.15867959,  0.21721164, -2.13175211]
 
# 7154.75
b1 = [ 3.21394758, -0.0444906,   0.56833609, -4.66068163, -1.09439272, -1.45517348,
 -1.76064495, -1.07538817,  0.4566654,  -2.95902791]

# 6309.75
b2 = [ 3.61915568,  0.18671514 ,-1.98891176, -2.7823522 , -0.68276472, -1.65478349,
 -1.50630609 ,-1.72050836 , 0.25412111 ,-2.69515125]

# 7099.25 
b3 = [ 3.07959639,  0.176854,    1.60330948, -2.73171287, -0.76421597, -1.47024251,
 -1.49440979, -1.05189468,  0.14523966, -2.23133034]

#4747.5
b4 = [ 3.31433527,  0.08562031, -2.05162709 ,-3.28826507 ,-0.92470719 ,-1.58079878,
 -1.52789408, -1.39767174 , 0.27357165 ,-2.96608145]

# 6876.75
b5 = [ 3.25299482,  0.05961312,  0.94883318, -2.61583425, -0.73656341, -1.2681185,
 -1.67128628, -1.09792809,  0.17987898, -3.10567234]

#5784.625
b7 = [ 3.73309485,  -0.42246031, -0.44342626, -4.9549383 , -1.32421613,
       -1.3410186 , -2.00469422, -2.00761084, -0.02158181, -5.52861351]

# 4796.5  
b8 = [ 3.24653716,  0.25456556, -0.6816676 , -5.10434954, -1.4647866 ,
       -1.27801286, -1.62128642, -1.72695781,  0.09099751, -4.93358547]

# 7335.75
b9 = [ 3.75939374,  0.35630412, 15.31408412, -4.98850843, -1.502686,   
       -1.16647816, -1.72665223, -1.74285002, -0.11057638, -4.60854415]



# 10*12
# 10809.25
b6 = [  2.15038223,  -1.95920461,  7.16996471 ,  -1.28827932 , -1.49574597,
  -1.76609432  ,-1.256799,   -2.31959307 , -1.89839022, -11.81404516]

'''
Petit test
1000 65.5157470703125
4000 277.6678819656372
5000 343.7036590576172
6000 411.08251309394836
7000 475.72121000289917
8000 540.9159390926361
9000 604.9966039657593
10000 674.8205981254578
(479684, 10375, 700.0290400981903)
'''

'''
for i in range(4,15):
    BA.bats_list[i]=Bat(i,10,0.95)

BA.bats_list[4].position=ba_30
BA.bats_list[5].position=ba_50
BA.bats_list[6].position=ba_30
BA.bats_list[7].position=b1
BA.bats_list[8].position=b2
BA.bats_list[9].position=b3
BA.bats_list[10].position=b4
BA.bats_list[11].position=b3
BA.bats_list[12].position=b5
BA.bats_list[13].position=b6
BA.bats_list[14].position=b5
'''

'''
1000 22.316277027130127
2000 44.276533126831055
3000 66.16078400611877
4000 90.89919900894165
7000 172.64687514305115
8000 198.5853590965271
9000 220.50861310958862
10000 242.43686699867249
11000 264.47612714767456
12000 286.3523790836334
13000 308.07262110710144
14000 329.96987295150757
15000 351.96513199806213
16000 374.49541997909546
17000 400.2508931159973
18000 425.3213269710541
19000 447.37758898735046
20000 469.570858001709
21000 491.50311303138733
23000 535.4986290931702
24000 557.6098940372467
25000 579.3941400051117
26000 601.4073989391327
27000 623.4536600112915
28000 645.5129210948944
30000 689.1564180850983
(1400042, 30496, 700.0030379295349)
'''