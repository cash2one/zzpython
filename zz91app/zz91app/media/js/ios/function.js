if (winflag==2){
	var request = {
		QueryString: function(val) {
			var uri = window.location.search;
			var re = new RegExp("" + val + "=([^&?]*)", "ig");
			return ((uri.match(re)) ? (uri.match(re)[0].substr(val.length + 1)) : null);
		}
	}
	if (!nowherf){
		var nowherf = request.QueryString("url2");
	}
	if (nowherf){
		nowherf = nowherf.replace("TandT", "&").replace("wenhao", "?");
		nowherf = nowherf.replace(".com//",".com/");
	}
	
	var url=nowherf;
	var wintype = request.QueryString("wintype");
	if (!company_id){var company_id = request.QueryString("company_id");}
	if (!company_id){var company_id=0}
	if (!clientid){var clientid=request.QueryString("clientid")}
	if (!clientid){var clientid=""}
	var appsystem = request.QueryString("appsystem");
	if (!appsystem){appsystem="iOS"}
	var visitoncode = request.QueryString("visitoncode");
}
if (winflag==1){
	var nowherf="/index_ios.html";
	var url=nowherf;
	var company_id=0;
}

if ((nowherf=="/info.html" || nowherf=="/huzhupost/" || nowherf=="/order/price.html" || nowherf=="/order/business.html") && company_id==0){
	nowherf="/login/?tourl="+nowherf;
}


var nowwintype;
var nWaiting;

var blankpage = 2;
var indexwin = new Array();
var winarr = new Array();
var loadnum = 1;
var nowurl;
var isback = 1;

var winInterval = 600000;
var Intent = null,
	BitmapFactory = null;
var main = null;
var msgchickurl = "";
var minwindow;
var reloadnum=1;
var oldaddress;
var nowaddress;
if (window.plus) {
	//appsystem = plus.os.name;
	visitoncode = plus.runtime.version;
}
var keywords;
var dwtype;
var bottomlabelvalue=1;
var rt;

function reloadiosapp(){
	var netstats = getnetstats();
	var pcontent = document.getElementById("errcontent");
	var mainbody = document.getElementById("mainbody");
	if (netstats != "未连接网络") {
		if (pcontent && mainbody) {
			pcontent.style.display = "none";
			mainbody.style.display = "";
			return true;
		}else{
			return false;
		}
	} else {
		if (pcontent && mainbody) {
			pcontent.style.display = "";
			mainbody.style.display = "none";
			return false;
		}else{
			return false;
		}
	}
}
	//判断网络环境

function getnetstats() {
	var types = {};
	var netstatst="未连接网络";
	if (window.plus){
		types[plus.networkinfo.CONNECTION_UNKNOW] = "未知";
		types[plus.networkinfo.CONNECTION_NONE] = "未连接网络";
		types[plus.networkinfo.CONNECTION_ETHERNET] = "有线网络";
		types[plus.networkinfo.CONNECTION_WIFI] = "WiFi网络";
		types[plus.networkinfo.CONNECTION_CELL2G] = "2G蜂窝网络";
		types[plus.networkinfo.CONNECTION_CELL3G] = "3G蜂窝网络";
		types[plus.networkinfo.CONNECTION_CELL4G] = "4G蜂窝网络";
		netstatst = types[plus.networkinfo.getCurrentType()];
	}
	return netstatst;
}

