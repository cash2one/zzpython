var defaultqueryString={};
mui.plusReady(function() {
	var info = plus.push.getClientInfo();
	if (info.token) {
		clientid = info.token;
	} else {
		if (info.clientid) {
			clientid = info.clientid;
		}
	}
	var userimei = plus.device.imei;
	appsystem=plus.os.name;
	visitoncode=plus.runtime.version;
	//默认参数
	defaultqueryString={
		company_id:company_id,
		clientid:clientid,
		appsystem:appsystem,
		t:Math.ceil(new Date/3600000)
	}
	//弹出外网url
	if (url){
		if (url.indexOf("blank.html") > 0){
			//alert(url)
			openwebad("http://www.zz91.com/zt/voidhtml5/index.html");
			closewindow();
	//		window.scrollTo(0, 0);
	//		if (window.plus) {
	//			nWaiting = plus.nativeUI.showWaiting("数据加载中，请稍候......");
	//		}
	//		ws = plus.webview.currentWebview();
	//		var weburl = "http://m.zz91.com/2016zadanplay/index.html";
	//		embed = plus.webview.create(weburl, "embed", {
	//			top: "45px",
	//			bottom: "0px"
	//		});
	//		ws.append(embed);
	//		embed.loadURL(weburl);
	//		if (nWaiting) {
	//			nWaiting.close();
	//		}
		}
	}
	
});
//form 提交
function getFormQueryString(frmID) {
	//var frmID = document.getElementById(frmID);
	var arg = defaultqueryString;
	var i, queryString = "",
		and = "";
	var item; // for each form's object
	var itemValue; // store each form object's value

	for (i = 0; i < frmID.length; i++) {
		item = frmID[i]; // get form's each object
		if (item.name != '') {
			if (item.type == 'select-one') {
				itemValue = item.options[item.selectedIndex].value;
			} else if (item.type == 'checkbox' || item.type == 'radio') {
				if (item.checked == false) {
					continue;
				}
				itemValue = item.value;
			} else if (item.type == 'button' || item.type == 'submit' || item.type == 'reset' || item.type == 'image') { // ignore this type
				continue;
			} else {
				itemValue = item.value;
			}
			itemValue = encodeURIComponent(itemValue);
			arg[item.name]=itemValue
			//queryString += and + item.name + '=' + itemValue;
			//and = "&";
		}
	}
	return arg;
}
//修改密码
function modpasswd(frm) {
	var oldCold = frm.oldcold.value;
	var newCold = frm.newcold.value;
	var sedCold = frm.sedcold.value;
	if (!oldCold) {
		alert("原密码不能为空");
		frm.oldcold.focus();
		return;
	}
	if (!newCold) {
		alert("新密码不能为空");
		frm.newcold.focus();
		return;
	}
	if (!sedCold) {
		alert("重复密码不能为空");
		frm.sedcold.focus();
		return;
	}
	if (oldCold == newCold) {
		//document.getElementById('newcold').parentNode.getElementsByTagName('p')[0].style.visibility = "visible"
		alert("新密码不能和老密码相同！");
		return;
	}
	if (sedCold != newCold) {
		//document.getElementById('sedcold').parentNode.getElementsByTagName('p')[0].style.visibility = "visible"
		alert("重复密码输入错误！");
		return;
	}
	var nWaiting;
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("数据加载中，请稍候......");
	}
	var arg = getFormQueryString(frm);
	mui.ajax(zzweburl + "/modpasswdsave.html", {
		data: arg,
		dataType: 'json', //服务器返回json格式数据
		type: 'get', //HTTP请求类型
		success: function(data) {
			var ret = data;
			if (ret.error_code == 0) {
				if (nWaiting) {
					nWaiting.close();
				}
				plus.ui.alert("修改成功！")
				closewindow();
			} else {
				mui.toast('您输入的旧密码有错误，请重新输入！');
			}
			if (nWaiting) {
				nWaiting.close();
			}
			return false;
		},
		error: function(xhr, type, errorThrown) {
			//异常处理；
			mui.toast('网络错误,请检查网络是否正常！');
			if (nWaiting) {
				nWaiting.close();
			}
		}
	});
	return false;
}
//每日抢购
function open_qg(money) {
	var qianbaoblance = $('#qianbaoblance').val();
	var paytype = $('#paytype').val();
	if (paytype=="30"){
		payopen("guoqin100");
		return;
	}
	if (parseInt(qianbaoblance) >= money) {
		if (paytype == "20") {
			openfloatdiv(event, 'huangye');
		}
		if (paytype == "21") {
			openfloatdiv(event, 'chk1');
		}
	} else {
		if (paytype == "21") {
			openfloatdiv(event, 'chk1');
		}else{
			openfloatdiv(event, 'bal');
		}
	}
	return false;
}
function openwebad(weburl) {
	plus.runtime.openURL(weburl);
}
mui.plusReady(function () {
	if(plus.networkinfo.getCurrentType() == plus.networkinfo.CONNECTION_NONE){
		mui.toast("当前网络不给力，无法加载广告");
	}else{
		
		//屏幕真实宽度
		var width = window.innerWidth;
		var height = window.innerHeight;
		//根据投放广告的比例，计算广告高度
		var adHeight = parseInt(width)*3/20;
		//广告投放域名地址
		var ltu = encodeURIComponent('http://subject.huanbao.com/baidu/ad1.html');
		//投放广告的服务端页面标题
		var title = encodeURIComponent('ZZ91再生网');
		var url = "http://pos.baidu.com/acom?adn=1&at=97&aurl=&cad=1&ccd=24&cec=UTF-8&cfv=18&ch=0&col=zh-CN&conOP=0&cpa=1&dai=1&dis=0&ltr=&lunum=6&n=90027019_cpr&pis=10000x10000&ps=0x0&qn=b16741b193c4549f&rad=&rsi5=4&rss0=&rss1=&rss2=&rss3=&rss4=&rss5=&rss6=&rss7=&scale=20.5&skin=mobile_skin_white_red&td_id=2340825&tn=template_inlay_all_mobile&tpr=1444143680033&ts=1&xuanting=0&tt=1444143680015.20.305.311&dtm=BAIDU_DUP2_SETJSONADSLOT&dc=2&wt=1&distp=1001"
		//var url = 'http://pos.baidu.com/acom?adn=1&at=97&aurl=&cad=1&ccd=24&cec=UTF-8&cfv=18&ch=0&col=en-US&conOP=0&cpa=1&dai=1&dis=0&ltr=&lunum=6&n=99099160_cpr&pis=10000x10000&ps=0x0&qn=31f2f2a7de233256&rad=&rsi5=4&rss0=&rss1=&rss2=&rss3=&rss4=&rss5=&rss6=&rss7=&scale=20.3&skin=mobile_skin_white_blue&td_id=2340825&tn=template_inlay_all_mobile&tpr=1436841400149&ts=1&xuanting=0&tt=1436841400136.14.87.89&dtm=BAIDU_DUP2_SETJSONADSLOT&dc=2&wt=1&distp=1001';
		url += '&conW='+width+'&conH='+adHeight+'&ltu='+ltu;
		url += '&di=u2340825';//广告id
		url += '&pcs='+width+'x'+height;
		url += '&psr='+width+'x'+height;
		url += '&pss='+width+'x0';
		url += '&rsi0='+width+'&rsi1='+adHeight;
		url += '&ti='+title;
		
		
		var adBottom = mui.os.ios?('-'+adHeight+'px'):'50';
		
		//var ad = plus.webview.create(url,'ad',{height:adHeight+'px',bottom:adBottom});
		//目前Android平台不支持子webview的setStyle动画，因此分平台处理；
		if(mui.os.ios){
			//为了支持iOS平台左侧边缘滑动关闭页面，需要append进去；
//			plus.webview.currentWebview().append(ad);
//			ad.addEventListener('loaded',function () {
//				ad.setStyle({
//					bottom:'50',
//					transition: {
//						duration: 150
//					}
//				});
//			});
		}else{
//			ad.addEventListener('loaded',function () {
//				//ad.show('slide-in-bottom');
//			});
		}
		
		//ad.appendJsFile('_www/js/ad.js');
		
		//设置主页面的底部留白，否则会被遮住；
		//document.querySelector('.mui-content').style.paddingBottom = adHeight + 'px';
	}
});
function regfunction(frm) {
	var checkflag = 0;
	var checklist = ""
	var arg = "";
	if (window.plus) {
		var nWaiting = plus.nativeUI.showWaiting();
	}
	for (var i = 0; i < frm.length; i++) {
		var objinput = frm[i];
		var objtype = objinput.type;
		var objvalue = objinput.value;
		var objname = objinput.name;
		if (objname != "") {
			if (objinput.type == "radio" || objinput.type == "checkbox") {
				if (objinput.checked == true) {
					if (checklist.indexOf(objname) < 0) {
						checkflag = 0;
					}
					if (checkflag == 1) {
						checklist += "," + objvalue;
					} else {
						checklist += "&" + objname + "=" + objvalue;
					}
				}
				checkflag = 1;
			} else {
				checkflag = 0;
				arg += "&" + objname + "=" + objvalue;
			}
		}



		if (objinput.title != "" && objinput.title) {
			if (objinput.title.substring(0, 1) == "*") {
				if (objinput.value == "") {

					plus.ui.alert(objinput.title.substring(1));
					objinput.focus();
					if (nWaiting) {
						nWaiting.close();
					}
					return false
				}
			}
		}

	}
	mui.post(zzweburl+"/regsave.html", arg, function(data) {
		
		if (!isJson(data)){
			var j = JSON.parse(data);
		}else{
			var j=data;
		}
		var err = j.err;
		
		var errkey = j.errkey;
		if (nWaiting) {
			nWaiting.close();
		}
		if (err == "true") {
			if (j.type == "regerr") {
				var errflag = j.errflag;
				var errname = j.errname;
				$(".c-red").html("");
				$("#regerr" + errflag).html(errkey);
				document.getElementById(errname).focus();
			} else {
				if (j.type == "forgetpasswd") {
					$(".c-red").html(errkey);
				} else {
					plus.ui.alert(errkey);
				}
			}
		} else {
			if (j.type) {
				if (j.type == "regsuc") {
					plus.ui.alert('注册成功！');
					company_id = j.company_id;
					if (window.plus) {

						var wobj = plus.webview.currentWebview();
						if (wobj) {
							var opener = wobj.opener();
							if (opener) {
								opener.evalJS('loadappbody();');
							}
							var parent = wobj.parent();
							if (parent) { //又得evalJS
								parent.evalJS('loadappbody();');
							}
						}
						closewindow();
					}
				}
			} else {

			}
		}
		if (nWaiting) {
			nWaiting.close();
		}
	}, function() {
		if (nWaiting) {
			nWaiting.close();
		}
	});
}
shareHide();
//下载新的app
function downloadnewapp() {
	plus.runtime.launchApplication({
		pname: "com.zz91.app2",
		extra: {
			url: "http://www.zz91.com"
		}
	}, function(e) {
		$("#mainbody").html("<div class=midload>ZZ91再生网app已全新改版</div>");
		$(".mui-bar").css("display","none");
		plus.ui.confirm("ZZ91再生网app已全新改版，请更新最新版-。", function(i) {
			if (0 == i.index) {
				var appUrl = zzweburl + "/app/zz91-1.3.0.apk?" + (new Date()).getTime().toString();
				//mui.toast('下载新版应用中...');
				//openwebad("http://m.zz91.com/app.html");
				showdowninfo();
				
				var options = {
					method: "GET",
					filename: "_downloads/zz91-1.3.0.apk",
				};
				showdowninfo();
				var url = "_downloads/zz91-1.3.0.apk";       // 这个url是你的文件路径，文件路径怎么获取就不用多说了吧
				plus.io.resolveLocalFileSystemURL(url, function( entry ) {
				    entry.remove( function ( e ) {
				        console.log( "删除成功" );
				    }, function ( e ) {
				        console.log( "删除失败" );
				    });
				});
				var dtask = plus.downloader.createDownload(appUrl, options);
				dtask.addEventListener("statechanged", function(task, status) {
					showdowninfopercent((parseInt(task.downloadedSize/ 1024) / 1000).toString())
					if ( task.state == 4) {
						// 下载完成 
						$(".hint").remove();
						plus.downloader.clear();
						plus.runtime.openFile("_downloads/zz91-1.3.0.apk", {}, function(e) {
							plus.nativeUI.alert("升级失败：" + e.emssage);
						});
						plus.runtime.quit();
					}  
				});
				dtask.start();
				
			} else {
				return false;
			}
			
		}, "提示", ["立即更新", "取　　消"]);

	});
}
//下载提示框
function showdowninfo() {
	var ts = "正在下载应用...";
	$(".hint").remove()
	var hintHtml = '<div class="hint" style="position:fixed;color:#fff;line-height:18px;font-size:14px;width:100%">' + '<span style="display:block;margin:0 8px;background:#000;opacity:0.8;border-radius:5px;padding:10px 10px;text-align:center" id="downloadstate">' + ts + '<span>' + '</div>';
	$("body").append(hintHtml);
	$(".hint").css("bottom", "80px");
}

function showdowninfopercent(percent) {
	$("#downloadstate").html("正在下载应用 已下载" + percent + "M");
	if (percent == 100) {
		$(".hint").remove()
	}
}
mui.plusReady(function() {
	downloadnewapp()
})
