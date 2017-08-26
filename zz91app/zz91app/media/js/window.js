//返回
function winback(){
	var backwin=1;
	//左边菜单打开时
	if (tragfx=="show"){
		offCanvasHide();
		return false;
	}
	for (var i=1;i<winlenght;i++){
		var oldwin=document.getElementById("dcontent"+i.toString());
		if (oldwin){
			if (oldwin.style.display==""){
				if (i>1){
					backwin=winarr[i][1];
				}else{
					if (winDrag==false){
						
						var btnArray = ['确定', '取消'];
						mui.confirm('确认退出？', '提示', btnArray, function(e) {
							if (e.index == 0) {
								plus.navigator.closeSplashscreen();
								plus.runtime.quit();
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
					}
				}
			}
			oldwin.style.display="none"
		}
	}
	var content = document.getElementById("dcontent"+backwin.toString());
	if (content){
		content.style.display="";
		nowwin=backwin;
		nowurl=winarr[nowwin][5]
	}
	
	if (winarr[backwin]!=null){
		wintype=winarr[backwin][4]
		showheader(wintype);
		mui.scrollTo(winarr[backwin][2],30);
	}
	//closepulldiv();
}
//通用加载页面
function gotourl(url,wintype) {
	if (wintype=="blank"){
		url=url.replace("&","[and]").replace("?","wenhao")
		mui.openWindow({
			id:url,
			url: "blank.html?url2="+url+"&wintype="+wintype+"&company_id="+company_id.toString(),
			preload: false //TODO 等show，hide事件，动画都完成后放开预加载
		});
		return false;
	}
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var nWaiting;
	var backwin=1;
	//closepulldiv();
	for (var i=1;i<winlenght;i++){
		var oldwin=document.getElementById("dcontent"+i.toString());
		if (oldwin){
			if (oldwin.style.display==""){
				backwin=i;
			}
			oldwin.style.display="none";
		}
	}
	if (url.indexOf("http://app.zz91.com")<0){
		if (url.indexOf("?")<0){
			url="http://app.zz91.com/"+url+"?t="+Math.ceil(new Date/3600000)+"&company_id="+company_id.toString()+"&win="+win.toString();
		}else{
			url="http://app.zz91.com/"+url+"&t="+Math.ceil(new Date/3600000)+"&company_id="+company_id.toString()+"&win="+win.toString();
		}
	}
	
	
	var content = document.getElementById("dcontent"+win.toString());
	if (content==null){
		winarr[win]=[win,backwin,0,2,wintype,url]
		document.getElementById("mainbody").innerHTML+="<div class='mui-content' id='dcontent"+win.toString()+"'></div>"
	}else{
		content.style.display="";
		if (winarr[win]){
			winarr[win][3]=2;
		}
		
	}
	
	if (winarr[win]==null){
		winarr[win]=[win,backwin,0,2,wintype,url]
	}
	showheader(wintype);
	var content = document.getElementById("dcontent"+win.toString());
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
					nowwin=win;
					win+=1;
					if (win>=winlenght){win=2}
					if (nWaiting) {
						nWaiting.close();
					}
				} else {
					var btnArray = ['重试加载', '取消'];
					mui.confirm('哎呀,网络不给力，点击重试加载试试！', '提示', btnArray, function(e) {
						if (e.index == 0) {
							gotourl(url,wintype);
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
					})
				}
				break;
			default:
				break;
		}
	}
	xhr.open("GET", url);
	xhr.send();
	nowurl = url;	
}
//加载头部和底部
function showheader(wintype){
	//头部底部
	var title="ZZ91再生网"
	if (wintype=="myrc" || wintype=="myrc_products"){
		title="生意管家"
	}
	if (wintype=="trade"){
		title="交易中心"
	}
	if (wintype=="price"){
		title="行情报价"
	}
	if (wintype=="huzhu"){
		title="再生互助"
	}
	if (wintype=="news"){
		title="资讯中心"
	}
	var topstr="<a><img src=\"images/logo.png\" onclick=\"gotourl('/index.html','index');\"></a>"+
"<a class=\"mui-icon mui-icon-bars mui-pull-right\" href=\"javascript:offCanvasShow()\"></a>"
	var topstr1="<a class=\"mui-action-back mui-icon mui-icon-left-nav mui-pull-left\"></a>"+
"<a class=\"mui-icon mui-icon-bars mui-pull-right\" href=\"javascript:offCanvasShow()\"></a>"+
"<h1 class=\"mui-title\">"+title+"</h1>"
	if (wintype=="index"){
		document.getElementById("apptop").innerHTML=topstr
	}else{
		document.getElementById("apptop").innerHTML=topstr1
	}
//	mui.get("http://app.zz91.com/top.html?type="+wintype+"&t="+Math.ceil(new Date/3600000), function(data) {
//		document.getElementById("apptop").innerHTML = data;
//	});
	var botttomstr="<div style=\"position: fixed;bottom: 0;left: 0;\">"+
	"<a class=\"mui-tab-item\" href=\"javascript:gotourl('/index.html','index');\">"+
	"	<span class=\"mui-tab-label\">动态</span>"+
	"</a>"+
	"<a class=\"mui-tab-item\" href=\"javascript:gotourl('/trade.html','trade');\">"+
	"	<span class=\"mui-tab-label\">商机</span>"+
	"</a>"+
	"<a class=\"mui-tab-item\" href=\"#\" onclick=fj()>"+
	"	<span class=\"mui-tab-label\">附近</span>"+
	"</a>"+
	"</div>";
	
	var bottomquestion="<span class=\"mui-icon mui-icon-plus zz91-question-addpic\"></span>"+
	"<textarea rows=\"1\" placeholder=\"多行文本框\" class=\"zz91-question-addtext\"></textarea>"+
	"<a class=\"mui-btn mui-btn-success zz91-question-addsend\">发送</a>";
	
	var  bottomhuzhu="<center style=\"padding-top: 10px;\">"+
		"<button onclick=\"gotourl('/myrc_index/','myrc')\" class=mui-btn-success>  我要提问    </button> "+
	"</center>";
	
	document.getElementById("appbottom").innerHTML = botttomstr;
	if (wintype=="huzhu"){
		document.getElementById("appbottom").innerHTML=bottomhuzhu;
	}
	if (wintype=="question"){
		document.getElementById("appbottom").innerHTML=bottomquestion;
	}
	
//	mui.get("http://app.zz91.com/bottom.html?type="+wintype+"&t="+Math.ceil(new Date/3600000), function(data) {
//		document.getElementById("appbottom").innerHTML = data;
//	});
}
function fj(){
	var keywords;
	keywords=nowprovice.replace("省","");
	keywords+=" "+nowcity.replace("市","");
	var url="/offerlist/?keywords="+keywords;
	gotourl(url,'trade');
}
var pushServer = "http://demo.dcloud.net.cn/helloh5/push/";
var message = null;
// 监听plusready事件  
document.addEventListener("plusready", function() {
	//message = document.getElementById("message");
	// 监听点击消息事件
	plus.push.addEventListener("click", function(msg) {
		// 判断是从本地创建还是离线推送的消息
		switch (msg.payload) {
			case "LocalMSG":
				//outSet( "点击本地创建消息启动：" );
				break;
			default:
				//outSet( "点击离线推送消息启动：");
				break;
		}
		// 提示点击的内容
		plus.ui.alert(msg.content);
		// 处理其它数据
		logoutPushMsg(msg);
	}, false);
	
	// 监听在线消息事件
	plus.push.addEventListener("receive", function(msg) {
		if (msg.aps) { // Apple APNS message
			//outSet( "接收到在线APNS消息：" );
			//alert(1)
		} else {
			//alert(2)
			//outSet( "接收到在线透传消息：" );
		}
		logoutPushMsg(msg);
	}, false);
}, false);
/**
 * 日志输入推送消息内容
 */
function logoutPushMsg(msg) {
	//outLine( "title: "+msg.title );
	//outLine( "content: "+msg.content );
	if (msg.payload) {
		if (typeof(msg.payload) == "string") {
			//outLine( "payload(String): "+msg.payload );
		} else {
			//outLine( "payload(JSON): "+JSON.stringify(msg.payload) );
		}
	} else {
		//outLine( "payload: undefined" );
	}
	if (msg.aps) {
		//outLine( "aps: "+JSON.stringify(msg.aps) );
	}
}

function getPushInfo11() {
		var info = plus.push.getClientInfo();
		//outSet( "获取客户端推送标识信息：" );
		//outLine( "token: "+info.token );
		//outLine( "clientid: "+info.clientid );
		//outLine( "appid: "+info.appid );
		//outLine( "appkey: "+info.appkey );
		createLocalPushMsg();
}
function getPushInfo() {
		var info = plus.push.getClientInfo();
		alert(info.clientid);
		//outSet( "获取客户端推送标识信息：" );
		//outLine( "token: "+info.token );
		//outLine( "clientid: "+info.clientid );
		//outLine( "appid: "+info.appid );
		//outLine( "appkey: "+info.appkey );
}
	/**
	 * 本地创建一条推动消息
	 */

function createLocalPushMsg() {
		var options = {
			cover: false
		};
		var str = dateToStr(new Date());
		str += ": 欢迎使用Html5 Plus创建本地消息！";
		plus.push.createMessage(str, "LocalMSG", options);
		//outSet( "创建本地消息成功！" );
		//outLine( "请到系统消息中心查看！" );
		if (plus.os.name == "iOS") {
			//outLine('*如果无法创建消息，请到"设置"->"通知"中配置应用在通知中心显示!');
		}

	}
	/**
	 * 请求‘简单通知’推送消息
	 */

function requireNotiMsg() {
	var url = pushServer + 'notiPush.php?appid=' + encodeURIComponent(plus.runtime.appid);
	url += ('&cid=' + encodeURIComponent(plus.push.getClientInfo().clientid));
	url += ('&title=' + encodeURIComponent('Hello H5+'));
	url += ('&content=' + encodeURIComponent('欢迎回来体验HTML5 plus应用！'));
	//outSet(url);
	plus.runtime.openURL(url);
}

//左滑菜单
function offCanvasHide() {
		var offCanvas = mui('#offCanvas');
		//document.getElementById('offCanvasHide').addEventListener('tap', function() {
		//offCanvas.offCanvas('toggle')//toggle or hide;
		offCanvas.offCanvas('hide');
		//}); 
}
//左滑菜单
function offCanvasShow() {
	var offCanvas = mui('#offCanvas');
	offCanvas.offCanvas('show') //toggle or hide;
}
//链接通用函数
(function($) {
	$.ready(function() {
		$('body').on('tap', 'a', function(e) {
			var id = this.getAttribute('href');
			var wintarget="blank";
			
			if (nowurl.indexOf("/priceindex/")>=0){
				wintarget="price"
			}
			if (nowurl.indexOf("/category/")>=0){
				wintarget="trade"
			}
			if (id && id.substring(0,1)!="#") {
				if (window.plus) {
					if (id.indexOf("javascript:")<0){
			        	gotourl(id,wintarget);
			        }else{
			        	eval(id);
			        }
				}
			}
		});
		
	});
})(mui);
//退出
function loginout() {
	if (confirm('确认退出？')) {
		plus.navigator.closeSplashscreen();
		plus.runtime.quit();
	}
}

//登陆
function zz91login(frm){
	var username=frm.username.value;
	var passwd=frm.passwd.value;
	if (window.plus) {
		nWaiting = plus.nativeUI.showWaiting();
	}
	var arg="username="+username;
	arg+="&passwd="+passwd;
	arg+="&appid="+clientid;
	mui.post("http://app.zz91.com/loginof.html",function(data){
		if (data=="suc"){
			company_id=data;
			loadappbody();
		}else{
			alert(data);
		}
		if (nWaiting) {
			nWaiting.close();
		}
	},function(){
		
	},arg);
	return false;
}

//交易中心列表导航滚动js
function showtrade(objname,h){
	var pobj=objname.parentNode.parentNode.getElementsByClassName("tradelistnav");
	for (var i=0;i<pobj.length;i++){
		if (pobj[i].style.display=="block"){
			pobj[i].slideUp(10,h);
		}
	}
	var obj = objname.getElementsByTagName("div")[0];
	if(obj.style.display!='none'){
		obj.slideUp(10,h);
	}else{
		obj.slideDown(10,h);
	}
}



window.HTMLElement.prototype.slideDown=function(speed,height)
{
	var o = this;
	clearInterval(o.slideFun);
	var h = height;
	var i = 0;
	o.style.height = '0px';	
	//o.style.width = '150px';
	o.style.display = 'block';
	o.style.overflow = 'hidden';
	o.slideFun = setInterval(function(){
		
		i = i + 5;
		if(i>h) i=h;
		o.style.height = i+'px';
		if(i>=h)
		{
			o.style.removeProperty('overflow');
			clearInterval(o.slideFun);
		}	
	},speed);
}

window.HTMLElement.prototype.slideUp=function(speed,height)
{
	var o = this;
	clearInterval(o.slideFun);
	var h = height;
	var i = h;
	o.style.overflow = 'hidden';
	o.slideFun = setInterval(function(){
		i -= 5;
		if(i<0) i=0;
		o.style.height = i+'px';
		if(i<=0)
		{
			o.style.display = 'none';
			o.style.removeProperty('overflow');
			//more.className = more.className.replace(' moreclick','');
			clearInterval(o.slideFun);
		}	
	
	},speed);
}