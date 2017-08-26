// JavaScript Document

function change(dex){
	var id=document.getElementById("menu");
	var taga=id.getElementsByTagName("div");
	var len=taga.length;
		for(var i=0;i<len;i++){
		var divname='JKDiv_'+i.toString();
		if(i==(parseInt(dex))){
			taga[i].style.backgroundColor='#fff';
			taga[i].style.border='1px solid #29b341';
			taga[i].style.color='#000';
			document.getElementById(divname).style.display="block";
			
		}else{
			taga[i].style.backgroundColor='#fff';
			document.getElementById("mt"+dex).style.backgroundColor='#29b341';
			document.getElementById("mt"+dex).style.lineHeight='32px';
			document.getElementById("mt"+dex).style.color='#fff';
			document.getElementById("mt"+(1-dex)).style.borderBottom="none";
			document.getElementById(divname).style.display="none"; 
			
		}
	}
}

window.onload=function(){
	var speed=10;
	var annheight = 87;
	var anndelay = 3000;
	var timeout ;
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
