#!/bin/bash

# for debian based Operating Systems only

# install requirements 
sudo apt update -y
sudo apt install git python3 python3-pip curl -y

# download and configure project
cd $HOME
git clone --depth=1 https://github.com/dmdhrumilmistry/SSO-Flask.git
cd $HOME/SSO-Flask
python3 -m pip install -r requirements.txt

# start project
waitress-serve --listen=*:80 app:app