#!/bin/bash
cd ..
direct=$1
if [ -z $direct ]
then
    direct="gradebook"
fi
echo "Installing gradebook in $direct"
virtualenv $direct
cd $direct
bin/pip install flask
bin/pip install gunicorn
bin/pip install passlib
mkdir db
echo "Gradebook should be correctly set up."
echo "Run gradebook with the following command:"
echo -e "\tsudo bin/gunicorn -b 0.0.0.0:80 grades:app"
