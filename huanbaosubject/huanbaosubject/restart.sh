export PYTHONTEMP="/var/pythoncode/subject/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
  python /var/pythoncode/subject/manage.py runfcgi host=192.168.110.2 port=8001 --settings=settings
fi