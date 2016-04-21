if [ -z "$(pgrep gunicorn)" ]; then
    echo "Starting gunicorn"
    sudo bin/gunicorn --bind 0.0.0.0:80 grades:app 2> logs/log.txt &
else
    if [ "$1" == "stop" ]; then
        echo "Killing gunicorn"
        sudo pkill gunicorn
    elif [ "$1" == "restart" ]; then
        echo "Restarting gunicorn"
        sudo pkill gunicorn
        sudo bin/gunicorn --bind 0.0.0.0:80 grades:app 2> logs/log.txt &
    else
        echo "Already running"
    fi
fi
echo "Done"
