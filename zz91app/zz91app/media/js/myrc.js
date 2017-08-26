//生意管家供求列表
function myrcproducts(frm,url){
	var arg="";
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	//alert(document.getElementsByName("proid").length)
	arg += "company_id=" + company_id.toString();
	arg += "&proid=0"
	for (var i = 0; i < frm.length; i++) {
		var objinput = frm[i];
		var objtype = objinput.type;
		var objvalue = objinput.value;
		var objname = objinput.name;
		
		if(objname!=""){
			if (objinput.type == "checkbox") {
				if (objinput.checked == true) {
					arg += "," + objvalue;
				}
			} 
		}
	}
	mui.post(url, function(data) {
		var j=JSON.parse(data);
		var err=j.err;
		var errkey=j.errkey;
		if (err == "true") {
			alert(errkey);
		} else {
			if (j.type){
				//供求刷新
				//if (j.type=="proreflush"){
					loaddata(nowherf);
				//}
			}
			//window.location.reload();
		}
		if (nWaiting) {
			nWaiting.close();
		}
	},function(){
		
	},arg);
	return false;
}
function editpro(frm,url){
	var arg="";
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
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
					gotourl('products_update/?'+arg,'blank');
					if (nWaiting) {
						nWaiting.close();
					}
					break
				}
			} 
		}
	}
}

//删除邀请回复
function mycommunitydel(post_id,ptype,pid){
	document.getElementById("pid").value=pid;
	document.getElementById("ptype").value=ptype;
	document.getElementById("post_id").value=post_id;
	openoverlay('', '确实要删除吗？', 0, 200, '.mycommunitydel');
}