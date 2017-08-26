export PYTHONTEMP="/usr/apps/pythoncode/zz91yang/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /usr/apps/pythoncode/zz91yang/manage.py runfcgi host=192.168.2.21 port=8003 --settings=settings
