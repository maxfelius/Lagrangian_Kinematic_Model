'''
@author: Max Felius
'''

#import
import numpy as np
import time, os, sys

#package imports
from Point_Geometry_Package.zg import zg

#defining the inverse model for case 1 and 2
def case_inverse_kinematic_model(v,t,R,r,y):
    '''
    Non-Linear Least Squares for determining kinematic model parameters
    
    Input:
    :type v: int
    :type t: np.array(float)
    :type R: int
    :type r: np.array(float)
    :type y: np.array(float)
    
    Output
    :rtype R: int
    :rtype v: int
    '''
    #maximum number of runs
    n = 10000
    
    #initial values
    Qyy = np.eye(len(r))
    invQyy = np.linalg.inv(Qyy)
    
    #start the timer
    start = time.time()
    
    for i in range(n):
        #expected deformation
        yhat = v*t*zg(R,r)
        
        #compute the difference in measured and computed subsidence
        dy = y - yhat
        
        #defining the jacobian matrix
        A1 = t*zg(R,r)
        A2 = ((2*v*t*np.pi*r**2)/(R**3))*zg(R,r)
        # A2 = ((2*R**2 + 2*np.pi*r**2)/(R**3))*(v*t)*zg(R,r)
           
        J = np.array([A1,A2]).T
        
        cond_number = np.linalg.cond(J)
        
        Qxhat = np.linalg.inv(J.T @ invQyy @ J)
        dx = Qxhat @ J.T @ invQyy @ dy
        
        v_old = v
        R_old = R
        v = v + dx[0]
        R = R + dx[1]
        
        dx_hat = np.array([v_old-v,R_old-R]).T
        
        if dx_hat.T @ Qxhat @ dx_hat < sys.float_info.epsilon:
#             print(f'Stopped at iteration {i+1}.\nThe computed values are v={v} and R={R}.')
            break
    
#     if i == n-1:
#         print(f'Ended using the maximum number of iterations: {n}.\nThe computed values are v={v} and R={R}.')
    
#     print(f'The total runtime was: {time.time()-start} seconds.')
    
    ehat = yhat - y
    
    return ehat, y, cond_number
