//定义数据API接口的appKey
var appKey = "5ed1ca988555463cae6707d46309322e";
//定义相关变量
var page = 1;
var deviceId;
//首页获得栏目地址
function getNavlist() {
	//api.showProgress();
	api.ajax({
		url : hosturl+'/sex/mynavlist.html?mid='+UserInfo.memberID()+'&deviceId='+deviceId+"&t=" + (new Date()).getTime().toString(),
		method : 'get',
		timeout : 30,
		pageParam : {},
		dataType : 'json',
		returnAll : false
	}, function(ret, err) {
		if (ret) {
			//ret = eval(ret)
			var navHtml = '', frames = [];
			for (var i in ret.mycolumn) {
				var active = i == 0 ? 'nav_active' : '';
				navHtml += '<li data-index="' + i + '" id="' + ret.mycolumn[i].id + '" class="' + active + '" tapmode="" onclick="openFrame(' + ret.mycolumn[i].id + ',' + i + ')">' + ret.mycolumn[i].typename + '</li>';
			}
			localStorage.removeItem('havehtml0');
			for (var i in ret.allcolumn) {
				var frame = {};
				localStorage.removeItem('havehtml'+ret.allcolumn[i].id.toString());
				frame.name = 'frame_' + i;
				frame.url = i == 0 ? '../html/sexmain.html?typeid=' + ret.allcolumn[i].id.toString() : '../html/sexmain.html?typeid=' + ret.allcolumn[i].id.toString();
				frame.pageParam = {
					typeid : ret.allcolumn[i].id,
					index : ret.allcolumn[i].numb,
					deviceId:deviceId
				};
				frames.push(frame);
				typelist.push(ret.allcolumn[i].id);
			}
			$("#scroller").find('ul').html(navHtml);
			if (ret){
				liwidth = ret.length;
				navliwidth = $("#scroller").find('li').width();
				navwidth = (liwidth * navliwidth + $("body").width() / 2 - 30).toString();
				$("#scroller").css("width", navwidth.toString() + "px");
				loaded();
				openfooter(frames);
			}
			api.hideProgress();
		} else {
			api.toast({
				msg : err.msg,
				location : 'middle'
			})
			api.hideProgress();
		};
	});
}