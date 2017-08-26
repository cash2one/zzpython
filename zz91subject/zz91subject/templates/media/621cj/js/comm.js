
window.onresize = function(){
	getSize();

}
getSize();
function getSize(){

	var winWidth = $("body").width();
	var winHeight = $("body").height();

	if((winHeight/winWidth)<(9/16)){
		var mainWidth = 1600*(winHeight/900);
		var left = (winWidth - mainWidth)/2
		$(".main").width(mainWidth);
		$(".main").css("left",left+"px")
		var font_Size = 20*(winHeight/900);
		document.getElementsByTagName('html')[0].style.fontSize = font_Size + "px"
	}else{
		$(".main").width(winWidth);
		$(".main").css("left",0)
		var font_Size = 20*(winWidth/1600);
		document.getElementsByTagName('html')[0].style.fontSize = font_Size + "px"
	}
	
}
