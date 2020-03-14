import kaggle
kaggle.api.authenticate()

import os
kaggle_data = 'silver'

if kaggle_data=='gold':
    # Download the COVIDdataset and save files in 'covid_data/' (GOLD)
    os.system("rm -rf covid_data ")
    os.system("kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset ")
    os.system("unzip novel-corona-virus-2019-dataset.zip -d covid_data ")
    os.system("rm -rf novel-corona-virus-2019-dataset.zip ")

    date_field = 'ObservationDate'
    country_field = 'Country/Region'

elif kaggle_data=='silver':
    # Download the COVIDdataset and save files in 'covid_data/' (SILVER)
    os.system("rm -rf covid_data ")
    os.system("kaggle datasets download -d imdevskp/corona-virus-report")
    os.system("unzip corona-virus-report.zip -d covid_data ")
    os.system("rm -rf corona-virus-report.zip ")
    os.system("mv covid_data/covid_19_clean_complete.csv covid_data/covid_19_data.csv")

    date_field = 'Date'
    country_field = 'Country/Region'

elif kaggle_data=='other':

    # Download the COVIDdataset and save files in 'covid_data/' (LESS IMPORTANT)
    os.system("rm -rf covid_data ")
    os.system("kaggle datasets download -d vignesh1694/covid19-coronavirus")
    os.system("unzip covid19-coronavirus.zip -d covid_data ")
    os.system("rm -rf covid19-coronavirus.zip ")
    os.system("mv covid_data/2019_nCoV_data.csv covid_data/covid_19_data.csv")

    date_field = 'Date'
    country_field = 'Country'


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.pyplot import figure


# To return the RMS between different countries
def distance_between_countries(df_1, df_2):
    difference = df_1['Active'] - df_2['Active']
    difference_not_nan = difference[difference.isnull()==False] # These are the non NaN values
    if len(difference_not_nan)==0: # There are not values to compare to obtain RMS, so its useless
        score = 10*(10**20)
    elif len(difference_not_nan)>0:
        score = sum(abs(difference_not_nan))
        
    return score

# For obtaining the oprimal shifted plot
def optimal_shifted_df(df_italy, df_country, days_range):
    score_dictionary = {}
    if days_range!=0:
        for days_to_move in range(-days_range,days_range):
            df_country_shifted = df_country.shift(periods=days_to_move, freq=None, axis=0)
            score_dictionary[days_to_move] = distance_between_countries(df_italy, df_country_shifted)
        optimal_day = min(score_dictionary, key=score_dictionary.get)
    else:
        optimal_day = 0
    df_country_shifted = df_country.shift(periods=optimal_day, freq=None, axis=0)
    
    #print(score_dictionary)
    #print(optimal_day)
    
    return df_country_shifted, optimal_day


# Defining dataframe for specified country
def get_country_cases(country):
    df_total = pd.read_csv('covid_data/covid_19_data.csv')
    df_country = df_total[df_total[country_field]==country]
    df_country['Active'] = df_country['Confirmed'] - (df_country['Deaths'] + df_country['Recovered'])
    
    # Indexes must be the same when I want to compare different countries
    df_country['Datetime'] = pd.to_datetime(df_country[date_field])
    df_country = df_country.set_index('Datetime')
    
    return df_country

get_country_cases('Spain').tail(5) # Last 5 days



# Required imports 
import math
import numpy as np

# Country lists
df_list = []
last_days_to_show = 20
color_vector = ['blue','red','green']
country_names = ['Italy','Spain','Germany']
days_window_size = 20 # to define a range = [-20,20] in order to obtain RMS.
                      # '0' if I dont want to shift graphs

# Defining new cases 
for name in country_names:
    df_list.append(get_country_cases(name))



# Define plot parameters
ax = plt.gca()

for i, df_country in enumerate(df_list):
    if i==0: # Italy     
        df_italy = df_country.copy()
        ax_0 = df_italy.tail(last_days_to_show).plot(kind='line', lw=4, color=color_vector[0], grid=True, figsize=(15,10), x=date_field, y='Active', ax=ax)   
    else:
        df_country_shifted, optimal_day = optimal_shifted_df(df_italy, df_country, days_window_size)
        globals()['ax_'+str(i)] = df_country_shifted.tail(last_days_to_show).plot(kind='line', lw=4, color=color_vector[i], grid=True, figsize=(15,10), x=date_field, y='Active', ax=ax)   
        country_names[i] += ': ' + str(optimal_day) + ' days'
        
        
ax_0 = df_italy.tail(last_days_to_show).plot(kind='line', lw=4, color=color_vector[0], grid=True, figsize=(15,10), x=date_field, y='Active', ax=ax)   
ax_0 = df_italy.tail(last_days_to_show).plot(kind='bar', alpha=0, legend=False, color='blue', grid=True, figsize=(15,10), x=date_field, y='Active', ax=ax)


ax.set_ylabel("Active cases")
ax.legend(country_names)
    
# Plot the data
plt.show()