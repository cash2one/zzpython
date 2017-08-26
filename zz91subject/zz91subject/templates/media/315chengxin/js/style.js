$(document).ready(function(e) {
    $(".float-click").click(function(){
		//$(".float").stop(true,true).fadeIn();
	});
	$(".close").click(function(){
		//$(".float").stop(true,true).fadeOut();
	});
});
function AutoScroll(obj){
	$(obj).find("ul").animate({
		marginLeft:"-328px"
	},500,function(){
		$(this).css({marginLeft:"0px"}).find("li:first").appendTo(this);
	});
}
$(document).ready(function(){
	setInterval('AutoScroll("#s1")',3000);
});