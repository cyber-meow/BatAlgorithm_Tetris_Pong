# -*- coding: utf-8 -*-
"""
Created on Tue May 17 19:23:18 2016

@author: cyber
"""

from pybrain.tools.shortcuts import buildNetwork

def bot_simple(pon):
    
    posy = pon.paddle1_pos[1]
    vel = pon.ball_vel
    pos = pon.ball_pos
    pp,bvx,bvy,bpx,bpy = posy,vel[0]*pon.directionx,vel[1]*pon.directiony,pos[0],pos[1]
    
    if bpy > pp + pon.HALF_PAD_HEIGHT:
        return -1
    elif bpy < pp + pon.HALF_PAD_HEIGHT:
        return 1
    return 0
    

def bot_neuron(hide,params):

    assert len(params) == 7*hide+1

    n = buildNetwork(5,hide,1)
    n._setParameters(params)

    def player(pon):
        posy = pon.paddle1_pos[1]
        vel = pon.ball_vel
        pos = pon.ball_pos
        return n.activate([posy,vel[0]*pon.directionx,vel[1]*pon.directiony,pos[0],pos[1]])

    return player