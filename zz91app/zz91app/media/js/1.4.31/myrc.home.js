function ajaxInfo(){
	var login_sn = UserInfo.has_login();
	
	if (login_sn){
		
		$(".havelogin").show();
		$(".nologin").hide();
		var data={
			company_id : UserInfo.memberID(),
			usertoken : UserInfo.token(),
			appsystem : api.systemType,
			clientid : api.deviceId,
			datatype : "json",
		}
		//alert(UserInfo.token())
		api.ajax({
			url : hosturl +"myrc_index/",
			method : "get",
			timeout : 30,
			dataType : 'json',
			returnAll : false,
			data : {
				values : data
			}
		}, function(ret, err) {
			if (ret){
				if (ret.hasOwnProperty("tokenerr")){
					n=n+1;
					if (n>=5){
						relogin()
					}else{
						if (ret.tokenerr=='true'){
							tokeninfo();
							ajaxInfo()
						}
					}
					return;
				}
				if (ret.err=="true"){
					zzalert(ret.errkey);
					relogin();
					return;
				}
				//未完善公司信息提示完善
				if (ret.completeflag){
					if (ret.completeflag.showflag==1){
						$(".completediv").show();
						$(".zxinfo").css("margin-top","1px");
						$(".showtext").html(ret.completeflag.text);
						$(".nowanshan").show();
					}else{
						$(".completediv").hide();
						$(".zxinfo").css("margin-top","-15px");
						$(".nowanshan").hide();
					}
				}
				//是否企业秀
				if (ret.isqiyexiu){
					$(".qiyexiu").show();
				}else{
					$(".qiyexiu").hide();
				}
				companyname=ret.companyname;
				//诚信认证
				if (!ret.zxinfo){
					$(".zxinfo").show();
					$(".norenzheng").show();
				}else{
					$(".zxinfo").hide();
					$(".norenzheng").show();
					if (ret.zxinfo=='0'){
						$(".norenzheng").html("未审核")
					}
					if (ret.zxinfo=='2'){
						$(".norenzheng").html("审核未通过")
					}
					if (ret.zxinfo=='1'){
						$(".norenzheng").hide();
					}
				}
				if(ret.ldbvalue){
					//设置来电宝客户类型
					$api.setStorage("ldbvalue", 1);
					$(".ldbmain").show();
					$(".ldbnav").show();
					$(".qiandaomain").hide();
					$(".nomalnav").hide();
					$(".my-name").html("您好，" + ret.contact + "！")
					$(".blance").text(ret.blance);
					$(".ldbtel").text("您的来电宝电话："+ret.ldbvalue.front_tel)
					$(".ldbjtl").text(ret.ldbjtl);
					mobilevalue=ret.mobile;
					var faceurl=ret.faceurl;
					showfacehtml(faceurl)
				}else{
					$api.setStorage("ldbvalue", 0);
					$(".ldbmain").hide();
					$(".ldbnav").hide();
					$(".qiandaomain").show();
					$(".nomalnav").show();
					$(".my-name").html("您好，" + ret.contact + "！")
					$(".blance").text(ret.blance);
					mobilevalue=ret.mobile;
					var faceurl=ret.faceurl;
					showfacehtml(faceurl)
					//我的留言提示数字
					if (ret.qcount==0){
						$(".questioncount").hide();
					}else{
						$(".questioncount").show();
						$(".questioncount").text(ret.qcount);
					}
					//签到
					if (ret.qiandao){
						$(".haveqiandao").show();
						$(".qiandaobtn").hide();
					}else{
						$(".haveqiandao").hide();
						$(".qiandaobtn").show();
					}
				}
				//商务助理
				if (ret.cslist){
					$(".csname").html(ret.cslist.name);
					$(".cstel").html("<a href='tel:"+ret.cslist.tel+"'>"+ret.cslist.tel+"</a>");
					$(".cszhuli").show();
				}
				if (ret.tokenerr=='true'){
					tokeninfo();
					ajaxInfo()
				}
				
			}else{
				if (n<=20){
					ajaxInfo();
					n=n+1
				}else{
					relogin()
					return;
				}
				if(err){
					saveerrlog(err.body);
				}
			}
			$("#loading").hide();
			//zzalert(JSON.stringify(ret))
		});
	}else{
		relogin();
	}
}
//重新显示登陆
function relogin(){
	$(".havelogin").hide();
	$(".nologin").show();
	$("#loading").hide();
	$(".qiandaomain").hide();
	showfacehtml();
}
ajaxInfo()
