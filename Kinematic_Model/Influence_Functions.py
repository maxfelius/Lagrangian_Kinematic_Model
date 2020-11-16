'''
@author: Max Felius

Different classes for different influence functions

Roadmap:
- Gaussian Influence Function (Finished)
- Bals Influence Function (finished)
- Beyer Influence Function (finished)
- Making 2D test scheme (unfinished)
'''

#import
import numpy as np
import matplotlib.pyplot as plt

class Gaussian:
    '''
    Gaussian (stochastic) influence function
    '''
    def __init__(self,x,x0,y,y0,R,H):
        '''
        Initiate variables
        '''
        self.x = x
        self.x0 = x0
        self.y = y
        self.y0 = y0
        self.R = R
        self.H = H
        
    def zg(self):
        return -(1/(self.R*self.R))*np.exp(-np.pi * ((self.x-self.x0)**2 + (self.y-self.y0)**2)/self.R**2)

    def xhdisp(self):
        s = self.zg()
        return s * ((self.x-self.x0)/self.H)

    def yhdisp(self):
        s = self.zg()
        return s * ((self.y-self.y0)/self.H)

class Bals:
    '''
    Bals Influence Function
    '''
    def __init__(self,x,x0,y,y0,R,H):
        '''
        Initiate variables
        '''
        self.x = x
        self.x0 = x0
        self.y = y
        self.y0 = y0
        self.R = R
        self.H = H
    
    def zg(self):
        r = np.sqrt((self.x-self.x0)**2 + (self.y-self.y0)**2)

        zone = np.arctan(r/self.H)

        return -1*(1/(1+r**2))*np.cos(zone)**2
        # return -np.cos(zone)**2

    def xhdisp(self):
        s = self.zg()
        return s * ((self.x-self.x0)/self.H)

    def yhdisp(self):
        s = self.zg()
        return s * ((self.y-self.y0)/self.H)

class Beyer:
    '''
    '''
    def __init__(self,x,x0,y,y0,R,H):
        '''
        Initiate variables
        '''
        self.x = x
        self.x0 = x0
        self.y = y
        self.y0 = y0
        self.R = R
        self.H = H
    
    def zg(self):
        r = np.sqrt((self.x-self.x0)**2 + (self.y-self.y0)**2)

        kz = -((3)/(np.pi*self.R**2))*(1-(r/self.R)**2)**2

        kz[r>self.R] = 0

        return kz

    def xhdisp(self):
        s = self.zg()
        return s * ((self.x-self.x0)/self.H)

    def yhdisp(self):
        s = self.zg()
        return s * ((self.y-self.y0)/self.H)

def _test():
    '''
    Few tests to test this script
    '''
    x = np.linspace(0,10,100)
    y = np.linspace(0,10,100)
    x0 = 4
    y0 = 4
    R = 3
    S = 2
    H = 10

    #influence functions
    kz_gaus = Gaussian(x,x0,y,y0,R,H)
    kz_bals = Bals(x,x0,y,y0,R,H)
    kz_beyer = Beyer(x,x0,y,y0,R,H)

    #Figure creation
    fig, ax = plt.subplots(nrows=3,ncols=3,figsize=(15,10))
    ax[0,0].plot(x,S*S*kz_gaus.zg())
    ax[0,1].plot(x,S*kz_gaus.xhdisp())
    ax[0,2].plot(y,S*kz_gaus.yhdisp())

    ax[1,0].plot(x,S*kz_bals.zg())
    ax[1,1].plot(x,S*kz_bals.xhdisp())
    ax[1,2].plot(y,S*kz_bals.yhdisp())

    ax[2,0].plot(x,S*kz_beyer.zg())
    ax[2,1].plot(x,S*kz_beyer.xhdisp())
    ax[2,2].plot(y,S*kz_beyer.yhdisp())

    plt.show()

def _test2():
    '''
    Second test.

    Test the 2d ability of these influence functions
    '''
    pass

if __name__ == '__main__':
    _test()