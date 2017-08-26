/******************************
	zz91再生资源搜索引擎JS代码
******************************/




$(document).ready(function(e) {
    $("#m1-navClick li").click(function(){
		$("#m1-navClick li").css("background","#ccc");
		$("#m1-navClick li").css("color","#000");
		$(this).css("background","#009944");
		$(this).css("color","#fff");
	});
	$("#m5-nav li").click(function(){
		$("#m5-nav li").css("font-weight","100");
		$(this).css("font-weight","700");
	});
	
	
});

jQuery.fn.addFavorite = function(l, h) {
	 return this.click(function() {
		 var t = jQuery(this);
		 if(jQuery.browser.msie) {
			window.external.addFavorite(h, l);
		 } else if (jQuery.browser.mozilla || jQuery.browser.opera) {
			 t.attr("rel", "sidebar");
			 t.attr("title", l);
			 t.attr("href", h);
		 } else {
			 alert("请使用Ctrl+D将本页加入收藏夹！");
		 }
	 });
};
$(function(){
	$('#keleyi').addFavorite(document.title,location.href);
});