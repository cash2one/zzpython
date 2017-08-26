export PYTHONTEMP="bestjoysite.xml"
pid=`ps -ef|grep "uwsgi"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
sleep 1
uwsgi -x bestjoysite.xml
