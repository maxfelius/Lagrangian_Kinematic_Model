'''
Building a heatmap to see where the points usually lie

@author: Max Felius
'''

#import
import numpy as np
import pandas as pd
import os, sys, time
import matplotlib.pyplot as plt

xdata = np.array([])
ydata = np.array([])

for item in os.listdir():
    if item.endswith('.csv'):
        data = pd.read_csv(item)
        
        t = data['time'].values
        xdata = np.concatenate((xdata,data['x'][t==t[-1]].values))
        ydata = np.concatenate((ydata,data['y'][t==t[-1]].values))

pd_data = np.array([xdata,ydata]).T
df = pd.DataFrame(pd_data,columns=['pnt_rdx','pnt_rdy'])

df.to_csv('test.csv')


plt.figure()
plt.scatter(xdata,ydata)
plt.show()
