$(function(){
	$("body").on("click",".quanlink",function(){
		var url = $(this).attr("url");
		//资讯
		if (url.indexOf("m.zz91.com/news/newsdetail") >= 0) {
			url = url.replace("http://m.zz91.com/news/newsdetail", "")
			url = url.replace(".htm", "")
			infoid = url;
			var pageParam = {
				wintitle: "资讯详情",
				type: "detail",
				bounces: false,
				infoid: infoid
			};
			openWin("detail" + infoid.toString(), "../news/detail.html", pageParam);
		}
		//供求
		if (url.indexOf("m.zz91.com/detail/") >= 0) {
			url = url.replace("http://m.zz91.com/detail/?id=", "")
			//url = url.replace(".html", "")
			id = url;
			var pageParam = {
				wintitle: "供求详情",
				type: "infomation-heart",
				id: id,
				nav_list: [{
					"typename": "供求详情",
					"id": 1
				}, {
					"typename": "公司简介",
					"id": 2
				}], //头部划动标题
				frame_url: ["../trade/firm-detail.html", "../trade/firm.html"], //打开frame组的页面集合
				topnumber: 2,
				bounces: false
			};
			openWin("infomation-heart", "infomation-heart.html", pageParam);
		}
		//报价
		if (url.indexOf("m.zz91.com/jiage/detail") >= 0) {
			url = url.replace("http://m.zz91.com/jiage/detail", "")
			url = url.replace(".html", "")
			id = url;
			var pageParam = {
				wintitle: "报价详情",
				type: "price-detail",
				id: id
			};
			openWin("price-detail" + id, "../price/price-detail.html", pageParam);
		}
		//公司
		
		if (url.indexOf("mobile.m.zz91.com/mobile/index") >= 0) {
			url = url.replace("http://mobile.m.zz91.com/mobile/index", "")
			url = url.replace(".htm", "")
			id = url;
            var pageParam = {
                wintitle:"公司详情",
                type:"companyshop",
                showbottom : 1,
				forcompany_id : id,
                bounces:false
            };
            openWin("companyshop", "../company/shop.html", pageParam);
		}
		//资讯
		if (url.indexOf("m.zz91.com/huzhu/") >= 0) {
			url = url.replace("http://m.zz91.com/huzhu/", "")
			url = url.replace(".html", "")
			infoid = url;
			var pageParam = {
				wintitle : "互助详情",
				type : "double-heart"+infoid,
				bounces : false, //窗口弹动
				infoid : infoid
			};
			openWin("cunity-detail"+infoid, "../huzhu/cunity-detail.html", pageParam);
		}

	});
	function ioserrtradedetail(){
		if ($(".aui-toast").find(".firm-img").attr("style")){
			//alert($(".aui-toast").find(".firm-img").attr("style"))
			return;
		}
		//setTimeout("ioserrtradedetail()", 1000);
	}
	if (location.href.indexOf("/html/trade/firm-detail.html")>=0){
		//ioserrtradedetail()
		window.onload=function(){
			//alert()
			//$(".firm-img").css("display","none");
		}
	}
	if (location.href.indexOf("/html/huzhu/cunity-detail.html")>=0){
		ioserrhuzhu()
	}
	function ioserrhuzhu(){
		if (!api){return;}
		if (api.appVersion!='1.4.1'){
			return;
		}
		var id=api.pageParam.infoid;
		var data = {
			company_id : UserInfo.memberID(),
			usertoken : UserInfo.token(),
			appsystem : api.systemType,
			datatype : "json",
		}
		zzappajax("get",hosturl+"/huzhuview/"+id+".htm",data,function(ret){
			$(".b_pinlun").attr("company_id",ret.company_id);
			$(".ask-nickname").attr("company_id",ret.company_id);
			//alert($(".quanlink").attr("url"))
			$(".quanlink").click(function(){
				var url = $(".quanlink").attr("url");
				//alert(url)
			})

			var infoid=id
			//保存分享数据到本地
			var title = ret.title;
			localStorage.setItem("share_title", "" + title);
			localStorage.setItem("share_description", "我正在查看" + title + "，赶紧跟我一起来体验！http://m.zz91.com/huzhu/" + infoid.toString() + ".html 点击链接查看");
			localStorage.setItem("share_url", "http://m.zz91.com/huzhu/" + infoid.toString() + ".html");
			localStorage.setItem("share_pic", "http://img0.zz91.com/zz91/images/indexLogo.png");
			//点击收藏
		},'')
		var html='<div class="mark" id="mark"></div>'
		html+='<div class="mainbody"></div>'
		html+='<footer class="aui-nav" id="aui-footer">'
		html+=	'<ul class="czfoot">'
		html+=		'<li class="b_dianzhan" postid="'+id+'">'
		html+=			'<span class="aui-iconfont aui-icon-appreciatefill dianzhan" style="font-size:20px"></span> 点赞(<span class="zhanmun">0</span>)'
		html+=		'</li>'
		html+=		'<li class="b_guanzhu">'
		html+=			'<span class="aui-iconfont aui-icon-focus"></span> 关注'
		html+=		'</li>'
		html+=		'<li class="b_pinlun" company_id="0">'
		html+=			'<span class="aui-iconfont aui-icon-comment"></span> 回复'
		html+=		'</li>'
		html+=		'<li class="ask-nickname" company_id="0">'
		html+=			'<span class="aui-iconfont aui-icon-phone"></span> 联系他'
		html+=		'</li>'
		html+=	'</ul>'
		html+='</footer>'
		$("body").append(html);
	}
	
});
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