// JavaScript Document
function checkForm(frm){
	varlulfs="";
	for(var i=0;i<frm.length;i++)
	{
		var objinput=frm[i];
		if (objinput.title!="")
		{
			if (objinput.type=="radio")
			{
				if(objinput.checked==true)
				{
					varlulfs=varlulfs+objinput.title+"\n";
				}
			}else{
				varlulfs=varlulfs+objinput.title+":"+objinput.value+"\n";
			}
			if (objinput.title.substring(0,1)=="*")
			{
				if (objinput.value=="")
				{
					alert(objinput.title.substring(1)+"不能为空！");
					objinput.focus();
					return false
				}
			}
		}
	}
	frm.contents.value = varlulfs;
}