var wxload=false;
var meta = document.getElementsByTagName('meta');
var share_desc = '';
{%if desc%}share_desc="{{desc}}";{%endif%}
for(i in meta){
	if(typeof meta[i].name!="undefined"&&meta[i].name.toLowerCase()=="description"){
		share_desc = meta[i].content;
	}
}
var shareimg=document.images[0].src;
if (shareimg=="" || !shareimg){
	shareimg='http://img0.zz91.com/zz91/images/minilogo.jpg';
}
{%if pic%}shareimg="{{pic}}";{%endif%}
function sharefunction() {
	wx.onMenuShareAppMessage({
		title: document.title,
		desc: share_desc,
		link: location.href,
		imgUrl:shareimg ,
		trigger: function(res) {
			wxload = true;
		},
		success: function(res) {
			//alert('已分享');
			wxload = true;
			$('#mcover').hide();
		},
		cancel: function(res) {
			//alert('已取消');
		},
		fail: function(res) {
			//alert(JSON.stringify(res));
		}
	});
	wx.onMenuShareTimeline({
		title: document.title,
		desc: share_desc,
		link: location.href,
		imgUrl: shareimg,
		trigger: function(res) {
			//$('#mcover').show();
			wxload = true;
		},
		success: function(res) {
			//alert('已分享');
			$('#mcover').hide();
		},
		cancel: function(res) {
			//alert('已取消');
		},
		fail: function(res) {
			//alert(JSON.stringify(res));
		}
	});
	if(wxload == false) {
		setTimeout("sharefunction()", 2000)
	}
}
function wxconfig(){
	wx.config({
		debug: false,
		appId: '{{appid}}',
		timestamp: '{{timestamp}}',
		nonceStr: '{{nonceStr}}',
		signature: '{{signature}}',
		jsApiList: [
			'checkJsApi',
			'onMenuShareTimeline',
			'onMenuShareAppMessage',
			'hideMenuItems',
		]
	});
}
wxconfig();
sharefunction();
window.onload = sharefunction()
if(wxload == false) {
	setTimeout("sharefunction()", 1000)
}