export PYTHONTEMP="/mnt/pythoncode/zz91crm_test/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi

python /mnt/pythoncode/zz91crm_test/manage.py runserver 192.168.2.4:9090 &
#python /mnt/pythoncode/zz91crm_test/zz91crm/manage.py runfcgi host=192.168.2.4 port=8011 --settings=settings
