//显示，修改头像
function showfacehtml(faceurl){
	if (faceurl){
		var facehtml="<img src='"+faceurl+"'>";
	}else{
		var facehtml="<img src='../../image/noavatar.gif'>"
	}
	$("#faceurl").html(facehtml)
	//getchoujiangnum()
}
function getchoujiangnum(){
	var ajaxurl="http://pyapp.zz91.com/choujiangcount.html?company_id="+UserInfo.memberID()+"&p"+(new Date()).getTime().toString();
	$.getScript(ajaxurl, function() {
		var ccount=_suggest_result_.count;
		if (parseInt(ccount)>0){
			api.confirm({
				title : '2016端午大抽奖',
				msg : '恭喜您在“2016端午抽奖”活动中获得'+ccount+'次抽奖机会，赶紧去试试运气吧？',
				buttons : ['取消', '立即抽奖']
			}, function(ret, err) {
				if (ret) {
					if (ret.buttonIndex == 2) {
						var pageParam = {
							wintitle : "2016端午抽奖",
							type : "2016daunwu",
							bounces : false
						};
						openWin("2016daunwu", "http://m.zz91.com/choujiang/index.html", pageParam);
					}
				} else {
					
				}
			});
		}
	});
}
function tokeninfo(){
	var data={
		pwd_hash : UserInfo.password(),
		username : UserInfo.username(),
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