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
	//plugin defaults
	$.fn.Sonline.defualts ={
		Position:"left",//left或right
		Top:100,//顶部距离，默认200px
		Effect:true, //滚动或者固定两种方式，布尔值：true或
		DefaultsOpen:true, //默认展开：true,默认收缩：false
		Qqlist:"" //多个QQ用','隔开，QQ和客服名用'|'隔开
	}
	


	//子插件：设置列表参数
	$.fn.setList = function(opts){
		$(".year-main").append("<div class='SonlineBox' id='SonlineBox'><div class='contentBox'><div class='floatBox1'><a onclick='bookmarks(this);' action-data='1F'>废塑料专区</a></div><div class='floatBox2'><a onclick='bookmarks(this);' action-data='2F'>废金属专区</a></div><div class='floatBox3'><a onclick='bookmarks(this);' action-data='3F'>综合废料专区</a></div><div class='floatBox4'onclick='bookmarks(this);' action-data='Top'><a>返回顶部</a></div></div></div>");
		var qqListHtml = $.fn.Sonline.splitStr(opts);
		$("#SonlineBox").append(qqListHtml);
		$("#SonlineBox").css({left:970});
		//else if(opts.Position=="right"){$("#SonlineBox").css({right:0})}
		$("#SonlineBox").css({top:opts.Top});
		var allHeights=0;
		if($("#SonlineBox > .contentBox").height() < $("#SonlineBox > .openTrigger").height()){
			allHeights = $("#SonlineBox > .openTrigger").height();
		} else{allHeights = $("#SonlineBox > .contentBox").height();}
		$("#SonlineBox").height(allHeights);
		$("#SonlineBox > .openTrigger").css({left:970});
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
	
	//分割QQ
	$.fn.Sonline.splitStr = function(opts){
		var strs= new Array(); //定义一数组
		var QqlistText = opts.Qqlist;
		strs=QqlistText.split(","); //字符分割
		var QqHtml=""
		for (var i=0;i<strs.length;i++){	
			var subStrs= new Array(); //定义一数组
			var subQqlist = strs[i];
			subStrs = subQqlist.split("|"); //字符分割
			QqHtml = ""
		}
		return QqHtml;
	}
})(jQuery);    


 