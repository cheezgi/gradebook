# gradebook
flask/gunicorn web gradebook

## installation

Run the following commands to install `gradebook`:

```
$ git clone https://github.com/cheezgi/gradebook.git somepath
# somepath/install.sh somepath
```

This program relies on Flask and Gunicorn. To run as a Gunicorn app, run the following:

```
# gunicorn -b 0.0.0.0:80 grades:app
```

To deploy with a different server, you can uncomment the uWSGI related lines in `test.py`
and set up a reverse proxy config for your server that points to localhost:8000,
then run gunicorn without `-b 0.0.0.0:80`.
