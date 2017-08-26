//商机定制
function orderclick(id){
		var obj=$("#orderm"+id);
		var str=obj.find(".item-div-icon").css("display");
		if(str==="none"){
			obj.removeClass("item-div-style");
			obj.addClass("item-div-click");
			obj.find(".item-div-icon").css("display","block");
			obj.find(".item_div_i").attr("checked",'true');
		}else{
			obj.removeClass("item-div-click");
			obj.addClass("item-div-style");
			obj.find(".item-div-icon").css("display","none");
			obj.find(".item_div_i").removeAttr("checked");
		}
		submitfrm(document.getElementById("formorder"),"http://app.zz91.com/order/save_collect.html")
		//$("#formorder").submit();
		
}

//加载新数据
function loaddata(url) {
	if (window.plus) {
		var nWaiting = plus.nativeUI.showWaiting();
	}
	mui.get("" + url, function(data) {
		document.getElementById("dcontent").innerHTML = data;
		mui.init();
		if (nWaiting) {
			nWaiting.close();
		}
		mui.scrollTo(0,10);
	}, function() {
		document.getElementById("dcontent").innerHTML = "<br /><br /><center>该信息不存在！</center>";
	});
	nowherf=url;
}
//打开新窗口
function gotourl(url, wintype) {
	url = url.replace("&", "[and]").replace("?", "wenhao")
	if (wintype == "blank") {
		mui.openWindow({
			id: url,
			url: "/blank.html?url2=" + url + "&wintype=" + wintype + "&company_id=" + company_id.toString(),
			preload: false //TODO 等show，hide事件，动画都完成后放开预加载
		});
	}
}
//翻页
var page = 2;
function loadmorep(obj, url) {
	if (url.indexOf("?") < 0) {
		url = url + "?page=" + page.toString() + "&t=" + Math.ceil(new Date / 3600000);
	} else {
		url = url + "&page=" + page.toString() + "&t=" + Math.ceil(new Date / 3600000);
	}
	obj.style.display = "";
	obj.innerHTML = "正在加载中...";

	if (url != "" && url != null) {
		mui.get("http://app.zz91.com/" + url, function(data) {
			if (data != "") {
				var newNode = document.createElement("div");
				newNode.innerHTML = data;
				obj.parentNode.insertBefore(newNode, obj);
				if (obj) {
					page += 1;
					obj.innerHTML = "<span class='mui-icon mui-icon-down'></span><span>点此加载更多</span>";
				}
				mui.init();
			} else {
				obj.style.display = "none";
			}
		});
	}
}
//互助回复
function huzhureplay(replayid, tocompany_id) {
	var bbs_post_reply_id = document.getElementById("bbs_post_reply_id");
	if (bbs_post_reply_id) {
		document.getElementById("bbs_post_reply_id").value = replayid;
		document.getElementById("tocompany_id").value = tocompany_id;
		openoverlay('', '回复', 0, 180, '.d-reply');
	}
}