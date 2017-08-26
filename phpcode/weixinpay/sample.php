<?php
require_once "jssdk.php";
$jssdk = new JSSDK("wx2891ef70c5a770d6", "d3f9436cfc50cd9e4f62f96893a1ee0c");
$signPackage = $jssdk->GetSignPackage();
$sign= strtoupper(md5("out_trade_no="+$signPackage["timestamp"]+"&partner=1230440002&key=d3f9436cfc50cd9e4f62f96893a1ee0c"));
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title></title>
</head>
<body>
  
</body>
<script src="http://res.wx.qq.com/open/js/jweixin-1.0.0.js"></script>
<button class="btn btn_primary" id="chooseWXPay">chooseWXPay</button>
<script>
  /*
   * 注意：
   * 1. 所有的JS接口只能在公众号绑定的域名下调用，公众号开发者需要先登录微信公众平台进入“公众号设置”的“功能设置”里填写“JS接口安全域名”。
   * 2. 如果发现在 Android 不能分享自定义内容，请到官网下载最新的包覆盖安装，Android 自定义分享接口需升级至 6.0.2.58 版本及以上。
   * 3. 常见问题及完整 JS-SDK 文档地址：http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
   *
   * 开发中遇到问题详见文档“附录5-常见错误及解决办法”解决，如仍未能解决可通过以下渠道反馈：
   * 邮箱地址：weixin-open@qq.com
   * 邮件主题：【微信JS-SDK反馈】具体问题
   * 邮件内容说明：用简明的语言描述问题所在，并交代清楚遇到该问题的场景，可附上截屏图片，微信团队会尽快处理你的反馈。
   */
  wx.config({
    debug: true,
    appId: '<?php echo $signPackage["appId"];?>',
    timestamp: <?php echo $signPackage["timestamp"];?>,
    nonceStr: '<?php echo $signPackage["nonceStr"];?>',
    signature: '<?php echo $signPackage["signature"];?>',
    jsApiList: [
		'checkJsApi',
		'onMenuShareTimeline',
		'onMenuShareAppMessage',
		'onMenuShareQQ',
		'onMenuShareWeibo',
		'hideMenuItems',
		'showMenuItems',
		'hideAllNonBaseMenuItem',
		'showAllNonBaseMenuItem',
		'translateVoice',
		'startRecord',
		'stopRecord',
		'onRecordEnd',
		'playVoice',
		'pauseVoice',
		'stopVoice',
		'uploadVoice',
		'downloadVoice',
		'chooseImage',
		'previewImage',
		'uploadImage',
		'downloadImage',
		'getNetworkType',
		'openLocation',
		'getLocation',
		'hideOptionMenu',
		'showOptionMenu',
		'closeWindow',
		'scanQRCode',
		'chooseWXPay',
		'openProductSpecificView',
		'addCard',
		'chooseCard',
		'openCard'
	  ]
  });
  wx.ready(function () {
    // 在这里调用 API
  });
  wx.ready(function () {
	document.querySelector('#chooseWXPay').onclick = function () {
		// 注意：此 Demo 使用 2.7 版本支付接口实现，建议使用此接口时参考微信支付相关最新文档。
		wx.chooseWXPay({
		  timestamp: <?php echo $signPackage["timestamp"];?>,
		  nonceStr: '<?php echo $signPackage["nonceStr"];?>',
		  package: 'addition=action_id%3dgaby1234%26limit_pay%3d&bank_type=WX&body=aa&fee_type=1&input_charset=GBK&notify_url=http://m.zz91.com/&out_trade_no=<?php echo $signPackage["timestamp"];?>&partner=1230440002&spbill_create_ip=115.236.188.99&total_fee=1&sign=<?php echo $sign;?>',
		  signType: 'MD5', // 注意：新版支付接口使用 MD5 加密
		  paySign: '<?php echo $signPackage["signature"];?>'
		});
	  };
	});
	wx.error(function (res) {
		alert(res.errMsg);
	});
</script>
</html>
