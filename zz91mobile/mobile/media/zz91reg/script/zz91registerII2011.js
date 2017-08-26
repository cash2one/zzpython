// JavaScript Document
// hetao138@gmail.com   2011-2-12
// register step II tabs
	$(function(){
		//确定当前内容显示
		$(".tradeBeganServiceCont > .tradeBeganCont").eq($(".tradeBeganService li").index(this)).slideDown(1500);
		$(".tradeBeganService li").click(function(){
		$(this).addClass("selected").siblings().removeClass("selected");
		$(".tradeBeganServiceCont > .tradeBeganCont").eq($(".tradeBeganService li").index(this)).fadeIn(1000).siblings().hide();
		});
	})	