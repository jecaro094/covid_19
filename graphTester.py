
from services.mail import MailSender
from services.kaggleData import KaggleData
from services.covidGraphics import CovidGraphics 

from datetime import date, timedelta
import os



def send_gmail_message(text_message, subject):
    username = os.environ['GMAIL_USER']
    password = os.environ['GMAIL_PASS']
    sender = os.environ['GMAIL_USER']

    images = list()
    images.append({
        'id': 'data',
        'path': 'data.png'
    })

    mail_sender = MailSender(username, password)
    mail_sender.send(sender=sender, recipients=[os.environ['GMAIL_DEST']],
                     subject=subject, images=images,
                     message_plain=text_message, message_html=text_message)

# MAIN CODE
def job():

    global sent_once
    global yesterday_previous
    global yesterday_updated
    global cont
    global kaggle_dataset

    # Consider each covid-19 kaggle dataset
    for kaggle_data in kaggle_dataset:
        # Define object with 'KaggleData' class
        kd = KaggleData(kaggle_data, yesterday_previous, yesterday_updated, sent_once)
        yesterday_previous = kd.yesterday_previous
        yesterday_updated = kd.yesterday_updated
        # Keep the data from the dataset with dates from yesterday
        if kd.send_image:
            print("SENDING DATA...")
            break
        else:
            print("NOT SENDING DATA")

    # Main code
    if kd.send_image:

        cg = CovidGraphics(kd)
        cg.text_message = ''
        cg.subject = f'{date.today()}: {cg.cases} cases'
        sent_once = True


# Variables considered to get info from yesterday
yesterday_previous = date.today() - timedelta(days=2)
yesterday_updated = date.today() - timedelta(days=1)

# Considered in plots
cont = 0

# Datasets considered
kaggle_dataset = ['gold','silver','other']

# Required to know if I have sent an image
sent_once = False

# Only sends data once! 
job()

        