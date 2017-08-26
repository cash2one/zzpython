
function openWin(name, url, pageParam) {
	var systemType = api.systemType;
	pageParam['url'] = url;
	pageParam['mid'] = UserInfo.memberID();
	pageParam['wname']=name+"_";
	pageParam['deviceId']=deviceId;
	if (name && url) {
		api.openWin({
			name : name,
			url : "../html/win_blank.html",
			pageParam : pageParam,
			bounces : false,
			vScrollBarEnabled : false,
			hScrollBarEnabled : false,
			animation : {
				type : "push", //动画类型（详见动画类型常量）
				subType : "from_right", //动画子类型（详见动画子类型常量）
				duration : 300,                //动画过渡时间，默认300毫秒
			},
			showProgress : false
		});
	}
	api.closeSlidPane();
}

function loadcommonurl(url, pageParam) {
	var wintitle = pageParam.wintitle;
	var wname = pageParam.wname;
	var bounces=true;
	var bounces1=pageParam.bounces;
	if (bounces1==false){bounces=bounces1}
	if (!wintitle) {
		$("#wintitle").css("display", "none");
		bounces=false;
	};
	$(".mui-title").text(wintitle);
	var oHeight = $(".main").height();
	var oWidth = $(".main").width();
	var topHeight = $("header").height();
	var bottomHeight=$("footer").height();
	api.openFrame({
		name : wname,
		url : url,
		rect : {
			x : 0,
			y : topHeight,
			w : oWidth,
			h : oHeight-topHeight-bottomHeight-1
		},
		pageParam : pageParam,
		bounces : bounces,
		bgColor : 'rgb(255,255,255,255)',
		vScrollBarEnabled : true,
		hScrollBarEnabled : true,
		showProgress : false
	});
}

//获取n到m随机整数
function rd(n, m) {
	var c = m - n + 1;
	return Math.floor(Math.random() * c + n);
}
function toDetail(id) {
	var pageParam = {
		id : id,
		wintitle:"正文",
		type:"detail"
	};
	openWin("detail","./detail.html",pageParam);
}
function openFrame(name, url, pageParam) {
	var header = $api.byId('header');
	$api.fixIos7Bar(header);
	var headerPos = $api.offset(header);
	
	api.openFrame({
		name : name,
		url : url,
		pageParam : pageParam,
		bounces : false,
		vScrollBarEnabled : false,
		hScrollBarEnabled : false,
		rect : {
			x : 0,
			y : headerPos.h,
			w : 'auto',
			h : 'auto'
		}
	});
}

function openSearchBar() {
	var searchBar = api.require('searchBar');
	searchBar.open({
		placeholder : "请输入菜谱关键词进行搜索",
		bgImg : "widget://res/searchBar_bg.png"
	}, function(ret, err) {
		if (ret.isRecord) {
			api.toast({
				msg : "暂未上线",
				duration : 2000,
				location : 'bottom'
			});
			//录音功能
			//	        var obj = api.require('speechRecognizer');
			//			obj.record({
			//			},function(ret,err){
			//			    if(ret.status){
			//				    searchBar.setText({
			//					     text:ret.wordStr
			//					 });
			//			    }else{
			////			        api.toast({
			////					    msg: err.msg,
			////					    duration:2000,
			////					    location: 'bottom'
			////					});
			//			    }
			//			});
		}
		else {
			var pageParam = {
				key : ret.text
			};

			openWin("searchlist", "./html/searchlist.html", pageParam);
		}
	});
}

function UserInfo() {
};

//清除登录信息
UserInfo.clear = function() {
	localStorage.removeItem('username');
	localStorage.removeItem('password');
	localStorage.removeItem('token');
	localStorage.removeItem('memberID');
	//mermer_id = "0";
};

//检查是否包含自动登录的信息
UserInfo.auto_login = function() {
	var username = UserInfo.username();
	var pwd = UserInfo.password();
	if (!username || !pwd) {
		return false;
	}
	return true;
};
//检查是否已登录
UserInfo.has_login = function() {
	var username = UserInfo.username();
	var pwd = UserInfo.password();
	var token = UserInfo.token();
	if (!username || !pwd || !token) {
		return false;
	}
	return true;
};

UserInfo.username = function() {
	if (arguments.length >= 1) {
		localStorage.setItem('username', arguments[0].toString());
	}
	if (arguments.length == 0) {
		return localStorage.getItem('username');
	}
	if (arguments[0] === '') {
		localStorage.removeItem('username');
		return;
	}
};

UserInfo.memberID = function() {
	if (arguments.length >= 1) {
		localStorage.setItem('memberID', arguments[0].toString());
	}
	if (arguments.length == 0) {
		return localStorage.getItem('memberID');
	}
	if (arguments[0] === '') {
		localStorage.removeItem('memberID');
		return;
	}
};

UserInfo.password = function() {
	if (arguments.length >= 1) {
		localStorage.setItem('password', arguments[0].toString());
	}
	if (arguments.length == 0) {
		return localStorage.getItem('password');
	}
	if (arguments[0] === '') {
		localStorage.removeItem('password');
		return;
	}
};

UserInfo.token = function() {
	if (arguments.length >= 1) {
		localStorage.setItem('token', arguments[0].toString());
	}
	if (arguments.length == 0) {
		return localStorage.getItem('token');
	}
	if (arguments[0] === '') {
		localStorage.removeItem('token');
		return;
	}
};
UserInfo.get_pwd_hash = function(pwd) {
	return $.md5(pwd);
};
UserInfo.onSuccess = function(token, username, pwd_hash, memberID) {
	UserInfo.username(username);
	UserInfo.memberID(memberID);
	UserInfo.password(pwd_hash);
	UserInfo.token(token);
	//把获取到的token保存到storage中
};

UserInfo.onError = function(errcode) {
	mui.toast(errcode);
};
//if (UserInfo.has_login()) {
//	usertoken = UserInfo.token();
//	memberID = UserInfo.memberID();
//}

deviceId = localStorage.getItem('deviceId');
