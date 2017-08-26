export PYTHONTEMP="/var/pythoncode/maps_zz91/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /var/pythoncode/maps_zz91/manage.py runfcgi host=192.168.110.120 port=8002 --settings=settings