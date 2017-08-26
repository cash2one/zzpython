export PYTHONTEMP="/var/pythoncode/zz91about/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  python /var/pythoncode/zz91about/manage.py runfcgi host=192.168.110.116 port=8002 --settings=zz91about.settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  python /var/pythoncode/zz91about/manage.py runfcgi host=192.168.110.116 port=8002 --settings=zz91about.settings
fi
