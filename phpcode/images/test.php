<?php
function curl($url){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_REFERER, 'http://www.weather.com.cn/forecast/index.shtml');//必须滴
	curl_setopt($ch, CURLOPT_COOKIE,'isexist=1');//最好带上 比较稳定
	curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0');
	curl_setopt($ch, CURLOPT_HEADER, 0);
	$data = curl_exec($ch);
	curl_close($ch);
	return $data;
}
$city = '杭州';
$url = 'http://toy1.weather.com.cn/search?cityname='.urlencode($city).'&callback=jsonp'.time().mt_rand(100, 999).'&_='.time().mt_rand(100, 999);
$result = explode('~', substr(strtolower(curl($url)), 28, -4));
#echo curl($url);
var_export($result);//http://my.oschina.net/cart/
exit();
?>