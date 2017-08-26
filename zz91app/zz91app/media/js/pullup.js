var pullflag=false;

function scrollpp() {
	if (winarr[nowwin]){
		winarr[nowwin][2]=$(window).scrollTop();
	}
	if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
		var dcontent=document.getElementById("dcontent"+nowwin.toString());
		var pullmore = dcontent.getElementsByTagName("input")[0];
		if (pullmore != null) {
			if (pullmore.id=="pullmore"){
				var page=winarr[nowwin][3]
				var url=pullmore.title+"?page="+(page+1).toString();
				var pulldiv = "<div id=pulldiv"+nowwin.toString()+" class='pulldiv' onclick=loadMore('"+url+"')>" +
			"<span class='mui-icon mui-icon-down'></span><span>点此加载更多</span></div>"
				var objpulldiv = document.getElementById("pulldiv"+nowwin.toString());
				if (objpulldiv) {
					objpulldiv.style.display = "";
				} else {
					$("#dcontent"+nowwin.toString()).append(pulldiv);
					var objpulldiv = document.getElementById("pulldiv"+nowwin.toString());
				}
				loadMore(url)
				//loaded(url);
			}
		}
	}
}
function loadmorep(obj,url){
	var page=winarr[nowwin][3];
	if (url.indexOf("?")<0){
		url=url+"?page="+page.toString()+"&t="+Math.ceil(new Date/3600000);
	}else{
		url=url+"&page="+page.toString()+"&t="+Math.ceil(new Date/3600000);
	}
	obj.style.display="";
	obj.innerHTML="正在加载中...";
	if (url!="" && url!=null && (obj.style.display=="" || obj.style.display=="block")){
		mui.get("http://app.zz91.com/" + url, function(data) {
			if (data!=""){
				var newNode = document.createElement("div");
				newNode.innerHTML = data;
				obj.parentNode.insertBefore(newNode, obj);
				if (obj){
					winarr[nowwin][3]+=1;
					obj.innerHTML="<span class='mui-icon mui-icon-down'></span><span>点此加载更多</span>";
				}
				
			}else{
				obj.style.display="none";
			}
			//alert(pullflag)
			//pullflag=false;
		});
	}
}
function loadMore(url) {
	if (url!="" && url!=null){
		mui.get("http://app.zz91.com/" + url, function(data) {
			if (data!=""){
				var dcontent=document.getElementById("dcontent"+nowwin.toString());
				var pullmore = dcontent.getElementsByTagName("ul")[0];
				var pageinfo = dcontent.getElementsByTagName("input")[0];
				if (pullmore != null) {
					var newNode = document.createElement("div");
					newNode.innerHTML = data;
					pullmore.insertBefore(newNode, null);
					if (pageinfo){
						winarr[nowwin][3]+=1;
					}
					var pulldiv = "<div id=pulldiv"+nowwin.toString()+" class='pulldiv'>" +
					"<span class='mui-icon mui-icon-down'></span><span>点此加载更多</span></div>"
					var objpulldiv = document.getElementById("pulldiv"+nowwin.toString());
					if (objpulldiv) {
						objpulldiv.style.display = "";
					} else {
						$("#dcontent"+nowwin.toString()).append(pulldiv);
						var objpulldiv = document.getElementById("pulldiv"+nowwin.toString());
					}
					
					setTimeout(function() { //延后显示避免低端机上闪屏
						//closepulldiv();
					}, 1000);
					
				}
			}
			
		});
	}
}

