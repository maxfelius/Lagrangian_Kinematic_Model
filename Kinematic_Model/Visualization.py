'''
@author: Max Felius
'''

#imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import mpld3
import sys

#personal imports
import Sinkhole_Object as SO

class visualization:
    '''
    '''
    def __init__(self,x0,y0,H,H_min,M,w,draw,x_range,y_range,t,time_type):
        '''
        '''
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

        #time
        self.t = t
        self.time_type = time_type

        #sinkhole type
        self.mechanism = 'suffosion'

        #creating the sinkhole object
        self.obj = SO.sinkhole_function(self.x0,self.y0,self.H,self.H_min,self.M,self.w,np.rad2deg(self.draw),self.x_range,self.y_range)

    def interactive_figure(self):
        '''
        source: https://matplotlib.org/3.1.1/gallery/widgets/slider_demo.html
        '''
        if self.mechanism.lower() == 'suffosion':
            x_new, y_new, z_new = self.obj.suffosion(self.t,self.time_type)
        elif self.mechanism.lower() == 'stoping':
            x_new, y_new, z_new = self.obj.stoping(self.t,self.time_type)

        plot_box = self.create_cavity_position()

        zmax = min(plot_box[:,0,2])

        fig, ax = plt.subplots(figsize = (10, 7))
        plt.subplots_adjust(bottom=0.25)
        ax = plt.axes(projection ="3d")
        ax.set_xlabel('Distance East [m]')
        ax.set_ylabel('Distance North [m]')
        ax.set_zlabel('Distance Up [m]')
        ax.set_zlim(min(plot_box[:,0,2]),0.1)
        ax.set_title(f'Time step: {0}. Mechanism: {self.mechanism}')

        # Creating initial plot
        number = 0
        p = ax.scatter3D(x_new[:,number] , y_new[:,number] , z_new[:,number] , c=z_new[:,-1])
        ax.plot3D(plot_box[:,number,0],plot_box[:,number,1],plot_box[:,number,2])
        fig.colorbar(p)

        ax.margins(x=0)

        axcolor = 'lightgoldenrodyellow'
        axtime = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

        stime = Slider(axtime, 'Time', 0, len(self.t)-1, valinit=0, valstep=1)

        def update(val):
            ax.clear()
            num = int(np.round(val))

            #create new plot
            ax.scatter3D(x_new[:,num] , y_new[:,num] , z_new[:,num] , c=z_new[:,-1])
            ax.plot3D(plot_box[:,num,0],plot_box[:,num,1],plot_box[:,num,2])
            ax.set_xlabel('Distance East [m]')
            ax.set_ylabel('Distance North [m]')
            ax.set_zlabel('Distance Up [m]')
            ax.set_zlim(min(plot_box[:,0,2]),0.1)
            ax.set_title(f'Time step: {num}. Mechanism: {self.mechanism}')
            fig.canvas.draw_idle()

        stime.on_changed(update)

        plt.show()

    def interactive_figure_los(self,theta,alpha):
        '''
        Input:
        theta: float #incidence angle in radians
        alpha: float #Heading angle in radians
        '''

        #Projection vector for the line of sight
        p = np.array([-np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha),np.cos(theta)])

        if self.mechanism.lower() == 'suffosion':
            x_new, y_new, z_new = self.obj.suffosion(self.t,self.time_type)
        elif self.mechanism.lower() == 'stoping':
            x_new, y_new, z_new = self.obj.stoping(self.t,self.time_type)
        
        plot_box = self.create_cavity_position()

        #convert output xyz to los displacement
        #it is los w.r.t. the first epoch
        x_disp = x_new - x_new[:,0].reshape((x_new.shape[0],1))
        y_disp = y_new - y_new[:,0].reshape((y_new.shape[0],1))
        z_disp = z_new - z_new[:,0].reshape((z_new.shape[0],1))

        #pre-allocate space
        los = np.zeros(x_new.shape)
        for i in range(len(self.t)):
            los[:,i] = p @ np.array([x_disp[:,i],y_disp[:,i],z_disp[:,i]])

        zmax = min(plot_box[:,0,2])

        fig, ax = plt.subplots(figsize = (10, 7))
        plt.subplots_adjust(bottom=0.25)
        ax = plt.axes(projection ="3d")
        ax.set_xlabel('Distance East [m]')
        ax.set_ylabel('Distance North [m]')
        ax.set_zlabel('Distance Up [m]')
        ax.set_zlim(min(plot_box[:,0,2]),0.1)
        ax.set_title('Time step: 0. Mechanism: {}. Line-Of-Sight. theta: {:.2f} rad. alpha: {:.2f} rad'.format(self.mechanism,theta,alpha))

        # Creating initial plot
        number = 0

        p = ax.scatter3D(x_new[:,number] , y_new[:,number] , los[:,number] , c=los[:,-2])
        ax.plot3D(plot_box[:,number,0],plot_box[:,number,1],plot_box[:,number,2])
        cbar = fig.colorbar(p)
        cbar.set_label('Line of Sight Displacement [m]', rotation=270)
        ax.margins(x=0)

        axcolor = 'lightgoldenrodyellow'
        axtime = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

        stime = Slider(axtime, 'Time', 0, len(self.t)-1, valinit=0, valstep=1)

        def update(val):
            ax.clear()
            num = int(np.round(val))

            #create new plot
            ax.scatter3D(x_new[:,0] , y_new[:,0] , los[:,num] , c=los[:,-2])
            ax.plot3D(plot_box[:,num,0],plot_box[:,num,1],plot_box[:,num,2])
            ax.set_xlabel('Distance East [m]')
            ax.set_ylabel('Distance North [m]')
            ax.set_zlabel('Distance Up [m]')
            ax.set_zlim(min(plot_box[:,0,2]),0.1)
            ax.set_title('Time step: {}. Mechanism: {}. Line-Of-Sight. theta: {:.2f} rad. alpha: {:.2f} rad'.format(num,self.mechanism,theta,alpha))
            # ax.set_title(f'Time step: {num}. Mechanism: {self.mechanism}. Line-Of-Sight. theta: {theta}. alpha: {alpha}')
            # ax.set_title(f'Time step: {num}. Mechanism: {self.mechanism}')
            fig.canvas.draw_idle()


        stime.on_changed(update)

        plt.show() 

    def cross_section_selector(self):
        '''
        Method for making a cross section of the sinkhole
        '''
        if self.mechanism.lower() == 'suffosion':
            x_new, y_new, z_new = self.obj.suffosion(self.t,self.time_type)
        elif self.mechanism.lower() == 'stoping':
            x_new, y_new, z_new = self.obj.stoping(self.t,self.time_type)

        fig, ax = plt.subplots(figsize = (10, 7))
        plt.subplots_adjust(bottom=0.25)
        ax.set_xlabel('Distance East [m]')
        ax.set_ylabel('Distance North [m]')
        ax.set_title(f'Time step: {0}. Mechanism: {self.mechanism}. Select a Time Step to start the selection')

        # Creating initial plot
        number = 0
        p = ax.scatter(x_new[:,number] , y_new[:,number],c=z_new[:,-1])
        fig.colorbar(p)

        ax.margins(x=0)

        axcolor = 'lightgoldenrodyellow'
        axtime = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

        stime = Slider(axtime, 'Time', 0, len(self.t)-1, valinit=0, valstep=1)

        def update(val):
            ax.clear()
            num = int(np.round(val))

            #create new plot
            ax.scatter(x_new[:,num] , y_new[:,num], c=z_new[:,-1])
            ax.set_xlabel('Distance East [m]')
            ax.set_ylabel('Distance North [m]')
            ax.set_title(f'Time step: {num}. Mechanism: {self.mechanism}')
            points = plt.ginput(n=2,timeout=0,show_clicks=True,mouse_stop=2)
            fig.canvas.draw_idle()

            x = [] 
            y = []
            for pt in points: 
                x.append(pt[0])
                y.append(pt[1])

            # plot your selection
            self.plot_cross_section(x,y,num,x_new[:,num],y_new[:,num],z_new[:,num])

        stime.on_changed(update)

        plt.show()

    def plot_cross_section(self,x,y,num,x_new,y_new,z_new):
        '''
        Method for plotting the cross section results

        Input:
        :type x: list[float]
        :type y: list[float]
        :type num: int
        :type x_new: list[float]
        :type y_new: list[float]
        :type z_new: list[float]
        '''
        buffer = 2 #[m]

        #extract the points
        a = np.array([x[0],y[0]])
        b = np.array([x[1],y[1]])
        p = np.array([x_new,y_new])
        Np = p[0].shape[0]
        
        ab = b - a
        abdist2 = np.dot(ab,ab)
        
        assert abdist2 != 0, 'The two points specifying the line are the same.'

        ap = np.array([p[0]-a[0],p[1]-a[1]])
        t = (ab @ ap)/abdist2
        p2 = (np.tile(a,[Np,1]) + (t.reshape((len(t),1)) @ ab.reshape((2,1)).T)).T
        dist = np.sqrt(abs(p[0]-p2[0])**2 + abs(p[1]-p2[1])**2)
        
        index1 = np.where(t < 0)
        index2 = np.where(t > 1)
        index3 = np.where(dist > buffer/2)
        
        index = np.concatenate((index1[0],index2[0],index3[0]))
        
        x_subset = np.delete(x_new,index)
        y_subset = np.delete(y_new,index)
        z_subset = np.delete(z_new,index)
        t = np.delete(t,index)
        xNew = t*np.sqrt(abdist2)  

        #plot the points
        fig, ax = plt.subplots(figsize = (10,7))
        ax = plt.axes(projection ="3d")
        ax.set_xlabel('Distance East [m]')
        ax.set_ylabel('Distance North [m]')
        ax.set_zlabel('Distance Up [m]')
        ax.set_title('Time step {}. Coordinates ({:.2f},{:.2f}) and ({:.2f},{:.2f})'.format(num,x[0],y[0],x[1],y[1]))

        p = ax.scatter3D(x_subset , y_subset ,z_subset , c=z_subset)
        fig.colorbar(p)
        plt.show()

    def stoping_cavity(self,t_out,x0,y0,w,M,H_start,H_end,draw):
        '''
        Method for computing the box of the cavity
        '''
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
            
            #bottom
            b1[idx+1,:] = np.array([x0-0.5*w,y0-0.5*w,-Hi-0.5*M])
            b2[idx+1,:] = np.array([x0+0.5*w,y0-0.5*w,-Hi-0.5*M])
            b3[idx+1,:] = np.array([x0+0.5*w,y0+0.5*w,-Hi-0.5*M])
            b4[idx+1,:] = np.array([x0-0.5*w,y0+0.5*w,-Hi-0.5*M])

            #top
            t1[idx+1,:] = np.array([x0-0.5*w,y0-0.5*w,-Hi+0.5*M])
            t2[idx+1,:] = np.array([x0+0.5*w,y0-0.5*w,-Hi+0.5*M])
            t3[idx+1,:] = np.array([x0+0.5*w,y0+0.5*w,-Hi+0.5*M])
            t4[idx+1,:] = np.array([x0-0.5*w,y0+0.5*w,-Hi+0.5*M])

        plot_box = np.array([b1,b2,b3,b4,b1,t1,t2,t3,t4,t1,b1,b4,t4,t3,b3,b2,t2])

        return plot_box   

    def suffosion_cavity(self,t_out,x0,y0,w,M,H_start,H_end,draw):
        '''
        Method to create suffosion box for in the simulation plot
        '''
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
            Ri = Hi*np.tan(draw)
            
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
        
        return plot_box

    def create_cavity_position(self):
        '''
        '''
        #middle point
        x_m = self.x0
        y_m = self.y0
        z_m = self.H
        w = self.w
        M = self.M
        draw = self.draw
        H_start = self.H
        H_end = self.H_min
        
        t_out = self.t
        
        #normalize output
        t_out = t_out/max(t_out)

        if self.mechanism.lower() == 'suffosion':
            plot_box = self.suffosion_cavity(t_out,x_m,y_m,w,M,H_start,H_end,draw)
            return plot_box
        elif self.mechanism.lower() == 'stoping':
            plot_box = self.stoping_cavity(t_out,x_m,y_m,w,M,H_start,H_end,draw)
            return plot_box
        else:
            print('No Mechanism Specified. Please specify a mechanism')

