#!/bin/bash

# for debian based Operating Systems only

# install requirements 
echo -e "[*] Updating and Installing packages\n\n"
sudo apt update -y
sudo apt install git python3 python3-pip -y

# download and configure project
echo -e "[*] Downloading and Configuring Project\n\n"
cd $HOME
git clone --depth=1 https://github.com/dmdhrumilmistry/SSO-Flask.git
cd $HOME/SSO-Flask
python3 -m pip install -r requirements.txt

# ask for AWS creds and store it into .env file
echo -e "[*] Enter AWS Credentials\n"

echo -e "[+] AWS_ACCESS_KEY_ID: "
read AWS_ACCESS_KEY_ID
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID


echo -e "[+] AWS_SECRET_ACCESS_KEY: "
read AWS_SECRET_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

echo -e "[+] AWS_REGION_NAME: "
read AWS_REGION_NAME
export AWS_REGION_NAME=$AWS_REGION_NAME

# add local bin to path
echo -e "[*] Setting Path\n\n" 
export PATH=$HOME/.local/bin:$PATH:

# start project
waitress-serve --listen=*:5000 app:app