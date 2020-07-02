#!/bin/bash

script_folder="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_folder="$(dirname $script_folder)"

sudo apt-get update -y
sudo apt-get install --reinstall -y \
    psmisc \
    iw \
    hostapd \
    dnsmasq \
    wpasupplicant \
    net-tools \
    procps

sudo pip install --upgrade virtualenv

cd $project_folder/api
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
deactivate

