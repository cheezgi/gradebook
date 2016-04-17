#!/bin/bash
cd ..
dir = $1
if [ -z dir ]
then
    dir = "gradebook"
fi
echo "Installing gradebook in $dir"
virtualenv $dir
cd $dir
bin/pip install flask
bin/pip install gunicorn
bin/pip install passlib
mkdir db
echo "Gradebook should be correctly set up."
echo "Run gradebook with the following command:"
echo -e "\tsudo bin/gunicorn -b 0.0.0.0:80 grades:app"
