#!/bin/bash
echo "Installing python-virtualenv"
echo "----------------------------"
yes | sudo apt install python-virtualenv
if [ -n $1 ]
then
    echo "Starting python virtual environment in $1"
    echo "-----------------------------------------"
    virtualenv $1
    $1/bin/activate
    sudo $1/bin/pip install flask
    sudo $1/bin/pip install wtforms
    sudo $1/bin/pip install passlib
    sudo $1/bin/pip install gunicorn
else
    echo "Starting python virtual environment in grades"
    echo "---------------------------------------------"
    virtualenv grades
    grades/bin/activate
    sudo grades/bin/pip install flask
    sudo grades/bin/pip install wtforms
    sudo grades/bin/pip install passlib
    sudo grades/bin/pip install gunicorn
fi
