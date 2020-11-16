'''
@author: Max Felius

Time function

Roadmap:
- None

This script should work
'''
#imports
import numpy as np
import matplotlib.pyplot as plt

def type_time_function(t,t0,a,b,mode):
    if t-t0 <= 0:
        return 0
    else:
        if mode == 'linear':
            return a*(t-t0) + b
        elif mode == 'poly':
            return a*(t-t0)**2 + b*(t-t0)
        elif mode == 'exp':
            return a*np.exp(b*(t-t0))
        elif mode == 'log':
            return a*np.log(1+b*(t-t0))
        else:
            print('No mode selected')
            return 0

def time_function(t,time_type,t0=0,a=1,b=1):
    '''
    Time function to manage the speed of the suffosion or stopig simulation
    
    type t: list/np array
    type time_type: string
    type t0: int
    type a: int
    type b: int
    
    rtype: np array
    '''
    return np.array([type_time_function(x,t0,a,b,time_type) for x in t])

def _test():
    '''
    Few tests to test this script
    '''
    t = np.linspace(1,10,100)

    t0 = 5
    a = 2
    b = 3

    linear_time = time_function(t,'linear',t0,a,b)
    poly_time = time_function(t,'poly',t0,a,b)
    expo_time = time_function(t,'exp',t0,a,b)
    log_time = time_function(t,'log',t0,a,b)

    plt.figure()
    plt.plot(t,linear_time/max(linear_time))
    plt.plot(t,poly_time/max(poly_time))
    plt.plot(t,expo_time/max(expo_time))
    plt.plot(t,log_time/max(log_time))

    plt.show()

if __name__ == '__main__':
    _test()