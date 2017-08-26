export PYTHONTEMP="/var/pythoncode/zz91cp/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /var/pythoncode/zz91cp/manage.py runfcgi host=192.168.110.112 port=8008 --settings=zz91cp.settings