export PYTHONTEMP="/var/pythoncode/zz91yinyong/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
  #python /var/pythoncode/zz91yinyong/manage.py runfcgi host=192.168.110.120 port=8012 --settings=zz91yinyong.settings
else
  echo "kill pid $pid now"
  kill -9 $pid
  #python /var/pythoncode/zz91yinyong/manage.py runfcgi host=192.168.110.120 port=8012 --settings=zz91yinyong.settings
fi
