export PYTHONTEMP="/mnt/pythoncode/bestjoy/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  #kill -9 $pid
fi
#python /mnt/pythoncode/bestjoy/bestjoy/manage.py runfcgi host=192.168.2.4 port=8011 --settings=settings