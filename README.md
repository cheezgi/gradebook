# gradebook
flask/gunicorn web gradebook

###TODO

* Add grade insertion tools *(important)*
* Add improved user functionality
  * Sessions
  * Password changing
* Add data analysis tools *(important)*
  * Grade data
  * Transcript data
  * Attendance data

## installation

Run the following commands to install `gradebook`:

```
$ git clone https://github.com/cheezgi/gradebook.git
$ cd gradebook
$ ./install.sh
```

You can install gradebook to whatever directory you want by specifying it
to `git clone ... /your/dir` and `./install.sh /your/dir`.

This program relies on Flask and Gunicorn. To run as a Gunicorn app, run the following:

```
# gunicorn -b 0.0.0.0:80 grades:app
```

To deploy with a different server, you can uncomment the uWSGI related lines in `grades.py`
and set up a reverse proxy config for your server that points to localhost:8000,
then run gunicorn without `-b 0.0.0.0:80`.

Alternatively, run the following commands:

```
apt install python python-virtualenv
git clone https://github.com/cheezgi/gradebook.git somepath
virtualenv somepath
cd somepath
bin/activate
bin/pip install flask passlib gunicorn
deactivate
mkdir db
bin/gunicorn -b 0.0.0.0:80 grades:app
```

Now you can navigate to the server's IP address and make sure it's working.

##setup

Before entering any data into the databases, make sure you do the following:

Log in as an admin and change the password. The default credentials are
`admin` and `password`. Then, under **Create databases** click Create to set up
the new databases.

If you encounter any errors with database setup, try `touch`ing the following database
files:

```
users.db
students.db
teachers.db
gardes.db
classes.db
attendance.db
schedules.db
```

You could also try the following command:

`sudo chmod +rw *.db`

This should fix database problems you may have.
