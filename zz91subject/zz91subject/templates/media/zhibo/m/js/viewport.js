window.onresize = function(){
	getSize();
}
function getSize(){
	var winWidth = document.body.clientWidth;
	var font_Size = 40*(winWidth/320);
	document.getElementsByTagName('html')[0].style.fontSize = font_Size + "px"
}
getSize();