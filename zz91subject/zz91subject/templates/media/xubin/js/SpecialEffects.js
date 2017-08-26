

var b=setInterval("show()",1500);
function show(){
	var a=Math.floor(Math.random()*6+1);
	$("#HideNum").val(a);
	$(".m2-item-box1").stop().animate({"margin-top":"0px"});
	$("#item"+a).stop().animate({"margin-top":"-345px"});
}

function change(obj){
	$(obj).parent().animate({"margin-left":"-820px"},"slow");
	$(obj).animate({"right":"820px"},"slow");
}

function bian(obj){
	$(".m2-item-box1").stop().animate({"margin-top":"0px"});
	$(obj).stop().animate({"margin-top":"-345px"});
	
}
$(document).ready(function(e) {
	$(".mainblock2").bind({
		mouseover:function(){clearInterval(b)},
		mouseout:function(){b=setInterval("show()",1500)}
	});
});	