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

function loadcommonurl(url, pageParam) {
	
	var wintitle = pageParam.wintitle;
	var wname = pageParam.wname;
	var showbottom = pageParam.showbottom;
	if (pageParam.bounces == false) {
		var bounces = pageParam.bounces;
	} else {
		var bounces = true;
	}
	if (!wintitle) {
		if (wname != "offer-list_") {
			$(".my-gout").css("display", "block");
		} else {
			$(".shaxuan").css("display", "block");
		}
		if (pageParam.type == "price") {
			$(".my-gout").css("display", "none");
		}
		if (pageParam.type == "company-list") {
			$(".my-gout").css("display", "none");
		}
	} else if (wintitle) {
		$(".select").html(wintitle);
		var module = pageParam.module;
		if (module) {
			//$(".font-wen").text(module);
		}
		$(".font-wen").css("display", "block");
	}
	var oHeight = $(".main").height();
	var oWidth = $(".main").width();
	var topHeight = $("header").height();
	if (pageParam.hiddentop){
		topHeight=topHeight-$(".topbar").height();
		$(".topbar").hide();
	}
	var bottomHeight = $("footer").height();

	var $body = $api.dom('body');
	var header_h = topHeight;
	var body_h = $api.offset($body).h;
	var footer_h = bottomHeight;
	var rect_h;
	if (showbottom && showbottom == 1) {
		$("footer").show();
		var bottomHeight = $("footer").height();
		var footer_h = bottomHeight;
		rect_h = body_h - header_h - footer_h;
	} else {
		$("footer").hide();
		rect_h = 'auto';
	}
	pageParam['topHeight']=topHeight;
	api.openFrame({
		name : wname,
		url : url,
		rect : {
			x : 0,
			y : topHeight,
			w : 'auto',
			h : rect_h
		},
		pageParam : pageParam,
		bounces : bounces,
		bgColor : 'rgb(255,255,255,255)',
		vScrollBarEnabled : true,
		hScrollBarEnabled : true,
		showProgress : true,
		allowEdit:true,
		reload: true,
		slidBackEnabled: true,
	});
	tokeninfo();
	//统计数据
	//
	var tongjidata = {
		company_id : UserInfo.memberID(),
		usertoken : UserInfo.token(),
		appsystem : api.systemType,
		datatype : "json",
		visitoncode : api.appVersion,
		clientid : api.deviceId,
		//url :pageParam
		//url : url + "?" + parseParam(pageParam),
	}
	
	api.ajax({
		url : hosturl + "tongji/t.html",
		method : "get",
		timeout : 30,
		dataType : 'json',
		returnAll : false,
		data : {
			values : tongjidata
		}
	}, function(ret, err) {
		if (err) {
			saveerrlog(err.body);
		}
	});
}