def _test():
    '''
    first test
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

    t = np.arange(0,10,1)
    time_type = 'poly'

    obj = visualization(x0,y0,H,H_min,M,w,draw,x_range,y_range,t,time_type)

    obj.obj.kz_type = 'Gaussian'

    obj.interactive_figure()

def _test2():
    '''
    first test
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

    t = np.arange(0,10,1)
    time_type = 'poly'

    obj = visualization(x0,y0,H,H_min,M,w,draw,x_range,y_range,t,time_type)

    obj.mechanism = 'stoping'
    obj.obj.kz_type = 'Gaussian'

    obj.interactive_figure()   

def _test3():
    '''
    Function to test the line of sight plot
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

    t = np.arange(0,10,1)
    time_type = 'poly'

    obj = visualization(x0,y0,H,H_min,M,w,draw,x_range,y_range,t,time_type)

    obj.mechanism = 'stoping'
    obj.obj.kz_type = 'Gaussian'
    
    theta = np.deg2rad(45)
    alpha = np.deg2rad(190)

    obj.interactive_figure_los(theta,alpha) 

def _test4():
    '''
    Testing the cross sectional tool
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

    t = np.arange(0,10,1)
    time_type = 'poly'

    obj = visualization(x0,y0,H,H_min,M,w,draw,x_range,y_range,t,time_type)

    obj.mechanism = 'stoping'
    obj.obj.kz_type = 'Gaussian'

    obj.cross_section_selector() 

if __name__ == '__main__':
    _test4()