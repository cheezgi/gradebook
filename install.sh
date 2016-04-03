#!/bin/bash
echo "Installing python-virtualenv"
echo "----------------------------"
yes |  apt install python-virtualenv
if [ -n $1 ]
then
    echo "Starting python virtual environment in $1"
    echo "-----------------------------------------"
    virtualenv $1
    $1/bin/activate
    $1/bin/pip install flask
    $1/bin/pip install wtforms
    $1/bin/pip install passlib
    $1/bin/pip install gunicorn
else
    echo "Starting python virtual environment in grades"
    echo "---------------------------------------------"
    virtualenv grades
    grades/bin/activate
    grades/bin/pip install flask
    grades/bin/pip install wtforms
    grades/bin/pip install passlib
    grades/bin/pip install gunicorn
fi
