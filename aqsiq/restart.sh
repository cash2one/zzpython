export PYTHONTEMP="/var/pythoncode/aqsiq/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /var/pythoncode/aqsiq/manage.py runfcgi host=192.168.110.116 port=8006 --settings=aqsiq.settings
