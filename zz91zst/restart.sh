export PYTHONTEMP="/var/pythoncode/zz91zst/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  python /var/pythoncode/zz91zst/manage.py runfcgi host=192.168.110.120 port=8002 --settings=settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  python /var/pythoncode/zz91zst/manage.py runfcgi host=192.168.110.120 port=8002 --settings=settings
fi
