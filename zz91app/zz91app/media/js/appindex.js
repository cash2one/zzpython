var jsstr;
var loadnum=1;
var messagenum=0;
var zzajax1 = function(method, url, arg, successCallback, errorCallback) {
	var xhr = new XMLHttpRequest();
	var protocol = /^([\w-]+:)\/\//.test(url) ? RegExp.$1 : window.location.protocol;
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			if ((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304 || (xhr.status === 0 && protocol === 'file:')) {
				successCallback && successCallback(xhr.responseText);
			} else {
				errorCallback && errorCallback();
			}
		}
	};
	xhr.open(method, url, true);
	if (method == "post") {
		xhr.send(arg);
	} else {
		xhr.send();
	}
};
var shopfun = {
	opencontact: function() {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = 5;
		if (parseInt(qianbaoblance) >= money) {
			openfloatdiv(event, 'showphone1');
		} else {
			openfloatdiv(event, 'bal');
		}
	},
	chongzhi: function(furl) {
		if (appsystem == "iOS") {
			//requestquery("http://app.zz91.com/chongzhi.html","");
			plus.ui.alert("我们已将支付方式以短信和邮件的方式发送给您，请注意查收！")
		} else {
			gotourl(furl, 'blank');
		}
	},
	openadurl: function(furl) {
		plus.runtime.openURL(furl);
	},
	name: 1
};
var myrc = {
	favoritedel: function(id, obj) {
		var btnArray = ['确定', '取消'];
		mui.confirm('确认要删除吗？', '提示', btnArray, function(e) {
			if (e.index == 0) {
				var arg = "company_id=" + company_id;
				arg += "&id=" + id;
				zzajax1("post", "http://app.zz91.com/myrc/favoritedel.html", arg, function(data) {
					var j = JSON.parse(data);
					if (j && j.err) {
						if (j.err == "false") {
							var favor = obj.parentNode
							if (favor) {
								favor.style.display = "none";
							}
						} else {
							plus.ui.alert(j.errkey);
						}
						if (nWaiting) {
							nWaiting.close();
						}
					} else {
						if (nWaiting) {
							nWaiting.close();
						}
					}
				}, function(data) {});
			} else if (e.index == 1) {
				if (nWaiting) {
					nWaiting.close();
				}
			} else {
				if (nWaiting) {
					nWaiting.close();
				}
			}
		});
	},
	forgetpasswd: function(frm, url) {
		var arg = "";
		if (window.plus) {
			nWaiting = plus.nativeUI.showWaiting();
			arg += "company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&t=" + (new Date()).getTime().toString();
			var checkflag = 0;
			for (var i = 0; i < frm.length; i++) {
				var objinput = frm[i];
				var objtype = objinput.type;
				var objvalue = objinput.value;
				var objname = objinput.name;
				if (objname != "") {
					if (objinput.type == "radio" || objinput.type == "checkbox") {
						if (objinput.checked == true) {
							if (arg.indexOf(objname) < 0) {
								checkflag = 0;
							}
							if (checkflag == 1) {
								arg += "," + objvalue;
							} else {
								arg += "&" + objname + "=" + objvalue;
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
		}

		zzajax1("post", url, arg, function(data) {
			var j = JSON.parse(data);
			if (j) {
				var err = j.err;
				var errkey = j.errkey;
				if (err == "true") {
					if (j.type == "forgetpasswd") {
						$(".c-red").html(errkey);
					}
				} else {
					if (j.type == "forgetpasswd") {
						$(".c-red").html("");
						var result = j.result;
						var step = j.step;
						var mobile = result.mobile;
						var account = result.account;
						loaddata("http://app.zz91.com/forgetpasswdpage.html?mobile=" + mobile + "&account=" + account + "&clientid=" + clientid + "&step=" + step+"&t="+(new Date()).getTime().toString());
					}
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
		return false;
	},
	//重置密码成功后自动登陆
	forgetpasswdload: function(cid) {
		company_id = cid;
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
		}
		closewindow();
	}
};
var messages = {
	views: function(urlp, obj, isview) {
		var messagescount = document.getElementById("messagescount");
		var count = $("#messagescount").html();
		messagenum=document.getElementById("mtype");
		if (messagenum){
			messagenum=messagenum.value;
		}else{
			messagenum=0
		}
		if (isview != "1" && obj.style.color == "") {
			if (count != "" && count != "0") {
				$("#messagescount").html((count - 1).toString())
			}
			if (count - 1 == 0) {
				messagescount.style.display = "none";
			}
			obj.style.color = "#C4C4C4";
			var mainwin=plus.webview.getWebviewById( "HBuilder" );
			if (mainwin){
				mainwin.evalJS('messages.showviewnum('+messagenum.toString()+');');
			}
			var wobj = plus.webview.currentWebview();
			if (wobj) {
				var opener = wobj.opener();
				if (opener) {
					opener.evalJS('messages.showviewnum('+messagenum.toString()+');');
				}
			}
		}
		if (count == "" || count == "0") {
			messagescount.style.display = "none";
		}
		gotourl(urlp, "blank");
	},
	showviewnum:function(num){
		var messagescount = document.getElementById("messagescount");
		if (messagescount){
			var count = $("#messagescount").html();
			if (count != "" && count != "0") {
				$("#messagescount").html((count - 1).toString())
			}
			if (count - 1 == 0) {
				messagescount.style.display = "none";
			}
		}
		var messagescount = document.getElementById("messagescount"+num.toString());
		if (messagescount){
			var count = $("#messagescount"+num.toString()).html();
			if (count != "" && count != "0") {
				$("#messagescount"+num.toString()).html((count - 1).toString())
			}
			if (count - 1 == 0) {
				messagescount.style.display = "none";
			}
		}
	},
	readall:function(){
		var messagescount = document.getElementById("messagescount")
		if (messagescount){messagescount.style.display="none"}
		var messagescount = document.getElementById("messagescount0")
		if (messagescount){messagescount.style.display="none"}
		var messagescount = document.getElementById("messagescount1")
		if (messagescount){messagescount.style.display="none"}
		var messagescount = document.getElementById("messagescount2")
		if (messagescount){messagescount.style.display="none"}
		var messagescount = document.getElementById("messagescount3")
		if (messagescount){messagescount.style.display="none"}
	},
	openlist:function(num){
		messagenum=num;
		gotourl("messagelistmongo.html?mtype="+num.toString(), "blank");
	}
};

var downloader = {
	down: function(durl, srvVer) {
		var dtask = null;
		if (dtask) {
			return;
		}
		//var durl = "http://app.zz91.com/app/zz91-1.0.2.apk";
		var options = {
			method: "GET"
		};
		dtask = plus.downloader.createDownload(durl, options);
		dtask.addEventListener("statechanged", function(task, status) {
			switch (task.state) {
				case 1: // 开始
					break;
				case 2: // 已连接到服务器
					break;
				case 3: // 已接收到数据

					var downloadwindowjindu = document.getElementById("downloadwindowjindu");
					downloadwindowjindu.innerHTML = '下载数据: <span id="dsize"></span>/' + parseInt(task.totalSize / 1024) / 1000 + "M";
					var ds = document.getElementById("dsize");
					ds.innerText = parseInt(task.downloadedSize / 1024) / 1000 + "M";

					break;
				case 4: // 下载完成
					closeoverlay();
					plus.runtime.openFile("_downloads/zz91-" + srvVer + ".apk", {}, function(e) {
						plus.nativeUI.alert("升级失败：" + e.emssage);
					});
					break;
			}
		});
		dtask.start();
	},
	htmldown: function(html) {
		var dtask = null;
		if (dtask) {
			return;
		}
		var durl = "http://app.zz91.com/app/html/index.html";
		var options = {
			method: "GET"
		};
		dtask = plus.downloader.createDownload(durl, options);
		dtask.addEventListener("statechanged", function(task, status) {
			switch (task.state) {
				case 1: // 开始
					break;
				case 2: // 已连接到服务器
					break;
				case 3: // 已接收到数据
					break;
				case 4: // 下载完成
					//plus.io.FileEntry.moveTo("_www/","index.html",'','');
					break;
			}
		});
		dtask.start();
	}
};
var msgchickurl = "";
// 监听plusready事件  
document.addEventListener("plusready", function() {
	// 监听点击消息事件
	plus.push.addEventListener("click", function(msg) {
		if (msgchickurl == "") {
			gotourl(msg.payload, "messages");
			msgchickurl = msg.payload;
		}
		if (msg.payload != msgchickurl) {
			msgchickurl = "";
		}
	}, false);
	// 监听在线消息事件
	plus.push.addEventListener("receive", function(msg) {
		//alert(msg)
		if (msg.aps) { // Apple APNS message

		} else {

		}
	}, false);
}, false);
//链接通用函数
(function($) {
	$.ready(function() {
		$('body').on('tap', 'a', function(e) {
			var id = this.getAttribute('href');
			var wintarget = "blank";
			if (nowurl) {
				if (nowurl.indexOf("/priceindex/") >= 0) {
					wintarget = "price"
				}
				if (nowurl.indexOf("/category/") >= 0) {
					wintarget = "trade"
				}
			}
			if (id && id.substring(0, 1) != "#") {
				if (window.plus) {
					if (id.indexOf("javascript:") < 0) {
						if (id.indexOf("tel:") >= 0) {
							eval("dialtel(" + id.replace("tel:", "") + ")")
						} else {
							if (appsystem == "iOS") {
								gotourl(id, wintarget);
							} else {
								gotourl(id, wintarget);
							}
						}
					} else {
						if (id.indexOf("tel:") > 0) {
							eval("dialtel(" + id.replace("tel:", "") + ")")
						} else {
							if (appsystem == "iOS") {
								eval(id);
							} else {
								eval(id);
							}
							if (id.indexOf("/qianbao/") > 0) {
								plus.storage.setItem("qianbaonum", 1);
							}
						}
					}
				}
			}
		});
	});
})(mui);
//8进制加密
function EnEight(txt){
    var monyer = new Array();
    var i,s;
    for(i=0;i<txt.length;i++)
        monyer+="\\"+txt.charCodeAt(i).toString(8); 
    return monyer;
}
//8进制解密
function DeEight(txt){
    var monyer = new Array();var i;
    var s=txt.split("\\");
    for(i=1;i<s.length;i++)
        monyer+=String.fromCharCode(parseInt(s[i],8));
    return monyer;
}
//收藏
function favorite(querylist) {
	if (company_id == 0) {
		jsstr="favorite('"+querylist+"')"
		jsstr=escape(jsstr)
		gotourl("/login/?jsstr="+jsstr, "blank");
	} else {
		var furl = "http://app.zz91.com/favorite/";
		requestquery(furl, querylist);
	}
}
function telclick(url) {
	zzajax1("get", url, '', function(data) {
	}, '')
}

function dialtel(telphone) {
	plus.device.dial(telphone, false);
	telclick("http://m.zz91.com/trade/telclicklog.html?tel=" + telphone + "&pagefrom=apptrade&company_id="+company_id.toString());
}
// 上传文件
function upload(p) {
	var index=document.getElementsByTagName("img").length;
	if (index > 5) {
		plus.ui.alert("最多上传5张图片");
		return false;
	}
	var wt = plus.nativeUI.showWaiting("正在上传图片中，请稍后......");
	var task = plus.uploader.createUpload(server, {
			method: "POST"
		},
		function(t, status) { //上传完成
			if (status == 200) {
				//plus.storage.setItem("uploader",t.responseText);
				wt.close();
				
				//document.getElementById("mark").style.display="none";
				plus.ui.alert("上传成功！")
				index += 1;
				//document.getElementById("mark").setAttribute('style', 'display:none');
				document.getElementById("imglist").innerHTML += "<img src='" + t.responseText + "' width=80 height=80>";
			} else {
				wt.close();
			}
		}
	);
	task.addData("randid", getRandid());
	task.addFile(p, {
		key: 'uploadkey'
	});
	task.start();
}
function payopen(paytype) {
	window.scrollTo(0, 0);
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("数据加载中，请稍候......");
	}
	ws = plus.webview.currentWebview();
	var weburl = "http://app.zz91.com/qianbao/chongzhi.html?company_id=" + company_id.toString() + "&appsystem=" + appsystem + "&paytype=" + paytype + "&ttt=" + (new Date()).getTime().toString()
	embed = plus.webview.create(weburl, "embed", {
		top: "45px",
		bottom: "0px"
	});
	ws.append(embed);
	embed.loadURL(weburl);
	if (nWaiting) {
		nWaiting.close();
	}
}

function reloadpay() {
	loaddata(nowherf);
}
//打开弹出窗
function openfloatdiv(e,obj){
	if (company_id == 0) {
		jsstr="openfloatdiv('','"+obj+"')"
		jsstr=escape(jsstr)
		gotourl("/login/?jsstr="+jsstr, "blank");
	}else{
		minwindow=true;
		$("#"+obj).lightbox_me({
			overlaySpeed:0,
			lightboxSpeed:0,
			centered: true, 
			onLoad: function() {
				minwindow=obj;
			},
			onClose:function(){
				minwindow=null;
			}
	    });
	 }
}

//加载头部和底部
function showheader(wintype) {
	//头部底部
	var active1 = "";
	var active2 = "";
	var active3 = "";
	var active4 = "";
	var active5 = "";
	var title = "ZZ91再生网"
	if (wintype == "myrc" || wintype == "myrc_products") {
		title = "生意管家"
		active4 = "mui-active"
	}
	if (wintype == "login") {
		title = "用户登录"
		active2 = "mui-active"
	}
	if (wintype == "reg") {
		title = "用户注册"
		active2 = "mui-active"
	}
	if (wintype == "error") {
		title = "网络错误"
		active2 = "mui-active"
	}
	if (wintype == "trade" || wintype == "tradelist") {
		title = "交易中心"
		active2 = "mui-active"
	}
	if (wintype == "price") {
		title = "行情报价"
		active2 = "mui-active"
	}
	if (wintype == "huzhu") {
		title = "再生互助"
		active2 = "mui-active"
	}
	if (wintype == "news") {
		title = "资讯中心"
		active2 = "mui-active"
	}
	if (wintype == "tradeindex") {
		title = "商机"
		active2 = "mui-active"
	}
	if (wintype == "messages") {
		title = "消息"
		active5 = "mui-active"
	}
	if (wintype == "fj") {
		title = "附近商机"
		active1 = "mui-active"
	}
	if (wintype == "newindex") {
		title = "ZZ91再生网"
		active3 = "mui-active"
	}
	if (wintype == "order") {
		title = "商机定制"
		active2 = "mui-active"
	}
	if (wintype == "company") {
		title = "公司黄页"
		active2 = "mui-active"
	}
	if (wintype == "myorder") {
		title = "我的定制"
		active2 = "mui-active"
	}
	if (wintype == "favorite") {
		title = "我的收藏夹"
		active4 = "mui-active"
	}
	if (wintype == "qianbao") {
		title = "再生钱包"
		active4 = "mui-active"
	}
	if (wintype == "zhangdan") {
		title = "我的账单"
		active4 = "mui-active"
	}
	var topstr = "<a><img src=\"images/logo.png\"></a>" +
		"<a class=\"mui-icon mui-icon-gear mui-pull-right\" href=\"javascript:gotourl('/set.html','blank')\"></a>"
	var topstr1 = "<a class=\"mui-action-back mui-icon mui-icon-left-nav mui-pull-left\"></a>" +
		"<a class=\"mui-icon mui-icon-gear mui-pull-right\" href=\"javascript:gotourl('/set.html','blank')\"></a>" +
		"<h1 class=\"mui-title\">" + title + "</h1>"
	var topstr2 = "<a class=\"mui-pull-left\"><img src=\"images/logo.png\" /></a>" +
		//"<a class=\"mui-icon mui-icon-bars mui-pull-right\"></a>" +
		"<a class=\"mui-action-back mui-btn mui-btn-link mui-pull-right\" onclick=\"loginout()\">关闭</a>" +
		"<h1 class=\"mui-title\">" + title + "</h1>"
	var topstr3 = "<a class=\"mui-action-back mui-icon mui-icon-left-nav mui-pull-left\"></a>" +
		//"<a class=\"mui-icon mui-icon-bars mui-pull-right\"></a>" +
		"<h1 class=\"mui-title\">" + title + "</h1>"

	if (wintype == "index" || wintype == "newindex") {
		document.getElementById("apptop").innerHTML = topstr
	} else {
		document.getElementById("apptop").innerHTML = topstr1
	}
	if (wintype == "login") {
		document.getElementById("apptop").innerHTML = topstr1
	}
	if (wintype == "reg") {
		document.getElementById("apptop").innerHTML = topstr1
	}
	var botttomstr = "<nav class=\"mui-bar mui-bar-tab\" id=\"appbottom\"><div style=\"position: fixed;bottom: 0;left: 0;\">" +
		"<a class=\"mui-tab-item " + active3 + "\" href=\"javascript:gotourl('/index.html','newindex');\">" +
		"	<span class=\"mui-icon mui-icon-home\"></span><span class=\"mui-tab-label\" >首页</span>" +
		"</a>" +
		"<a class=\"mui-tab-item " + active5 + "\" href=\"javascript:gotourl('/messagelist/','messages');\">" +
		"	<span class=\"mui-badge mui-badge-danger message-num\" id='messagescount' style='display:none'>1</span><span class=\"mui-icon mui-icon-email\"></span><span class=\"mui-tab-label\">消息</span>" +
		"</a>" +
		"<a class=\"mui-tab-item " + active1 + "\" href=\"javascript:fj()\">" +
		"	<span class=\"mui-icon mui-icon-location\"></span><span class=\"mui-tab-label\">附近</span>" +
		"</a>" +
		"<a class=\"mui-tab-item " + active4 + "\" href=\"javascript:gotourl('/myrc_index/','myrc');\">" +
		"	<span class=\"mui-icon mui-icon-contact\"></span><span class=\"mui-tab-label\">管家</span>" +
		"</a>" +
		"</div><input type=hidden id=bottomcheck></nav>";


	var bottomquestion = "<nav class=\"mui-bar mui-bar-tab\" id=\"appbottom\"><span class=\"mui-icon mui-icon-plus zz91-question-addpic\"></span>" +
		"<textarea rows=\"1\" placeholder=\"多行文本框\" class=\"zz91-question-addtext\"></textarea>" +
		"<a class=\"mui-btn mui-btn-success zz91-question-addsend\">发送</a></nav>";

	var bottomhuzhu = "<nav class=\"mui-bar mui-bar-tab\" id=\"appbottom\"><center style=\"padding-top: 10px;\">" +
		"<button onclick=\"gotourl('/huzhupost/','blank')\" class=mui-btn-success style=\"width: 90%;\">  我要提问    </button> " +
		"</center></nav>";

	
	if (wintype == "login" || wintype == "error" || wintype == "reg") {
		document.getElementById("appbottom").innerHTML = "";
	} else {
		if (!document.getElementById("bottomcheck")){
			document.getElementById("appbottom").innerHTML = botttomstr;
		}
	}
	if (wintype == "huzhu") {
		document.getElementById("appbottom").innerHTML = bottomhuzhu;
	}
	if (wintype == "question") {
		document.getElementById("appbottom").innerHTML = bottomquestion;
	}
	getmessagesnum(company_id);
}

function loadappbody() {
	var netstatus = 0;
	var companyid = plus.storage.getItem("companyid");
	company_id = companyid;
	appsystem = "Android";
	if (company_id == null) {
		company_id = 0;
	}
	if (company_id == null || company_id.toString() == "0") {
		if (clientid == "" || clientid == "null" || !clientid) {
			clientid = "No" + plus.device.imei.toString();
		} else {
			var info = plus.push.getClientInfo();
			if (info.token) {
				clientid = info.token;
			} else {
				if (info.clientid) {
					clientid = info.clientid;
				}
			}
		}
		var userimei = plus.device.imei;
		
		zzajax1("get", "http://app.zz91.com/logininfo1.html?appid=" + clientid + "&appsystem=" + appsystem + "&userimei=" + userimei + "&ttt=" + (new Date()).getTime().toString(), '', function(data) {
			var j = JSON.parse(data);
			if (j.company_id == 0) {
				gotourl("/index.html", "newindex");
				netstatus = 1;
			} else {
				company_id = j.company_id;
				netstatus = 1;
				gotourl("/index.html", "newindex");
			}
		}, function() {
			showheader("error");
			var pcontent = document.getElementById("pcontent");
			var mainbody = document.getElementById("mainbody");
			if (pcontent) {
				//content.style.display = "";
				//mainbody.style.display = "none";
				var errhtml='<div class="midload">'+
					'<h5>网络不给力,请检查网络是否正常！</h5>'+
					'<br />'+
					'<button class="mui-btn mui-btn-warning" onclick="reloadapp(this);">'+
					'刷新重试'+
					'</button>'+
					'<button class="mui-btn mui-btn-warning mui-btn-outlined" onclick="mui.closeapp();">'+
					'	退出'+
					'</button>'+
				'</div>'
				pcontent.innerHTML=errhtml
			}
			mainbody.style.display = "";
			company_id = 0;
		});
		if (nWaiting) {
			nWaiting.close();
		}
	} else {
		gotourl("/index.html", "newindex");
		netstatus = 1;
	}
	var shortcutfirst = plus.storage.getItem("shortcutfirst");
	if (appsystem == "Android" && !shortcutfirst) {
		createShortcut();
		plus.storage.setItem("shortcutfirst", "1");
	}
}

function regloadbody(cid) {
	company_id = cid;
	if (nowurl) {
		nowurl = nowurl.replace("company_id=0", "company_id=" + cid.toString());
	}
	var url = nowurl;
	var trueurl = url;
	if (cid == 0) {
		url = "/login/";
		wintype = "login";
	}
	if (winflag == 2) {
		var wvs = plus.webview.all();
		for (var i = 0; i < wvs.length; i++) {
			wvs[i].evalJS('loadcompanyid(' + company_id.toString() + ');');
		}
		//执行js
		if (jsstr && jsstr!=""){
			var wobj = plus.webview.currentWebview();
			if (wobj) {
				var opener = wobj.opener();
				if (opener) {
					opener.evalJS(unescape(jsstr));
				}
			}
		}
		closewindow();
		return false;
	}
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	url = url.replace("/companyinfo/?company_id=", "/companyinfo/?forcid=");
	if (url.indexOf("http://app.zz91.com") < 0) {
		if (url.indexOf("?") < 0) {
			url = "http://app.zz91.com/" + url + "?t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&win=" + win.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		} else {
			url = "http://app.zz91.com/" + url + "&t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&win=" + win.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		}
	}
	var content = document.getElementById("dcontent1");

	if (content) {
		content.innerHTML = "<br /><br /><center class=midload><img src=images/96R.gif><br>正在为您努力加载中......<br /></center>"
	} else {
		closewindow();
		var content = document.getElementById("dcontent");
		//			var mainwin=plus.webview.getWebviewById( "HBuilder" );
		//			if (mainwin){
		//				mainwin.evalJS('loadcompanyid('+company_id.toString()+');');
		//			}
		return false;
	}
	zzajax("get", url, '', function(data) {
		content.innerHTML = data;
		if (nWaiting) {
			nWaiting.close();
		}
	}, function(data) {

	});
	showheader(nowwintype);
	netstatus = 1
}


//侧滑
var ws = null,
	wc = null;

function showSide(searchtext) {
	// 防止快速点击可能导致多次创建
	// 显示侧滑页面
	if (window.plus){
		ws = plus.webview.currentWebview();
		// 用户点击后
		ws.addEventListener("maskClick", function() {
			wc.close("auto");
		}, false);
	}
	if (wc) {
		return;
	}
	// 开启遮罩
	ws.setStyle({
		mask: "rgba(0,0,0,0.5)"
	});
	
	// 创建侧滑页面
	var url="offerlistside.html?keywords="+searchtext.toString()+"&tflag=az";
	url = url.replace("&", "TandT").replace("?", "wenhao")
	wc = plus.webview.create("/blank.html?url2="+url+"&wintype=" + wintype + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode, "side", {
		left: "30%",
		width: "70%",
		popGesture: "none"
	});
	// 侧滑页面关闭后关闭遮罩
	wc.addEventListener('close', function() {
		ws.setStyle({
			mask: "none"
		});
		wc = null;
	}, false);
	// 侧滑页面加载后显示（避免白屏）
	wc.addEventListener("loaded", function() {
		wc.show("slide-in-right", 200);
	}, false);
}
var ws=null,as='slide-in-right',at=200;
var back=function(hide){
	if(window.plus){
		ws||(ws=plus.webview.currentWebview());
		if(hide||ws.preate){
			ws.hide('auto',at);
		}else{
			ws.close('auto',at);
		}
	}else if(history.length>1){
		history.back();
	}else{
		window.close();
	}
}
//供求筛选
function sidetradeloaddata(frm) {
	var wobj = plus.webview.currentWebview();
	var checkflag = 0;
	var arg = "";
	var nobjname;
	for (var i = 0; i < frm.ptype.length; i++){
		if (frm.ptype[i].checked == true) {
			arg+="&ptype="+frm.ptype[i].value;
		}
	}
	var provincelist="";
	for (var i = 0; i < frm.province.length; i++){
		if (frm.province[i].checked == true) {
			provincelist+=""+frm.province[i].value+"|";
		}
	}
	if (provincelist.length>=1){
		provincelist=provincelist.substr(0,provincelist.length-1)
	}
	arg+="&province="+provincelist;
	arg+="&keywords="+frm.keywords.value;
	if (wobj) {
		var opener = wobj.opener();
		if (opener) {
			wobj.close();
			opener.evalJS('gotourl("/offerlist/?'+arg+'","tradelist");');
		}
		var parent = wobj.parent();
		if (parent) { //又得evalJS
			//parent.evalJS('loadappbody();');
		}
	}
}
function sideloaddata(url, wintype) {
	var wobj = plus.webview.currentWebview();
	if (wobj) {
		var opener = wobj.opener();
		if (opener) {
			wobj.close();
			opener.evalJS('gotourl("' + url + '","' + wintype + '");');
		}
		var parent = wobj.parent();
		if (parent) { //又得evalJS
			//parent.evalJS('loadappbody();');
		}
	}
}
//打开 web 的url
function openweburl(url) {
	if (wc) {
		return;
	}
	url = url.replace("&", "TandT").replace("?", "wenhao")
	//mainurl="/getweburl.html?weburl="+url;
	//gotourl(mainurl,"blank")
	wc = plus.webview.create("http://m.zz91.com", "side", {
		width: "100%",
		popGesture: "none"
	});
	wc.addEventListener('close', function() {
		wc = null;
	}, false);
	// 页面加载后显示（避免白屏）
	wc.addEventListener("loaded", function() {
		wc.show("slide-in-right", 200);
	}, false);
}

function loadcompanyid(cid) {
	company_id = cid;
}
//回复楼主
function backbbsform(frm) {
	if (company_id == 0) {
		gotourl("/login/", "blank");
	} else {
		return submitfrm(frm, 'http://app.zz91.com/huzhu_replay/');
	}
}
function bbsformreply(replayid, tocompany_id) {
	if (company_id == 0) {
		jsstr="huzhureplay("+replayid+","+tocompany_id+")"
		jsstr=escape(jsstr)
		gotourl("/login/?jsstr="+jsstr, "blank");
	} else {
		huzhureplay(replayid, tocompany_id)
	}
}
//供求留言
function tradeleavewords(pid, tocompany_id) {
	if (company_id == 0) {
		jsstr="tradeleavewords("+pid+","+tocompany_id+")"
		jsstr=escape(jsstr)
		gotourl("/login/?jsstr="+jsstr, "blank");
	} else {
		openoverlay('', '回复', 0, 180, '.d-leavewords');
	}
}
//重新加载
function reloadapp(obj) {
	neterr();
	obj.innerHTML = "刷新重试...";
	obj.value="刷新重试...";
	//loadappbody();
}
//网络掉线
function neterr(){
	var pcontent = document.getElementById("pcontent");
	var mainbody = document.getElementById("mainbody");
	var netstats = getnetstats();
	if (netstats != "未连接网络") {
		if (pcontent) {
			pcontent.style.display = "none";
			mainbody.style.display = "";
			//loadappbody();
		}
	} else {
		if (pcontent) {
			pcontent.style.display = "";
			mainbody.style.display = "none";
			mui.toast('网络错误,请检查网络是否正常！');
			return 
		}
	}
	if (pcontent) {
		var errhtml='<div class="midload">'+
			'<h5>网络不给力,请检查网络是否正常！</h5>'+
			'<br />'+
			'<button class="mui-btn mui-btn-warning" onclick="reloadapp(this);">'+
			'刷新重试'+
			'</button>'+
			'  <button class="mui-btn mui-btn-warning mui-btn-outlined" onclick="closewindow();">'+
			'	退出'+
			'</button>'+
		'</div>'
		pcontent.innerHTML=errhtml
	}
}
//登陆
function zz91login(frm) {
	
		var username = frm.username.value;
		var passwd = frm.passwd.value;
		var tourl = frm.tourl.value;
		var wintarget = frm.wintarget.value;
		jsstr = frm.jsstr.value.toString();
		
		if (username == "" || passwd == "") {
			return false;
		}
		
		var arg = "username=" + username;
		arg += "&passwd=" + passwd;
		arg += "&appid=" + clientid;
		arg += "&loginflag=1";
		arg += "&appsystem=" + appsystem;
		mui.get("http://app.zz91.com/loginof.html?"+arg, arg, function(data) {
			var j = JSON.parse(data);
			if (j && j.err) {
				if (j.err == "false") {
					company_id = j.result;
					tourl = tourl.replace("company_id=0", "company_id=" + company_id);
					if (tourl != "") {
						nowurl = tourl;
						nowwintype = "index";
						plus.storage.setItem("companyid", company_id);
						regloadbody(company_id);
						if (nWaiting) {
							nWaiting.close();
						}
					} else {
						if (winflag == 2) {
							plus.storage.setItem("companyid", company_id);
							regloadbody(company_id);
							if (nWaiting) {
								nWaiting.close();
							}
						} else {
							loadappbody();
						}
					}
					plus.storage.setItem("companyid", company_id);
				} else {
					plus.ui.alert(j.errkey);
				}
				if (nWaiting) {
					nWaiting.close();
				}
			} else {
				if (nWaiting) {
					nWaiting.close();
				}
			}
		}, function(data) {

		});
		return false;
	}
//全部标为已读
function updatemessagesall(){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("数据更新中...");
	}
	var nWaitingfj = plus.nativeUI.toast("数据更新中...");
	var arg = "company_id=" + company_id;
	arg += "&clientid=" + clientid;
	mui.get("http://app.zz91.com/messagesreadall.html?" + arg, '', function(data) {
		var j = JSON.parse(data);
		gotourl(nowherf,'messages')
		if (nWaiting) {
			nWaiting.close();
		}
		var wobj = plus.webview.currentWebview();
		if (wobj) {
			var opener = wobj.opener();
			if (opener) {
				opener.evalJS('messages.readall()');
			}
		}
		var nWaitingfj = plus.nativeUI.toast("全部标为已读");
	}, function(data) {
		plus.ui.alert("系统错误！请稍后重试.");
	});
	if (nWaiting) {
		nWaiting.close();
	}
	return false;
}
var _openrequest=null;
function requestquery(furl,querylist){
	if (_openrequest){
		return;
	}
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg = {
		company_id:company_id,
		clientid:clientid,
		appsystem:appsystem
	};
	//var arg="company_id="+company_id.toString()+"&clientid="+clientid+"&appsystem="+appsystem+querylist
	var arrchecklist=querylist.split("&");
	if (arrchecklist.length>1){
		for (var a=1;a<arrchecklist.length;a++){
			if (arrchecklist[a]){
				var arrchecklist1=arrchecklist[a].split("=");
				var checkname=arrchecklist1[0];
				var checkvalue=arrchecklist1[1];
				arg[checkname]=checkvalue;
			}
		}
	}
	mui.post(furl, arg,function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		_openrequest=null;
		if (err == "true") {
			if (j.type=="viewcontact"){
				closeoverlay();
				openfloatdiv(event,'bal');
				return false;
			}else{
				plus.ui.alert(errkey);
			}
			
		} else {
			if (j.type){
				switch(j.type){
					//发布供求成功提醒
					case "favorite":
						openoverlay('', '提示', 0, 200, '.favorite');
						break;
					case "viewcontact":
						loaddata(nowherf);
						closeoverlay();
						break;
					case "pro_report":
						closeoverlay();
						openfloatdiv(event,'tippOff');
						break;
					default:
						closeoverlay();
				}
			}
			
		}
		
		if (nWaiting) {
			nWaiting.close();
		}
	});
	return false;
}

//切换账号

function changeaccount() {
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg = "company_id=" + company_id;
	arg += "&clientid=" + clientid;

	mui.get("http://app.zz91.com/changeaccount.html?" + arg, '', function(data) {
		var j = JSON.parse(data);
		company_id = 0;
		plus.storage.setItem("companyid", company_id);
		if (j.changeflag) {
			//			contactperson = "<div onclick=login()>点此登录</div>";
			//			var welcome = document.getElementById("navwelcome");
			//			if (welcome) {
			//				if (contactperson) {
			//					welcome.innerHTML = contactperson;
			//				}
			//			}
			//			var mainwin=plus.webview.getWebviewById( "HBuilder" );
			//			if (mainwin){
			//				mainwin.evalJS('regloadbody(' + company_id + ');');
			//			}

			if (nWaiting) {
				nWaiting.close();
			}
			regloadbody(0);
		}
		if (nWaiting) {
			nWaiting.close();
		}
	}, function(data) {
		plus.ui.alert("系统错误！请稍后重试.")
	});
	return false;
}
//商机定制/ 为登录提示登录
function openblank(url){
	if (company_id == 0) {
		jsstr="gotourl('"+url+"','blank')";
		jsstr=escape(jsstr);
		gotourl("/login/?jsstr="+jsstr, "blank");
	} else {
		gotourl(url,"blank");
	}
}
function zz91search(frm, url, wintype) {
	var keywords = frm.searchtext.value;
	gotourl(url + keywords, "blank");
}
//交易中心列表页底部
function bottomlabel(m){
	bottomlabelvalue=m;
	var bottomlabelname=document.getElementById("bottomlabel"+m.toString())
	if (bottomlabelname){
		bottomlabelname.className="mui-tab-item mui-active"
	}
}
//
function myFun(result) {
	var searchname="";
	$.getScript('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', function(_result) {
        if (remote_ip_info.ret == '1') {
        	searchname=remote_ip_info.city;
        	searchname = searchname.replace("省", "");
			searchname = searchname.replace("市", "");
			plus.storage.removeItem("nowaddress");
			plus.storage.setItem("nowaddress", searchname);
            //alert('国家：' + remote_ip_info.country + '<BR>省：' + remote_ip_info.province + '<BR>市：' + remote_ip_info.city + '<BR>区：' + remote_ip_info.district + '<BR>ISP：' + remote_ip_info.isp + '<BR>类型：' + remote_ip_info.type + '<BR>其他：' + remote_ip_info.desc);
        } else {
            //alert('没有找到匹配的IP地址信息！');
        }
    });
	
}
//
function fjsearch(){
	var url = "/offerlist/?province=" + nowaddress + "&keywords="+keywords;
	gotourl(url, 'blank');
}
//重新定位
function redingwei(){
	dwtype=1;
	var redingweispan = document.getElementById("redingweispan")
	if (redingweispan){
		redingweispan.className="mui-spinner";
	}
	setTimeout(dingw, 1000);
}
//web地址定位
function dingw() {
	myFun();
	nowaddress = plus.storage.getItem("nowaddress");
	if (dwtype == 1) {
		var mylocation_status = document.getElementById("mylocation_status")
		if (mylocation_status && nowaddress) {
			mylocation_status.innerHTML = nowaddress;
			var redingweispan = document.getElementById("redingweispan")
			if (redingweispan){
				redingweispan.className="mui-icon mui-icon-reload";
			}
			dwtype = 2;
		} else {
			var redingweispan = document.getElementById("redingweispan")
			if (redingweispan){
				redingweispan.className="mui-spinner";
			}
			setTimeout(dingw, 2000);
		}
	}else{
		redingweispan.className="mui-icon mui-icon-reload";
	}
}
var keywords;
function refjdw(){
	var url = "/fj.html?keywords=" + keywords + "&myaddress=GPS定位中...";
	redingwei()
	gotourl(url, 'fj');
}
function fj(){
	var searchname="";
	if (document.getElementById("searchtext")){
		keywords=searchtext.value;
	}else{
		keywords=""
	}
	$.getScript('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', function(_result) {
        if (remote_ip_info.ret == '1') {
        	searchname=remote_ip_info.city;
        	searchname = searchname.replace("省", "");
			searchname = searchname.replace("市", "");
			plus.storage.removeItem("nowaddress");
			plus.storage.setItem("nowaddress", searchname);
			fjdw();
            //alert('国家：' + remote_ip_info.country + '<BR>省：' + remote_ip_info.province + '<BR>市：' + remote_ip_info.city + '<BR>区：' + remote_ip_info.district + '<BR>ISP：' + remote_ip_info.isp + '<BR>类型：' + remote_ip_info.type + '<BR>其他：' + remote_ip_info.desc);
        } else {
        	refjdw();
            //alert('没有找到匹配的IP地址信息！');
        }
    });
}
//附近商机
function fjdw() {
	var url;
	if (document.getElementById("searchtext")){
		keywords=searchtext.value;
	}else{
		keywords=""
	}
	oldaddress = plus.storage.getItem("oldaddress");
	nowaddress = plus.storage.getItem("nowaddress");
	
	if (oldaddress != nowaddress) {
		plus.storage.setItem("oldaddress", nowaddress);
	} else {
		if (oldaddress != null && nowaddress != null) {
			url = "/offerlist/?province=" + nowaddress + "&keywords="+keywords+"";
			if (winflag==1){
				gotourl(url, 'blank');
			}else{
				gotourl(url, 'fj');
			}
			return;
		}
	}
	refjdw();
}
function gotourl(url, wintype) {
	if (wintype != "blank") {
		nowwintype = wintype;
	}
	//return neterr();
	checkUpdate();
	blankpage = 2;
	var trueurl = url;
	if (company_id == 0 || company_id == "0") {
		if (wintype == "laidianbao" || wintype == "myrc" || wintype == "qianbao" || wintype == "messages" || wintype == "order" || url == "/qianbao/") {
			openblank(url)
			//url = "/login/?tourl=" + url + "&wintarget=" + wintype;
			//wintype = "blank";
			return;
		}
	}
	url = url.replace("/companyinfo/?company_id=", "/companyinfo/?forcid=");
	if (wintype == "blank" || wintype == "reg") {
		url = url.replace("&", "TandT").replace("?", "wenhao")
		mui.openWindow({
			id: url,
			url: "/blank.html?url2=" + url + "&wintype=" + wintype + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode,
			preload: false //TODO 等show，hide事件，动画都完成后放开预加载
		});
		return;
	}
	
	var backwin = 1;
	if (url.indexOf("http://app.zz91.com") < 0) {
		if (url.indexOf("?") < 0) {
			url = "http://app.zz91.com/" + url + "?t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&win=" + win.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		} else {
			url = "http://app.zz91.com/" + url + "&t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&win=" + win.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		}
	}
	if (indexwin) {
		var backwin = indexwin[indexwin.length - 1];
		if (backwin) {
			if (backwin[1] == trueurl) {
				if (nWaiting) {
					nWaiting.close();
				}
				return;
			}
		}
	}

	if (isback == 1) {
		indexwin.push([wintype, trueurl]);
	}
	var content = document.getElementById("dcontent1");
	if (content) {
		showheader(wintype);
		if (window.plus) {
			nWaiting = plus.nativeUI.showWaiting("数据加载中......");
		}
		
	} else {
		var content = document.getElementById("dcontent");
		if (window.plus) {
			nWaiting = plus.nativeUI.showWaiting("数据加载中......");
		}
	}

		//plus.storage.clear();
	//	var backcontent = plus.storage.getItem(trueurl);
	//	var backcontenttime = plus.storage.getItem(trueurl+'time');
	//	if (backcontent && backcontenttime && trueurl!="/messagelist/"){
	//		var dc = parseInt(backcontenttime);
	//		var dn = (new Date()).getTime();
	//		if (dn - dc > winInterval) { // 未超过上次升级检测间隔，不需要进行升级检查
	//			plus.storage.removeItem(trueurl);
	//			plus.storage.removeItem(trueurl+'time');
	//		}else{
	//			content.innerHTML=backcontent;
	//			iOSclosecontent();
	//			if (nWaiting) {
	//				nWaiting.close();
	//			}
	//			window.scrollTo(0, 0);
	//			return;
	//		}
	//	}
	var xhr = null;
	var textvalue = "";
	var protocol = /^([\w-]+:)\/\//.test(url) ? RegExp.$1 : window.location.protocol;
	xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		
		switch (xhr.readyState) {
			case 4:
				if ((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304 || (xhr.status === 0 && protocol === 'file:')) {
					textvalue = xhr.responseText;
					content.innerHTML = textvalue;
					//plus.storage.setItem(trueurl, textvalue);
					//plus.storage.setItem(trueurl+'time', (new Date()).getTime().toString());
					if (nWaiting) {
						nWaiting.close();
					}
					//alert(xhr.readyState)
				} else {
					loadnum += 1;
					if (loadnum <= 3) {
						gotourl(url, wintype);
						if (nWaiting) {
							nWaiting.close();
						}
					} else {
						var btnArray = ['重试加载', '取消'];
						mui.confirm('哎呀,网络不给力，点击重试加载试试！', '提示', btnArray, function(e) {
							if (e.index == 0) {
								gotourl(url, wintype);
							} else if (e.index == 1) {
							} else {
							}
						});
						if (nWaiting) {
							nWaiting.close();
						}
					}
				}
				if (nWaiting) {
					nWaiting.close();
				}
				break;
			default:
				
				break;
		}
	}
	xhr.open("GET", url);
	xhr.send();
	nowurl = url;
	nowherf = url;
	window.scrollTo(0, 0);
	tongji();
}
//生意管家供求 一键刷新
function refreshall(frm,url){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg={
		company_id:company_id
	};
	mui.post(url, arg,function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		if (err == "true") {
			plus.ui.alert(errkey);
		} else {
			if (j.type){
				loaddata(nowherf);
			}
		}
		if (nWaiting) {
			nWaiting.close();
		}
	});
	return false;
}
var shares = null,
	bhref = false;
var Intent = null,
	File = null,
	Uri = null,
	main = null;
// H5 plus事件处理
function shareplusReady() {
	updateSerivces();
	if (plus.os.name == "Android") {
		Intent = plus.android.importClass("android.content.Intent");
		File = plus.android.importClass("java.io.File");
		Uri = plus.android.importClass("android.net.Uri");
		main = plus.android.runtimeMainActivity();
	}
}
if (window.plus) {
	//var rightobj=document.getElementById("apptop");
	if (winflag==2){
		$("#apptop").append("<a id=\"icon-close\" class=\"mui-icon mui-icon-close mui-pull-right\" onclick=\"closewindow();\"></a>")
	}
	shareplusReady();
	closewriting();
} else {
	document.addEventListener("plusready", shareplusReady, false);
}
//定时关闭加载筐
var wtt=1;
function closewriting(){
	setTimeout(function() {
		wtt+=1;
		if (wtt<10){
			closewriting()
		}else{
			if (nWaiting) {
				nWaiting.close();
			}
		}
	}, 1000);
}
/**
 * 调用系统分享
 * 调用
 */
function shareSystem() {
		if (plus.os.name !== "Android") {
			plus.nativeUI.alert("此平台暂不支持系统分享功能!");
			return;
		}
		var intent = new Intent(Intent.ACTION_SEND);
		var p = "";
		if (pic && pic.realUrl) {
			p = pic.realUrl;
			if (p.substr(0, 7) === "file://") {
				p = p.substr(7);
			} else if (p.sub(0) !== "/") {
				p = plus.io.convertLocalFileSystemURL(p);
			}
		}
		var f = new File(p);
		var uri = Uri.fromFile(f);
		if (f.exists() && f.isFile()) {
			console.log("image/*");
			intent.setType("image/*");
			intent.putExtra(Intent.EXTRA_STREAM, uri);
		} else {
			console.log("text/plain");
			intent.setType("text/plain");
		}
		intent.putExtra(Intent.EXTRA_SUBJECT, sharetitle.value);
		intent.putExtra(Intent.EXTRA_TEXT, sharecontent.value);
		intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
		main.startActivity(Intent.createChooser(intent, "系统分享"));
	}
	/**
	 * 更新分享服务
	 */

function updateSerivces() {
		plus.share.getServices(function(s) {
			shares = {};
			for (var i in s) {
				var t = s[i];
				shares[t.id] = t;
			}
		}, function(e) {
			//outSet( "获取分享服务列表失败："+e.message );
		});
	}
	// 打开分享

function shareShow() {
		bhref = false;
		var ids = [{
				id: "weixin",
				ex: "WXSceneSession"
			}, {
				id: "weixin",
				ex: "WXSceneTimeline"
			}, {
				id: "sinaweibo"
			}, {
				id: "tencentweibo"
			}],
			bts = [{
				title: "发送给微信好友"
			}, {
				title: "分享到微信朋友圈"
			}, {
				title: "分享到新浪微博"
			}, {
				title: "分享到腾讯微博"
			}];
		if (plus.os.name == "iOS") {
			ids.push({
				id: "qq"
			});
			bts.push({
				title: "分享到QQ"
			});
		}
		plus.nativeUI.actionSheet({
				cancel: "取消",
				buttons: bts
			},
			function(e) {
				var i = e.index;
				if (i > 0) {
					shareAction(ids[i - 1].id, ids[i - 1].ex);
				}
			}
		);
	}
	// 分析链接

function shareHref() {
		bhref = true;
		var ids = [{
				id: "weixin",
				ex: "WXSceneSession"
			}, {
				id: "weixin",
				ex: "WXSceneTimeline"
			},{id:"sinaweibo"}],
			bts = [{
				title: "发送给微信好友"
			}, {
				title: "分享到微信朋友圈"
			},{title:"分享到新浪微博"}, {
				title: "更多分享"
			}];
		//	if(plus.os.name=="iOS"){
		//		ids.push({id:"qq"});
		//		bts.push({title:"分享到QQ"});
		//	}
		plus.nativeUI.actionSheet({
				cancel: "取消",
				buttons: bts
			},
			function(e) {
				var i = e.index;
				if (i > 0 && i <= 3) {
					shareAction(ids[i - 1].id, ids[i - 1].ex);
				}
				if (i == 4) {
					shareSystem()
				}
			}
		);
	}
	/**
	 * 分享操作
	 * @param {String} id
	 */

function shareAction(id, ex) {
		var s = null;
		//outSet( "分享操作：" );
		if (!id || !(s = shares[id])) {
			//outLine( "无效的分享服务！" );
			return;
		}
		if (s.authenticated) {
			//outLine( "---已授权---" );
			shareMessage(s, ex);
		} else {
			//outLine( "---未授权---" );
			s.authorize(function() {
				shareMessage(s, ex);
			}, function(e) {
				//outLine( "认证授权失败："+e.code+" - "+e.message );
			});
		}
	}
	/**
	 * 发送分享消息
	 * @param {plus.share.ShareService} s
	 */

function shareMessage(s, ex) {
		var msg = {
			content: sharecontent.value,
			extra: {
				scene: ex
			}
		};
		if (bhref) {
			msg.href = zsharehref.value;
			if (zsharehrefTitle && zsharehrefTitle.value != "") {
				msg.title = zsharehrefTitle.value;
			}
			if (zsharehrefDes && zsharehrefDes.value != "") {
				msg.content = zsharehrefDes.value;
			}
			msg.thumbs = ["_www/icon.png"];
		} else {
			if (pic && pic.realUrl) {
				msg.pictures = [pic.realUrl];
			}
		}
		//outLine(JSON.stringify(msg));
		s.send(msg, function() {
			outLine("分享到\"" + s.description + "\"成功！ ");
		}, function(e) {
			outLine( "分享到\""+s.description+"\"失败: "+e.code+" - "+e.message );
		});
	}
	/**
	 * 解除所有分享服务的授权
	 */

function cancelAuth() {
	try {
		//outSet( "解除授权：" );
		for (var i in shares) {
			var s = shares[i];
			if (s.authenticated) {
				//outLine( "取消\""+s.description+"\"");
			}
			s.forbid();
		}
		// 取消授权后需要更新服务列表
		updateSerivces();
		//outLine( "操作成功！" );
	} catch (e) {
		alert(e);
	}
}


//钱包提醒
//if (plus.storage.getItem("qianbaonum")){
//	var qianbaonum=document.getElementById("qianbaonum");
//	if (qianbaonum){
//		qianbaonum.style.display="none";
//	}
//}
//plus.storage.clear();
function tongji(){
	var turl="http://app.zz91.com/tongji/t.html?t="+ (new Date()).getTime().toString()+"&clientid=" + clientid + "&appsystem=" + appsystem;
	if (nowherf){
		turl+="&url="+nowherf.replace("&","^and^");
	}
	turl+="&visitoncode="+visitoncode.toString()
	turl+="&company_id="+company_id.toString();
	zzajax1("get",turl, '',function(data) {
		
	}, function() {
	});
}
$(document).ready(function() {
	tongji();
});

//邀请码
function inviteapp(frm){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
		var url="http://app.zz91.com/invite/invite_save.html";
		var arg="company_id="+frm.company_id.value;
		arg+="&code="+frm.code.value;
		arg+="&clientid="+frm.clientid.value;
		arg+="&t="+(new Date()).getTime().toString();
		zzajax("post", url, arg, function(data) {
			var j = JSON.parse(data);
			if (j) {
				var err = j.err;
				var errkey = j.errkey;
				if (err == "true") {
					if (j.type == "invite") {
						$(".c-red").html(errkey);
					}
				} else {
					if (j.type == "invite") {
						$(".c-red").html("");
						loaddata("http://app.zz91.com/invite/invite.html?suc=1&t="+(new Date()).getTime().toString());
					}
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
		return false;
	}
}
var wgtVer=null;
var checkUrl="http://app.zz91.com/app/version.txt";
var wgtUrl="http://app.zz91.com/app/zz91-1.3.0.apk";
if(window.plus){
	plus.runtime.getProperty(plus.runtime.appid,function(inf){
		//wgtVer=inf.version;
		//plus.nativeUI.toast("当前应用版本："+wgtVer);
		//checkUpdate()
	});
}
var installfirst=null;
function checkUpdate(){
	if (installfirst){
		return;
	}
	installfirst=1;
	wgtVer=plus.runtime.version;
	//plus.nativeUI.toast("数据更新中...");
	//plus.nativeUI.toast("检测更新...");
	var xhr=new XMLHttpRequest();
	xhr.onreadystatechange=function(){
		switch(xhr.readyState){
			case 4:
			//plus.nativeUI.closeWaiting();
			if(xhr.status==200){
				//console.log("检测更新成功："+xhr.responseText);
				var newVer=xhr.responseText;
				if(wgtVer&&newVer&&(wgtVer!=newVer)){
					downWgt();	// 下载升级包
				}else{
					plus.nativeUI.toast("无新版本可更新！"+newVer);
				}
			}else{
				//console.log("检测更新失败！");
				plus.nativeUI.toast("检测更新失败！");
			}
			break;
			default:
			break;
		}
	}
	xhr.open('GET',checkUrl);
	xhr.send();
}
// 下载wgt文件

function downWgt(){
	plus.nativeUI.toast("下载更新文件中...");
	plus.downloader.createDownload( wgtUrl, {filename:"_doc/update/"}, function(d,status){
		if ( status == 200 ) { 
			//console.log("下载wgt成功："+d.filename);
			installWgt(d.filename);	// 安装wgt包
		} else {
			//console.log("下载wgt失败！");
			plus.nativeUI.toast("下载更新程序失败！");
		}
		//plus.nativeUI.closeWaiting();
	}).start();
}
// 更新应用资源
function installWgt(path){
	plus.nativeUI.toast("安装应用更新文件中...");
	plus.runtime.openFile("_doc/update/zz91-1.3.0.apk", {}, function(e) {
		plus.nativeUI.alert("升级失败：" + e.emssage);
	});
//	plus.runtime.install(path,{},function(){
//		plus.nativeUI.closeWaiting();
//		//console.log("安装wgt文件成功！");
//		plus.nativeUI.alert("ZZ91应用程序已经更新完成！立即重启应用",function(){
//			plus.runtime.restart();
//		});
//	},function(e){
//		//plus.nativeUI.closeWaiting();
//		//console.log("安装wgt文件失败["+e.code+"]："+e.message);
//		plus.nativeUI.toast("安装更新文件失败！");
//	});
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
		var title = encodeURIComponent('中国环保网');
		           //http://pos.baidu.com/acom?adn=1&at=97&aurl=&cad=1&ccd=24&cec=UTF-8&cfv=18&ch=0&col=zh-CN&conOP=0&cpa=1&dai=1&dis=0&ltr=&lunum=6&n=90027019_cpr&pcs=1600x746&pis=10000x10000&ps=0x0&psr=1600x900&pss=1600x0&qn=b16741b193c4549f&rad=&rsi0=746&rsi1=187&rsi5=4&rss0=&rss1=&rss2=&rss3=&rss4=&rss5=&rss6=&rss7=&scale=20.5&skin=mobile_skin_white_red&td_id=2340825&tn=template_inlay_all_mobile&tpr=1444143680033&ts=1&xuanting=0&tt=1444143680015.20.305.311&dtm=BAIDU_DUP2_SETJSONADSLOT&dc=2&di=u2340825&ti=%E4%B8%AD%E5%9B%BD%E7%8E%AF%E4%BF%9D%E7%BD%91&wt=1&distp=1001&conW=746&conH=187
		var url = 'http://pos.baidu.com/acom?adn=1&at=97&aurl=&cad=1&ccd=24&cec=UTF-8&cfv=18&ch=0&col=en-US&conOP=0&cpa=1&dai=1&dis=0&ltr=&lunum=6&n=99099160_cpr&pis=10000x10000&ps=0x0&qn=31f2f2a7de233256&rad=&rsi5=4&rss0=&rss1=&rss2=&rss3=&rss4=&rss5=&rss6=&rss7=&scale=20.3&skin=mobile_skin_white_blue&td_id=2340825&tn=template_inlay_all_mobile&tpr=1436841400149&ts=1&xuanting=0&tt=1436841400136.14.87.89&dtm=BAIDU_DUP2_SETJSONADSLOT&dc=2&wt=1&distp=1001';
		url += '&conW='+width+'&conH='+adHeight+'&ltu='+ltu;
		url += '&di=u2340825';//广告id
		url += '&pcs='+width+'x'+height;
		url += '&psr='+width+'x'+height;
		url += '&pss='+width+'x0';
		url += '&rsi0='+width+'&rsi1='+adHeight;
		url += '&ti='+title;
		
		
		var adBottom = mui.os.ios?('-'+adHeight+'px'):'0';
		
		var ad = plus.webview.create(url,'ad',{height:adHeight+'px',bottom:adBottom});
		//目前Android平台不支持子webview的setStyle动画，因此分平台处理；
		if(mui.os.ios){
			//为了支持iOS平台左侧边缘滑动关闭页面，需要append进去；
			plus.webview.currentWebview().append(ad);
			ad.addEventListener('loaded',function () {
				ad.setStyle({
					bottom:'0',
					transition: {
						duration: 150
					}
				});
			});
		}else{
			ad.addEventListener('loaded',function () {
				ad.show('slide-in-bottom');
			});
		}
		
		ad.appendJsFile('_www/js/ad.js');
		
		//设置主页面的底部留白，否则会被遮住；
		document.querySelector('.mui-content').style.paddingBottom = adHeight + 'px';
	}
});
function openwebad(weburl) {
	plus.runtime.openURL(weburl);
}
//下载新的app
function downloadnewapp() {
	plus.runtime.launchApplication({
		pname: "com.zz91.app2",
		extra: {
			url: "http://m.zz91.com"
		}
	}, function(e) {
		$("#mainbody").html("<div class=midload>ZZ91再生网app已全新改版</div>");
		$(".mui-bar").css("display","none");
		plus.ui.confirm("ZZ91再生网app已全新改版，请更新最新版1。", function(i) {
			if (0 == i.index) {
				var appUrl = zzweburl + "/app/zz91-1.3.0.apk?" + (new Date()).getTime().toString();
				//mui.toast('下载新版应用中...');
				openwebad("http://m.zz91.com/app.html");
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