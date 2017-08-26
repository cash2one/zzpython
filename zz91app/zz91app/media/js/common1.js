//登陆
var logincheck=null;
function zz91login(frm) {
	if (logincheck){return;}
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

	mui.get("http://app.zz91.com/loginof.html?" + arg, arg, function(data) {
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

function viewcompanycontact(url, urlrequest) {
	requestquery(url, urlrequest)
}

function regfunction(frm) {
	var checkflag = 0;
	var checklist = ""
	var arg = "";
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
	mui.post("http://app.zz91.com/regsave.html", arg, function(data) {
		var j = JSON.parse(data);
		var err = j.err;
		
		var errkey = j.errkey;
		
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
var wgtVer=null;
var checkUrl="http://apptest.zz91.com/app/version.txt";
var wgtUrl="http://apptest.zz91.com/app/zz91.wgt";
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
	plus.runtime.install(path,{},function(){
		plus.nativeUI.closeWaiting();
		//console.log("安装wgt文件成功！");
		plus.nativeUI.alert("ZZ91应用程序已经更新完成！立即重启应用",function(){
			plus.runtime.restart();
		});
	},function(e){
		//plus.nativeUI.closeWaiting();
		//console.log("安装wgt文件失败["+e.code+"]："+e.message);
		plus.nativeUI.toast("安装更新文件失败！");
	});
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
		plus.ui.confirm("ZZ91再生网app已全新改版，请更新最新版2。", function(i) {
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