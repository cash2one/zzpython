
window.onload=function(){
	var announcement = document.all.announcement;
	var announcementbody = document.all.announcementbody;
	var announcementbody2  = document.all.announcementbody2;
	var speed=20;
	//var annheight = 120;
	var annheight = announcementbody.offsetHeight/2;
	var anndelay = 3000;
	var timeout ;
	var inter;
	//alert(announcementbody.offsetHeight);
	//填充内容，使滚动条能够拉过所有消息
	announcementbody2.innerHTML=announcementbody.innerHTML

	//每间隔speed毫秒执行move函数
	timeout = setTimeout(function(){
							inter=setInterval(move,speed)
						}, anndelay);
	
	function move(){
		//防止刚好移动一条消息停止移动的时候，触发了定时anndelay毫秒后继续移动，
		//但是还没有到时间，鼠标却移动上去了，就应该停止移动，
		//但是anndelay毫秒时间到了，鼠标还没有移出，消息却执行setTimeout函数，继续移动
		if(timeout){
			clearTimeout(timeout);
		}
		//当滚动条滚过三条消息之后将其置为o,即回到初始位置,实现不断轮询移动
		if(announcementbody.offsetHeight-announcement.scrollTop<=0)
			announcement.scrollTop-=announcementbody.offsetHeight
		else{
			//每次滚动条向下移动1个像素
			announcement.scrollTop++
		}
		//当滚动条移动一条消息的高度的时候停止移动
		if(announcement.scrollTop%annheight == 0){
			clearInterval(inter)
			//停止anndelay 毫秒后继续不断移动
			timeout = setTimeout(function(){
							inter=setInterval(move,speed)
						}, anndelay);
		}
	}
	//停止移动
	announcement.onmouseover=function() {
		if(timeout){
			clearTimeout(timeout);
		}
		clearInterval(inter)
	}
	//开始移动
	announcement.onmouseout=function(){
		if(timeout){
			clearTimeout(timeout);
		}
		inter=setInterval(move,speed)
	};
}
