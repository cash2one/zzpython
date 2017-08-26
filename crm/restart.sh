export PYTHONTEMP="/usr/apps/pythoncode/crm/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /usr/apps/pythoncode/crm/manage.py runfcgi host=192.168.2.21 port=8000 --settings=settings
