'''
@author: Max Felius

Sinkhole object 
Script creating a sinkhole class for easy parameter overview

The sinkhole object also holds the method of the suffosion of a cavity or the stoping of the cavity

ROADMAP/TODO:
- implement a test (DONE)
- implement stoping method
- improve and correct the suffosion method (DONE)
'''

#imports
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import mpld3

#imports package
import Kinematic_Model.Time_Vector as tv
import Kinematic_Model.Influence_Functions as infl

class sinkhole_function:
    '''
    Sinkhole object holding sinkhole parameters and methods that apply.
    '''
    def __init__(self,x0,y0,H,H_min,M,w,draw,x_range,y_range):
        self.x0 = x0
        self.y0 = y0
        self.H = H
        self.H_min = H_min
        self.M = M
        self.w = w
        self.draw = np.deg2rad(draw)
        self.R = self.H*np.tan(self.draw)
        self.wc = self.H/np.cos(self.draw)
        self.S = (2*self.M*self.w)/(self.w + self.wc)

        self.x_range = x_range
        self.y_range = y_range

        #create a grid
        xv, yv = np.meshgrid(self.x_range,self.y_range)

        #unravel the grid
        self.x_grid = np.ravel(xv)
        self.y_grid = np.ravel(yv)
        self.z_grid = np.zeros((self.x_grid.shape))

        #time variables
        self.a = 1
        self.b = 1

        #influence function
        self.kz_type = 'Gaussian' # ['Gaussian','Bals','Beyer']

    def reset_sinkhole(self,H_in):
        self.H = H_in
        self.R = self.H*np.tan(self.draw)
        self.wc = self.H/np.cos(self.draw)
        self.S = (2*self.M*self.w)/(self.w + self.wc)
        
    def reset_subsidence(self,M_in,H_in):
        self.M = M_in
        self.H = H_in
        self.S = (2*self.M*self.w)/(self.w + self.wc)

    def suffosion(self,t,time_type):
        '''
        Suffosion sinkhole simulator
        
        Cavity increases in size going upwards
        
        Input:
        type x,y,z: (nx1) array
        type t: (mx1) array 
        type time_type: string
        
        Output:
        rtype x,y,z: (nxm) array
        '''            
        # Per time step, a new column of x,y,z should be added. 
        # New positional values for x,y,z are calculated by combining the influence function and the time function
        H_start = self.H
        H_end = self.H_min
        
        #get variables
        x_in = self.x_grid
        y_in = self.y_grid
        z_in = self.z_grid

        t_out = tv.time_function(t,time_type,0,self.a,self.b)

        #normalize output
        t_out = t_out/max(t_out)
        
        #predefine output matrix
        x_out = np.zeros((len(x_in),1+len(t_out)))
        y_out = np.zeros((len(x_in),1+len(t_out)))
        z_out = np.zeros((len(x_in),1+len(t_out)))
        
        #copy input
        x_out[:,0] = x_in
        y_out[:,0] = y_in
        z_out[:,0] = z_in

        for idx,ti in enumerate(t_out):
            Hi = H_start-ti*(H_start-H_end)
            Mi = self.M+ti*(H_start-H_end)
            Ri = Hi*np.tan(self.draw)
            wci = Hi/np.cos(self.draw)

            Si = (2*Mi*self.w)/(self.w + wci) #[m], max subsidence

            #create sinkhole influence object
            if self.kz_type.lower() == 'gaussian':
                kz = infl.Gaussian(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            elif self.kz_type.lower() == 'bals':
                kz = infl.Bals(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            elif self.kz_type.lower() == 'beyer':
                kz = infl.Beyer(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            else:
                print('No influence function selected. Going with the Gaussian Influence Function.')
                kz = infl.Gaussian(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)

            # Vertical Displacement
            sz = Si*kz.zg()

            # Horizontal Displacement x-direction
            sx = Si*kz.xhdisp()

            # Horizontal Displacement y-direction
            sy = Si*kz.yhdisp()
            
            x_out[:,idx+1] = x_out[:,idx] + sx 
            y_out[:,idx+1] = y_out[:,idx] + sy
            z_out[:,idx+1] = z_out[:,idx] + sz 
        
        return x_out, y_out, z_out

    def stoping(self,t,time_type):
        '''
        Method that simulates the stoping of a cavity
        
        Output:
        rtype x,y,z: (nxm) array
        '''
        
        H_start = self.H
        H_end = self.H_min

        #get variables
        x_in = self.x_grid
        y_in = self.y_grid
        z_in = self.z_grid

        #get time vector
        t_out = tv.time_function(t,time_type,0,self.a,self.b)

        #normailize output
        t_out = t_out/max(t_out)

        #predefine output matrix
        x_out = np.zeros((len(x_in),1+len(t_out)))
        y_out = np.zeros((len(x_in),1+len(t_out)))
        z_out = np.zeros((len(x_in),1+len(t_out)))

        #copy input
        x_out[:,0] = x_in
        y_out[:,0] = y_in
        z_out[:,0] = z_in

        for idx, ti in enumerate(t_out):
            Hi = H_start-ti*(H_start-H_end)
            Mi = self.M
            Ri = Hi*np.tan(self.draw)
            wci = Hi/np.cos(self.draw)

            Si = (2*Mi*self.w)/(self.w + wci) #[m]

            #create sinkhole influence object
            if self.kz_type.lower() == 'gaussian':
                kz = infl.Gaussian(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            elif self.kz_type.lower() == 'bals':
                kz = infl.Bals(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            elif self.kz_type.lower() == 'beyer':
                kz = infl.Beyer(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            else:
                print('No influence function selected. Going with the Gaussian Influence Function.')
                kz = infl.Gaussian(x_out[:,idx],self.x0,y_out[:,idx],self.y0,Ri,Hi)
            
            # Vertical Displacement
            sz = Si*kz.zg()

            # Horizontal Displacement x-direction
            sx = Si*kz.xhdisp()

            # Horizontal Displacement y-direction
            sy = Si*kz.yhdisp()
            
            x_out[:,idx+1] = x_out[:,idx] + sx 
            y_out[:,idx+1] = y_out[:,idx] + sy
            z_out[:,idx+1] = z_out[:,idx] + sz 
        
        return x_out, y_out, z_out


def _test():
    '''
    Few tests to test this script
    '''

    x0 = 25
    y0 = 25
    H = 10
    H_min = 3
    M = 2
    w = 10
    draw = 35
    nx = 30
    x_range = np.linspace(15,35,nx)
    y_range = np.linspace(15,35,nx)

    #time
    t = np.arange(0,10,1)
    time_type = 'poly'

    obj = sinkhole_function(x0,y0,H,H_min,M,w,draw,x_range,y_range)

    x_out, y_out, z_out = obj.suffosion(t,time_type)

    # for i in range(len(t)):
    i = 5
    fig, ax = plt.subplots(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    p = ax.scatter3D(x_out[:,i],y_out[:,i],z_out[:,i],c=z_out[:,i])
    ax.set_title(f'Step {i}')
    fig.colorbar(p)

    plt.show()

def _test2():
    '''
    second round of tests. This function will test the stoping method
    '''
    x0 = 25
    y0 = 25
    H = 10
    H_min = 3
    M = 2
    w = 10
    draw = 35
    nx = 30
    x_range = np.linspace(15,35,nx)
    y_range = np.linspace(15,35,nx)

    #time
    t = np.arange(0,10,1)
    time_type = 'poly'

    obj = sinkhole_function(x0,y0,H,H_min,M,w,draw,x_range,y_range)

    x_out, y_out, z_out = obj.stoping(t,time_type)

    # for i in range(len(t)):
    i = 5
    fig, ax = plt.subplots(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    p = ax.scatter3D(x_out[:,i],y_out[:,i],z_out[:,i],c=z_out[:,i])
    ax.set_title(f'Step {i}. Stoping method test')
    fig.colorbar(p)

    plt.show()

if __name__ == '__main__':
    _test2()
