# Required imports 
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.pyplot import figure

class CovidGraphics:
    def __init__(self, kd):
        self.color_vector = ['blue','red','green']
        self.country_names = ['Italy','Spain','Germany']

        self.cases = 'Active'
        self.text_message = 'Message to attach to the e-mail'

        self.df_list = []
        self.last_days_to_show = 35
        self.cont = 0
        self.days_window_size = 20 # to define a range = [-20,20] in order to obtain RMS.
                                   # '0' if I dont want to shift graphs

        self.kd = kd

        self.display_plots()

    # Defining dataframe for specified country
    def get_country_cases(self, country, country_field, date_field):
        df_total = pd.read_csv('covid_data/covid_19_data.csv')
        df_country = df_total[df_total[country_field]==country]
        df_country['Active'] = df_country['Confirmed'] - (df_country['Deaths'] + df_country['Recovered'])
        
        # Indexes must be the same when I want to compare different countries
        df_country['Datetime'] = pd.to_datetime(df_country[date_field])
        df_country = df_country.set_index('Datetime')
        
        return df_country


    # To return the RMS between different countries
    def distance_between_countries(self, df_1, df_2):
        difference = df_1[self.cases] - df_2[self.cases]
        difference_not_nan = difference[difference.isnull()==False] # These are the non NaN values
        if len(difference_not_nan)==0: # There are not values to compare to obtain RMS, so its useless
            score = 10*(10**20)
        elif len(difference_not_nan)>0:
            score = sum(abs(difference_not_nan))
            
        return score

    
    # For obtaining the optimal shifted plot
    def optimal_shifted_df(self, df_italy, df_country, days_range):
        score_dictionary = {}
        if days_range!=0:
            for days_to_move in range(-days_range,days_range):
                df_country_shifted = df_country.shift(periods=days_to_move, freq=None, axis=0)
                score_dictionary[days_to_move] = self.distance_between_countries(df_italy, df_country_shifted)
            optimal_day = min(score_dictionary, key=score_dictionary.get)
        else:
            optimal_day = 0
        df_country_shifted = df_country.shift(periods=optimal_day, freq=None, axis=0)
        
        #print(score_dictionary)
        #print(optimal_day)
        
        return df_country_shifted, optimal_day

    def display_plots(self):
        # Country lists
        self.cont += 1
        self.last_days_to_show += self.cont
        

        # Defining new cases 
        for name in self.country_names:
            self.df_list.append(self.get_country_cases( name, self.kd.country_field, self.kd.date_field))


        # Define plot parameters
        ax = plt.gca()

        for i, df_country in enumerate(self.df_list):
            if i==0: # Italy     
                df_italy = df_country.copy()
                ax_0 = df_italy.tail(self.last_days_to_show).plot(kind='line', lw=4, color=self.color_vector[0], grid=True, figsize=(15,10), x=self.kd.date_field, y=self.cases, ax=ax)   
            else:
                df_country_shifted, optimal_day = self.optimal_shifted_df(df_italy, df_country, self.days_window_size)
                globals()['ax_'+str(i)] = df_country_shifted.tail(self.last_days_to_show).plot(kind='line', lw=4, color=self.color_vector[i], grid=True, figsize=(15,10), x=self.kd.date_field, y=self.cases, ax=ax)   
                self.country_names[i] += ': ' + str(optimal_day) + ' days'
                
                
        ax_0 = df_italy.tail(self.last_days_to_show).plot(kind='line', lw=4, color=self.color_vector[0], grid=True, figsize=(15,10), x=self.kd.date_field, y=self.cases, ax=ax)   
        ax_0 = df_italy.tail(self.last_days_to_show).plot(kind='bar', alpha=0, legend=False, color='blue', grid=True, figsize=(15,10), x=self.kd.date_field, y=self.cases, ax=ax)


        ax.set_ylabel(f"{self.cases} cases")
        ax.legend(self.country_names)
            
        # Plot the data
        #plt.show()
        plt.savefig('data.png')

