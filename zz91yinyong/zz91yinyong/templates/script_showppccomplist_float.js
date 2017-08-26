var adstr="";
adstr="<style>"+
".ldbbottom{"+
"	border-top:solid 1px #0C3;"+
"	height:48px;"+
"	background-color:#F5F5F5;"+
"	width:100%;"+
"	text-align:center;"+
"	background-image: url(http://img0.zz91.com/zz91/images/ldbbottomleft.png);"+
"	font-size:12px;"+
"	background-repeat: no-repeat;"+
"	background-position: left top;z-index:10000;"+
"	position: fixed; bottom: 0px; left: 0px;padding:auto;margin:auto;"+
"}"+
".ldbbottom ul{"+
"	font-weight:bold;"+
"	list-style-type: none;"+
"	margin-left:130px;"+
"}"+
".ldbbottom ul li{"+
"	float:left;"+
"	margin-right:10px;margin-top:10px"+
"}"+
".ldbbottom ul li a{"+
"	background-color: #FFF;"+
"	border: 1px solid #0C6;"+
"	display: inline-block;"+
"	padding: 5px;"+
"	text-decoration: none;"+
"	font-weight:normal;"+
"	color:#000;"+
"	margin-bottom:5px;overflow:hidden;height:18px;line-height:20px;"+
"}"+
".ldbbottom ul li a:hover{"+
"	color:#FFF;"+
"	background-color: #093;"+
"}"+
".ldbbottom .ldbsearchtext{"+
"	border:solid 1px #090;"+
"	background-color:#fff;"+
"	height:24px;"+
"}"+
".ldbbottom .ldbsearch{"+
"	border:solid 1px #090;"+
"	background-color:#090;"+
"	color:#FFF;"+
"	height:28px;overflow:hidden"+
"}"+
".ldbbottom #ldbcontent{"+
"	overflow:hidden;"+
"	width:70%;"+
"	float:left;"+
"	height:48px;"+
"}"+
".ldbbottom .ldbcontentright{"+
"	overflow:hidden;"+
"	float:right;height:48px;"+
"	width:25%;margin-right:10px;line-height:20px;"+
"}"+
".ldbbottom .ldbcontentright input{"+
"	padding:1px;"+
"}"+
"</style>"+
"<div class=\"ldbbottom\">"+
"<ul>"+
"	<div id=\"ldbcontent\">"+
{%for list in listall.list%}
"	<li><a href=\"http://www.zz91.com/ppc/s-{{list.label_hex}}/\" target=_blank>{{list.label}}</a></li>"+
{%endfor%}
"    </div>"+
"    <div class=\"ldbcontentright\"><form method=get action='http://www.zz91.com/ppc/s/searchfirst/' target=_blank onsubmit='return ldbsearch(this)'>"+
"    <li style=\"border-left:solid 1px #CCC; width:260px; text-align:left; padding-left:10px; float:right\"><span onclick=\"changepage()\" style='cursor:pointer;float:left;padding-top:5px;padding-right:5px'>换一换</span> "+
"        <input type=\"text\" name=\"keywords\" id=\"keywords\" style=\"width:100px\" class=\"ldbsearchtext\" style='padding:auto'/><input type=\"submit\" class=\"ldbsearch\" value=\"搜索一下\" style='padding:auto'/>"+
"    </li></form>"+
"    </div>"+
"</ul>"+
"</div>";
document.write(adstr);
var com_id=0;
var page=1;
var zzajaxppc = function(url, successCallback, errorCallback) {
	$.getScript(url, function(data,status) {
		if (status=="success" || status=="notmodified"){
			successCallback && successCallback(data);
		}else{
			errorCallback && errorCallback();
		}
	});
};
function changepage(){
	page+=1;
	if (page>={{listall.count}}){
		page=1;
	}
	var url="http://pyapp.zz91.com/showppccomplist_float.html?keywords={{keywords}}&page="+page.toString()+"&company_id="+com_id.toString();
	zzajaxppc(url,function(data){
		var result = _suggest_result_;
		var obj=document.getElementById("ldbcontent")
		if (obj){
			obj.innerHTML=result
		}
	},function(){});
}

function getloginstatus(){
	var url="http://www.zz91.com/getLoginStatus.htm";
	zzajaxppc(url,function(data){
		if (success=="true"){
			com_id=companyId;
		}
		changepage();
	},function(){});
}
function ldbsearch(frm){
	if (frm.keywords.value.length>0){
		return true;
	}else{
		return false;
	}
}
getloginstatus();

