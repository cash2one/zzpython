export PYTHONTEMP="zz91daohangsite.xml"
pid=`ps -ef|grep "uwsgi"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
sleep 3
uwsgi -x zz91daohangsite.xml
