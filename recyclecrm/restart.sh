export PYTHONTEMP="/mnt/pythoncode/zz91crm_test/recyclecrm"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  #kill -9 $pid
fi
#python /mnt/pythoncode/zz91crm_test/recyclecrm/manage.py runserver 192.168.2.4:9092 &
#python /mnt/pythoncode/huanbao/manage.py runfcgi host=192.168.2.4 port=8012 --settings=huanbao.settings