# Required imports 
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib import dates
#from matplotlib.pyplot import figure

from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot
from bokeh.plotting import figure
from bokeh.palettes import plasma
from bokeh.models import Range1d, ColumnDataSource

class CovidGraphics:
    def __init__(self, kd):
        self.color_vector = ['green']
        self.country_names = ['Germany']

        self.cases = 'Active'

        self.df_list = []
        self.last_days_to_show = 35
        self.cont = 0
        self.days_window_size = 20 # to define a range = [-20,20] in order to obtain RMS.
                                   # '0' if I dont want to shift graphs

        self.kd = kd

        #self.display_plots()
        self.display_new_daily_cases_bokeh('Spain', 'Recovered')

    # Defining dataframe for specified country
    def get_country_cases(self, country, country_field, date_field):
        df_total = pd.read_csv('covid_data/covid_19_data.csv')
        df_country = df_total[df_total[country_field]==country]
        df_country['Active'] = df_country['Confirmed'] - (df_country['Deaths'] + df_country['Recovered'])

        # Just to redefine 'Deaths' name, minor change...
        df_country['Death'] = df_country['Deaths']
        
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
        plt.show()
        #plt.savefig('data.png')

    def display_new_daily_cases(self):
        # Country lists
        self.cont += 1
        self.last_days_to_show += self.cont
        daily_list =[]
        self.cases = 'New'

        # Input country...
        name = 'Germany'
        source_cases = 'Active' # 'Death', 'Active', 'Recovered', 'Confirmed' (not very useful last one)

        # Dataframe with active cases (also)
        self.df_list.append(self.get_country_cases(name, self.kd.country_field, self.kd.date_field))

        # Define new daily cases ('New')
        for i, active in enumerate(self.df_list[0][source_cases]):
            if i==0:
                daily_list.append(active)
            else:
                daily_list.append(active-prev_active)
            prev_active = active
            
        #print(daily_list)
        self.df_list[0]['New'] = daily_list


        # Define plot parameters
        ax = plt.gca()
                
        ax_0 = self.df_list[0].tail(self.last_days_to_show).plot(kind='bar', alpha=1, legend=False, color='purple', grid=True, figsize=(15,10), x=self.kd.date_field, y=self.cases, ax=ax)

        ax.set_ylabel(f"{self.cases} {source_cases} Cases")
        ax.legend([name])
            
        # Plot the data
        plt.show()
        #plt.savefig('data.png')

    def display_new_daily_cases_bokeh(self, name, source_cases):
        # Country lists
        self.cont += 1
        self.last_days_to_show += self.cont
        daily_list =[]
        self.cases = 'New'

        # Input country...
        #name = 'Germany'
        #source_cases = 'Active' # 'Death', 'Active', 'Recovered', 'Confirmed' (not very useful last one)

        # Dataframe with active cases (also)
        self.df_list.append(self.get_country_cases(name, self.kd.country_field, self.kd.date_field))

        # Define new daily cases ('New')
        for i, active in enumerate(self.df_list[0][source_cases]):
            if i==0:
                daily_list.append(active)
            else:
                daily_list.append(active-prev_active)
            prev_active = active
            
        #print(daily_list)
        self.df_list[0]['New'] = daily_list

        # Implementing bokeh plots
        source = ColumnDataSource(self.df_list[0].tail(self.last_days_to_show))
        dates = source.data[self.kd.date_field].tolist()
        p = figure(x_range=dates, plot_height=650, plot_width=1200, title="-----", toolbar_location=None, tools="", tooltips=[(f"New {source_cases} cases", "@New")])
        p.vbar(x=self.kd.date_field, width=0.6 , top='New' , fill_color='purple', legend_label=name, source=source)
        p.xaxis.major_label_orientation = math.pi/2
        show(p)
