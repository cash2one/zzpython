#!/bin/bash

# Replace these three settings.
PROJDIR="/var/pythoncode/maps_zz91"
PIDFILE="$PROJDIR/maps.pid"
SOCKET="$PROJDIR/maps.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi
exec python manage.py runfcgi method=prefork socket=${SOCKET} pidfile=${PIDFILE}
