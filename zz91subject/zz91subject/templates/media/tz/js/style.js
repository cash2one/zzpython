function check() { 
var regC = /[^ -~]+/g; 
var str = t1.value; 

if (regC.test(str)){ 
    t1.value = t1.value.substr(0,50); 
} 
} 


function setTab(tag,name,cursel){
	cursel_0=cursel;
	for(var i=1; i<=links_len; i++){
		var menu = document.getElementById(name+i);
		var menu1 = document.getElementById("on"+tag+i);
		var menudiv = document.getElementById("con_"+name+"_"+i);
		if(i==cursel){
			menu.className="ul_tag_";
			menu1.className="tag_";
			menudiv.style.display="block";
		}
		else{
			menu.className="ul_tag";
			menu1.className="tag";
			menudiv.style.display="none";
		}
	}
}


onload=function(){
	var links = document.getElementById("tab1").getElementsByTagName('div')
	links_len=links.length;
	for(var i=0; i<links_len; i++){
		links[i].onmouseover=function(){
			clearInterval(iIntervalId);
			
		}
	}
}


$(document).ready(function(){
  $(".more").click(function(){
	  $("#content1").slideToggle(function(){
			$(".more").text($("#content1").is(":hidden") ?  ">>更多" :"—收起");
		});
		
  });
});



















