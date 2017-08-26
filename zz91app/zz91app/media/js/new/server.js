//微信支付
function wxpaypost(wxdata) {
	amount=wxdata['total_fee']/100
	out_trade_no=wxdata['out_trade_no']
	var wxPay = api.require('wxPay');
	wxPay.config({
		apiKey: 'wx6bb99d2f0581b5b0',
		mchId: '1340905101',
		partnerKey: 'OR3g3vtcNAdvm25ycHKfH5KWrLY9kAvd',
		notifyUrl: 'http://m.zz91.com/zz91payverify_notify.html'
	}, function(ret, err) {
		if (ret.status) {
			//zzalert('配置商户支付参数成功');
			$paySubmitWx();
		} else {
			//zzalert(err.code);
			zzalert("支付异常！请重试或选择其他支付方式。");
			api.hideProgress();
		}
		//api.hideProgress();
	});

	//var wxPay = api.require('wxPay');

	$paySubmitWx = function() {
		wxPay.pay({
			description: '再生钱包充值-微信',
			totalFee: amount * 100,
			tradeNo: out_trade_no,
			spbillCreateIP: '196.168.1.1',
			deviceInfo: api.deviceId,
			detail: '再生钱包充值-微信',
			attach: '',
			feeType: 'CNY',
			
		}, function(ret, err) {
			if (ret.status) {
				var data = {
					out_trade_no: out_trade_no,
					trade_no: out_trade_no,
					trade_status: "TRADE_SUCCESS",
				}
				api.showProgress({
					title: '充值中，请不要关闭窗口！',
					modal: true
				});
				api.ajax({
					url: 'http://m.zz91.com/zz91payverify_notify.html',
					method: "post",
					timeout: 30,
					dataType: 'html',
					returnAll: false,
					data: {
						values: data
					}
				}, function(ret, err) {
					if (pagefrom == "qianbao") {
						api.execScript({
							name: 'burse',
							frameName: 'burse_',
							script: 'ajaxInfo()'
						});
					}
					api.alert({
						title: '提示',
						msg: '支付成功',
						buttons: ['确定']
					});
					//更新生意管家数据
					api.execScript({
						name: 'root',
						script: 'changemyrcindex()'
					});
					api.hideProgress();
					api.closeWin();
				});

			} else {
				//zzalert(err.body);
				if (err.code == "-1") {
					zzalert("系统错误，或接口还未开通!");
				}
				api.hideProgress();
			}
		});
	}
}
//点击举报
function alert_jubaocheck(){
	var chk_value =[];
	var sscheck=0;
	$('input[name="report"]:checked').each(function(){    
		chk_value.push($(this).val());
		sscheck=1;
	});
	if (chk_value && sscheck==1){
		api.execScript({
			name : api.winName,
			frameName : 'frame_0',
			script : "jubaocheck('"+chk_value+"')"
		});
		api.execScript({
			name : api.winName,
			frameName : api.winName+'_',
			script : "jubaocheck('"+chk_value+"')"
		});
	}
	return true;
};
function btnClick(index){
	//支付页面,显示联系方式
	if (wintype=='showcontact'){
		showcontact();
	}
	if (wintype=='topproducts'){
		topproducts();
	}
	if (wintype=='buybook'){
		if (index==1){
    		var b=buybook();
    		if (b==false){
    			return false;
    		}
    	}
	}
	if (wintype=='buyprolistad'){
		if (index==1){
    		var b=buyprolistad();
    		if (b==false){
    			return false;
    		}
    	}
	}
	if (wintype=='buyservice'){
		if (index==1){
    		var b=buyservice();
    		if (b==false){
    			return false;
    		}
    	}
	}
	if (wintype=='buyshuaxin'){
		if (index==1){
    		var b=buyshuaxin();
    		if (b==false){
    			return false;
    		}
    	}
	}
	//举报信息
	if (index==1){
		alert_jubaocheck();
	}
	//alert(wintype)
	if (wintype=='jubao'){
		if (index==1){
    		var b=alert_jubaocheck();
    		if (b==false){
    			return false;
    		}
    	}
	}

    api.sendEvent({
        name: 'auiAlertEvent',
        extra: {buttonIndex:index}
    });
    closeselect();
}
function openWin(name, url, pageParam) {
	var systemType = api.systemType;
	pageParam['url'] = url;
	pageParam['mid'] = UserInfo.memberID();
	pageParam['wname'] = name + "_";
	pageParam['company_id'] = UserInfo.memberID();
	pageParam['usertoken'] = UserInfo.token();
	pageParam['appsystem'] = api.systemType;
	
	if (name && url) {
		api.openWin({
			name : name,
			url : "widget://html/comm/win-blank.html",
			//url : "/html/comm/win-blank.html",
			pageParam : pageParam,
			bounces : false,
			vScrollBarEnabled : false,
			hScrollBarEnabled : false,
			animation : {
				type : "push", //动画类型（详见动画类型常量）
				subType : "from_right", //动画子类型（详见动画子类型常量）
				duration : 300,                //动画过渡时间，默认300毫秒
			},
			showProgress : true,
			allowEdit:true
		});

	}
	api.closeSlidPane();
}
function tokeninfo(){
	var data={
		pwd_hash : UserInfo.password(),
		username : UserInfo.username(),
		clientid : api.deviceId,
	}
	var datainfo={
		company_id : UserInfo.memberID(),
		usertoken : UserInfo.token(),
	}
	var login_sn = UserInfo.has_login();
	if (login_sn){
		zzappajax("post",hosturl+"user/tokeninfo.html",datainfo,function(ret){
			//zzalert(JSON.stringify(ret))
			if (ret.err=="true"){
				//如果token过期，重新获得
				zzappajax("post",hosturl+"user/get_token.html",data,function(ret){
					//zzalert(JSON.stringify(ret))
					if (ret.err=="false"){
						var token=ret.result
						//保存信息到本地
						UserInfo.token(token);
					}else{
						UserInfo.clear();
						//havelogin();
					}
				},function(errret){
					//zzalert(JSON.stringify(errret))
				})
			}
		},'')
	}
}
//打开大广告
function openbigad(){
	api.execScript({
		name : "root",
		script : "shuang11kanjia()"
	});
	//openwindows("noorder",hosturl+"app/html/ad/shuang11.html");
}
//缩小到小广告
function closetosmallad(){
	$(".smallad").remove();
	var hintHtml = '<div class="smallad" style="position:fixed;bottom:80px;right:0px;color:#fff;line-height:16px;font-size:12px;width:60px;height:60px;border-radius:0px;text-align:center;" onclick=openbigad()>' + '<span style="text-align:center;color:#fff;margin-top:5px;"><img src="http://apptest.zz91.com/app/html/ad/shuang11/images/chuxiao.png" style="width:100%" /><span>' + '</div>';
	$("body").append(hintHtml);
}
//if (location.href.indexOf("index-frame.html")>=0){
	//closetosmallad();
//}
//closetosmallad();
if (location.href.indexOf("/html/ye/detail.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/new/ye.detail.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
//alert(location.href)
if (location.href.indexOf("/html/comm/search.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/new/comm.search.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
//供求列表
if (location.href.indexOf("/html/trade/trade-list.html")>=0){
	$(".moretradefloat").css({"left":"50%","right":"auto",'margin-left':'-40px','width':'80px','height':'40px','bottom':'5px','line-height':'40px','font-size':'16px'})
	$(".moretradefloat").on("click",function(){
		$("#mark").fadeIn();
    	$(".moretrade").slideDown()
    })
	$(".moretrade").on("click","span",function(){
		var k=$(this).text();
		keywordssearch(k);
		closemoretrade();
    })
}
//留言回复
if (location.href.indexOf("/html/trade/huifu.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/new/trade.huifu.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
