function setTab(name,cursel,n){
 for(i=1;i<=n;i++){
  var menu=document.getElementById(name+i);
  var con=document.getElementById("con_"+name+"_"+i);
  menu.className=i==cursel?"checked_bg":"";
  con.style.display=i==cursel?"block":"none";
 }
}
function changePic(n)
{
var imgsrc='../images/'+n+'miniinchover.png';
document.getElementById("minipic"+n).src=imgsrc; 
}
function changePic2(n)
{
	 var imgsrc='../images/'+n+'miniinc.png';
document.getElementById("minipic"+n).src=imgsrc; 
}
AddBookmark=function(tit,url){
    
    if(window.sidebar){//IE
        window.sidebar.addPanel(tit,url,'')
    }
    else if(document.all){//FireFox
        window.external.AddFavorite(url,tit);
    }
    else if(window.opera && window.print){//opera
        return true
    }
    else{//默认
        alert("浏览器不支持快捷方式添加收藏夹！请按Ctrl+D手动添加！");
    }
}

function getFormvalue(frm)
{
	varlulfs="";
	for(var i=0;i<frm.length;i++)
	{
		var objinput=frm[i];
		if (objinput.title!="")
		{
		  varlulfs=varlulfs+objinput.title+":"+objinput.value;	
		}
	}
	//alert(varlulfs);
	frm.contents.value = varlulfs;
}
function checkForm(frm){
        var f = frm;
        if (f.UserName.value=="") {
            alert("请输入姓名!");
            f.UserName.focus();
            return false;
        }

        if (f.pwd.value == "") {
            alert("请输入密码!");
            f.pwd.focus();
            return false;
        }
		varlulfs="";
		for(var i=0;i<frm.length;i++)
		{
			var objinput=frm[i];
			if (objinput.title!="")
			{
			  varlulfs=varlulfs+objinput.title+":"+objinput.value+"\n";
			}
		}
		//alert(varlulfs);
		frm.contents.value = varlulfs;
    }
function topsearchsubmit(frm)
{
	var searchname=frm.topsearchname.value;
	tourl="http://tags.zz91.com/tagssearchList/"+UTF8UrlEncode(searchname)+"/"
	frm.target='_blank'
	frm.action=tourl
}
function UTF8UrlEncode(input){    
   
        var output = "";    
   
        var currentChar = '';    
   
        for(var counter = 0; counter < input.length; counter++){    
   
            currentChar = input.charCodeAt(counter);    
   
            if((0 <= currentChar) && (currentChar <= 127))    
   
                output = output + UTF8UrlEncodeChar(currentChar);    
   
            else   
   
                output = output + encodeURIComponent(input.charAt(counter));    
   
        }    
   
        var reslut = output.toUpperCase();    
        return reslut.replace(/%26/, "%2526");     
    } 
	function UTF8UrlEncodeChar(input){    
   
        if(input <= 0x7F) return "%" + input.toString(16);    
   
        var leadByte = 0xFF80;    
   
        var hexString = "";    
   
        var leadByteSpace = 5;    
   
        while(input > (Math.pow(2, leadByteSpace + 1) - 1)){    
   
            hexString = "%" + ((input & 0x3F) | 0x80).toString(16) + hexString;    
   
            leadByte = (leadByte >> 1);    
   
            leadByteSpace--;    
   
            input = input >> 6;    
   
        }    
   
        return ("%" + (input | (leadByte & 0xFF)).toString(16) + hexString).toUpperCase();    
   
	} 