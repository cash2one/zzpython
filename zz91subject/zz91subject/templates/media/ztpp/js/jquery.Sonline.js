/*
此插件基于Jquery
插件名：jquery.Sonline(在线客服插件)
开发者 似懂非懂
版本 1.0
Blog：www.haw86.com
Down:http://www.codefans.net
*/
(function($){
	$.fn.Sonline = function(options){
        var opts = $.extend({}, $.fn.Sonline.defualts, options); 
		$.fn.setList(opts); //调用列表设置
		if(opts.DefaultsOpen == false){
			$.fn.Sonline.close(opts.Position,0);
		}
		
		//Ie6兼容或滚动方式显示
		if ($.browser.msie && ($.browser.version == "6.0") && !$.support.style||opts.Effect==true) {$.fn.Sonline.scrollType();}
		else if(opts.Effect==false){$("#SonlineBox").css({position:"absolute"});}
	}

	


	//子插件：设置列表参数
	$.fn.setList = function(opts){
		$(".main").append("<div class='SonlineBox' id='SonlineBox'><div class='contentBox'><div class='float'><a href='http://www.zz91.com/weixin2014/' target='_blank'></a></div></div></div>");
		$("#SonlineBox").css({left:970});
		//else if(opts.Position=="right"){$("#SonlineBox").css({right:0})}
		$("#SonlineBox").css({top:opts.Top});
		var allHeights=0;
		if($("#SonlineBox > .contentBox").height() < $("#SonlineBox > .openTrigger").height()){
			allHeights = $("#SonlineBox > .openTrigger").height()+4;
		} else{allHeights = $("#SonlineBox > .contentBox").height()+4;}
		$("#SonlineBox").height(allHeights);
		$("#SonlineBox > .openTrigger").css({left:960});
		//else if(opts.Position=="right"){$("#SonlineBox > .openTrigger").css({right:0});}
	}
	
	//滑动式效果
	$.fn.Sonline.scrollType = function(){
		$("#SonlineBox").css({position:"absolute"});
		var topNum = parseInt($("#SonlineBox").css("top")+"");
		$(window).scroll(function(){
			var scrollTopNum = $(window).scrollTop();//获取网页被卷去的高
			$("#SonlineBox").stop(true,true).delay(0).animate({top:scrollTopNum+topNum},"slow");
		});
	}
})(jQuery);    


 