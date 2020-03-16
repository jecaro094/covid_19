# Required imports 
import math
import numpy as np
from services.mail import MailSender
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.pyplot import figure
import kaggle
import os

kaggle.api.authenticate()
kaggle_dataset = ['gold','silver','other']

yesterday_previous = date.today() - timedelta(days=2)
yesterday_updated = date.today() - timedelta(days=1)
sent_once = False
cont = 0

# Defining dataframe for specified country
def get_country_cases(country, country_field, date_field):
    df_total = pd.read_csv('covid_data/covid_19_data.csv')
    df_country = df_total[df_total[country_field]==country]
    df_country['Active'] = df_country['Confirmed'] - (df_country['Deaths'] + df_country['Recovered'])
    
    # Indexes must be the same when I want to compare different countries
    df_country['Datetime'] = pd.to_datetime(df_country[date_field])
    df_country = df_country.set_index('Datetime')
    
    return df_country

def get_kaggle_dataset(kaggle_data):

    global yesterday_updated
    global yesterday_previous
    global sent_once
    send_image = False

    os.system("mkdir covid_data ")

    if kaggle_data=='gold':
        # Download the COVIDdataset and save files in 'covid_data/' (GOLD)
        os.system("rm -rf covid_data ")
        os.system("kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset")
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

    # 'date_condition==TRUE': new data was registered yesterday
    yesterday_updated = date.today() - timedelta(days=1)
    if yesterday_previous!=yesterday_updated:
        yesterday_previous = yesterday_updated
        sent_once = False
        print(f'IMAGE SENT --> {sent_once}')
    else:
        print(f'IMAGE SENT --> {sent_once}')

    date_condition = str(yesterday_updated) in str(get_country_cases('Spain', country_field, date_field).index.values[-1])


    # Condition satisfied: run code
    if date_condition and sent_once==False:
        send_image = True
    else:
        send_image = False

    return send_image, country_field, date_field


# To return the RMS between different countries
def distance_between_countries(df_1, df_2):
    difference = df_1['Active'] - df_2['Active']
    difference_not_nan = difference[difference.isnull()==False] # These are the non NaN values
    if len(difference_not_nan)==0: # There are not values to compare to obtain RMS, so its useless
        score = 10*(10**20)
    elif len(difference_not_nan)>0:
        score = sum(abs(difference_not_nan))
        
    return score

# For obtaining the optimal shifted plot
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

def send_gmail_message():
    username = os.environ['GMAIL_USER']
    password = os.environ['GMAIL_PASS']
    sender = os.environ['GMAIL_USER']

    images = list()
    images.append({
        'id': 'data',
        'path': 'data.png'
    })

    mail_sender = MailSender(username, password)
    mail_sender.send(sender, [os.environ['GMAIL_DEST']], 'Imagen del coronavirus', images=images)


while(True):

    # Consider each covid-19 kaggle dataset
    for kaggle_data in kaggle_dataset:
        send_image, country_field, date_field = get_kaggle_dataset(kaggle_data)
        # Keep the data from the dataset with dates from yesterday
        if(send_image):
            print('SEND DATA')
            break

    # Main code
    if send_image==True:

        # Country lists
        df_list = []
        cont += 1
        last_days_to_show = 22 + cont
        color_vector = ['blue','red','green']
        country_names = ['Italy','Spain','Germany']
        days_window_size = 20 # to define a range = [-20,20] in order to obtain RMS.
                            # '0' if I dont want to shift graphs

        # Defining new cases 
        for name in country_names:
            df_list.append(get_country_cases(name, country_field, date_field))


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
        #plt.show()
        plt.savefig('data.png')

        sent_once = True

        # Send 'data.png' via gmail
        # Allowed non-secure application access to the account: 'jecarobd@gmail.com'
        # Otherwise, 'MailSender' gives an authentification error.
        send_gmail_message()
        




