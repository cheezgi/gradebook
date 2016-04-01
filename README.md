# gradebook
flask/gunicorn web gradebook

## installation

Run the following commands to install `gradebook`:

```
$ sudo apt install python python-virtualenv
$ git clone https://github.com/cheezgi/gradebook.git somepath
$ cd somepath/..
$ virtualenv somepath
$ cd somepath
$ bin/activate
(somepath)$ bin/pip install flask gunicorn
(somepath)$ deactivate
$ sudo bin/gunicorn -b 0.0.0.0:80 test:app
```

Your grade server is now up and running. To deploy, run `bin/gunicorn` without the
IP address directory, and set up your web server to proxy to gunicorn on port 8000.
Supposedly it is fine to run gunicorn for production, but I haven't done any stress
testing yet.
