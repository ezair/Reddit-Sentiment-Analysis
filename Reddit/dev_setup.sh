# @author Eric Zair
# @file dev_setup.sh
# @date: 05/02/2020
#
# Simple setup bash script used to setup this project
# for users that are running linux.
#
# We install all python packages needed, install the resources for
# NLTK, install doxygen (for project documentation), and finally,
# run the documentation setup script that I built.


# Make sure that python is setup correctly.
sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip -y

# Install all required packages.
sudo pip install -r deps/requirements.txt

# This is required, so that we avoid confliciton with bson and mongodb packages.
sudo pip uninstall bson
sudo pip uninstall pymongo
sudo pip install pymongo

# python script that just downloads and installs the nltk library.
python3 ./deps/nltk_downloader.py

# All of this projects doccumentation is supported by doxygen.
# We want the user to load in documentation for the project using the
# generate_open_docs.py script that I wrote.
sudo apt-get install doxygen
python3 ./docs/generate_open_docs.py
