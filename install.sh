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
touch db/attendance.db
touch db/classes.db
touch db/grades.db
touch db/schedules.db
touch db/students.db
touch db/teachers.db
touch db/users.db
bin/python install.py
echo "Gradebook should be correctly set up."
echo "Run gradebook with the following command:"
echo -e "\tsudo bin/gunicorn -b 0.0.0.0:80 grades:app"
