export PYTHONTEMP="/var/pythoncode/zz91otherweb/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /var/pythoncode/zz91otherweb/manage.py runfcgi host=192.168.110.150 port=8015 --settings=zz91otherweb.settings
