# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Python Notebook Showing Different Visualization Options
# 
# @author: Max Felius
# 
# Notebook to show how to use the Lagrangian Kinematic Model Package
# 
# NOTE: The script does not work interactively in Python Notebooks
# 
# ## Contents:
# - Visualization suffosion, Linear Time and Gaussian Influence Function
# - Visualization stoping, Linear Time and Gaussian Influence Function
# - Visualization suffosion, Polynomial Time and Gaussian Influence Function
# - Visualization stoping, Polynomial Time and Gaussian Influence Function
# - Visualization suffosion, Linear Time and Bals Influence Function
# - Visualization suffosion, Linear Time and Beyer Influence Function
# 
# - Visualization Line of Sight, stoping, Linear Time and Gaussian Influence Function
# 
# - Showing the Cross Section tool using stoping, Linear Time and Gaussian Influence Function
# 
# ## Handy Websites
# https://kapernikov.com/ipywidgets-with-matplotlib/

# %%
#imports
import numpy as np
import sys, os
from decouple import config #package to obscure my path

#import package
#sys.path.extend([config('package')])
sys.path.extend(os.path.join(os.getcwd(),'Kinematic_Model'))

#import the visualization package
from Kinematic_Model.Visualization import visualization

#global variables
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

# %% [markdown]
# ## Visualization suffosion, Linear Time and Gaussian Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'suffosion'
obj.time_type = 'linear'
obj.obj.kz_type = 'Gaussian'

obj.interactive_figure()

# %% [markdown]
# ## Visualization stoping, Linear Time and Gaussian Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'notebook')

obj.mechanism = 'stoping'
obj.time_type = 'linear'
obj.obj.kz_type = 'Gaussian'

obj.interactive_figure()

# %% [markdown]
# ## Visualization suffosion, Polynomial Time and Gaussian Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'suffosion'
obj.time_type = 'poly'
obj.obj.kz_type = 'Gaussian'

obj.interactive_figure()

# %% [markdown]
# ## Visualization stoping, Polynomial Time and Gaussian Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'stoping'
obj.time_type = 'poly'
obj.obj.kz_type = 'Gaussian'

obj.interactive_figure()

# %% [markdown]
# ## Visualization suffosion, Linear Time and Bals Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'suffosion'
obj.time_type = 'linear'
obj.obj.kz_type = 'Bals'

obj.interactive_figure()

# %% [markdown]
# ## Visualization suffosion, Linear Time and Beyer Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'suffosion'
obj.time_type = 'linear'
obj.obj.kz_type = 'Beyer'

obj.interactive_figure()

# %% [markdown]
# ## Visualization Line of Sight, stoping, Linear Time and Gaussian Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'stoping'
obj.time_type = 'linear'
obj.obj.kz_type = 'Gaussian'

theta = np.deg2rad(45)
alpha = np.deg2rad(190)

obj.interactive_figure_los(theta,alpha) 

# %% [markdown]
# ## Showing the Cross Section tool using stoping, Linear Time and Gaussian Influence Function

# %%
# get_ipython().run_line_magic('matplotlib', 'qt')

obj.mechanism = 'stoping'
obj.time_type = 'linear'
obj.obj.kz_type = 'Gaussian'

obj.cross_section_selector() 


