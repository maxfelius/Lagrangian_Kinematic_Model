'''
@author: Max Felius
'''

#import
import numpy as np

#import packages
from Point_Geometry_Package.zg import zg_nois

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
        z_array = np.concatenate((z_array,step*v_wink2016_gaus*zg_nois(R_wink2016_gaus,r)))
        t = np.concatenate((t,[delta_days[nitems]]*n))
        r_array = np.concatenate((r_array,r))
        nitems += 1
    
    return x_array, y_array, z_array, t, r_array, nitems
