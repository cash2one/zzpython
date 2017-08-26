// JavaScript Document

$(document).ready(function(e) {
    $("#item-box1").mouseover(function(){
		$("#item-img2").fadeOut("slow");
		$("#item-img1").fadeIn("slow");
		//$("#item-img1").children("img").attr("src","images/item2-box1.jpg");
		$(this).children("img").attr("src","images/img1_hover.jpg");
	});
	$("#item-box2").mouseover(function(){
		$("#item-img1").fadeOut("slow");
		$("#item-img2").fadeIn("slow");
		//$("#item-img1").children("img").attr("src","images/item2-box2.jpg");
		$(this).children("img").attr("src","images/img2_hover.jpg");
	});
	$("#item-box1").mouseout(function(){
		$(this).children("img").attr("src","images/img1.jpg");
	});
	$("#item-box2").mouseout(function(){
		$(this).children("img").attr("src","images/img2.jpg");
	});
	
	
	$("#item-box3").mouseover(function(){
		$("#item-img3").fadeOut("slow");
		$("#item-img4").fadeIn("slow");
		//$("#item-img1").children("img").attr("src","images/item2-box1.jpg");
		$(this).children("img").attr("src","images/img3_hover.jpg");
	});
	$("#item-box4").mouseover(function(){
		$("#item-img4").fadeOut("slow");
		$("#item-img3").fadeIn("slow");
		//$("#item-img1").children("img").attr("src","images/item2-box2.jpg");
		$(this).children("img").attr("src","images/img4_hover.jpg");
	});
	$("#item-box3").mouseout(function(){
		$(this).children("img").attr("src","images/img3.jpg");
	});
	$("#item-box4").mouseout(function(){
		$(this).children("img").attr("src","images/img4.jpg");
	});
});


/*倒计时*/
$(function(){
	countDown("2013/11/11 00:00:00","#demo01 .day","#demo01 .hour","#demo01 .minute","#demo01 .second");
});
function countDown(time,day_elem,hour_elem,minute_elem,second_elem){
	//if(typeof end_time == "string")
	var end_time = new Date(time).getTime(),//月份是实际月份-1
	//current_time = new Date().getTime(),
	sys_second = (end_time-new Date().getTime())/1000;
	var timer = setInterval(function(){
		if (sys_second > 0) {
			sys_second -= 1;
			var day = Math.floor((sys_second / 3600) / 24);
			var hour = Math.floor((sys_second / 3600) % 24);
			var minute = Math.floor((sys_second / 60) % 60);
			var second = Math.floor(sys_second % 60);
			day_elem && $(day_elem).text(day);//计算天
			$(hour_elem).text(hour<10?"0"+hour:hour);//计算小时
			$(minute_elem).text(minute<10?"0"+minute:minute);//计算分
			$(second_elem).text(second<10?"0"+second:second);// 计算秒
		} else { 
			clearInterval(timer);
		}
	}, 1000);
}
/*倒计时*/
/*弹出框*/
function pop_up(obj){	
	jIframe('img.html', '行业热门推荐截图效果请点击','730','370');
	$.ajax({
		type:GET,
		data:{'company_id':company_id},
		success: function(result){
			
		}
	});

}
function pop_up2(obj){	
	jIframe('img2.html', '地区至尊广告截图效果请点击','975','300');
	$.ajax({
		type:GET,
		data:{'company_id':company_id},
		success: function(result){
			
		}
	});

}
/*弹出框*/