$(document).ready(function(e) {
	$(window).scroll(function () {
		var a=$("body").scrollTop();
		if(a>=300){
			bbb();
		}else{
			aaa();
		}
	});
});

function bookmarks(obj){
	var obj1=$(obj).attr("action-data");
	
	var zuobiao=$("#"+obj1).offset().top-60;
	$('body,html').animate({scrollTop:zuobiao+'px'},"slow");
}
function bbb(){
	$(function(){
		$("body").Sonline({
			Position:"right",//left或right
			Top:-400,//顶部距离，默认200px
			Effect:true, //滚动或者固定两种方式，布尔值：true或false
			DefaultsOpen:true, //默认展开：true,默认收缩：false
			Qqlist:"" //多个QQ用','隔开，QQ和客服名用'|'隔开
		});
	});
}
function aaa(){
	$(function(){
		$("body").Sonline({
			Position:"right",//left或right
			Top:0,//顶部距离，默认200px
			Effect:true, //滚动或者固定两种方式，布尔值：true或false
			DefaultsOpen:true, //默认展开：true,默认收缩：false
			Qqlist:"" //多个QQ用','隔开，QQ和客服名用'|'隔开
		});
	});
}
