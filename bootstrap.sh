#!/usr/bin/env bash

sudo add-apt-repository ppa:fkrull/deadsnakes
apt-get update
apt-get install -y python3.5
apt-get install -y python3-pip
apt-get install -y git
pip3 install virtualenv