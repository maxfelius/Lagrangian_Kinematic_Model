import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)

        #get sinkhole parameters
        sinkhole = sinkhole_functions()
        sinkhole_params = sinkhole_example()

        x_unravel = sinkhole_params.x_unravel
        y_unravel = sinkhole_params.y_unravel
        z_unravel = sinkhole_params.z_unravel

        self.t = np.arange(0,10,0.5)#np.linspace(0,10,30)#[x for x in range(10)]

        self.x_new, self.y_new, self.z_new = sinkhole.suffosion(sinkhole_params,x_unravel,y_unravel,z_unravel,self.t,'linear')
        self.plot_box = sinkhole.create_cavity_position(sinkhole_params.x0,sinkhole_params.y0,self.t,sinkhole_params,'suffosion','linear')

        self.z_color = -self.z_new/min(self.z_new[:,-1])

        self.createWidgets()

    def createWidgets(self):
        
        #figure settings
        fig=plt.figure(figsize=(8,8))
        ax = plt.axes(projection ="3d")
        canvas=FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().grid(row=0,column=1)

        #initial plot
        p = ax.scatter3D(self.x_new[:,0] , self.y_new[:,0] , self.z_new[:,0] , c=self.z_new[:,-1])
        ax.clear()
        self.plot(canvas,ax,0)
        fig.colorbar(p)

        #create slider
        self.Slider_1 = ttk.Scale(master=root,command=lambda val: self.plot(canvas,ax,val),from_=0,to=len(self.t)-1)
        self.Slider_1.grid(row=0,column=0)

    def plot(self,canvas,ax,val):
        ax.clear()
        val = int(np.round(float(val)))
        ax.scatter3D(self.x_new[:,val] , self.y_new[:,val] , self.z_new[:,val] , c=self.z_color[:,val])
        ax.plot3D(self.plot_box[:,val,0],self.plot_box[:,val,1],self.plot_box[:,val,2])

        #graph settings
        ax.set_xlabel('Distance East [m]')
        ax.set_xlabel('Distance North [m]')
        ax.set_xlabel('Distance Up [m]')
        ax.set_zlim(min(self.plot_box[:,-1,2]),0.1)
        ax.set_title(f'Time step: {val}')

        canvas.draw()

        #here set axes
    
class sinkhole_example:
    '''
    Parameters for an example sinkhole
    '''
    def __init__(self):
        #epicenter sinkhole
        self.x0 = 25
        self.y0 = 25
        # number of points
        self.nx = 50
        # range
        self.x_range = 15 # meters (around center)
        self.y_range = 15 # meters (around center)
        self.x = np.linspace(self.x0-self.x_range/2, self.x0+self.x_range/2, self.nx)
        self.y = np.linspace(self.y0-self.y_range/2,self.y0+self.y_range/2, self.nx)
        #Define Sinkhole parameters
        self.w = 5 #[m], width of the cavity
        self.H = 10 #[m], depth/height of the cavity
        self.draw = 35 * (np.pi/180) #[rad], angle of draw
        self.M = 4 #[m], cavity height
        self.R    = self.H*np.tan(self.draw)  # [m]
        self.wc   = self.H/np.cos(self.draw)  # [m]
        self.S    = (2*self.M*self.w)/(self.w + self.wc) #[m], max subsidence
        self.xv, self.yv = np.meshgrid(self.x, self.y)
        #start at ground level
        self.zv = np.zeros((self.nx,self.nx))
        #Create 1D vectors for plotting efficiency
        self.x_unravel = np.ravel(self.xv)
        self.y_unravel = np.ravel(self.yv)
        self.z_unravel = np.ravel(self.zv)

    def reset_sinkhole(self,H_in):
        self.H = H_in
        self.R = self.H*np.tan(self.draw)
        self.wc = self.H/np.cos(self.draw)
        self.S = (2*self.M*self.w)/(self.w + self.wc)
        
    def reset_subsidence(self,M_in,H_in):
        self.M = M_in
        self.H = H_in
        self.S = (2*self.M*self.w)/(self.w + self.wc)

