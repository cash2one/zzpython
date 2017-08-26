// JavaScript Document

function setTab(name,cursel){
	cursel_0=cursel;
	for(var i=1; i<=links_len; i++){
		var menudiv = document.getElementById("con_"+name+"_"+i);
		if(i==cursel){
			menudiv.style.display="block";
		}
		else{
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


function show(src){
	 for(var i=1;i<=5;i++){
		if(i==src){
		   document.getElementById("t"+src).style.display="block";
		}else{
		   document.getElementById("t"+i).style.display="none";
		}
	 }
  }
  
  function miss(no){
	  for(var i=1;i<=5;i++){
		  if(i==no){
			  document.getElementById("t"+i).style.display="none"
			  }
		  }
	  }