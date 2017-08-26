// 门市部
$(document).ready(function() {
	
	
	
	$("#AnNiu2_left").click(function(){
		$(this).children("img").attr("src","images/anniu_left1.jpg");
		$("#AnNiu2_right").children("img").attr("src","images/anniu_right2.jpg");
		$("#ZiZhuanZiZhi").css("display","block");
		$("#ChenXinDangAn").css("display","none");
		});
	$("#AnNiu2_right").click(function(){
		$(this).children("img").attr("src","images/anniu_right1.jpg");
		$("#AnNiu2_left").children("img").attr("src","images/anniu_left2.jpg");
		$("#ZiZhuanZiZhi").css("display","none");
		$("#ChenXinDangAn").css("display","block");
		
		});
	
	
	
	
	
	
	
    $("#nav li").mouseover(function(){
			$(this).css("background","#0072a3");

	});
	$("#nav li").mouseout(function(){
			$(this).css("background","none");
	});
	$("#nav_click ul li").click(function(){
		$("#nav li ").children(".nav_li_block").css("display","none");
		$(this).children(".nav_li_block").css("display","block");
//	});
});




});	


