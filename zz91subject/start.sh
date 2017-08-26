export PYTHONTEMP="zz91subjectsite.xml"
pid=`ps -ef|grep "uwsgi"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
sleep 2
uwsgi -x zz91subjectsite.xml
