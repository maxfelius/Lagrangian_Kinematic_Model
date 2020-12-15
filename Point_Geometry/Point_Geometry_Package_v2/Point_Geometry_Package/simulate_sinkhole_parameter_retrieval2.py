'''
@author: Max Felius

'''

#imports
import numpy as np
from tqdm import tqdm
import os, sys, time
import pandas as pd
import matplotlib.pyplot as plt

#packages imports
from Point_Geometry_Package.get_random_subsamples import get_random_subsamples
from Point_Geometry_Package.get_subsampled_arrays import get_subsampled_arrays
from Point_Geometry_Package.case_inverse_kinematic_model import case_inverse_kinematic_model

#create object class
class simulate_sinkhole:
    '''
    Object Holding Sinkhole Parameters and methods to create and retrieve parameters
    '''
    def __init__(self):
        '''
        Setting the variables
        '''
        #Create cell to make point samples
        #using the sinkhole from wink2016 for generating the point samples
        self.v_wink2016_gaus = 0.00031316308355901993
        self.R_wink2016_gaus = 553.0609564207193 
        self.delta_days = np.array([0, 12, 24, 36, 48, 60, 72, 96, 108, 120, 132])

        #coordinates
        self.x0 = 0
        self.y0 = 0

        #other parameters
        self.n = 100
        self.max_subs = 100
        self.n_sims = 20

        #computing parameters
        self.compute_parameters()

        #save variables
        self.ehat_saved = []
        self.y_saved = [] #it is only used to determine the 'fit'
        self.fit_saved = []
        self.number_subs = []

        self.fit_total_save = np.zeros((1,1))
        self.cond_number_total_save = np.zeros((1,1))
        self.y = np.zeros((1,1))
        self.ehat = np.zeros((1,1))

        #initial parameters
        self.R = 500
        self.v = 1

    def compute_parameters(self):
        #Define the sinkhole grid
        self.x_range = self.R_wink2016_gaus
        self.y_range = self.R_wink2016_gaus
        self.x = np.linspace(self.x0-self.x_range,self.x0+self.x_range,self.n)
        self.y = np.linspace(self.y0-self.y_range,self.y0+self.y_range,self.n)

        #creat x/y grid
        self.xv, self.yv = np.meshgrid(self.x,self.y)

        #unravel the grids
        self.x_unravel = self.xv.ravel()
        self.y_unravel = self.yv.ravel()

    def reset(self):
        self.compute_parameters()
        print('Done recomputing spatial parameters')

    def save_exception(self,t,x_array,y_array,z_array,num_sub,num_sim,foldername):
        '''
        Save the exception for later investigation
        '''
                
        header = ['time','x','y','subsidence']

        data = np.array([t,x_array,y_array,z_array]).T

        filename=f'num_sub{num_sub}-num_sim{num_sim}'

        df = pd.DataFrame(data,columns=header)
        df.to_csv(os.path.join(foldername,filename+'.csv'))

        #making the figure

        plt.figure()
        h = plt.scatter(x_array[t==t[-1]],y_array[t==t[-1]],c=z_array[t==t[-1]])
        plt.title(filename)
        plt.colorbar(h)
        plt.savefig(os.path.join(foldername,filename+'.png'))
        plt.close()

    def simulate_sinkhole_parameter_retrieval(self):
        '''
        '''
        #check if the folder is present to save the exceptions
        foldername_start = 'data_point_geometry'
        i = 1
        while True:
            foldername = foldername_start+'_{:02d}'.format(i)
            if not os.path.exists(foldername):
                os.mkdir(foldername)
                break
            else:
                i += 1
        
        self.number_subs = [x for x in range(1,self.max_subs)]
        
        #reset save variables
        self.ehat_saved = []
        self.y_saved = [] #it is only used to determine the 'fit'
        self.fit_saved = []

        self.fit_total_save = np.zeros((self.n_sims,self.max_subs-1))
        self.cond_number_total_save = np.zeros((self.n_sims,self.max_subs-1))
        self.y = np.zeros((self.n_sims,self.max_subs-1))
        self.ehat = np.zeros((self.n_sims,self.max_subs-1))


        for sim_num in tqdm(range(self.n_sims),'Simulating'):
            for n_sub in self.number_subs:
                x_sub, y_sub = get_random_subsamples(n_sub,self.x_unravel,self.y_unravel)

                #compute the radius
                r = np.sqrt((x_sub-self.x0)**2 + (y_sub-self.y0)**2)
                
                #Get simulated measured data
                x_array, y_array, z_array, t, r_array, nitems = get_subsampled_arrays(x_sub,y_sub,r,self.delta_days,self.v_wink2016_gaus,self.R_wink2016_gaus)

                #catch singular matrices
                try:
                    ehat, y, cond_number = case_inverse_kinematic_model(self.v,t,self.R,r_array,z_array)

                    fit = 100*(1-(np.sum(abs(ehat))/np.sum(abs(y))))

                    #filter out nan values
                    if np.isnan(fit) or fit < 0:
                        fit = 0
                    if np.isnan(cond_number)or cond_number > 1e10:
                        cond_number = 1e10
                except:
                    ehat = 0
                    y = 0
                    fit = 0
                    cond_number = 1e10
                    
                    #save the point geometry and make a figure
                    num_sub = n_sub
                    num_sim = sim_num
                    self.save_exception(t,x_array,y_array,z_array,num_sub,num_sim,foldername)

                #saving variables
                self.fit_total_save[sim_num,n_sub-1] = fit
                self.cond_number_total_save[sim_num,n_sub-1] = cond_number
                # self.y[sim_num,n_sub-1] = y
                # self.ehat[sim_num,n_sub-1] = ehat

def _test():
    obj = simulate_sinkhole()
    obj.simulate_sinkhole_parameter_retrieval()

    #extracting average fit percentages    
    avg_data = np.sum(obj.fit_total_save,axis=0)/obj.n_sims

    #Plot the results
    plt.figure(figsize=(10,5))
    plt.plot(obj.number_subs,avg_data)
    plt.scatter(obj.number_subs,avg_data)

    #mean of the conditional number. SKIPPED THE FIRST ENTRY
    mean = np.mean(avg_data)

    plt.title('Random subsampling of the dataset. Mean fit percentage: {:.0f}%'.format(mean))
    plt.ylabel('Fit Percentage [%]')
    plt.xlabel('Number of random points used')

    plt.grid(True)

def _test2():
    pass

def main():
    pass

if __name__ == '__main__':
    main()