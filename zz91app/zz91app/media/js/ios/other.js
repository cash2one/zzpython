var jsstr;
var loadnum=1;
var messagenum=0;
var zzweburl="http://app.zz91.com";
var loadfirst=true
function loadfirsthtml() {
	if (loadfirst==false){
		return;
	}
	loadfirst=false;
	zzajax("get", zzweburl+"/top.html", '', function(data) {
		var apptop = document.getElementById("apptop");
		if (apptop) {
			apptop.innerHTML = data;
		}
	}, '');
	var userimei=plus.device.imei;
	appsystem = "iOS";
	clientid=plus.device.uuid;
	if (!clientid){
		clientid = "No" + (new Date()).getTime().toString();
	}
	zzajax("get",zzweburl+"/logininfo1.html?appid=" + clientid + "&appsystem=" + appsystem+"&userimei="+userimei, '',function(data) {
		var j = JSON.parse(data);
		company_id = j.company_id;
		plus.storage.removeItem("companyid");
		plus.storage.setItem("companyid", company_id);
		netstatus = 1;
		gotourl("/index_ios.html?iosapp=1&iosindex=1", "newindex");
	}, function() {
		var pcontent = document.getElementById("errcontent");
		var mainbody = document.getElementById("mainbody");
		if (pcontent && mainbody) {
			pcontent.style.display = "";
			mainbody.style.display = "none";
			return false;
		}
		company_id=0;
	});
	
}
function openhttpurl(furl){
	plus.runtime.openURL(furl);
}
function plusReady() {
	if (window.plus){
		visitoncode=plus.runtime.version;
		appsystem = "iOS";
		//clientid=plus.device.uuid;
		//alert(clientid)
		if (winflag == 1) {
			loadfirsthtml();
		}
		if (winflag == 2) {
			//loaddata(nowherf);
		}
		plus.storage.setItem("clientid",clientid);
	}
}

