window.onresize = function(){
	getSize();
}
getSize();
function getSize(){
	var winWidth = document.body.clientWidth;
	var font_Size = 40*(winWidth/375);
	document.getElementsByTagName('html')[0].style.fontSize = font_Size + "px"
}