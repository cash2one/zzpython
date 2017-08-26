export PYTHONTEMP="mobile.settings"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  #python manage.py runfcgi host=127.0.0.1 port=8014 --settings=mobile.settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  #python manage.py runfcgi host=127.0.0.1 port=8014 --settings=mobile.settings
fi
