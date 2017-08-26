export PYTHONTEMP="zz91seowebsite.xml"
pid=`ps -ef|grep "uwsgi"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
#python /var/pythoncode/zz91seoweb/manage.py runfcgi host=192.168.110.112 port=8009 --settings=zz91seoweb.settings
