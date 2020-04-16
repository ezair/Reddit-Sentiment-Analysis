# Make sure that python is setup correctly.
sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip -y

# Install all required packages.
pip install -r deps/requirements.txt

# This is required, so that we avoid confliciton with bson and mongodb packages.
sudo pip uninstall bson
sudo pip uninstall pymongo
sudo pip install pymongo
