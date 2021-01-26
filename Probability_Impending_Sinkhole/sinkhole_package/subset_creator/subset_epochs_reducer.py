'''
@author: Max Felius

This is a small script to reduce the number of epochs
'''

#imports
import numpy as np
import pandas as pd
import re, os
from decouple import config

class reduce_subset:
    '''
    input: 
        filedoc: str

    output:

    '''
    def __init__(self,filedoc):
        #list of important header for coordinates
        self.header_list = ['pnt_lon','pnt_lat','pnt_rdx','pnt_rdy'] 

        #import my data
        self.data = pd.read_csv(filedoc)

        #other parameters
        self.reduce_epochs = 30 #select the last 30 epochs

    def get_sentinel_epochs(self,header_list):
        '''
        Get the list of epochs
        '''
        filter_option = re.compile(r'd_\d{8}')
        epochs = list(filter(lambda x: filter_option.match(x) != None, header_list))
        return epochs

    def reduce_subset(self):
        '''
        function to reduce the subset
        '''
        data_coordinates = self.data[self.header_list]

        epochs = self.get_sentinel_epochs(list(self.data))

        data_epochs = self.data[epochs[-50:]]

        #combine dataset
        data_reduced = data_coordinates.join(data_epochs)

        return data_reduced

def _test():
    filename = 'subset_r120_lon6.06_lat50.87_full-pixel_mrss_rsat2_asc_t109_v3_b728bb51760435c769a9d45b3e8e74d6325b90fa.csv'

    subset_obj = reduce_subset(os.path.join('subsets',filename))
    subset_obj.header_list = ['pnt_lon','pnt_lat']
    data_reduced = subset_obj.reduce_subset()

    data_reduced.to_csv(os.path.join('subsets','subset_r120_lon6.06_lat50.87_mrss_rsat2_asc_t109_last50epochs.csv'))

if __name__ == '__main__':
    _test()
