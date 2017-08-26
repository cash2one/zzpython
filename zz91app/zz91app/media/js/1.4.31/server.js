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
//打开大广告
function openbigad(){
	api.execScript({
		name : "root",
		script : "shuang11show()"
	});
	//openwindows("noorder",hosturl+"app/html/ad/shuang11.html");
}
//缩小到小广告
function closetosmallad(){
	$(".smallad").remove();
	var hintHtml = '<div class="smallad" style="position:fixed;bottom:80px;right:0px;color:#fff;line-height:16px;font-size:12px;width:60px;height:60px;border-radius:0px;text-align:center;" onclick=openbigad()>' + '<span style="text-align:center;color:#fff;margin-top:5px;"><img src="http://apptest.zz91.com/app/html/ad/shuang11/images/chuxiao.png" style="width:100%" /><span>' + '</div>';
	$("body").append(hintHtml);
}
//closetosmallad();
//搜索
if (location.href.indexOf("/html/comm/search.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/1.4.31/comm.search.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
if (location.href.indexOf("/html/comm/search_body.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/1.4.31/comm.search_body.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
if (location.href.indexOf("/html/service/show2.html")>=0 || location.href.indexOf("/html/service/show3_1.html")>=0 || location.href.indexOf("/html/service/show5_1.html")>=0 || location.href.indexOf("/html/service/show7_1.html")>=0 || location.href.indexOf("/html/service/show12.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/1.4.31/service.show2.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
if (location.href.indexOf("/html/price/price.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/1.4.31/price.price.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
if (location.href.indexOf("/html/myrc/my-home.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/1.4.31/myrc.home.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}
apiready = function() {
	oldappupdateverson();
}
