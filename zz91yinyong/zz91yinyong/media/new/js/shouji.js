function rightsearch(){
	var obj=document.getElementById("topsearch")
	if (obj.style.display=="none"){
		obj.style.display="";
	}else{
		obj.style.display="none";
	}
}
function chtab(n)
{
	jQuery(".floattop li").removeClass("ptabon");
	document.getElementById("cntab"+n).className="ptabon";
	for (i=1;i<=3;i++){
		document.getElementById("pcateg"+i).style.display="none";
	}
	var pcateg=document.getElementById("pcateg"+n)
	if (pcateg.style.display=="none"){
		pcateg.style.display="";
		
	}else{
		pcateg.style.display="none";
	}
	if (n==1 || n==2){
		document.getElementById("topsearch").style.marginTop="140px";
	}else{
		document.getElementById("topsearch").style.marginTop="100px";
	}	
}
function chtabt(n){
	jQuery(".floattop li").removeClass("ptabon");
	document.getElementById("cntab"+n).className="ptabon";
}

