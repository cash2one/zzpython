$(document).ready(function(e) {
		var y=$("#pm-FloatBox").offset().top;
		$(document).bind("scroll",function(){
			if($(window).scrollTop()<=100){
				
			}else{
				var offsetTop=$(window).scrollTop()-200 +"px"; 
				$("#pm-FloatBox").animate({top : offsetTop },{ duration:1000 , queue:false }); 
			}
			
		});  
	});