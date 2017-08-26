// JavaScript Document

function change(dex){
	var id=document.getElementById("menu");
	var taga=id.getElementsByTagName("div");
	var len=taga.length;
		for(var i=0;i<len;i++){
		var divname='JKDiv_'+i.toString();
		if(i==(parseInt(dex))){
			taga[i].style.backgroundColor='#ebeaea';
			document.getElementById(divname).style.display="block";
			
		}else{
			taga[i].style.backgroundColor='#b0e4c8';
			document.getElementById("mt"+dex).style.backgroundColor='#b0e4c8';
			document.getElementById("mt"+(1-dex)).style.borderBottom="none";
			document.getElementById(divname).style.display="none"; 
			
		}
	}
}