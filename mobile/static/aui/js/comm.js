var zzajax = function(method, url, data, successCallback, errorCallback) {
	$.ajax({
		type: method,
		url: url,
		data: data,
		dataType: "json",   //返回格式为json
		traditional: true,
		cache:false, 
		success: function(ret) {
			successCallback && successCallback(ret);
		},
		error: function(err) {
			errorCallback && errorCallback(err);
		}
	});
}
function show_time(endtime) {
	var endtime = endtime.replace(/-/gm, '/');
	var time_end = new Date().getTime();
	//设定当前时间
	var time_start = new Date(endtime).getTime();
	//设定目标时间
	// 计算时间差
	var time_distance = time_end - time_start;
	// 天
	var int_day = Math.floor(time_distance / 86400000)
	//time_distance -= int_day * 86400000;
	// 时
	var int_hour = Math.floor(time_distance / 3600000)
	// 分
	var int_minu = Math.floor(time_distance / 60000)
	if (int_day > 0) {
		str = endtime.split(' ');
		return str[0]
	} else if (int_hour>0) {
		return int_hour + "小时前"
	} else {
		return int_minu + "分钟前"
	}
}

function zzalert(txt){
	
}
function yuebuzuFun(){
	layer.confirm('您的再生钱包余额不足，是否要充值后再开通服务', {
		btn: ['我要充值','取消'] //按钮
	}, function(){
		layer.open({
			type: 2,
			title: '在线充值',
			shadeClose: true,
			shade: 0.4,
			area: ['80%', '70%'],
			content: 'http://m.zz91.com/qianbao/minichongzhi.html' //iframe的url
		}); 
	}, function(){
		layer.closeAll();
	});
}
function mobileyuebuzuFun(){
	layer.confirm('您的再生钱包余额不足，是否要充值后再开通服务', {
		btn: ['我要充值','取消'] //按钮
	}, function(){
		layer.open({
			type: 2,
			title: '在线充值',
			shadeClose: true,
			shade: 0.4,
			area: ['80%', '70%'],
			content: 'http://m.zz91.com/qianbao/minichongzhi.html' //iframe的url
		}); 
	}, function(){
		layer.closeAll();
	});
}
//是否登录
function havelogin(company_id,host){
	if (company_id==0 || !company_id || company_id=="0" || company_id=='' || company_id=='None'){
		window.location='/login/?done='+host;
		return null;
	}else{
		return '1'
	}
}
//收藏
function shoucInfo(data,host) {
	layer.load(2)
	zzajax("get","/myrc/favorite_save.html",data,function(ret){
		if (ret) {
			if (ret.err=='login'){
				window.location="/login/?done="+host;
				return;
			}
			if (ret.err == "true") {
				layer.msg("收藏失败");
			} else {
				layer.msg(ret.errkey);
			}
		} else {
			layer.msg("收藏失败");
		};
		layer.closeAll('loading');
	},function(){
		layer.closeAll('loading');
	});
}
//是否收藏
function isfavor(obj,flag){
	if (flag==1){
		obj.removeClass("aui-icon-favor");
		obj.addClass("aui-icon-favorfill");
	}else{
		obj.removeClass("aui-icon-favorfill");
		obj.addClass("aui-icon-favor");
	}
}
