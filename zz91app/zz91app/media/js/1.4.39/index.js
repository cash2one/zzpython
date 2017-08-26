function zz91adopen(){
	receviedxg()
}

function rongcloudcontact(){
	var adloadflag = $api.getStorage("adload");
	if (!adloadflag){adloadflag=0}
	if (!adloadflag || adloadflag <= 3) {
		//openwindows("noorder",hosturl+"app/html/ad/feizhizh/gg.html?p=1");
		//$api.setStorage("adload", adloadflag+1);
	}
	openwindows("noorder",hosturl+"app/html/ad/qingliangyixiaH5/gg.html");
//	var data={
//		'ggtype':'hongbao',
//	}
//	zzappajax("get", hosturl + "app/ggopen.html", data, function(ret) {
//		if (ret) {
//			var openflag = ret.openflag;
//			if (openflag==0){
//				openwindows("noorder",hosturl+"app/html/ad/hongbao/gg.html");
//			}
//		}
//	}, function(err) {
//	})
}
//打开红包
function hongbaoopen(){
	var login_sn = UserInfo.has_login();
	if (!login_sn) {
		var pageParam = {
			wintitle : "登录再生网",
			type : "frm-login"
		};
		openWin("frm-login", "../myrc/frm-login.html", pageParam);
		return false;
	} else {
		var memberID=UserInfo.memberID();
		api.execScript({
			name:'root',
			frameName : "noorder",
			script : "openhongbao("+memberID+")"
		});
		//openwindows("noorder",hosturl+"app/html/ad/hongbao/gg.html");
	}
}
//打开购买商务大全
function bookopen(){
	var index=4;
	var pageParam = {
		wintitle : "商务大全",
		type : "serviceshow"+index,
		bounces : false,
	};
	openWin("serviceshow"+index, "../service/show"+index+".html", pageParam);
}
//保存错误日志信息
function saveerrlog(content) {
	//return;
	var data = {
		content : content,
	}
	api.hideProgress();
}
//购买企业建站服务
function opencreatewebsite(){
	if (!havelogin()) {
		return false;
	}
	var data = {
		paytype: '62',
		money: "1500",
		datatype: 'json',
		t: (new Date()).getTime().toString()
	}
	api.confirm({
		title: '提示',
		msg: "确定要购买吗？",
		buttons: ['确定购买', '取消']
	}, function(ret, err) {
		if (ret.buttonIndex == 1) {
			zzappajax("get", hosturl + 'qianbao/qianbaopay.html', data, function(ret) {
				if (ret) {
					if (ret.err == 'false') {
						api.confirm({
							title: '提示',
							msg: "你已经购买成功，我们将尽快与你联系。",
							buttons: ['关闭']
						}, function(ret, err) {
							if (ret) {
								
							} else {}
						});

					}
					if (ret.err == 'true' && ret.blanceflag == '0') {
						api.hideProgress();
						yuebuzuFun();
					}
					if (ret.err == 'true' && ret.blanceflag == '1') {
						zzalert(ret.errtext);
					}
					api.hideProgress();
				} else {
					api.hideProgress();
					if (err) {
						saveerrlog(err.body);
					}
				};
			}, function() {
				api.hideProgress();
			})
		}
	})
}
//购买显示联系方式+供求自动刷新 抢购服务
function openshowcontactandreflush() {
	if (!havelogin()) {
		return false;
	}
	var data = {
		paytype: '48',
		money: "500",
		datatype: 'json',
		t: (new Date()).getTime().toString()
	}
	api.confirm({
		title: '提示',
		msg: "确定要购买吗？",
		buttons: ['确定购买', '取消']
	}, function(ret, err) {
		if (ret.buttonIndex == 1) {
//			api.showProgress({
//				title: '加载中...',
//				modal: false
//			});
			zzappajax("get", hosturl + 'qianbao/qianbaopay.html', data, function(ret) {
				if (ret) {
					if (ret.err == 'false') {
						api.confirm({
							title: '提示',
							msg: ret.errtext,
							buttons: ['关闭', '查看我的服务']
						}, function(ret, err) {
							if (ret) {
								if (ret.buttonIndex == 2) {
									var pageParam = {
										wintitle: "我的服务",
										type: "myservice",
									};
									openWin("myservice", "../service/myservice.html", pageParam);
								} else {
									//api.closeWin();
								}
							} else {}
						});

					}
					if (ret.err == 'true' && ret.blanceflag == '0') {
						api.hideProgress();
						yuebuzuFun();
					}
					if (ret.err == 'true' && ret.blanceflag == '1') {
						zzalert(ret.errtext);
					}
					api.hideProgress();
				} else {
					api.hideProgress();
					if (err) {
						saveerrlog(err.body);
					}
				};
			}, function() {
				api.hideProgress();
			})
		}
	})

}