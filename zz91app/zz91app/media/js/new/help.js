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