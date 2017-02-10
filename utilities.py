# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:34:25 2016

@author: cyber
"""


def setAllArgs(obj, argdict):
    for n in list(argdict.keys()):
        if hasattr(obj, n):
            setattr(obj, n, argdict[n])
        else:
            print('Warning: parameter name', n, 'not found!')  


def modifyf(f,rayon):
    def res(arr):
        for x in arr:
            if abs(x)>rayon:
                return -float("inf")
        return f(arr)
    return res
    
    