isJson = function(obj) {
	var isjson = typeof(obj) == "object" && Object.prototype.toString.call(obj).toLowerCase() == "[object object]" && !obj.length;
	return isjson;
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
	chongzhi:function(furl) {
		if (appsystem=="iOS"){
			gotourl(furl,'blank');
			//requestquery("http://app.zz91.com/qianbao/chongzhi.html","");
		}else{
			gotourl(furl,'blank');
		}
	},
	openadurl:function(furl) {
		plus.runtime.openURL(furl);
	},
	name:1
};
var myrc = {
	favoritedel: function(id, obj) {
		var btnArray = ['确定', '取消'];
		mui.confirm('确认要删除吗？', '提示', btnArray, function(e) {
			if (e.index == 0) {
				var arg = "company_id=" + company_id;
				arg += "&id=" + id;
				zzajax("post",zzweburl+"/myrc/favoritedel.html",arg, function(data) {
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
		
		zzajax("get",url+"?"+arg,arg, function(data) {
			if (data!=""){
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
							loaddata(zzweburl+"/forgetpasswdpage.html?mobile=" + mobile + "&account=" + account + "&clientid=" + clientid + "&step=" + step+"&t="+(new Date()).getTime().toString());
						}
					}
				}
			}else{
				plus.ui.alert("请输入账号！")
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
					opener.evalJS('regloadbody(' + company_id + ');');
				}
				var mainwin=plus.webview.getWebviewById( "HBuilder" );
				if (mainwin){
					mainwin.evalJS('regloadbody(' + company_id + ');');
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
			
			if (company_id=="0"){
				messagescount.style.display = "none";
			}
		}
		if (num){
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
			if (company_id=="0"){
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
	htmldown:function(html){
		var dtask = null;
		if (dtask) {
			return;
		}
		var durl = zzweburl+"/app/html/index.html";
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

//来电宝查看

function lookfirst(cid, id) {
	openoverlay('', '查看未接来电', '<br /><font color=#f00>提醒</font><br />查看该未接来电将扣除10元费用.<br />确定要查看吗？<br /><input type=button value=\'确定查看\' id=\'mobilebutton\' class=\'mui-btn mui-btn-danger\' onclick=lookcontact(' + cid + ',' + id.toString() + ') /></form><br /><br /></div>', 170, '');
}

function lookcontact(cid, id) {
	mui.get(zzweburl+"/ldb_weixin/lookcontact.html?id=" + id.toString() + "&company_id=" + cid.toString(), '',
		function(data) {
			if (data != "err\n" && data != "" && data != "err") {
				$("#lst-phone" + id.toString()).html(data);
				closeoverlay();
			} else {
				$(".mainlist").html("<br />您的帐户余额不足10元，请充值后查看！<br /><br /><button class='mui-btn mui-btn-green' onclick='gotourl(\"/ldb_weixin/balance.html\",\"blank\");closeoverlay();'>点此立即充值！</button>")
			}
		});
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
function loadcompanyid(cid) {
	company_id = cid;
}
function loginloadbody(cid) {
	company_id = cid;
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
	var arg="username=" + username;
	arg += "&passwd=" + passwd;
	arg += "&appid=" + clientid;
	arg += "&loginflag=1";
	arg += "&appsystem=" + appsystem;
	nWaiting = plus.nativeUI.showWaiting();
	mui.get(zzweburl+"/loginof.html?"+arg, arg, function(data) {
		var j = JSON.parse(data);
		if (j && j.err) {
			if (j.err == "false") {
				company_id = j.result;
				
				if (tourl){
					tourl = tourl.replace("company_id=0", "company_id=" + company_id);
					if (tourl != "") {
						nowurl = tourl;
						nowwintype = "index";
						if (nWaiting) {
							nWaiting.close();
						}
						loaddata(tourl)
					}
					
				}
				loginloadbody(company_id)
				var wobj = plus.webview.currentWebview();
				plus.storage.removeItem("companyid");
				plus.storage.setItem("companyid", company_id);
				if (wobj) {
					var opener = wobj.opener();
					if (opener) {
						//opener.evalJS('loginloadbody(' + company_id + ');');
					}
				}
				
				if (tourl == "") {
					closewindow();
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
	}, function(data) {
		if (nWaiting) {
			nWaiting.close();
		}
	});
	return false;
}

var msgchickurl="";
// 监听plusready事件  
document.addEventListener("plusready", function() {
	// 监听点击消息事件
	plus.push.addEventListener("click", function(msg) {
		if (msgchickurl==""){
			gotourl(msg.payload,"messages");
			msgchickurl=msg.payload;
		}
		if (msg.payload!=msgchickurl){
			msgchickurl="";
		}
	}, false);
	// 监听在线消息事件
	plus.push.addEventListener("receive", function(msg) {
		if (msg.aps) { // Apple APNS message

		} else {
	
		}
	}, false);
	
	
}, false);

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
//打开 web 的url
function openweburl(url) {
	if (wc) {
		return;
	}
	url = url.replace("&", "TandT").replace("?", "wenhao")
	wc = plus.webview.create("/blank.html?url2="+url+"&wintype=" + wintype + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode, "side", {
		top: "45px",
		width: "100%",
		popGesture: "none"
	});
	// 侧滑页面加载后显示（避免白屏）
	wc.addEventListener("loaded", function() {
		wc.show("slide-in-right", 200);
	}, false);
}
//头部导航
function navlink(url, wintype, obj) {
	$(".navtop ul li").removeClass();
	obj.className = "on";
	if (company_id == 0 && wintype=="messagelist") {
		jsstr="gotourl('"+url+"','blank')";
		jsstr=escape(jsstr);
		gotourl("/login/?jsstr="+jsstr, "blank");
	} else {
		gotourl(url, wintype);
	}
}
function payopen(paytype){
	window.scrollTo(0, 0);
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("数据加载中，请稍候......");
	}else{
		return;
	}
	ws=plus.webview.currentWebview();
	var userimei=plus.device.imei;
	var weburl=zzweburl+"/qianbao/chongzhi.html?company_id="+company_id.toString()+"&appsystem="+appsystem+"&paytype="+paytype+"&userimei="+userimei.toString()+"&ttt="+(new Date()).getTime().toString()
	embed=plus.webview.create(weburl,"embed",{top:"45px",bottom:"0px"});
	ws.append(embed);
	embed.loadURL(weburl);
	if (nWaiting) {
		nWaiting.close();
	}
}
//举报
function jubao(furl,querylist){
	var chk_value =[];
	$('input[name="report"]:checked').each(function(){    
		chk_value.push($(this).val());    
	});
	if (chk_value==[] || chk_value==''){
		plus.ui.alert("请选择你要举报的类目！");
		return false;
	}
	//alert(furl+querylist+"&chk_value="+chk_value)
	requestquery(furl,querylist+"&chk_value="+chk_value);
}

//生意管家供求列表
function myrcproducts(frm,url){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	proid="0"
	for (var i = 0; i < frm.length; i++) {
		var objinput = frm[i];
		var objtype = objinput.type;
		var objvalue = objinput.value;
		var objname = objinput.name;
		
		if(objname!=""){
			if (objinput.type == "checkbox") {
				if (objinput.checked == true) {
					proid += "," + objvalue;
				}
			} 
		}
	}
	var arg={
		company_id:company_id,
		proid:proid
	};
	mui.post(url, arg,function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		if (err == "true") {
			plus.ui.alert(errkey);
		} else {
			if (j.type){
				//供求刷新
				//if (j.type=="proreflush"){
					loaddata(nowherf);
				//}
			}
		}
		if (nWaiting) {
			nWaiting.close();
		}
	});
	return false;
}
function editpro(frm,url){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg="";
	arg += "proid="
	for (var i = 0; i < frm.length; i++) {
		var objinput = frm[i];
		var objtype = objinput.type;
		var objvalue = objinput.value;
		var objname = objinput.name;
		
		if(objname!=""){
			if (objinput.type == "checkbox") {
				if (objinput.checked == true) {
					arg +=  objvalue;
					gotourl('/products_update/?'+arg,'blank');
					if (nWaiting) {
						nWaiting.close();
					}
					break
				}
			} 
		}
		
	}
	if (nWaiting) {
		nWaiting.close();
	}
}
var _openrequest=null;
function requestquery(furl,querylist){
	if (_openrequest){
		return;
	}
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg="company_id="+company_id.toString()+"&clientid="+clientid+"&appsystem="+appsystem+querylist;
	//alert(furl+"?"+arg)
	if (furl == "http://app.zz91.com/favorite/"){
		apostye="post"
	}else{
		apostye="get"
	}
	
	zzajax(apostye,furl+"?"+arg, '',function(data) {
		if (data=="err"){
			if (nWaiting) {
				nWaiting.close();
			}
		}
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		_openrequest=null;
		
		if (err == "true") {
			if (j.type=="viewcontact"){
				closeoverlay();
				openfloatdiv(event,'bal');
				if (nWaiting) {
					nWaiting.close();
				}
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
						if (nWaiting) {
							nWaiting.close();
						}
						break;
					case "viewcontact":
						loaddata(nowherf);
						if (nWaiting) {
							nWaiting.close();
						}
						closeoverlay();
						break;
					case "pro_report":
						closeoverlay();
						openfloatdiv(event,'tippOff');
						if (nWaiting) {
							nWaiting.close();
						}
						break;
					default:
						closeoverlay();
				}
				
			}else{
				if (nWaiting) {
					nWaiting.close();
				}
			}
		}
		
		
	},function(){
		if (nWaiting) {
			nWaiting.close();
		}
	});
	return false;
}

//删除邀请回复
function mycommunitydel(post_id,ptype,pid){
	document.getElementById("pid").value=pid;
	document.getElementById("ptype").value=ptype;
	document.getElementById("post_id").value=post_id;
	openoverlay('', '确实要删除吗？', 0, 200, '.mycommunitydel');
}

//图片上传
var server = zzweburl+"/tradeimgupload.html";
var files = [];
var index = 1;
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
// 拍照添加文件

function appendByCamera() {
		plus.camera.getCamera().captureImage(function(p) {
			upload(p);
		});
	}
	// 从相册添加文件

function appendByGallery() {
		plus.gallery.pick(function(p) {
			upload(p)
		});
	}
	// 产生一个随机数

function getRandid() {
	//alert(document.getElementById("randid").value)
	return document.getElementById("randid").value;
	//return Math.floor(Math.random() * 100000000 + 10000000).toString();
}
//发布供求弹窗选择
function getselectvalue(obj){
	var selectname=obj.parentNode.title;
	document.getElementById(selectname).value=obj.title;
	closeoverlay();
}
function getpricevalue(obj){
	var selectname=obj.parentNode.title;
	var pricevalue=obj.parentNode.childNodes[1].value;
	//alert(pricevalue)
	document.getElementById(selectname).value=pricevalue;
	closeoverlay();
}
//消息提醒
function getmessagesnum(cid) {
	if (cid && cid.toString()!="0") {
		zzajax("get",zzweburl+"/messagescount.html?company_id=" + cid.toString()+"&ttt="+(new Date()).getTime().toString(),'',
			function(data) {
				var j = JSON.parse(data);
				if (isJson(j)) {
					var count = j.count;
					//count=2;
					if (count > 0) {
						var messagescount = document.getElementById("messagescount");
						if (messagescount) {
							messagescount.innerHTML = count;
							messagescount.style.display = "block";
							messagescount.style.position="absolute";
							messagescount.style.left="70%";
							messagescount.style.top="0px";
						}
						plus.runtime.setBadgeNumber( count );
					}else{
						plus.runtime.setBadgeNumber( 0 );
					}
				}else{
					plus.runtime.setBadgeNumber( 0 );
				}
			},'');
	}
}
//全部标为已读
function updatemessagesall(){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("数据更新中...");
	}
	var arg = "company_id=" + company_id;
	arg += "&clientid=" + clientid;
	mui.get(zzweburl+"/messagesreadall.html?" + arg, '', function(data) {
		var j = JSON.parse(data);
		gotourl(nowurl,'messages')
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
		plus.ui.alert("已经全部标为已读");
	}, function(data) {
		plus.ui.alert("系统错误！请稍后重试.");
	});
	if (nWaiting) {
		nWaiting.close();
	}
	return false;
}
function loadcompanyid(cid){
	company_id = cid;
}
//回复楼主
function backbbsform(frm){
	if (company_id==0){
		gotourl("/login/", "blank");
	}else{
		return submitfrm(frm,zzweburl+'/huzhu_replay/');
	}
}
function bbsformreply(replayid, tocompany_id){
	if (company_id==0){
		gotourl("/login/", "blank");
	}else{
		huzhureplay(replayid, tocompany_id)
	}
}
function zz91search(frm, url, wintype) {
	var keywords = frm.searchtext.value;
	gotourl(url + keywords+"&iosapp=1", wintype);
}
function bottomlabel(m){
	bottomlabelvalue=m;
	var bottomlabelname=document.getElementById("bottomlabel"+m.toString())
	if (bottomlabelname){
		bottomlabelname.className="mui-tab-item mui-active"
	}
	if (company_id!=0 && company_id){
		getmessagesnum(company_id)
	}
	tongji();
}
function dialtel(telphone) {
	plus.device.dial(telphone, false);
	telclick("http://m.zz91.com/trade/telclicklog.html?tel=" + telphone + "&pagefrom=apptrade&company_id="+company_id.toString());
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
var arrtop=document.getElementById("arrtop");
if (arrtop){
	arrtop.style.display="";
}
function scrolltop() {
	mui.scrollTo(0, 500);
	var arrtop = document.getElementById("arrtop");
	if (arrtop) {
		arrtop.style.display = "";
	}
}
//链接通用函数
(function($) {
	$.ready(function() {
		$('body').on('tap', 'a', function(e) {
			var id = this.getAttribute('href');
			var wintarget = "blank";
			if (nowurl){
				if (nowurl.indexOf("/priceindex/") >= 0) {
					//wintarget = "price"
				}
				if (nowurl.indexOf("/category/") >= 0) {
					wintarget = "trade"
				}
			}
			if (id && id.substring(0, 1) != "#") {
				if (window.plus) {
					if (id.indexOf("javascript:") < 0) {
						if (id.indexOf("tel:")>=0){
							eval("dialtel("+id.replace("tel:","")+")")
						}else{
							if (appsystem=="iOS"){
								gotourl(id, wintarget);
							}else{
								gotourl(id, wintarget);
							}
						}
					} else {
						if (id.indexOf("tel:")>0){
							eval("dialtel("+id.replace("tel:","")+")")
						}else{
							if (appsystem=="iOS"){
								eval(id);
							}else{
								eval(id);
							}
						}
					}
				}
			}
		});
	});
})(mui);
//邀请码
function inviteapp(frm){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
		var url=zzweburl+"/invite/invite_save.html";
		var arg="company_id="+frm.company_id.value;
		arg+="&code="+frm.code.value;
		arg+="&clientid="+frm.clientid.value;
		arg+="&t="+(new Date()).getTime().toString();
		
		zzajax("get", url+"?"+arg, arg, function(data) {
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
						if (nWaiting) {
							nWaiting.close();
						}
						loaddata(zzweburl+"/invite/invite.html?suc=1&t="+(new Date()).getTime().toString());
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
		
		if (nWaiting) {
			nWaiting.close();
		}
		return false;
	}
}
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
		var j = JSON.parse(data);
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
					plus.storage.setItem("company_id", company_id);
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
function tongji(){
	var turl=zzweburl+"/tongji/t.html?t="+ (new Date()).getTime().toString()+"&clientid=" + clientid + "&appsystem=" + appsystem;
	if (nowherf){
		turl+="&url="+nowherf.replace("&","^and^");
	}
	turl+="&visitoncode="+visitoncode
	turl+="&company_id="+company_id;
	zzajax("get",turl, '',function(data) {
	}, function() {
	});
}
$(document).ready(function(e) {
	tongji();
});
//修改密码
function modpasswd(frm) {
	var oldCold = frm.oldcold.value;
	var newCold = frm.newcold.value;
	var sedCold = frm.sedcold.value;
	if (!oldCold) {
		plus.ui.alert("原密码不能为空");
		frm.oldcold.focus();
		return;
	}
	if (!newCold) {
		plus.ui.alert("新密码不能为空");
		frm.newcold.focus();
		return;
	}
	if (!sedCold) {
		plus.ui.alert("重复密码不能为空");
		frm.sedcold.focus();
		return;
	}
	if (oldCold == newCold) {
		//document.getElementById('newcold').parentNode.getElementsByTagName('p')[0].style.visibility = "visible"
		plus.ui.alert("新密码不能和老密码相同！");
		return;
	}
	if (sedCold != newCold) {
		//document.getElementById('sedcold').parentNode.getElementsByTagName('p')[0].style.visibility = "visible"
		plus.ui.alert("重复密码输入错误！");
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

function loadmorep(obj, url) {
	if (url.indexOf("?") < 0) {
		url = url + "?page=" + blankpage.toString() + "&t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
	} else {
		url = url + "&page=" + blankpage.toString() + "&t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
	}
	obj.style.display = "";
	obj.innerHTML = "正在加载中...";
	if (url != "" && url != null && (obj.style.display == "" || obj.style.display == "block")) {
		zzajax("get", "http://app.zz91.com/" + url, '', function(data) {
			if (data != "") {
				var newNode = document.createElement("div");
				newNode.innerHTML = data;
				obj.parentNode.insertBefore(newNode, obj);
				if (obj) {
					blankpage += 1;
					obj.innerHTML = "<span class='mui-icon mui-icon-down'></span><span>点此加载更多</span>";
				}
			} else {
				obj.style.display = "none";
			}
		}, function() {
			obj.innerHTML = "<span class='mui-icon mui-icon-down'></span><span>点此加载更多</span>";
		});
	}
}
var btnArray = ['确定', '取消'];
mui.confirm('ZZ91再生网app已全新改版，请更新最新版！', '提示', btnArray, function(e) {
	if (e.index == 0) {
		openhttpurl("https://itunes.apple.com/us/app/zz91zai-sheng-wang/id944851616?l=zh&ls=1&mt=8")
	}
});