// JavaScript Document
function getFormvalue(frm)
{
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
					varlulfs=varlulfs+objinput.title+":"+objinput.value;
				}
			}else{
				varlulfs=varlulfs+objinput.title+":"+objinput.value;
			}
		}
	}
	alert(varlulfs);
	frm.contents.value = varlulfs;
}
 function checkForm(frm){
        var f = frm;
        if (f.UserName.value=="") {
            alert("请输入姓名!");
            f.UserName.focus();
            return false;
        }

        if (f.Company.value == "") {
            alert("请输入公司名称!");
            f.Company.focus();
            return false;
        }

       if (f.Address.value == "") {
            alert("请输入公司地址!");
            f.Address.focus();
            return false;
        }
    
        if (f.Tel.value == "") {
            alert("请输入电话号码!");
            f.Tel.focus();
            return false;
        }

        if (f.Email.value == "") {
            alert("请输入邮箱!");
            f.Email.focus();
            return false;
        }
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
						varlulfs=varlulfs+objinput.title+":"+objinput.value+"\n";
					}
				}else{
					varlulfs=varlulfs+objinput.title+":"+objinput.value+"\n";
				}
			}
		}
		alert(varlulfs);
		frm.contents.value = varlulfs;
    }