//退出
function loginout() {
	company_id=0;
	//plus.storage.clear();
	//alert(plus.storage.getItem("companyid"))
	plus.storage.removeItem("companyid");
	plus.storage.setItem("companyid", company_id);
//	var wvs=plus.webview.all();
//	for(var i=0;i<wvs.length;i++){
//		alert(wvs[i].id);
//		//HBuilder
//	}
	
	
	gotourl("/index_ios.html?iosapp=1&iosindex=1", "newindex");
	
//	var btnArray = ['确定', '取消'];
//	mui.confirm('确定要退出吗？', '提示', btnArray, function(e) {
//		if (e.index == 0) {
//			plus.runtime.quit();
//		}
//	});
}
var zzajax = function(method, url, arg, successCallback, errorCallback) {
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
function zz91search(frm, url, wintype) {
		var keywords = frm.searchtext.value;
		gotourl(url + keywords+"&iosapp=1", wintype);
}
//检查版本
var serverurl = "http://app.zz91.com/js/update.json?t=" + Math.ceil(new Date / 3600000),
	keyUpdate = "updateCheck", //取消升级键名
	keyAbort = "updateAbort", //忽略版本键名
	checkInterval = 864000, //升级检查间隔，单位为ms,7天为7*24*60*60*1000=60480000, 如果每次启动需要检查设置值为0
	dir = null;
var sjcheck = false;
function ioscheckupdate(){
	sjcheck = false;
	checkUpdate();
}
function checkUpdate() {
	if (sjcheck) {
		return;
	}
	sjcheck = true
	// 判断升级检测是否过期
	var lastcheck = plus.storage.getItem(keyUpdate);
	if (lastcheck) {
		if (document.getElementById("visiton")) {
			sjcheck = false;
		} else {
			var dc = parseInt(lastcheck);
			var dn = (new Date()).getTime();
			if (dn - dc < checkInterval) { // 未超过上次升级检测间隔，不需要进行升级检查
				if (document.getElementById("visiton")) {
					if (appsystem == "iOS") {
						plus.ui.alert("已是最新版本");
					}
				}
				return;
			} else {
				//sjcheck = false;
			}
		}

		// 取消已过期，删除取消标记
		plus.storage.removeItem(keyUpdate);
	}
	zzajax("get", serverurl, '', function(data) {
		var j = JSON.parse(data);
		//sjcheck = false;
		checkUpdateData(j)
	}, '');
}
	/**
	 * 检查升级数据
	 */

function showheader(wintype) {

}

function navlink(url, wintype, obj) {
	$(".navtop ul li").removeClass();
	obj.className = "on";
	gotourl(url, wintype);
}

function checkUpdateData(j) {
		var curVer = plus.runtime.version,
			inf = j["iOS"];
		if (inf) {
			var srvVer = inf.version;
			// 判断是否需要升级
			if (compareVersion(curVer, srvVer)) {
				// 提示用户是否升级
				plus.ui.confirm(inf.note, function(i) {
					if (0 == i) {
						minwindow = true;
						$("#downloadwindow").lightbox_me({
							overlaySpeed: 0,
							lightboxSpeed: 0,
							centered: true,
							onLoad: function() {
								minwindow = "downloadwindow";
							},
							onClose: function() {
								minwindow = null;
							}
						});
						downloader.down(inf.url, srvVer);
						plus.storage.setItem(keyUpdate, (new Date()).getTime().toString());
					} else {
						plus.storage.setItem(keyUpdate, (new Date()).getTime().toString());
					}
				}, "建议您更新最新版本", ["立即更新", "取　　消"]);
			} else {
				if (document.getElementById("visiton")) {
					if (appsystem == "iOS") {
						plus.ui.alert("已是最新版本");
					} else {
						mui.toast('已是最新版本');
					}
				}
				//mui.toast('已是最新版本');
			}
		}
	}
	/**
	 * 比较版本大小，如果新版本nv大于旧版本ov则返回true，否则返回false
	 * @param {String} ov
	 * @param {String} nv
	 * @return {Boolean}
	 */

function compareVersion(ov, nv) {
	if (!ov || !nv || ov == "" || nv == "") {
		return false;
	}
	var b = false,
		ova = ov.split(".", 4),
		nva = nv.split(".", 4);
	for (var i = 0; i < ova.length && i < nva.length; i++) {
		var so = ova[i],
			no = parseInt(so),
			sn = nva[i],
			nn = parseInt(sn);
		if (nn > no || sn.length > so.length) {
			return true;
		} else if (nn < no) {
			return false;
		}
	}
	if (nva.length > ova.length && 0 == nv.indexOf(ov)) {
		return true;
	}
}

//页面跳转同意函数
function gotourl(url, wintype) {
	if (wintype != "blank") {
		nowwintype = wintype;
	}
	checkUpdate();
	blankpage = 2;
	var trueurl = url;
	appsystem="iOS";
	if (plus.storage.getItem("companyid")==null || plus.storage.getItem("companyid")=="0"){
		if (company_id){
			plus.storage.removeItem("companyid");
			plus.storage.setItem("companyid", company_id);
		}
	}else{
		company_id=plus.storage.getItem("companyid");
		plus.storage.removeItem("companyid");
		plus.storage.setItem("companyid", company_id);
	}
	if (company_id==null){company_id=0};
	if (company_id.toString() == "0") {
		if (wintype == "laidianbao" || wintype == "myrc" || wintype == "qianbao" || wintype == "messages" || wintype == "order") {
			url = "/login/?tourl=" + url + "&wintarget=" + wintype;
			wintype = "login";
		}
	}
	url = url.replace("/companyinfo/?company_id=", "/companyinfo/?forcid=");
	if (wintype == "blank" || wintype == "reg" || wintype == "order" || wintype == "login") {
		url = url.replace("&", "TandT").replace("?", "wenhao");
		mui.openWindow({
			id: url,
			url: "/blank.html?url2=" + url + "&wintype=" + wintype + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode,
			preload: false //TODO 等show，hide事件，动画都完成后放开预加载
		});
		return;
	}
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("");
	}
	var backwin = 1;
	if (url.indexOf("http://app.zz91.com") < 0) {
		if (url.indexOf("?") < 0) {
			url = "http://app.zz91.com/" + url + "?t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		} else {
			url = "http://app.zz91.com/" + url + "&t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
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
	var content = document.getElementById("dcontent");

	if (content) {
		content.innerHTML = "<br /><br /><center class=midload><img src=images/96R.gif><br>正在为您努力加载中......<br /><br /><br /><a onclick=\"window.location.reload()\">点此重新加载</a></center>"
	}
	//plus.storage.clear();
	var backcontent = plus.storage.getItem(trueurl);
	var backcontenttime = plus.storage.getItem(trueurl + 'time');
	if (backcontent && backcontenttime && trueurl != "/messagelist/") {
		var dc = parseInt(backcontenttime);
		var dn = (new Date()).getTime();
		if (dn - dc > winInterval) { // 未超过上次升级检测间隔，不需要进行升级检查
			plus.storage.removeItem(trueurl);
			plus.storage.removeItem(trueurl + 'time');
		} else {
			//content.innerHTML=backcontent;
			if (nWaiting) {
				nWaiting.close();
			}
			window.scrollTo(0, 0);
			//return;
		}
	}
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
					if (company_id.toString()=="0"){
						iOSclosecontent();
					}
					//读取缓存数据
					if (window.plus) {
						plus.cache.calculate(function(size) {
							cachesize = parseInt(size / 1024);
							var cachediv = document.getElementById("cachesize");
							if (cachediv) {
								cachediv.innerHTML = cachesize + "KB";
							}
						});
						var visiton = document.getElementById("visiton");
						if (visiton) {
							visiton.innerHTML = "" + plus.runtime.version + "";
							visitoncode = plus.runtime.version;
						}
//						//高版本兼容问题
//						var newsnav = document.getElementById("newsnav");
//						if (newsnav) {
//							newsnav.style.display = "block";
//						}
//						var rightbutton = document.getElementById("rightbutton");
//						if (rightbutton) {
//							if (url.indexOf("/huzhuview/")>0){
//								rightbutton.style.display = "block";
//							}
//						}
						
					}
					plus.storage.setItem(trueurl, textvalue);
					plus.storage.setItem(trueurl + 'time', (new Date()).getTime().toString());
					if (nWaiting) {
						nWaiting.close();
					}
					//定位用
					dwtype=1;
					//底部导航
					bottomlabel(bottomlabelvalue);
				} else {
					loadnum += 1;
					if (loadnum <= 3) {
						gotourl(url, wintype);
					} else {
						var btnArray = ['重试加载', '取消'];
						mui.confirm('哎呀,网络不给力，点击重试加载试试！', '提示', btnArray, function(e) {
							if (e.index == 0) {
								gotourl(url, wintype);
								if (nWaiting) {
									nWaiting.close();
								}
							} else if (e.index == 1) {
								if (nWaiting) {
									nWaiting.close();
								}
							} else {
								if (nWaiting) {
									nWaiting.close();
								}
							}
							if (nWaiting) {
								nWaiting.close();
							}
						});
					}
				}
				break;
			default:
				if (nWaiting) {
					nWaiting.close();
				}
				break;
		}
	}
	xhr.open("GET", url);
	xhr.send();
	if (nWaiting) {
		nWaiting.close();
	}
	nowurl = url;
	window.scrollTo(0, 0);
}

