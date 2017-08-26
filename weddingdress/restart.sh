export PYTHONTEMP="/var/www/zzpython/weddingdress/"
pid=`ps -ef|grep "python"|grep "$PYTHONTEMP"|grep -v "grep"|awk '{print $2}'`
if [ "$pid" = "" ] ; then
  echo "no tomcat pid alive"
else
  echo "kill pid $pid now"
  kill -9 $pid
fi
python /var/www/zzpython/weddingdress/manage.py runfcgi host=192.168.2.40 port=8021 --settings=settings
