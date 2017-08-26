export PYTHONTEMP="/var/pythoncode/huanbaoadmin/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  python /var/pythoncode/huanbaoadmin/manage.py runfcgi host=192.168.110.2 port=8002 --settings=settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  python /var/pythoncode/huanbaoadmin/manage.py runfcgi host=192.168.110.2 port=8002 --settings=settings
fi