function scrolltop() {
	mui.scrollTo(0, 500);
	var arrtop = document.getElementById("arrtop");
	if (arrtop) {
		arrtop.style.display = "none";
	}
}

function loadfirsthtml() {
	zzajax("get", "http://app.zz91.com/top.html", '', function(data) {
		var apptop = document.getElementById("apptop");
		if (apptop) {
			apptop.innerHTML = data;
		}
	}, '');
	zzajax("get","http://app.zz91.com/logininfo1.html?appid=" + clientid + "&appsystem=" + appsystem, '',function(data) {
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

function loadjavascript(url, d, t) {
	var r = d.createElement(t),
		s = d.getElementsByTagName(t)[0];
	r.async = false;
	r.src = url + '?' + (new Date()).getTime().toString();
	s.parentNode.insertBefore(r, s);
}

function telclick(url) {
	zzajax("get", url, '', function(data) {

	}, '')
}

function dialtel(telphone) {
	plus.device.dial(telphone, false);
	telclick("http://m.zz91.com/trade/telclicklog.html?tel=" + telphone + "&pagefrom=apptrade");
}

function createLocalPushMsg() {
	var options = {
		cover: false
	};
	str = ": 欢迎使用Html5 Plus创建本地消息！";
	plus.push.createMessage(str, "LocalMSG", options);
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

//商机定制
function orderclick(id) {
	var obj = $("#orderm" + id);
	var str = obj.find(".item-div-icon").css("display");
	if (str === "none") {
		obj.removeClass("item-div-style");
		obj.addClass("item-div-click");
		obj.find(".item-div-icon").css("display", "block");
		obj.find(".item_div_i").attr("checked", 'true');
	} else {
		obj.removeClass("item-div-click");
		obj.addClass("item-div-style");
		obj.find(".item-div-icon").css("display", "none");
		obj.find(".item_div_i").removeAttr("checked");
	}
	ordersubmit(document.getElementById("formorder"), "http://app.zz91.com/order/save_collect.html")
}

function closewindow() {
	closeoverlay()
	var ws = plus.webview.currentWebview();
	ws.close();
}
//加载新数据

function loaddata(url) {
	if (window.plus) {
		var nWaiting = plus.nativeUI.showWaiting();
	}
	
	if (isback == 1) {
		//winarr.push(url);
	}
	if (url.indexOf("http://app.zz91.com") < 0) {
		nowurl=url;
		if (url.indexOf("?") < 0) {
			url = "http://app.zz91.com/" + url + "?t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		} else {
			url = "http://app.zz91.com/" + url + "&t=" + (new Date()).getTime().toString() + "&company_id=" + company_id.toString() + "&clientid=" + clientid + "&appsystem=" + appsystem + "&visitoncode=" + visitoncode;
		}
	}
	if (company_id.toString() == "0") {
		if (wintype == "laidianbao" || wintype == "myrc" || wintype == "qianbao" || wintype == "messages" || wintype == "order") {
			url = "/login/?tourl=" + url + "&wintarget=" + wintype;
			wintype = "login";
		}
	}
	zzajax("get", url, '', function(data) {
		
		lendata = data.indexOf("id=\"appnavname\"");
		if (lendata > 0) {
			document.getElementById("dcontent").innerHTML = data;
			page = 2;
			if (nWaiting) {
				nWaiting.close();
			}
			var navname = document.getElementById("appnavname")
			if (navname) {
				document.getElementById("apptopname").innerHTML = navname.value;
			} else {
				document.getElementById("apptopname").innerHTML = "ZZ91再生网";
			}
			if (minwindow == null) {
				mui.scrollTo(0, 10);
			}
			//读取缓存数据
			if (window.plus) {
				plus.cache.calculate(function(size) {
					cachesize = parseInt(size / 1024);
					var cachediv = document.getElementById("cachesize");
					if (cachediv) {
						cachediv.innerHTML = cachesize + "KB";
					}
				});
				var visiton = document.getElementById("visiton");
				if (visiton) {
					visiton.innerHTML = "" + plus.runtime.version + "";
					visitoncode = plus.runtime.version;
				}
				//高版本兼容问题
//				var newsnav = document.getElementById("newsnav");
//				if (newsnav) {
//					newsnav.style.display = "block";
//				}
//				var rightbutton = document.getElementById("rightbutton");
//				if (rightbutton) {
//					if (url.indexOf("/huzhuview/") > 0) {
//						rightbutton.style.display = "block";
//					}
//				}
			}
			reloadnum = 0;
		} else {
			if (document.getElementById("apptopname")){
				document.getElementById("apptopname").innerHTML = "系统错误";
				document.getElementById("dcontent").innerHTML = "<br /><br /><center>系统错误...<br /><br /><button onclick='closewindow();' class='mui-btn mui-btn-danger' type='button'>关闭</button></center>";
			}
			if (nWaiting) {
				nWaiting.close();
			}
		}
	}, function() {
		if (reloadnum <= 3) {
			var btnArray = ['重试加载', '取消'];
			mui.confirm('哎呀,网络不给力，点击重试加载试试！', '提示', btnArray, function(e) {
				if (e.index == 0) {
					loaddata(url);
					if (nWaiting) {
						nWaiting.close();
					}
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
			reloadnum += 1;
		} else {
			plus.ui.alert("系统问题请稍后再试！");
			if (nWaiting) {
				nWaiting.close();
			}
		}
		//winarr.pop();
	});
	nowherf = url;
}
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
	wc = plus.webview.create("side.html?keywords="+searchtext.toString(), "side", {
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
//打开图片
function openbigimg(pid){
	// 防止快速点击可能导致多次创建
	if (wc) {
		return;
	}
	// 创建侧滑页面
	var wc = plus.webview.create("/img.html?pid=" + pid, "side", {
		width: "100%",
		top:"0px",
		popGesture: "none"
	});
	// 侧滑页面加载后显示（避免白屏）
	wc.addEventListener("loaded", function() {
		wc.show("slide-in-right", 200);
	}, false);
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
//供求筛选
function sidetradeloaddata(frm) {
	var wobj = plus.webview.currentWebview();
	var checkflag = 0;
	var arg = "iosapp=1";
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
//
function myFun(result) {
	var cityName = result.name;
	var searchname = cityName;
	searchname = searchname.replace("省", "");
	searchname = searchname.replace("市", "");
	plus.storage.removeItem("nowaddress");
	plus.storage.setItem("nowaddress", searchname);
}
//
function fjsearch(){
	var url = "/offerlist/?province=" + nowaddress + "&keywords="+keywords+"&iosapp=1";
	gotourl(url, 'fj');
}
//重新定位
function redingwei(){
	dwtype=1;
	redingweispan.className="mui-spinner";
	dingw();
}
//web地址定位
function dingw() {
	if (BMap){
		var myCity = new BMap.LocalCity();
		myCity.get(myFun);
		nowaddress = plus.storage.getItem("nowaddress");
	}
	if (dwtype == 1) {
		var mylocation_status = document.getElementById("mylocation_status")
		if (mylocation_status && nowaddress) {
			mylocation_status.innerHTML = nowaddress;
			redingweispan.className="mui-icon mui-icon-reload";
			dwtype = 2;
		} else {
			setTimeout(dingw, 2000);
		}
		if (nWaiting) {
			nWaiting.close();
		}
	}
}
//附近商机
function fj() {
	var url;
	if (searchtext){
		keywords=searchtext.value;
	}
	oldaddress = plus.storage.getItem("oldaddress");
	
	if (BMap){
		var myCity = new BMap.LocalCity();
		myCity.get(myFun);
		nowaddress = plus.storage.getItem("nowaddress");
		if (oldaddress != nowaddress) {
			plus.storage.setItem("oldaddress", nowaddress);
		} else {
			if (oldaddress != null && nowaddress != null) {
				url = "/offerlist/?province=" + nowaddress + "&keywords="+keywords+"&iosapp=1";
				gotourl(url, 'fj');
				return;
			}
		}
	}
	if (nowaddress == null || nowaddress == "") {
		var url = "/fj.html?keywords=" + nowaddress + "&myaddress=GPS定位中...";
	} else {
		var url = "/fj.html?keywords=" + nowaddress + "&myaddress=" + nowaddress + "";
	}
	gotourl(url, 'fj');
	dingw();
}
function bottomlabel(m){
	bottomlabelvalue=m;
	var bottomlabelname=document.getElementById("bottomlabel"+m.toString())
	if (bottomlabelname){
		bottomlabelname.className="mui-tab-item mui-active"
	}
}

//登陆
function zz91login(frm) {
	var username = frm.username.value;
	var passwd = frm.passwd.value;
	var tourl = frm.tourl.value;
	var wintarget = frm.wintarget.value;
	if (username == "" || passwd == "") {
		return false;
	}
	var arg="username=" + username;
	arg += "&passwd=" + passwd;
	arg += "&appid=" + clientid;
	arg += "&loginflag=1";
	arg += "&appsystem=" + appsystem;
	zzajax("post","http://app.zz91.com/loginof.html", arg, function(data) {
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
				
				var wobj = plus.webview.currentWebview();
				plus.storage.removeItem("companyid");
				plus.storage.setItem("companyid", company_id);
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
//登录刷新
function regloadbody(cid) {
	company_id = cid;
	plus.storage.setItem("companyid", company_id);
	if (nowurl){
		nowurl = nowurl.replace("company_id=0", "company_id=" + cid.toString());
	}else{
		nowurl="/index_ios.html";
	}
	gotourl(nowurl, "newindex");
	netstatus = 1
}
//定制提交
function ordersubmit(frm,url){
	var item=frm.item_div_i;
	arg="ordervalue=";
	var selectitem="";
	for (var i=0;i<item.length;i++){
		var objinput = item[i];
		if (objinput.checked == true) {
			selectitem+=objinput.value+",";
		}
	}
	if (selectitem){
		arg+=selectitem.substr(0,selectitem.length-1);
	}
	arg+="&collect_type="+frm.collect_type.value;
	arg+="&company_id="+company_id.toString();
	zzajax("post",url,arg,function(data){
		var j = JSON.parse(data);
		if (j && j.err) {
			if (j.err == "false") {
				
			}else {
				plus.ui.alert(j.errkey);
			}
			if (nWaiting) {
				nWaiting.close();
			}
		}
	},function(data){
		if (nWaiting) {
			nWaiting.close();
		}
	});
}
//互助回复
function huzhureplay(replayid, tocompany_id) {
	var bbs_post_reply_id = document.getElementById("bbs_post_reply_id");
	if (bbs_post_reply_id) {
		document.getElementById("bbs_post_reply_id").value = replayid;
		document.getElementById("tocompany_id").value = tocompany_id;
		if (company_id != 0) {
			openoverlay('', '回复', 0, 180, '.d-reply');
		} else {
			gotourl("/login/?tourl=","blank");
		}
	}
}
//供求留言
function tradeleavewords(pid, tocompany_id) {
	if (company_id.toString() == "0") {
		//loaddata("http://app.zz91.com/login/?tourl=" + rt);
		gotourl("/login/?tourl=","blank");
	} else {
		openoverlay('', '回复', 0, 180, '.d-leavewords');
	}
}
//收藏
function favorite(querylist) {
	if (company_id.toString() == "0") {
		gotourl("/login/?tourl=","blank");
	} else {
		var furl = "http://app.zz91.com/favorite/";
		requestquery(furl, querylist);
	}
}
//iOS去掉支付环节
function iOSclosecontent(){
	
}
	//情况缓存

function getcachefunction() {
	plus.cache.clear(function() {
		plus.ui.alert("缓存已经清除成功!");
		var cachediv = document.getElementById("cachesize");
		if (cachediv) {
			cachediv.innerHTML = "0KB";
		}
	});
}

//通用表单提交
function submitfrm(frm, url) {
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting("数据上传中......");
	}
	if (company_id.toString()=="0" && url!="http://app.zz91.com/regsave.html" && url!="http://app.zz91.com/feedbacksave.html"){
		if (nowherf){
			if (nWaiting) {
				nWaiting.close();
			}
			gotourl("/login/?tourl=","blank");
		}else{
			if (nWaiting) {
				nWaiting.close();
			}
			gotourl(nowurl, nowwintype);
		}
		return false;
	}
	var arg = {
		company_id:company_id,
		clientid:clientid,
		appsystem:appsystem,
		t:Math.ceil(new Date/3600000)
	}
	var checkflag=0;
	var checklist=""
	for (var i = 0; i < frm.length; i++) {
		var objinput = frm[i];
		var objtype = objinput.type;
		var objvalue = objinput.value;
		var objname = objinput.name;
		if(objname!=""){
			if (objinput.type == "radio" || objinput.type == "checkbox") {
				if (objinput.checked == true) {
					if (checklist.indexOf(objname)<0){
						checkflag=0;
					}
					if (checkflag==1){
						checklist += "," + objvalue;
					}else{
						checklist += "&" + objname + "=" + objvalue;
					}
				}
				checkflag=1;
			} else {
				checkflag=0;
				//arg += "&" + objname + "=" + objvalue;
				arg[objname]=objvalue
			}
		}
		
		var arrchecklist=checklist.split("&");
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
	mui.post(url, arg,function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		if (err == "true") {
			if (j.type=="regerr"){
				var errflag=j.errflag;
				var errname=j.errname;
				$(".c-red").html("");
				$("#regerr"+errflag).html(errkey);
				document.getElementById(errname).focus();
			}else{
				if (j.type=="forgetpasswd"){
					$(".c-red").html(errkey);
				}else{
					plus.ui.alert(errkey);
				}
			}
		} else {
			if (j.type){
				//发布供求成功提醒
				if (j.type=="tradesave" || j.type=="questionback" || j.type=="leavewords" || j.type=="posthuzhu"){
					openoverlay('', '提示', 0, 250, '.postsuc');
				}else{
					if(j.type=="chongzhi"){
						var payload=j.content;
						var furl="http://app.zz91.com/zz91paysubmit.html?"+payload
						//plus.runtime.openURL(furl);
					}else{
						if (j.type=="regsuc"){
							plus.ui.alert('注册成功！');
							company_id=j.company_id;
							plus.storage.setItem("companyid",company_id);
							if (window.plus) {
							    var wobj = plus.webview.currentWebview();
								
								var mainwin=plus.webview.getWebviewById( "HBuilder" );
								if (mainwin){
									mainwin.evalJS('regloadbody(' + company_id + ');');
								}
								var opener = wobj.opener();
								if (opener) {
									opener.close();
								}
								closewindow();
							}
						}else{
							
							if (j.type=="forgetpasswd"){
								var result=j.result;
								var step=j.step;
								var mobile=result.mobile;
								var account=result.account;
								loaddata("http://app.zz91.com/forgetpasswdpage.html?mobile="+mobile+"&account="+account+"&clientid="+clientid+"&step="+step);
							}else{
								if (j.type=="infosave"){
									plus.ui.alert(j.errkey);
									if (nWaiting) {
										nWaiting.close();
									}
								}else{
									if (j.type=="savecollect"){
										
									}else{
										closeoverlay();
										loaddata(nowherf);
									}
									
								}
							}
							
						}
					}
				}
			}else{
				
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
function requestquery(furl,querylist){
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg="company_id="+company_id.toString()+"&clientid="+clientid+"&appsystem="+appsystem+querylist;
	zzajax("post",furl, arg,function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
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
	},function(data){
		if (nWaiting) {
			nWaiting.close();
		}
	});
	return false;
}
function loadappbody(){
	
}
document.addEventListener("plusscrollbottom", function() {
	var pulldiv = document.getElementById("pulldiv");
	if (pulldiv) {
		loadmorep(pulldiv, pulldiv.title)
	}
}, false);