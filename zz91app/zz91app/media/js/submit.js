var ajax = function(method, url, successCallback, errorCallback, arg) {
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
	if (method == "POST") {
		xhr.send(arg);
	} else {
		xhr.send();
	}

};
//通用表单提交
function submitfrm(frm, url) {
	var arg = "";
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	arg += "company_id=" + company_id.toString();
	var checkflag=0;

	for (var i = 0; i < frm.length; i++) {
		var objinput = frm[i];
		var objtype = objinput.type;
		var objvalue = objinput.value;
		var objname = objinput.name;
		if(objname!=""){
			if (objinput.type == "radio" || objinput.type == "checkbox") {
				if (objinput.checked == true) {
					if (checkflag==1){
						arg += "," + objvalue;
					}else{
						arg += "&" + objname + "=" + objvalue;
					}
				}
				checkflag=1;
			} else {
				checkflag=0;
				arg += "&" + objname + "=" + objvalue;
			}
		}
		if (objinput.title != "" && objinput.title) {
			if (objinput.title.substring(0, 1) == "*") {
				if (objinput.value == "") {
					alert(objinput.title.substring(1));
					objinput.focus();
					if (nWaiting) {
						nWaiting.close();
					}
					return false
				}
			}
		}
		
	}

	ajax("POST", url, function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		if (err == "true") {
			alert(errkey);
		} else {
			if (j.type){
				//发布供求成功提醒
				if (j.type=="tradesave" || j.type=="questionback"){
					openoverlay('', '提示', 0, 200, '.postsuc');
				}else{
					if (j.type=="savecollect"){
						
					}else{
						closeoverlay();
						loaddata(nowherf);
					}
					
				}
			}
			//window.location.reload();
		}
		if (nWaiting) {
			nWaiting.close();
		}
	}, function() {

	}, arg);
	return false;
}
function dialtel(telphone) {
	plus.device.dial( telphone, false );
}
