// JavaScript Document
$(document).ready(function(e) {
    $("#nav li a").mouseover(function(){
		var a=$(this).position().left;
		$("#a").stop().animate({left:a});
		$("#a").css("display","block");
	});

});



