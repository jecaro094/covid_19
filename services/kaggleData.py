import pandas as pd
import kaggle
from datetime import date, timedelta
import os

from services.covidGraphics import CovidGraphics as cg


class KaggleData:
    def __init__(self, kaggle_data, yesterday_previous, yesterday_updated, sent_once):

        # Variables considered to get info from yesterday
        self.yesterday_previous = yesterday_previous
        self.yesterday_updated = yesterday_updated

        # Have I just sent some data?
        self.sent_once = sent_once

        # Should I send an image?
        self.send_image = False 

        # Authentificate with my data in ".kaggle/kaggle.json"
        kaggle.api.authenticate()

        # Put dataset in "covid_data" folder
        self.get_kaggle_dataset(kaggle_data)


    def get_kaggle_dataset(self, kaggle_data):

        self.send_image = False
        os.system("mkdir covid_data ")

        if kaggle_data=='gold':
            # Download the COVID dataset and save files in 'covid_data/' (GOLD)
            os.system("rm -rf covid_data ")
            os.system("kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset")
            os.system("unzip novel-corona-virus-2019-dataset.zip -d covid_data ")
            os.system("rm -rf novel-corona-virus-2019-dataset.zip ")

            self.date_field = 'ObservationDate'
            self.country_field = 'Country/Region'

        elif kaggle_data=='silver':
            # Download the COVID dataset and save files in 'covid_data/' (SILVER)
            os.system("rm -rf covid_data ")
            os.system("kaggle datasets download -d imdevskp/corona-virus-report")
            os.system("unzip corona-virus-report.zip -d covid_data ")
            os.system("rm -rf corona-virus-report.zip ")
            os.system("mv covid_data/covid_19_clean_complete.csv covid_data/covid_19_data.csv")

            self.date_field = 'Date'
            self.country_field = 'Country/Region'


        elif kaggle_data=='other':

            # Download the COVID dataset and save files in 'covid_data/' (LESS IMPORTANT)
            os.system("rm -rf covid_data ")
            os.system("kaggle datasets download -d vignesh1694/covid19-coronavirus")
            os.system("unzip covid19-coronavirus.zip -d covid_data ")
            os.system("rm -rf covid19-coronavirus.zip ")
            os.system("mv covid_data/2019_nCoV_data.csv covid_data/covid_19_data.csv")

            self.date_field = 'Date'
            self.country_field = 'Country'

        # Update yesterday's date, in order to send the image
        if self.yesterday_previous!=self.yesterday_updated:
            self.yesterday_previous = self.yesterday_updated
            self.sent_once = False

        # 'date_condition==TRUE': new data was registered yesterday
        date_condition = str(self.yesterday_updated) in str(cg.get_country_cases(self, 'Spain', self.country_field, self.date_field).index.values[-1])


        # Condition satisfied: run code
        if date_condition and self.sent_once==False:
            self.send_image = True
        else:
            self.send_image = False

