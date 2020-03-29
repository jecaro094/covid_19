#!/bin/bash

echo "Getting GMAIL_PASSWORD in order to send e-mails..."
#read gmailpass
gmailpass=password
export GMAIL_PASS="$gmailpass"

echo "Getting GMAIL_USER in order to send e-mails..."
#read gmailuser
gmailuser=email@gmail.com
export GMAIL_DEST="$gmailuser"
export GMAIL_USER="$gmailuser"

echo "Running the application..."
python covid.py