function closepulldiv() {
	var objpulldiv = document.getElementById("pulldiv"+nowwin.toString());
	if (objpulldiv!=null) {
		objpulldiv.style.display = "none";
	}
}
function loaded(url) {
	//pullDownEl = document.getElementById('pullDown');
	//pullDownOffset = pullDownEl.offsetHeight;
	//alert(url)
	pullUpEl = document.getElementById('pulldiv'+nowwin.toString());	
	pullUpOffset = pullUpEl.offsetHeight;
	//alert(pullUpOffset)
	myScroll = new iScroll("dcontent"+nowwin.toString(), {
		useTransition: false,
		topOffset: pullUpOffset,
		vScrollbar:true,
		onRefresh: function () {
			//if (pullUpEl.className.match('loading')) {
				//pullUpEl.className = '';
				//pullUpEl.querySelector('.pulldiv').innerHTML = 'Pull up to load more...';
			//}
		},
		onScrollMove: function () {
			if (this.y < (this.maxScrollY - 5)) {
				//pullUpEl.className = 'flip';
				//pullUpEl.querySelector('.pulldiv').innerHTML = 'Release to refresh...';
				this.maxScrollY = this.maxScrollY;
			} else if (this.y > (this.maxScrollY + 5)) {
				//pullUpEl.className = '';
				//pullUpEl.querySelector('.pulldiv').innerHTML = 'Pull up to load more...';
				this.maxScrollY = pullUpOffset;
			}
			document.getElementById("appbottom").innerHTML=this.y;
			//this.topOffset=this.y;
			//this.y=this.y+2;
			//this.maxScrollY = 100000;
			
			//alert(this.maxScrollY)
		},
		onScrollEnd: function () {
			//if (pullUpEl.className.match('flip')) {
				//pullUpEl.className = 'loading';
				//pullUpEl.querySelector('.pulldiv').innerHTML = 'Loading...';				
				//pullUpAction();	// Execute custom function (ajax call?)
				//alert(url)
				//alert(this.y)
				//this.maxScrollY = pullUpOffset;
				//this.topOffset=this.y;
				//this.y=this.y;
				loadMore(url);
				//alert(url)
				myScroll.refresh();
				//this.disable()
			//}
		}
	});
	//document.addEventListener('touchmove', function (e) { e.preventDefault(); }, false);
	setTimeout(function () { document.getElementById("dcontent"+nowwin.toString()).style.left = '0'; }, 800);
}
//document.addEventListener('DOMContentLoaded', function () { setTimeout(loaded, 200); }, false);
(function($) {
	var startX = 0,
		startY = 0;
	//touchstart事件
	function touchSatrtFunc(evt) {
		try {
			//evt.preventDefault(); //阻止触摸时浏览器的缩放、滚动条滚动等

			var touch = evt.touches[0]; //获取第一个触点
			var x = Number(touch.pageX); //页面触点X坐标
			var y = Number(touch.pageY); //页面触点Y坐标
			//记录触点初始位置
			startX = x;
			startY = y;

			//var text = 'TouchStart事件触发：（' + x + ', ' + y + '）';
			//document.getElementById("result").innerHTML = text;
		} catch (e) {
			//alert('touchSatrtFunc：' + e.message);
		}
	}

	//touchmove事件，这个事件无法获取坐标
	function touchMoveFunc(evt) {
		try {
			//evt.preventDefault(); //阻止触摸时浏览器的缩放、滚动条滚动等
			var touch = evt.touches[0]; //获取第一个触点
			var x = Number(touch.pageX); //页面触点X坐标
			var y = Number(touch.pageY); //页面触点Y坐标

			var text = 'TouchMove事件触发：（' + x + ', ' + y + '）';
			//判断滑动方向
			if ((x - startX > 10 || x - startX < -10)) {
				text += '<br/>左右滑动';
				//alert(x - startX);
				//offCanvasHide();
			}
			if (y - startY != 0) {
				text += '<br/>上下滑动';
				
				//alert(2);
			}
			//document.getElementById("appbottom").innerHTML=$(window).scrollTop()
			winarr[nowwin][2]=$(window).scrollTop();
			
			//document.getElementById("result").innerHTML = text;
		} catch (e) {
			//alert('touchMoveFunc：' + e.message);
		}
	}

	//touchend事件
	function touchEndFunc(evt) {
		try {
			//evt.preventDefault(); //阻止触摸时浏览器的缩放、滚动条滚动等
			//scrollpp();
			//var text = 'TouchEnd事件触发';
			//document.getElementById("result").innerHTML = text;
		} catch (e) {
			//alert('touchEndFunc：' + e.message);
		}
	}

	//绑定事件
	function bindEvent() {
		document.addEventListener('touchstart', touchSatrtFunc, false);
		document.addEventListener('touchmove', touchMoveFunc, false);
		document.addEventListener('touchend', touchEndFunc, false);
	}

	//判断是否支持触摸事件
	function isTouchDevice() {
		//document.getElementById("version").innerHTML = navigator.appVersion;
		try {
			document.createEvent("TouchEvent");
			//alert("支持TouchEvent事件！");
			bindEvent(); //绑定事件
		} catch (e) {
			//alert("不支持TouchEvent事件！" + e.message);
		}
	}
	//window.onload = isTouchDevice;
	function isDragmore(){

		window.addEventListener('dragstart', function(event) {
			var detail = event.detail;
			var direction = detail.direction;
			var angle = detail.angle;
			
			//alert(tragfx)
			if (direction === 'up' && tragfx=="hide") {
				//document.body.innerHTML=event.detail.deltaX
				//scrollpp();
			}
			if (direction === 'left') {
				//offCanvasShow();
			
			}
			if (direction === 'right') {
				offCanvasHide();
				//alert(1);
			}
			winDrag=true;
		});
		window.addEventListener('drag', function(event,evt) {
			if (winDrag) {
				//if (!sliderRequestAnimationFrame) {
					//updateTranslate();
				//}
				//scrollpp();
				translateX = event.detail.deltaY * winfactor;
				//document.getElementById("appbottom").innerHTML=translateX
				//winarr[nowwin][2]=$(window).scrollTop();
				//event.detail.gesture.preventDefault();
			}
		});
	
		window.addEventListener('dragend', function(event) {
			var detail = event.detail;
			var direction = detail.direction;
			var angle = detail.angle;
			winDrag=false;
			//document.getElementById("appbottom").innerHTML=event.detail.deltaY
			if (direction === 'up' && tragfx=="hide") {
				//document.body.innerHTML=event.detail.deltaX
				//scrollpp();
			}
			if (winDrag) {
				//endDraging(false, event.detail);
			}
		});
	}
	
	window.onload = isDragmore;
//	$.ready(function() {
//		$('body').on('tap', 'a', function(e) {
//			var link=this.href
//			//alert(link)
//			//var id = this.getAttribute('href');
//			//alert(link.indexOf('gotourl'))
//			if (link.indexOf('gotourl')<0) {
//				//link.href = "javascript:void(0);";
//				//link.setAttribute("disabled", "disabled");
//			}else{
//				//this.href
//			}
//			return true;
//		});
//	});
})(mui);


//document.addEventListener( "plusscrollbottom", function (){
//	var dcontent=document.getElementById("dcontent"+nowwin.toString());
//	if (dcontent){
//		var obj = dcontent.getElementsByTagName("input");
//		for (i=0;i<=obj.length;i++){
//			if (obj[i]){
//				if (obj[i].id=="pullmore"){
//					moreobj=obj[i];
//				}
//			}
//		}
//		//alert(pullflag)
//		var obj1=moreobj.nextElementSibling;
//		if (moreobj && pullflag==false){
//			var url=moreobj.value;
//			if (url){
//				
//				//loadmorep(obj1,url);
//				pullflag=true;
//			}
//		}
//	}
//}, false );