class sinkhole_functions:
    '''
    Class that hold functions for generating sinkhole models
    '''
    def __init__(self):
        pass
    def zg(self,x,x0,y,y0,R,S):
        return -(S/(R*R))*np.exp(-np.pi * ((x-x0)**2 + (y-y0)**2)/R**2)

    def xhdisp(self,x,x0,y,y0,R,S,H):
        s = self.zg(x,x0,y,y0,R,S)
        return s * ((x-x0)/H)

    def yhdisp(self,x,x0,y,y0,R,S,H):
        s = self.zg(x,x0,y,y0,R,S)
        return s * ((y-y0)/H)
    
    def time_function(self,t,time_type,t0=0,a=1,b=1):
        '''
        Time function to manage the speed of the suffosion or stopig simulation
        
        type t: list/np array
        type time_type: string
        type t0: int
        type a: int
        type b: int
        
        rtype: np array
        '''
        def type_time_function(t,t0,a,b,mode):
            if t-t0 <= 0:
                return 0
            else:
                if mode == 'linear':
                    return a*(t-t0)
                elif mode == 'poly':
                    return a*(t-t0)**2 + b*(t-t0)
                elif mode == 'exp':
                    return a*np.exp((t-t0))
                elif mode == 'log':
                    return a*np.log(1+b*(t-t0))
                else:
                    print('No mode selected')
                    return 0

        return np.array([type_time_function(x,t0,a,b,time_type) for x in t])

    def suffosion(self,sinkhole,x_in,y_in,z_in,t,time_type):
        '''
        Suffosion sinkhole simulator
        
        Cavity increases in size going upwards
        
        Input:
        type sinkhole: sinkhole_function object
        type x,y,z: (nx1) array
        type t: (mx1) array 
        type: time_type: string
        
        Output:
        rtype x,y,z: (nxm) array
        '''            
        # Per time step, a new column of x,y,z should be added. 
        # New positional values for x,y,z are calculated by combining the influence function and the time function
        
        M = sinkhole.M
        w = sinkhole.w
        wc = sinkhole.wc
        R = sinkhole.R
        H_start = sinkhole.H
        H_end = 3
        
        a = 1
        b = 1
        
        t_out = self.time_function(t,time_type,t0=0,a=1,b=1)

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
            Mi = M+ti*(H_start-H_end)
            Ri = Hi*np.tan(np.deg2rad(35))
            
            Si = (2*Mi*w)/(w + wc) #[m], max subsidence

            # Vertical Displacement
            sz = self.zg(x_in,sinkhole.x0,y_in,sinkhole.y0,Ri,Si)

            # Horizontal Displacement x-direction
            sx = self.xhdisp(x_in,sinkhole.x0,y_in,sinkhole.y0,Ri,Si,Hi)

            # Horizontal Displacement y-direction
            sy = self.yhdisp(x_in,sinkhole.x0,y_in,sinkhole.y0,Ri,Si,Hi)
            
            x_out[:,idx+1] = x_out[:,idx] + sx 
            y_out[:,idx+1] = y_out[:,idx] + sy
            z_out[:,idx+1] = z_out[:,idx] + sz 
        
        return x_out, y_out, z_out
    
    def create_cavity_position(self,x0,y0,t,sinkhole,mechanism,time_type):
        '''
        '''
        if mechanism.lower() == 'suffosion':
            #middle point
            x_m = x0
            y_m = y0
            z_m = sinkhole.H
            w = sinkhole.w
            M = sinkhole.M

            H_start = sinkhole.H
            H_end = 3
            
            t_out = self.time_function(t,time_type,t0=0,a=1,b=1)
            
            #normalize output
            t_out = t_out/max(t_out)
            
            #pre-allocate space
            b1 = np.zeros((1+len(t_out),3))
            b2 = np.zeros((1+len(t_out),3))
            b3 = np.zeros((1+len(t_out),3))
            b4 = np.zeros((1+len(t_out),3))
            
            t1 = np.zeros((1+len(t_out),3))
            t2 = np.zeros((1+len(t_out),3))
            t3 = np.zeros((1+len(t_out),3))
            t4 = np.zeros((1+len(t_out),3))
            
            #bottom
            b1[0,:] = np.array([x0-0.5*w,y0-0.5*w,-H_start-0.5*M])
            b2[0,:] = np.array([x0+0.5*w,y0-0.5*w,-H_start-0.5*M])
            b3[0,:] = np.array([x0+0.5*w,y0+0.5*w,-H_start-0.5*M])
            b4[0,:] = np.array([x0-0.5*w,y0+0.5*w,-H_start-0.5*M])

            #top
            t1[0,:] = np.array([x0-0.5*w,y0-0.5*w,-H_start+0.5*M])
            t2[0,:] = np.array([x0+0.5*w,y0-0.5*w,-H_start+0.5*M])
            t3[0,:] = np.array([x0+0.5*w,y0+0.5*w,-H_start+0.5*M])
            t4[0,:] = np.array([x0-0.5*w,y0+0.5*w,-H_start+0.5*M])
            
            for idx,ti in enumerate(t_out):
                
                #Get new cavity parameters
                Hi = H_start-ti*(H_start-H_end)
                Mi = M+ti*(H_start-H_end)
                Ri = Hi*np.tan(np.deg2rad(35))
                
                #bottom
                b1[idx+1,:] = np.array([x0-0.5*w,y0-0.5*w,-H_start-0.5*M])
                b2[idx+1,:] = np.array([x0+0.5*w,y0-0.5*w,-H_start-0.5*M])
                b3[idx+1,:] = np.array([x0+0.5*w,y0+0.5*w,-H_start-0.5*M])
                b4[idx+1,:] = np.array([x0-0.5*w,y0+0.5*w,-H_start-0.5*M])

                #top
                t1[idx+1,:] = np.array([x0-0.5*w,y0-0.5*w,-Hi+0.5*M])
                t2[idx+1,:] = np.array([x0+0.5*w,y0-0.5*w,-Hi+0.5*M])
                t3[idx+1,:] = np.array([x0+0.5*w,y0+0.5*w,-Hi+0.5*M])
                t4[idx+1,:] = np.array([x0-0.5*w,y0+0.5*w,-Hi+0.5*M])

            plot_box = np.array([b1,b2,b3,b4,b1,t1,t2,t3,t4,t1,b1,b4,t4,t3,b3,b2,t2])

            #output shape: (17,len(t_out),3)
            return plot_box
        
        elif mechanism.lower() == 'stoping':
            print('Not built yet')
        
        else:
            print('No Mechanism Specified. Please specify a mechanism')


root=tk.Tk()
app=Application(master=root)
app.mainloop()
