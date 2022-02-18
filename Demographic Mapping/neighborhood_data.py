"""
Created on Wed Nov  3 22:12:54 2021
​
@author: emmas
"""

import pandas as pd 
​
​
FILENAME = 'demographics.xlsm'
​
​
''' Nested dictionary to represent statistics for each neighborhood ''' 
​
​
class Neighborhood: 
    
   
    
    def __init__(self, neighborhood):
        self.neighborhood = neighborhood
        self.data = {}
        
    def add_data_for(self, stat_type):
        ''' Adds entry of self.data with key:stat_type (sheet of demographics)
            and value: nested dict with key:column_name value: statistic ''' 
        
        # read in and clean data 
        df = pd.read_excel(FILENAME, stat_type, index_col=0)
        df = df[df.columns[~df.isnull().all()]]
        df = df.dropna()
        
        # remove spaces in row names 
        cols = list(df.index)
        clean_cols = [col.strip() for col in cols]
        df.rename(index=pd.Series(clean_cols))
        
        
        # take care of '%' headers 
        headers = list(df.columns.values)
        clean_heads = []
        for i in range(len(headers)):
            if '%' in headers[i]:
                clean_heads.append(headers[i-1] + ' %')
            else: 
                clean_heads.append(headers[i])
        df.columns = clean_heads
        
        # put data in dictionary 
        neigh_data = df.loc[self.neighborhood]
        stat_dict = neigh_data.to_dict()
        self.data[stat_type] = stat_dict
        
    def get_stat_type(self, stat_type):
        ''' Prints dictionary for stat type TODO: make it print in a nice format ''' 
        return self.data[stat_type]
           
    def get_stat(self, stat_type, stat):
        ''' Prints specific value for stat TODO: make it print in a nice format'''
        
        if '%' in stat:      
            return stat + ' : ' + str(round(self.data[stat_type][stat] * 100, 2))
        else: 
            return stat + ' : ' + str(round(self.data[stat_type][stat] * 100, 2))
         
​
​
​
    
    
​
​
if __name__ == '__main__':
    
    back_bay = Neighborhood('Back Bay')    
    back_bay.add_data_for('Race')
    back_bay.add_data_for('School Enrollment')
    print(back_bay.get_stat('Race', 'Asian alone'))
    print(back_bay.get_stat_type('Race'))