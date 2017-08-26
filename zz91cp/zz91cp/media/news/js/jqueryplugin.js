// JavaScript Document
/*  jquery插件开发模板
	(function($){ 
		$.fn.yourName = function(options){ 
			//各种属性、参数  
			var options = $.extend(defaults, options); 
			this.each(function(){ 
			//插件实现代码 
			}); 
		}; 
	})(jQuery);
*/
(function($){

	/*
 * tableUI
 * Date: 2011-5-8
 * 使用tableUI可以方便地增加表格体验。提供的功能有奇偶行颜色交替，鼠标移上高亮显示
 */	  
	$.fn.tableUI = function(options){
		var defaults = {
			evenRowClass:"evenRow",
			oddRowClass:"oddRow",
			activeRowClass:"activeRow"			
		}
		var options = $.extend(defaults, options);
		this.each(function(){
			var thisTable=$(this);

			$(thisTable).find("tr:even").addClass(options.evenRowClass);
			$(thisTable).find("tr:odd").addClass(options.oddRowClass);
			
			$(thisTable).find("tr").hover(function(){$(this).addClass(options.activeRowClass);},function(){$(this).removeClass(options.activeRowClass);});
			
		});
	};
	
	/*rollup---start----
	间断性向上滚动
	*/
	$.fn.rollup=function(time){
		if(arguments.length<1) time=2000;
		this.each(function(){ 
			var top;
			var thisDom=$(this);
			function tjcompany(){
				top = -(thisDom.find("li").eq(0).outerHeight(true)) + 'px';
				var thisImg=thisDom.find("li").eq(1).find("img");
				for(var i=0;i<thisImg.length;i++){
					if(!thisImg.eq(i).attr("src")) thisImg.eq(i).attr("src",thisImg.eq(i).attr("thissrc"));
				}
				thisDom.find("ul").animate({top:top}, {
					duration:800,
					complete:function(){
						thisDom.find("ul").append(thisDom.find("li").eq(0));
						thisDom.find("ul").css("top","0");
					}
				});
			}
			if(time=="one"){
				tjcompany();
			}else{
				var companyup=setInterval(tjcompany,time);
				thisDom.find("ul").hover(function(){
					clearInterval(companyup);},function(){companyup=setInterval(tjcompany,time);});
			}
		}); 

	}//rollup---end----
	/*rolldown---start----
	间断性向下滚动
	*/
	$.fn.rolldown=function(time){
		if(arguments.length<1) time=2000;
		this.each(function(){ 
			var top;
			var thisDom=$(this);
			function tjcompany(){
				top =-(thisDom.find("li:last").eq(0).outerHeight(true)) + 'px';
				thisDom.find("li:last").insertBefore(thisDom.find("li:first"));
				thisDom.find("ul").css("top",top);
				thisDom.find("ul").animate({top:0}, {
					duration:800,
					complete:function(){
						//thisDom.find("ul").css("top","0");
					}
				});
			}
			if(time=="one"){
				tjcompany();
			}else{
				var company=setInterval(tjcompany,time);
				thisDom.find("ul").hover(function(){
					clearInterval(company);},function(){company=setInterval(tjcompany,time);});
			}
		}); 

	}//rolldown---end----
	/*rollleft---start----
	间断性向左滚动
	*/
	$.fn.rollleft=function(time){
		if(arguments.length<1) time=2000;
		this.each(function(){ 
			var left;
			var thisDom=$(this);
			function tjcompany(){
				left =-(thisDom.find("li").eq(0).outerWidth(true)) + 'px';
				thisDom.find("ul").animate({left:left}, {
					duration:800,
					complete:function(){
						thisDom.find("ul").append(thisDom.find("li").eq(0));
						thisDom.find("ul").css("left","0");
					}
				});
			}
			if(time=="one"){
				tjcompany();
			}else{
				var company=setInterval(tjcompany,time);
				thisDom.find("ul").hover(function(){
					clearInterval(company);},function(){company=setInterval(tjcompany,time);});
			}
		}); 

	}//rollleft---end----
	/*rollright---start----
	间断性向左滚动
	*/
	$.fn.rollright=function(time){
		if(arguments.length<1) time=2000;
		this.each(function(){ 
			var left;
			var thisDom=$(this);
			function tjcompany(){
				left =-(thisDom.find("li:last").eq(0).outerWidth(true)) + 'px';
				thisDom.find("li:last").insertBefore(thisDom.find("li:first"));
				thisDom.find("ul").css("left",left);
				thisDom.find("ul").animate({left:0}, {
					duration:800,
					complete:function(){
						//thisDom.find("ul").append(thisDom.find("li").eq(0));
						//thisDom.find("ul").css("left","0");
					}
				});
			}
			if(time=="one"){
				tjcompany();
			}else{
				var company=setInterval(tjcompany,time);
				thisDom.find("ul").hover(function(){
					clearInterval(company);},function(){company=setInterval(tjcompany,time);});
			}
		}); 

	}//rollright---end----
	/*rollleftone---start----
	间断性不连续向左滚动
	*/
	$.fn.rollleftone=function(time){
		if(arguments.length<1) time=2000;
		this.each(function(){ 
			var left;
			var thisDom=$(this);
			function tjcompany(){
				left =-(thisDom.find("li").eq(0).outerWidth(true)) + 'px';
				thisDom.find("ul").animate({left:left}, {
					duration:800,
					complete:function(){
						//thisDom.find("ul").append(thisDom.find("li").eq(0));
						thisDom.find("ul").css("left","0");
					}
				});
			}
			if(time=="one"){
				tjcompany();
			}else{
				var company=setInterval(tjcompany,time);
				thisDom.find("ul").hover(function(){
					clearInterval(company);},function(){company=setInterval(tjcompany,time);});
			}
		}); 

	}//rollleftone---end----
	//picChange-----start---
	//图片多帧间断切换
	$.fn.picChange = function(options){ 
		var defaults = {
			intervaltime:5000,
			classliout:"banner_tab_li",
			classliover:"banner_tab_li2"
		}
		var options = $.extend(defaults, options);
		this.each(function(){ 
			var thisDom=$(this);
			var numLi=$(this).find("li").length;
			var tjpptl;
			thisDom.find("li").mouseover(function(){
				thisDom.find("span").hide();
				thisDom.find("span").eq(Number($(this).attr("txt"))-1).fadeIn(300);
				thisDom.find("li").addClass(options.classliout).removeClass(options.classliover);
				$(this).removeClass(options.classliout).addClass(options.classliover);
			});
		    function gettjscroll(){
			   var thisshow=thisDom.find("li:[class='"+options.classliover+"']").attr("txt");
			   if(thisshow==numLi) thisshow=0;
			   thisDom.find("li").eq(thisshow).mouseover();  
		    }
		    tjpptl=setInterval(gettjscroll,options.intervaltime);
		    thisDom.find("span").hover(function(){clearInterval(tjpptl);},function(){tjpptl=setInterval(gettjscroll,options.intervaltime);});	
		}); 
	};
	//picChange-----over---
	//picUpDown-----start---
	$.fn.picUpDown = function(options){ 
		var defaults = {
			intervaltime:4000,
			classliout:"banner_tab_li",
			classliover:"banner_tab_li2"
		}
		var options = $.extend(defaults, options);
		this.each(function(){ 
			var thisDom=$(this);
			var numLi=$(this).find("li").length;
			var spanHeight=parseInt($(this).find("span").css("height"));	
			thisDom.find("li").mouseover(function(){
				var top;								  
			    top=(Number($(this).attr("txt"))-1)*spanHeight;
				var imgDom=thisDom.find("img").eq(Number($(this).attr("txt"))-1);
				if(!imgDom.attr("src")) imgDom.attr("src",imgDom.attr("thissrc"));
		    	thisDom.find("div").eq(0).animate({top:-top},{duration:500});
				thisDom.find("li").addClass(options.classliout).removeClass(options.classliover);
				$(this).removeClass(options.classliout).addClass(options.classliover);
			});
			function gettjscroll(){
			   var thisshow=thisDom.find("li:[class='"+options.classliover+"']").attr("txt");
			   if(thisshow==numLi) thisshow=0;
			   thisDom.find("li").eq(thisshow).mouseover();  
		    }
		    tjpptl=setInterval(gettjscroll,options.intervaltime);
		    thisDom.find("span").hover(function(){clearInterval(tjpptl);},function(){tjpptl=setInterval(gettjscroll,options.intervaltime);});
		}); 
	};
	//picUpDown-----over----
	/*
	scrollstart---scrollstop---start----
	example:
	$(window).bind('scrollstart', function(){}); 
	$(window).bind('scrollstop', function(){}); 
	*/
	var special = $.event.special,uid1 = 'D' + (+new Date()),uid2 = 'D' + (+new Date() + 1);
	special.scrollstart = {
		setup: function() {             
			var timer, handler =  function(evt) {                     
				var _self = this, _args = arguments;                     
				if (timer) { 
					clearTimeout(timer); 
				}else{
					evt.type = 'scrollstart';                         
					$.event.handle.apply(_self, _args); 
				}                     
				timer = setTimeout(function(){timer = null;}, special.scrollstop.latency);
			};             
			$(this).bind('scroll', handler).data(uid1, handler);
		},
		teardown: function(){             
			$(this).unbind('scroll',$(this).data(uid1));
		}
	};     
	special.scrollstop = {         
		latency: 500, 
		setup: function() { 
			var timer,handler = function(evt) {
				var _self = this,
				_args = arguments; 
				if (timer) {clearTimeout(timer);}                     
				timer = setTimeout(function(){
					timer = null;
					evt.type = 'scrollstop';
					$.event.handle.apply(_self, _args);
				},special.scrollstop.latency);};             
				$(this).bind('scroll', handler).data(uid2, handler); 
			},         
		teardown: function() {$(this).unbind('scroll',$(this).data(uid2));}
	};
	//scrollstart---scrollstop---over----
	
})(jQuery);