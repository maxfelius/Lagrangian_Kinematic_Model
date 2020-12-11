'''
@author: Max Felius
'''

#import
import numpy as np

#import packages
from Point_Geometry_Package.zg import zg

def get_subsampled_arrays(x_sub,y_sub,r,delta_days,v_wink2016_gaus,R_wink2016_gaus):
    #create row arrays for x,y,z containing every epoch
    x_array = np.array([])
    y_array = np.array([])
    z_array = np.array([])
    t = np.array([])
    r_array = np.array([])

    nitems = 0
    for step in delta_days:
        n = len(x_sub)
        x_array = np.concatenate((x_array,x_sub))
        y_array = np.concatenate((y_array,y_sub))

        #Subsidence subsamples
        #Setting the noise level, std of 3 mm
        mu = 0 
        sigma = 0.003 #[m]
        noise = np.random.normal(mu, sigma, len(r))

        z_subsidence = noise*step*v_wink2016_gaus*zg(R_wink2016_gaus,r) #[m]

        z_array = np.concatenate((z_array,z_subsidence))
        t = np.concatenate((t,[delta_days[nitems]]*n))
        r_array = np.concatenate((r_array,r))
        nitems += 1
    
    return x_array, y_array, z_array, t, r_array, nitems
