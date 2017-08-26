function show1(){
	     	document.getElementById("jb2").style.display="block";
         	document.getElementById("jb1").style.display="none";
			document.getElementById("xz").style.display="block";
		}

function show2(){
			document.getElementById("ys2").style.display="block";
            document.getElementById("ys1").style.display="none";
			document.getElementById("xz").style.display="block";
	}

function change(dex)
{
var id=document.getElementById("menu");
var taga=id.getElementsByTagName("div");
var len=taga.length;
for(var i=0;i<len;i++)
{
var divname='JKDiv_'+i.toString();
if(i==(parseInt(dex)))
{
taga[i].style.backgroundColor='#F6F6F6';
document.getElementById(divname).style.display="block";
document.getElementById("m2").style.display="none";
}else{
taga[i].style.backgroundColor='#fff';
document.getElementById("mt"+dex).style.borderBottom="2px solid #f48432";
document.getElementById("mt"+(1-dex)).style.borderBottom="none";
document.getElementById(divname).style.display="none"; 
document.getElementById("m2").style.display="block";
}
}
}
