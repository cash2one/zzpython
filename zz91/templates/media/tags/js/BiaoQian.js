// 标签页






$(document).ready(function() {
    $(".search-submit").mouseover(function(){
		$(this).css("background","url(images/search_hover.jpg) no-repeat");	
	});
	$(".search-submit").mouseout(function(){
		$(this).css("background","url(images/search.jpg) no-repeat");	
	});
});