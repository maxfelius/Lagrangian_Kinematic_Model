'''
@author: Max Felius

This script hosts the influence functions and the influence functions with noise 
'''
#imports
import numpy as np

def zg(R,r):
    return np.exp(-np.pi*(r**2/R**2))

def zg_nois(R,r,noise_tune=0.21):
    return np.exp(-np.pi*(r**2/R**2)) + (noise_tune*(1/(R*R))*np.random.uniform(0,1,size=len(r)))
