function compareVersion(ov, nv) {
	if (!ov || !nv || ov == "" || nv == "") {
		return false;
	}
	var b = false, ova = ov.split(".", 4), nva = nv.split(".", 4);
	for (var i = 0; i < ova.length && i < nva.length; i++) {
		var so = ova[i], no = parseInt(so), sn = nva[i], nn = parseInt(sn);
		if (nn > no || sn.length > so.length) {
			return true;
		} else if (nn < no) {
			return false;
		}
	}
	if (nva.length > ova.length && 0 == nv.indexOf(ov)) {
		return true;
	}
}
function openApp() {
    api.openApp({
        androidPkg : 'android.intent.action.VIEW',
        mimeType : 'text/html',
        uri : 'http://app.zz91.com/app/zz91.apk'
    }, function(ret, err) {
        var msg = JSON.stringify(ret);
        api.alert({
            title : '确定版本更新',
            msg : '',
            buttons : ['确定']
        });
    });
}
function oldappupdateverson(){
	if (api.systemType == "android"){
		var updateflag = compareVersion(api.appVersion, '1.4.52');
		if (updateflag){
			api.confirm({
				title : '软件更新',
				msg : '你当前的版本太低了，建议你更新最新版本',
				buttons : ['立即更新','取消'],
				
			}, function(ret, err) {
				if (ret.buttonIndex == 1) {
					openApp()
				}
			});
		}
	}
}
function zz91adopen(){
	receviedxg()
}
function rongcloudcontact(){
	var adloadflag = $api.getStorage("adload");
	if (!adloadflag){adloadflag=0}
	if (!adloadflag || adloadflag <= 2) {
		openwindows("noorder",hosturl+"app/html/ad/feizhizh/gg.html");
	} else {
		
	}
	$api.setStorage("adload", adloadflag+1);
	oldappupdateverson()
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
//打开服务升级
function openserviceupdate() {
	var infoid = 698094;
	var pageParam = {
		wintitle : "互助详情",
		type : "double-heart",
		bounces : false, //窗口弹动
		infoid : infoid
	};
	openWin("cunity-detail", "../huzhu/cunity-detail.html", pageParam);
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