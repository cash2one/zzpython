export PYTHONTEMP="/var/pythoncode/zz91app/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  python /var/pythoncode/zz91app/manage.py runfcgi host=192.168.110.150 port=8006 --settings=zz91app.settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  python /var/pythoncode/zz91app/manage.py runfcgi host=192.168.110.150 port=8006 --settings=zz91app.settings
fi
