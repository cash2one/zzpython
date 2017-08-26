export PYTHONTEMP="/var/pythoncode/adminasto/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  python /var/pythoncode/adminasto/manage.py runfcgi host=192.168.110.120 port=8003 --settings=settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  python /var/pythoncode/adminasto/manage.py runfcgi host=192.168.110.120 port=8003 --settings=settings
fi