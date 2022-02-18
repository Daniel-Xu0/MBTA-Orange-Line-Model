"""
Daniel Xu, Emma Sommers, Timothy Demling
Final Project - Statistical Measures
Professor Park and Raichlin
"""
#%% Module Imports, Constant Initilizations

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import contextily as cx

DEMOGRAPHICS = 'demographics.xlsm'
MBTA = 'mbta_delays.csv'
boston_df = gpd.read_file('Boston_Neighborhoods.geojson')

station_neighborhood = {'Oak Grove':'Malden', 'Malden Center':'Malden',
                        'Wellington':'Medford', 'Assembly':'Somerville',
                        'Sullivan Square':'Charlestown', 
                        'Community College':'Charlestown', 
                        'North Station':'West End', 'Haymarket':'North End',
                        'State':'Downtown', 'Downtown Crossing':'Downtown',
                        'Chinatown':'Chinatown', 'Tufts Medical Center':'Downtown',
                        'Back Bay':'Back Bay', 'Massachusetts Avenue':'South End',
                        'Ruggles':'Fenway', 'Roxbury Crossing':'Roxbury',
                        'Jackson Square':'Jamaica Plain', 'Stony Brook':'Jamaica Plain',
                        'Green Street':'Jamaica Plain', 'Forest Hills':'Roslindale'}

#%% Function

def get_delays(filename):
    '''
    Function: Associate each orange line stop with a neighborhood in Boston,
              then compute the average delay time for each
    Parameters: file with delay times for each stop (filename - string)
    Return: List of each neighborhood's average MBTA delay time
    '''
    df = pd.read_csv(filename)
    neighborhoods = [station_neighborhood[stop] for stop in df['stop_name']]
    df['neighborhoods'] = neighborhoods
    
    delay_times = df.groupby('neighborhoods').mean()['delay_time']
    neighborhood_delays = list(delay_times.items())
    
    return neighborhood_delays

#%% Class - Visualizing Neighborhood Statistics

class Statistic:
    
    def __init__(self, boston_df):
        '''' Constructor Method '''

        self.boston_df = boston_df
        
        plt.rcParams["figure.figsize"]= 15,15
    
    def make_df(self, sheet_name):
        '''
        Method: Clean data in excel sheet and adds corresponding MBTA delay times
        for each neighborhood
        Parameters: name of sheet (statistic to be analyzed), avg delay time
                    for each neighborhood (list) 
        Return: cleaned dataframe of entire excel sheet
        '''
            
        # read in and clean data
        self.df = pd.read_excel(DEMOGRAPHICS, sheet_name, index_col=0)
        self.df = self.df[self.df.columns[~self.df.isnull().all()]]
        self.df = self.df.dropna()
        
        # remove spaces in row names
        cols = list(self.df.index)
        clean_cols = [col.strip() for col in cols]
        self.df.rename(index=pd.Series(clean_cols))
        
        # take care of '%' headers
        headers = list(self.df.columns.values)
        clean_heads = []
        for i in range(len(headers)):
            if '%' in headers[i]:
                clean_heads.append(headers[i-1] + ' %')
            else:
                clean_heads.append(headers[i])
                
        self.df.columns = clean_heads

        return self.df
    
    
    def get_stat_options(self):
        ''' Returns headers so users can choose to make a data frame for just
            one to be plotted'''
        return (list(self.df.columns))
    
    
    def specific_stat(self, stat, delays):
        ''' Makes data from for one stat so it can be easily graphed 
            Also add in delay times to the stat_df so we can plot it later '''
        
        self.stat_df = pd.DataFrame()
        if stat in list(self.df.columns):
            self.stat_df = pd.DataFrame(self.df[stat])
        else:
            return 'Statistic is not in dataset'
        
        self.stat_df['MBTA Delays'] = 0
        for neighborhood in delays:
            if neighborhood[0] in self.stat_df.index:
                self.stat_df.at[neighborhood[0], 'MBTA Delays'] = neighborhood[1]
        
        return self.stat_df
        
    def specific_stat_vis(self, stat, delays):
        ''' 
        Method: Create geopandas visualization of a specified statistic. 
                Alongside it, graph MBTA delay times for neighborhoods, too.
        Parameters: specific statistic to be visualized (string), delay times
                    to be graphed ()
        Return: geopandas heatmappish plot depicting each neighborhood's 
                respective data value and their orange line delay times
        '''
    
        self.specific_stat(stat, delays)
        
        joined_df = self.boston_df.join(how='left', on='Name', other=self.stat_df)
        
        stat_map = joined_df.plot(column=stat, cmap='gist_earth', legend=True)
        plt.axis('off')
        plt.title(stat, fontsize = 30)
        cx.add_basemap(stat_map, crs = self.boston_df.crs.to_string(), 
                       source=cx.providers.OpenStreetMap.Mapnik)
        plt.gcf().set_size_inches(14, 10)
        
        delay_map = joined_df.plot(column='MBTA Delays', cmap='gist_earth', legend=True)
        plt.axis('off')
        plt.title('MBTA Delays', fontsize = 30)
        cx.add_basemap(delay_map, crs = self.boston_df.crs.to_string(), 
                       source=cx.providers.OpenStreetMap.Mapnik)
        plt.gcf().set_size_inches(14, 10)
    
if __name__ == '__main__':
    
    nativity = Statistic(boston_df)
    
    nativity_df = nativity.make_df('Vehicles per Household')
    
    delays = get_delays(MBTA)
    
    nativity.specific_stat_vis('No Access to a Vehicle %', delays)
    
    

    
    
    
    