'''
@author: Max Felius
'''

#imports
import random
import numpy as np

def get_random_subsamples(n_sub,x_unravel,y_unravel):
# n_sub = 30
    idx = random.sample(range(0,len(x_unravel)),int(n_sub))
    
    #subsampling the arrays
    x_sub = x_unravel[idx]
    y_sub = y_unravel[idx]
    
    return x_sub, y_sub
