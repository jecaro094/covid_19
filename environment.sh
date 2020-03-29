#!/bin/bash

echo "Updating..."
sudo apt-get update --yes

echo "Installing unzip..."
sudo apt-get install unzip --yes

echo "Installing kaggle..."
sudo apt-get install kaggle --yes

# Get Miniconda and make it the main Python interpreter
echo "Getting Miniconda3"
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p ~/miniconda 
rm ~/miniconda.sh

# Get and save configuration file (kaggle)
