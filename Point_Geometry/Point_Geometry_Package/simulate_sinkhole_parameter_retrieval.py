'''
@author: Max Felius

'''

#imports
import numpy as np
import tqdm

#packages imports
from Point_Geometry_Package.get_random_subsamples import get_random_subsamples
from Point_Geometry_Package.get_subsampled_arrays import get_subsampled_arrays
from Point_Geometry_Package.case_inverse_kinematic_model import case_inverse_kinematic_model

def simulate_sinkhole_parameter_retrieval(delta_days,x0,y0,max_subs,n_sims,x_unravel,y_unravel):
    '''
    '''
    number_subs = [x for x in range(1,max_subs)]
    
    #save variables
    ehat_saved = []
    y_saved = []
    fit_saved = []

    fit_total_save = np.zeros((n_sims,max_subs-1))
    cond_number_total_save = np.zeros((n_sims,max_subs-1))

    # for sim_num in range(n_sims):
    for sim_num in tqdm(range(n_sims),'Simulating'):
        for n_sub in number_subs:
            x_sub, y_sub = get_random_subsamples(n_sub,x_unravel,y_unravel)

            #compute the radius
            r = np.sqrt((x_sub-x0)**2 + (y_sub-y0)**2)

            x_array, y_array, z_array, t, r_array, nitems = get_subsampled_arrays(x_sub,y_sub,r,delta_days)

            #initial parameters
            R = 500
            v = 100

            #catch singular matrices
            try:
                ehat, y, cond_number = case_inverse_kinematic_model(v,t,R,r_array,z_array)

                fit = 100*(1-(np.sum(abs(ehat))/np.sum(abs(y))))
            except:
                ehat = 0
                y = 0
                fit = 0
                cond_number = 1500

            #save variables
            ehat_saved.append(ehat)
            y_saved.append(y)
            fit_saved.append(fit)

            #filter out nan values
            if np.isnan(fit) or fit < 0:
                fit = 0
            if np.isnan(cond_number):
                cond_number = 1500

            fit_total_save[sim_num,n_sub-1] = fit
            cond_number_total_save[sim_num,n_sub-1] = cond_number
            
    return fit_total_save, cond_number_total_save, number_subs
