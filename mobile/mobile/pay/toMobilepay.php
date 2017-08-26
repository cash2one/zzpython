<?php 
include("yeepay/yeepayMPay.php");
include("config.php");
	//echo $_GET['company_id'];
	$yeepay = new yeepayMPay($merchantaccount,$merchantPublicKey,$merchantPrivateKey,$yeepayPublicKey);
	//$order_id = create_str(15);
	$order_id = $_GET["order_id"];

	//网页支付的订单在订单有效期内可以进行多次支付请求，但是需要注意的是每次请求的业务参数都要一致，交易时间也要保持一致。否则会报错“订单与已存在的订单信息不符”
	$transtime = time();//交易时间，是每次支付请求的时间，注意此参数在进行多次支付的时候要保持一致。
	$product_catalog ='7';//商品类编码是我们业管根据商户业务本身的特性进行配置的业务参数。
	$identity_id = create_str(15);
	$identity_id = $_GET["identity_id"];//用户身份标识，是生成绑卡关系的因素之一，在正式环境此值不能固定为一个，要一个用户有唯一对应一个用户标识，以防出现盗刷的风险且一个支付身份标识只能绑定5张银行卡
	$identity_type = 0;     //支付身份标识类型码
 	$user_ip = $_GET["user_ip"];//此参数不是固定的商户服务器ＩＰ，而是用户每次支付时使用的网络终端IP，否则的话会有不友好提示：“检测到您的IP地址发生变化，请注意支付安全”。        
 	$user_ip = GetIP();
 	//$user_ua = 'NokiaN70/3.0544.5.1 Series60/2.8 Profile/MIDP-2.0 Configuration/CLDC-1.1';//用户ua
	$user_ua = $_SERVER['HTTP_USER_AGENT'];
    $callbackurl ='http://m.zz91.com/pay/callback_get.html';//商户后台系统回调地址，前后台的回调结果一样
    $fcallbackurl ='http://m.zz91.com/pay/callback_get.html';//商户前台系统回调地址，前后台的回调结果一样
	$product_name = $_GET['product_name'];//出于风控考虑，请按下面的格式传递值：应用-商品名称，如“诛仙-3 阶成品天琊”
	$product_desc = $_GET['product_desc'];//商品描述
    $terminaltype = 3;
	$terminalid = '05-16-DC-59-C2-34';//其他支付身份信息
	$amount =(int)$_GET['amount'];
	//订单金额单位为分，支付时最低金额为2分，因为测试和生产环境的商户都有手续费（如2%），易宝支付收取手续费如果不满1分钱将按照1分钱收取。
				
	$url = $yeepay->webPay($order_id,$transtime,$amount,$product_catalog,$identity_id,$identity_type,$user_ip,$user_ua,$callbackurl,$fcallbackurl,$currency=156,$product_name,$product_desc,$terminaltype,$terminalid,$orderexp_date=60);

 	$arr = explode("&",$url);
 	$encrypt = explode("=",$arr[1]);
 	$data = explode("=",$arr[2]); 
 		
	echo($url);
	//echo '<script>location.href="'.$url.'"</script>';
	header("location:".$url); 
	exit;
	//var_dump($url);	


function create_str( $length = 8 ) {  
	// 密码字符集，可任意添加你需要的字符  
	$chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';  
	$str = '';  
	for ( $i = 0; $i < $length; $i++ )  
	{  
		// 这里提供两种字符获取方式  
		// 第一种是使用 substr 截取$chars中的任意一位字符；  
		// 第二种是取字符数组 $chars 的任意元素  
		// $password .= substr($chars, mt_rand(0, strlen($chars) – 1), 1);  
		$str .= $chars[ mt_rand(0, strlen($chars) - 1) ];  
	}  
	return $str;  
}
function GetIP(){
	if(!empty($_SERVER["HTTP_CLIENT_IP"])){
	  $cip = $_SERVER["HTTP_CLIENT_IP"];
	}
	elseif(!empty($_SERVER["HTTP_X_FORWARDED_FOR"])){
	  $cip = $_SERVER["HTTP_X_FORWARDED_FOR"];
	}
	elseif(!empty($_SERVER["REMOTE_ADDR"])){
	  $cip = $_SERVER["REMOTE_ADDR"];
	}
	else{
	  $cip = "无法获取！";
	}
	return $cip;
}
?>
