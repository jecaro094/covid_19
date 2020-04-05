#!/bin/bash

echo "Getting kaggle.json..."
cd
mv ~/Descargas/kaggle.json ~/.kaggle
sudo chmod 600 ~/.kaggle/kaggle.json


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

echo "Installing kaggle for pip..."
pip install kaggle

echo "Installing schedule for pip..."
pip install schedule