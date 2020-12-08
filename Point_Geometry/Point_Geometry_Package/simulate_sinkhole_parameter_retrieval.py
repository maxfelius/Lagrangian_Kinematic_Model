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

def simulate_sinkhole_parameter_retrieval(delta_days,x0,y0,max_subs,n_sims,x_unravel,y_unravel,v_model,R_model):
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
    
    number_subs = [x for x in range(1,max_subs)]
    
    #save variables
    ehat_saved = []
    y_saved = [] #it is only used to determine the 'fit'
    fit_saved = []

    fit_total_save = np.zeros((n_sims,max_subs-1))
    cond_number_total_save = np.zeros((n_sims,max_subs-1))

    for sim_num in tqdm(range(n_sims),'Simulating'):
        for n_sub in number_subs:
            x_sub, y_sub = get_random_subsamples(n_sub,x_unravel,y_unravel)

            #compute the radius
            r = np.sqrt((x_sub-x0)**2 + (y_sub-y0)**2)
            
            #Get simulated measured data
            x_array, y_array, z_array, t, r_array, nitems = get_subsampled_arrays(x_sub,y_sub,r,delta_days,v_model,R_model)

            #initial parameters
            R = 500
            v = 100

            #catch singular matrices
            try:
                ehat, y, cond_number = case_inverse_kinematic_model(v,t,R,r_array,z_array)

                fit = 100*(1-(np.sum(abs(ehat))/np.sum(abs(y))))

                #filter out nan values
                if np.isnan(fit) or fit < 0:
                    fit = 0
                if np.isnan(cond_number)or cond_number > 15000:
                    cond_number = 15000
            except:
                ehat = 0
                y = 0
                fit = 0
                cond_number = 15000
                
                #save the point geometry and make a figure
                num_sub = n_sub
                num_sim = sim_num
                save_exception(t,x_array,y_array,z_array,num_sub,num_sim,foldername)

            fit_total_save[sim_num,n_sub-1] = fit
            cond_number_total_save[sim_num,n_sub-1] = cond_number
            
    return fit_total_save, cond_number_total_save, number_subs


def save_exception(t,x_array,y_array,z_array,num_sub,num_sim,foldername):
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
