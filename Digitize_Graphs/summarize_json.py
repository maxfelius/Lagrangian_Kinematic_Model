'''
@author: Max Felius

Python script that will walk through all subfolders and combines the found json files into one

'''

#imports 
import numpy as np
import os, sys, time
import json

#save path to json files
json_path = []

#save dict
dt = {}

for root, dirs, files in os.walk(os.getcwd(), topdown=False):
   for name in files:
       if name.endswith('.json'):
           json_path.append(os.path.join(root,name))

for json_file in json_path:
    if json_file=='Summarized_Parameters.json':
        continue
    else:
        with open(json_file,'r') as file:
            data = json.load(file)
            data_key = list(data.keys())
            dt[data_key[0]] = data[data_key[0]]

with open('Summarized_Parameters.json','w') as output:
    json.dump(dt,output,indent=3)
    print('Combined Parameters...')
            
