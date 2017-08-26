function initDateObject()
{
	Date.prototype.compare=date_compare;
	Date.prototype.clone=date_clone;
	Date.prototype.format=date_format;
}
function date_format(sFormat)
{
	var dt=this;
	if(sFormat==null || typeof(sFormat)!="string")
		sFormat="";
	sFormat=sFormat.replace(/yyyy/ig,dt.getFullYear());
	var y=""+dt.getYear();
	if(y.length>2)
	{
		y=y.substring(y.length-2,y.length);
	}
	var month=dt.getMonth()+1;
	if(month<10)month="0"+month;
	var day=dt.getDate();
	if(day<10)day="0"+day;
	var hour=dt.getHours();
	if(hour<10)hour="0"+hour;
	var minute=dt.getMinutes();
	if(minute<10)minute="0"+minute;
	var second=dt.getSeconds();
	if(second<10)second="0"+second;
	sFormat=sFormat.replace(/yy/ig,y);
	sFormat=sFormat.replace(/MM/g,month);
	sFormat=sFormat.replace(/dd/ig,day);
	sFormat=sFormat.replace(/HH/ig,hour);
	sFormat=sFormat.replace(/mm/g,minute);
	sFormat=sFormat.replace(/SS/ig,second);
/*
	sFormat=sFormat.replace(/yy/ig,y);
	sFormat=sFormat.replace(/MM/g,dt.getMonth()+1);
	sFormat=sFormat.replace(/dd/ig,dt.getDate());
	sFormat=sFormat.replace(/HH/ig,dt.getHours());
	sFormat=sFormat.replace(/mm/g,dt.getMinutes());
	sFormat=sFormat.replace(/ss/g,dt.getSeconds());
*/	
	return sFormat;
}
function date_clone()
{
	return new Date(this.getFullYear(),this.getMonth(),this.getDate(),this.getHours(),this.getMinutes(),this.getSeconds());
}
function date_compare(dtCompare)
{
	var dt=this;
	var hr=0;
	
	if(dt && dtCompare)
	{
		if(dt.getFullYear()>dtCompare.getFullYear())
			hr=1;
		else if(dt.getFullYear()<dtCompare.getFullYear())
			hr=-1;
		else if(dt.getMonth()>dtCompare.getMonth())
			hr=1;
		else if(dt.getMonth()<dtCompare.getMonth())
			hr=-1;
		else if(dt.getDate()>dtCompare.getDate())
			hr=1;
		else if(dt.getDate()<dtCompare.getDate())
			hr=-1;
		else if(dt.getHours()>dtCompare.getHours())
			hr=1;
		else if(dt.getHours()<dtCompare.getHours())
			hr=-1;
		else if(dt.getMinutes()>dtCompare.getMinutes())
			hr=1;
		else if(dt.getMinutes()<dtCompare.getMinutes())
			hr=-1;
		else if(dt.getSeconds()>dtCompare.getSeconds())
			hr=1;
		else if(dt.getSeconds()<dtCompare.getSeconds())
			hr=-1;

	}
	return hr;
}
function date_getDateFromVT_DATE(dt)
{
	dt=dt.replace(/-/g,"/");
	dt=Date.parse(dt);
	if(isNaN(dt))
		dt=null;
	else
		dt=new Date(dt);
	return dt;
}
//Call the initialize function
initDateObject();
var m_iPickerCount=1;
var cl_dpMaxYear=9999;
var cl_dpMaxMonth=11;
var cl_dpMaxDay=31;
var cl_dpMinYear=1600;
var cl_dpMinMonth=0;
var cl_dpMinDay=1;
var cl_dpMaxHour=23;
var cl_dpMinHour=0;
var cl_dpMaxMinute=59;
var cl_dpMinMinute=0;
var cl_dpMaxSecond=59;
var cl_dpMinSecond=0;

function createDatePicker(txtName, bShowCheck, strDefaultDate, bHiddenDay,bHiddenHour,bHiddenMinute,bHiddenSecond)
{
    if(bShowCheck==null) bShowCheck=true;
    if(bHiddenDay == null)
    {
    	 bHiddenDay = false;
    	 bHiddenHour=true;
    	 bHiddenMinute=true;
    	 bHiddenSecond=true;
    }
    else if(bHiddenHour==null)
    {
    	 bHiddenHour=true;
    	 bHiddenMinute=true;
    	 bHiddenSecond=true;
    }
    else if(bHiddenMinute==null)
    {
    	 bHiddenMinute=true;
    	 bHiddenSecond=true;
    }
    else if(bHiddenSecond==null)
    {
         bHiddenSecond=true;
    }


	var dpID="dp_"+(m_iPickerCount++);
	var dt=dp_getValidDate(strDefaultDate, bHiddenDay,bHiddenHour,bHiddenMinute,bHiddenSecond);
	var isCheck = true;
	
	var stWidth = 240;
	if(!bShowCheck) stWidth -= 16;
	if(bHiddenDay) stWidth -= 28;
	if(bHiddenHour) stWidth-= 28;
	if(bHiddenMinute) stWidth-= 28;
	if(bHiddenSecond) stWidth-= 28;
	
	if(dt==null) {
	    dt= new Date();
	    dt.setMilliseconds(0);
	    if(bHiddenDay) {
	        dt.setDate(1);
	        dt.setHours(0);
	        dt.setMinutes(0);
	        dt.setSeconds(0);
            }
            else if(bHiddenHour)
            {
	        dt.setHours(0);
	        dt.setMinutes(0);
	        dt.setSeconds(0);
            }
            else if(bHiddenMinute)
            {
	        dt.setMinutes(0);
	        dt.setSeconds(0);
            }
            else if(bHiddenSecond)
            {
	        dt.setSeconds(0);
            }
	    isCheck = (bShowCheck?false:true);
	}
	document.write("<span class=DPFrame style=\"width:"+stWidth+"\" id="+dpID+">");
        document.write("<input class=DP" + (bShowCheck?"":"Hidden") + "Check type=checkbox "+(isCheck?"checked":"")+" onclick=\"return dp_CheckBoxClick();\">");
	document.write("<input class=DPYear type=text value="+dt.getFullYear()+" size=4 maxlength=4 onfocus=\"return dp_focus('year');\" onblur=\"return dp_blur('year');\" onkeypress=\"return KeyFilter('number');\" onkeydown=\"return dp_keyDown('year');\">");
	document.write("<font class=DPYearDes><a class=DPDropBtn style='cursor:hand' onclick='dp_DropClick();return false;' title=\"选择日期\">年</a></font>");
	document.write("<input class=DPMonth type=text value="+(dt.getMonth()+1)+" size=2 maxlength=2 onfocus=\"return dp_focus('month');\" onblur=\"return dp_blur('month');\" onkeypress=\"return KeyFilter('number');\" onkeydown=\"return dp_keyDown('month');\">");
	document.write("<font class=DPMonthDes><a class=DPDropBtn style='cursor:hand' onclick='dp_DropClick();return false;' title=\"选择日期\">月</a></font>");
	document.write("<input class=DP"+(bHiddenDay?"Hidden":"")+"Day type=text value="+dt.getDate()+" maxlength=2 onfocus=\"return dp_focus('day');\" onblur=\"return dp_blur('day');\" onkeypress=\"return KeyFilter('number');\" onkeydown=\"return dp_keyDown('day');\">");
	document.write("<font class=DP"+(bHiddenDay?"Hidden":"")+"DayDes><a class=DPDropBtn style='cursor:hand' onclick='dp_DropClick();return false;' title=\"选择日期\">日</a></font>");
	document.write("<span class=DPSep></span>");
	document.write("<a class=DPDropBtn style='cursor:hand' onclick='dp_DropClick();return false;' title=\"选择日期\"><img src=\"http://img0.zz91.com/front/admin/dj.gif\"> </a>");
	if(typeof(txtName)=="string" && txtName.length>0)
	{
		document.write("<input type=hidden value='"+(isCheck?dt.format("yyyy-MM-dd hh:mm:ss"):"")+"' name="+txtName+">");
	}

	document.write("<input class=DP"+(bHiddenHour?"Hidden":"")+"Hour type=text value="+dt.getHours()+" maxlength=2 onfocus=\"return dp_focus('hour');\" onblur=\"return dp_blur('hour');\" onkeypress=\"return KeyFilter('number');\" onkeydown=\"return dp_keyDown('hour');\">");
	document.write("<font class=DP"+(bHiddenHour?"Hidden":"")+"HourDes><a class=DPDropBtn style='cursor:hand' onclick=';return false;' title=\"选择小时\">时</a></font>");
	document.write("<input class=DP"+(bHiddenMinute?"Hidden":"")+"Minute type=text value="+dt.getMinutes()+" maxlength=2 onfocus=\"return dp_focus('minute');\" onblur=\"return dp_blur('minute');\" onkeypress=\"return KeyFilter('number');\" onkeydown=\"return dp_keyDown('minute');\">");
	document.write("<font class=DP"+(bHiddenMinute?"Hidden":"")+"MinuteDes><a class=DPDropBtn style='cursor:hand' onclick=';return false;' title=\"选择分钟\">分</a></font>");
	document.write("<input class=DP"+(bHiddenSecond?"Hidden":"")+"Second type=text value="+dt.getSeconds()+" maxlength=2 onfocus=\"return dp_focus('second');\" onblur=\"return dp_blur('second');\" onkeypress=\"return KeyFilter('number');\" onkeydown=\"return dp_keyDown('second');\">");
	document.write("<font class=DP"+(bHiddenSecond?"Hidden":"")+"SecondDes><a class=DPDropBtn style='cursor:hand' onclick=';return false;' title=\"选择秒数\">秒</a></font>");

	document.write("</span>");
	var dp=document.all(dpID);
	dp_initDatePicker(dp,dt,bHiddenDay,bHiddenHour,bHiddenMinute,bHiddenSecond);
	return dp;
}
function dp_getValidDate(str, bHiddenDay,bHiddenHour,bHiddenMinute,bHiddenSecond)
{
	//alert(str);
	if(str==null)
	    return null;
	
	var sDate=str.replace(/\//g,"-");
	    sDate=sDate.replace(/ /g,"-");
	    sDate=sDate.replace(/:/g,"-");
	var vArr=sDate.split("-");
	if(vArr.length==2){
		sDate=sDate +"-01-00-00-00";
		vArr=sDate.split("-");
	}
	if(vArr.length==3){
		sDate=sDate +"-00-00-00";
		vArr=sDate.split("-");
	}
        if(vArr.length!=6)
	    return null;
    var lYear = vArr[0];
    var lMonth = vArr[1];
    var lDay = vArr[2];
    var lHour= vArr[3];
    var lMinute= vArr[4];
    var lSecond= vArr[5];
	if(lYear==null || isNaN(parseInt(lYear,10)))
		return null;
	else
		lYear=parseInt(lYear,10);
	if(lMonth==null || isNaN(parseInt(lMonth,10)))
		return null;
	else
		lMonth=parseInt(lMonth,10)-1;
	if(lDay==null || isNaN(parseInt(lDay,10)))
		return null
	else
		lDay=parseInt(lDay,10);
	if(lHour==null || isNaN(parseInt(lHour,10)))
		return null
	else
		lHour=parseInt(lHour,10);
	if(lMinute==null || isNaN(parseInt(lMinute,10)))
		return null
	else
		lMinute=parseInt(lMinute,10);
	if(lSecond==null || isNaN(parseInt(lSecond,10)))
		return null
	else
		lSecond=parseInt(lSecond,10);

    if(bHiddenDay) lDay = 1;
    if(bHiddenHour)lHour=0;
    if(bHiddenMinute)lMinute=0;
    if(bHiddenSecond) lSecond=0;
	var dt=new Date(lYear,lMonth,lDay,lHour,lMinute,lSecond);
	var cdMax=new Date(cl_dpMaxYear,cl_dpMaxMonth,cl_dpMaxDay,23,59,59);
	var cdMin=new Date(cl_dpMinYear,cl_dpMinMonth,cl_dpMinDay,0,0,0);
	if(dt.compare(cdMax)>0 || dt.compare(cdMin)<0)
		dt=null;
	return dt;
}
function dp_initDatePicker(dp,dt,bHiddenDay,bHiddenHour,bHiddenMinute,bHiddenSecond)
{
	if(dp)
	{
		//Private Property
		dp.curDate=dt;
		dp.dpEnabled=true;
		dp.maxDay=cl_dpMaxDay;
		dp.maxMonth=cl_dpMaxMonth;
		dp.maxYear=cl_dpMaxYear;
		dp.minDay=cl_dpMinDay;
		dp.minMonth=cl_dpMinMonth;
		dp.minYear=cl_dpMinYear;
		dp.maxHour=cl_dpMaxHour;
		dp.minHour=cl_dpMinHour;
		dp.maxMinute=cl_dpMaxMinute;
		dp.minMinute=cl_dpMinMinute;
		dp.maxSecond=cl_dpMaxSecond;
		dp.minSecond=cl_dpMinSecond;
		dp.oldDate=dt.clone();
		//Private Method
		
		dp.getDropDownTable=dp_getDropDownTable;
		dp.getMonthName=dp_getMonthName;
		dp.hideDropDown=dp_hideDropDown;
		dp.initDropDown=dp_initDropDown;
		dp.onDateChange=dp_onDateChange;
		dp.refreshPostText=dp_refreshPostText;
		dp.showDropDown=dp_showDropDown;
		//Public Property
		//All Span Properties can be used;
		dp.offsetHor=0;
		//Public Method
		dp.bHiddenDay=bHiddenDay;
		dp.bHiddenHour=bHiddenHour;
		dp.bHiddenMinute=bHiddenMinute;
		dp.bHiddenSecond=bHiddenSecond;
		dp.getIsChecked=dp_getIsChecked;
		dp.setFocus=dp_setFocus;
		dp.format=dp_format;
		dp.getDateContent=dp_getDateContent;
		dp.getDay=dp_getDay;
		dp.getEnabled=dp_getEnabled;
		dp.getMonth=dp_getMonth;
		dp.getYear=dp_getYear;
		dp.getHour=dp_getHour;
		dp.getMinute=dp_getMinute;
        dp.getSecond=dp_getSecond;
		dp.refreshView=dp_refreshView;
		dp.setAccessKey=dp_setAccessKey;
		dp.setCurDate=dp_setCurDate;
		dp.setDateDes=dp_setDateDes;
		dp.setEnabled=dp_setEnabled;
		dp.setFormat=dp_setFormat;
		dp.setMaxDate=dp_setMaxDate;
		dp.setMinDate=dp_setMinDate;
		dp.setTabIndex=dp_setTabIndex;
		dp.setWeekName=dp_setWeekName;
		//Event
		dp.dateChanged=null;
		//Init View
		dp.refreshView();
	}
}
function dp_createDropDown()
{
	var ddt=getDropDownTable();
	if(ddt)
		return ddt;
	document.body.insertAdjacentHTML("BeforeEnd",
					"<TABLE id=dpDropDownTable CELLSPACING=0 "+
					"onclick=\"dp_ddt_dblclick();\" "+
					"ondblclick=\"dp_ddt_dblclick();\">"+
					"<TR class=DPTitle>"+
					"<TD><span class=DPBtn onclick=\"dp_yearChange(-1);\" title=\"上年\">&lt;&lt;</span>"+
					"<span class=DPBtn onclick=\"dp_monthChange(-1);\" title=\"上月\">&lt;</span></TD>"+
					"<TD align=center colspan=5 class=DPTitle></TD>"+
					"<TD><span class=DPBtn onclick=\"dp_monthChange(1);\" title=\"下月\">&gt;</span>"+
					"<span class=DPBtn onclick=\"dp_yearChange(1);\" title=\"下年\">&gt;&gt;</span></TD>"+
					"</TR>"+
					"<TR>"+
					"<TD class=DPWeekName>星期日</TD>"+
					"<TD class=DPWeekName>星期一</TD>"+
					"<TD class=DPWeekName>星期二</TD>"+
					"<TD class=DPWeekName>星期三</TD>"+
					"<TD class=DPWeekName>星期四</TD>"+
					"<TD class=DPWeekName>星期五</TD>"+
					"<TD class=DPWeekName>星期六</TD>"+
					"</TR>"+
					"</TABLE>");
	ddt=getDropDownTable();
	if(ddt)
	{
		var row=null;
		var cell=null;
		for(var i=2; i<8; i++)
		{
			row=ddt.insertRow(i);
			if(row)
			{
				for(var j=0; j<7; j++)
				{
					cell=row.insertCell(j);
				}
			}
		}
	}
	row=ddt.insertRow(8);
	cell=row.insertCell()
	if(ddt.rows.length!=9)
		ddt=null;
	return ddt;
}
function dp_getYear()
{
	var dp=this;
	return dp.curDate.getFullYear();
}
function dp_getMonth()
{
	var dp=this;
	return dp.curDate.getMonth()+1;
}
function dp_getDay()
{
	var dp=this;
	return dp.curDate.getDate();
}
function dp_getHour()
{
	var dp=this;
	return dp.curDate.getHours();
}
function dp_getMinute()
{
	var dp=this;
	return dp.curDate.getMinutes();
}
function dp_getSecond()
{
	var dp=this;
	return dp.curDate.getSeconds();
}

function dp_format(sFormat)
{
	var dp=this;
	return dp.curDate.format(sFormat);
}
function dp_setAccessKey(sKey)
{
	var dp=this;
	var src=dp.children[0];
	if(src && src.tagName=="INPUT")
	{
		src.accessKey=sKey;
	}
}
function dp_getEnabled()
{
	var dp=this;
	var val=false;
	if(dp.dpEnabled)
		val=true;
	else
		val=false;
	return val;
}
function dp_setEnabled(val)
{
	var dp=this;
	var hr=false;
	var src=dp.children[1];
	if(src && src.tagName=="INPUT")
	{
		src.disabled=!val;
		src=dp.children[3];
		if(src && src.tagName=="INPUT")
		{
			src.disabled=!val;
			src=dp.children[5];
			if(src && src.tagName=="INPUT")
			{
				src.disabled=!val;
				dp.dpEnabled=val;
				hr=true;
			}
		}
	}
	return hr;
}
function dp_setFocus()
{
	var dp=this;
	var src=dp.children[0];
	if(src && src.tagName=="INPUT" && !src.disabled)
	{
		src.focus();
	}
}
function dp_getDateContent()
{
	var dp=this;
	var con="";
	var sYearDes="";
	var sMonthDes="";
	var sDayDes="";
	var src=dp.children[1];
	if(src && src.tagName=="FONT")
	{
		sYearDes=src.innerText;
		src=dp.children[3];
		if(src && src.tagName=="FONT")
		{
			sMonthDes=src.innerText;
			src=dp.children[5];
			if(src && src.tagName=="FONT")
			{
				sDayDes=src.innerText;
				var dt=dp.curDate;
				con=dt.getFullYear()+sYearDes+(dt.getMonth()+1)+sMonthDes+dt.getDate()+sDayDes;
			}
		}
	}
	return con;
}
function dp_setFormat(sFormat)
{
	this.formatString=sFormat;
	this.refreshPostText();
}
function dp_CheckBoxClick()
{
    var src=event.srcElement;
    var dp=getParentFromSrc(src,"SPAN")
	if(src && src.tagName=="INPUT" && dp && dp.className=="DPFrame")
	{
        dp.refreshPostText();
    }
    return true;
}
function dp_getIsChecked()
{
    var dp=this;
    var src=dp.children[0];
    if(src && src.tagName=="INPUT")
        return src.checked;
    return false;        
}
function dp_refreshPostText()
{
	var dp=this;
    var src=dp.children[0];
    if(src && src.tagName=="INPUT")
    {
        var sFormat="yyyy-MM-dd HH:mm:ss";
	    if(typeof(dp.formatString)=="string")
	        sFormat=dp.formatString;
        var txt=dp.children[9];
        if(txt && txt.tagName=="INPUT")
            if(src.checked)
  	            txt.value=dp.format(sFormat);
            else
    	        txt.value="";
        if(typeof(dp.dateChanged)=="function") {
			dp.dateChanged();
	    }
    }
}
function dp_initDropDown()
{
	var dp=this;
	var ddt=dp.getDropDownTable();
	if(ddt)
	{
		ddt.curCell=null;
		var cell=null;
		var dt=new Date(dp.curDate.getFullYear(),dp.curDate.getMonth(),1);
		cell=ddt.rows[0].cells[1];
		if(cell)
		{
			cell.innerText=dp.getMonthName(dt.getMonth())+" "+dt.getFullYear();
		}
		var wd=dt.getDay();
		dt=new Date(dt.getFullYear(),dt.getMonth(),1-wd);
		var day=dt.getDate();
		for(var i=2; i<8; i++)
		{
			for(var j=0; j<7; j++)
			{
				cell=ddt.rows[i].cells[j];
				if(cell)
				{
					if(dp.curDate.getMonth()!=dt.getMonth())
						cell.className="DPCellOther";
					else if(dp.curDate.getDate()!=dt.getDate())
						cell.className="DPCell";
					else
					{
						cell.className="DPCell";
						dp_onCell(cell);
					}
					cell.innerText=day;
					cell.year=dt.getFullYear();
					cell.month=dt.getMonth();
					cell.day=day;
					dt.setDate(day+1);
					day=dt.getDate();
				}
			}
		}
		cell=ddt.rows[8].cells[0];
		cell.className="DPTodayCell";
		cell.innerText = "今天"
		dt = new Date();
		cell.year=dt.getFullYear();
		cell.month=dt.getMonth();
		cell.day=dt.getDate();
	}
}
function dp_getMonthName(lMonth)
{
	var mnArr=new Array("一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月");
	return mnArr[lMonth];
}
function dp_setWeekName()
{
	var dp=this;
	var ddt=dp.getDropDownTable();
	if(ddt)
	{
		var cell=null;
		for(var j=0; j<7; j++)
		{
			cell=ddt.rows[1].cells[j];
			if(cell)
			{
				cell.innerText=arguments[j];
			}
		}
	}
}
function dp_showDropDown()
{
	var dp=this;
	var ddt=dp.getDropDownTable();
	if(ddt)
	{
		if(ddt.style.display=="block")
		{
			dp.hideDropDown();
		}
		else
		{
			dp.initDropDown();
			if(ddt.clientWidth==0)
			{
				ddt.style.pixelLeft=-500;
				ddt.style.pixelTop=-500;
				ddt.style.display="block";
			}
			var ddtWidth=ddt.clientWidth==0?266:ddt.clientWidth;
			var ddtHeight=ddt.clientHeight==0?133:ddt.clientHeight;
			var lLeft=getOffsetLeft(dp);
			var lTop=getOffsetTop(dp)+dp.offsetHeight;
			if((lTop+ddtHeight)>(document.body.clientHeight+document.body.scrollTop))
			{
				lTop-=(ddtHeight+dp.offsetHeight+2);
			}
			if((lLeft+ddtWidth)>(document.body.clientWidth+document.body.scrollLeft))
			{
				lLeft=document.body.clientWidth+document.body.scrollLeft-ddtWidth-2;
			}
			var off=parseInt(dp.offsetHor,10);
			if(isNaN(off))
				off=0;
			ddt.style.pixelLeft=lLeft+off;
			ddt.style.pixelTop=lTop;
//			alert(lLeft+off);
//			alert(lTop);
			hideElement("select",lLeft+off,lTop,ddtWidth,ddtHeight);
			ddt.dpOldDocClick=document.onclick;
			ddt.dpOldDocKeyDown=document.onkeydown;
			event.cancelBubble=true;
			event.returnValue=false;
			document.onclick=dp_sub_docClick;
			document.onkeydown=dp_sub_dockeydown;
			ddt.style.display="block";
		}
	}
}
function getDropDownTable()
{
	var ddt=document.all("dpDropDownTable");
	if(!(ddt && ddt.tagName=="TABLE"))
		ddt=null;
	return ddt;
}
function dp_hideDropDown()
{
	var ddt=getDropDownTable();
	if(ddt)
	{
		ddt.style.display="none";
		document.onclick=ddt.dpOldDocClick;
		document.onkeydown=ddt.dpOldDocKeyDown;
		showElement("select");
	}
}
function dp_getDropDownTable()
{
	var dp=this;
	dp.dropDownTable=dp_createDropDown();
	if(dp.dropDownTable && dp.dropDownTable.tagName=="TABLE")
	{
		dp.dropDownTable.dp=dp;
		return dp.dropDownTable;
	}
	else
		return null;
}
function dp_onDateChange()
{
	var dp=this;
	if(dp.curDate.compare(dp.oldDate)!=0)
	{
		dp.oldDate=dp.curDate.clone();
		var src=dp.children[0];
	    if(src && src.tagName=="INPUT")	{ src.checked = true; }
		dp.refreshView();
		dp.refreshPostText();
	}
}
function dp_refreshView()
{
	var dp=this;
	var hr=false;
	if(dp && dp.curDate)
	{
		var src=dp.children[1];
		if(src && src.tagName=="INPUT")
		{
			src.value=dp.curDate.getFullYear();
			src=dp.children[3];
			if(src && src.tagName=="INPUT")
			{
				src.value=dp.curDate.getMonth()+1;
				src=dp.children[5];
				if(src && src.tagName=="INPUT")
				{
                     src.value=dp.curDate.getDate();
                     src=dp.children[10];
                     if(src && src.tagName=="INPUT")
                     {
                         src.value=dp.curDate.getHours();
                         src=dp.children[12];
                         if(src && src.tagName=="INPUT")
                         {
                             src.value=dp.curDate.getMinutes();
                             src=dp.children[14];
                             if(src && src.tagName=="INPUT")
                             {
                                 src.value=dp.curDate.getSeconds();
                                 hr=true;
                             }
                         }
                     }
	            }
			}
		}
	}
	return hr;
}
function dp_setTabIndex(lTabIndex)
{
	var dp=this;
	var hr=false;
	if(dp)
	{
		var src=dp.children[1];
		if(src && src.tagName=="INPUT")
		{
			src.tabIndex=lTabIndex;
			src=dp.children[3];
			if(src && src.tagName=="INPUT")
			{
				src.tabIndex=lTabIndex;
				src=dp.children[5];
				if(src && src.tagName=="INPUT")
				{
					src.tabIndex=lTabIndex;
					src=dp.children[8];
					if(src && src.tagName=="A")
					{
						src.tabIndex=lTabIndex;
                        src=dp.children[10];
                        if(src && src.tagName=="INPUT")
                        {
                            src.tabIndex=lTabIndex;
                            src=dp.children[12];
                            if(src && src.tagName=="INPUT")
                            {
                                src.tabIndex=lTabIndex;
                                src=dp.children[14];
                                if(src && src.tagName=="INPUT")
                                {
                                    src.tabIndex=lTabIndex;
                                    hr=true;
                                }
                            }
                        }
					}
				}
			}
		}
	}
	return hr;
}
function dp_setDateDes(sYearDes,sMonthDes,sDayDes)
{
	if(sYearDes==null)
		sYearDes="-";
	if(sMonthDes==null)
		sMonthDes="-";
	if(sDayDes==null)
		sDayDes="";
	var dp=this;
	var hr=false;
	var src=dp.children[2];
	if(src && src.tagName=="FONT")
	{
		src.innerText=sYearDes;
		src=dp.children[4];
		if(src && src.tagName=="FONT")
		{
			src.innerText=sMonthDes;
			src=dp.children[6];
			if(src && src.tagName=="FONT")
			{
				src.innerText=sDayDes;
				hr=true;
			}
		}
	}
	return hr;
}
function dp_setMaxDate(lYear,lMonth,lDay)
{
	var dp=this;
	var hr=false;
	if(dp)
	{
		lYear=parseInt(lYear,10);
		lMonth=parseInt(lMonth,10);
		lDay=parseInt(lDay,10);
		if(!(isNaN(lYear) || isNaN(lMonth) || isNaN(lDay)))
		{
			lMonth--;
			var dt=new Date(lYear,lMonth,lDay);
			var dMin=new Date(dp.minYear,dp.minMonth,dp.minDay);
			var cdMax=new Date(cl_dpMaxYear,cl_dpMaxMonth,cl_dpMaxDay);
			if(dt.compare(cdMax)<=0 && dt.compare(dMin)>=0)
			{
				dp.maxYear=dt.getFullYear();
				dp.maxMonth=dt.getMonth();
				dp.maxDay=dt.getDate();
				hr=true;
			}
		}
	}
	return hr;
}
function dp_setMinDate(lYear,lMonth,lDay)
{
	var dp=this;
	var hr=false;
	if(dp)
	{
		lYear=parseInt(lYear,10);
		lMonth=parseInt(lMonth,10);
		lDay=parseInt(lDay,10);
		if(!(isNaN(lYear) || isNaN(lMonth) || isNaN(lDay)))
		{
			lMonth--;
			var dt=new Date(lYear,lMonth,lDay);
			var dMax=new Date(dp.maxYear,dp.maxMonth,dp.maxDay);
			var cdMin=new Date(cl_dpMinYear,cl_dpMinMonth,cl_dpMinDay);
			if(dt.compare(dMax)<=0 && dt.compare(cdMin)>=0)
			{
				dp.minYear=dt.getFullYear();
				dp.minMonth=dt.getMonth();
				dp.minDay=dt.getDate();
				hr=true;
			}
		}
	}
	return hr;
}
function dp_setCurDate(lYear,lMonth,lDay,lHour,lMinute,lSecond)
{
	var dp=this;
	var hr=false;
	lYear=parseInt(lYear,10);
	lMonth=parseInt(lMonth,10);
	
	if(dp.bHiddenDay==false) {
	    lDay = parseInt(lDay,10);
	    if(dp.bHiddenHour==false){
	        lHour=parseInt(lHour,10);
	        if(dp.bHiddenMinute==false){
	        	lMinute=parseInt(lMinute,10);
	        	if(dp.bHiddenSecond==false){
	               lSecond=parseInt(lSecond,10);	        	
	        	}else{
	        	   lSecond=0;
	        	}
	        }else{
	            lMinute=0;
	            lSecond=0;
	        }
	    }else{
	        lHour=0;
            lMinute=0;
            lSecond=0;
	    }
	} else {
	    lDay = 1;
	    
	}
	if(!(isNaN(lYear) || isNaN(lMonth) || isNaN(lDay)))
	{
		var dt=new Date(lYear,lMonth-1,lDay,lHour,lMinute,lSecond);
		var dMax=new Date(dp.maxYear,dp.maxMonth,dp.maxDay,23,59,59,999);
		var dMin=new Date(dp.minYear,dp.minMonth,dp.minDay,0,0,0,0);
		if(dt.compare(dMax)<=0 && dt.compare(dMin)>=0)
		{
			dp.curDate=dt;
			dp.onDateChange();
			hr=true;
		}
	}
	if(!hr)
		dp.refreshView();
	return hr;
}
function dp_DropClick()
{
	var src=event.srcElement;
	var dp=getParentFromSrc(src,"SPAN")
	if(dp && dp.className=="DPFrame" && dp.dpEnabled)
	{
		dp.showDropDown();
	}
}
function dp_Drop2Click(scrType)
{
	var src=event.srcElement;
	var dp=getParentFromSrc(src,"SPAN")
	if(dp && dp.className=="DPFrame" && dp.dpEnabled)
	{
		dp.showDropDown();
	}
}
function dp_focus(srcType)
{
	var src=event.srcElement;
	if(src && src.tagName=="INPUT")
	{
		switch(srcType)
		{
			case 'year':
				break;
			case 'month':
				break;
			case 'day':
				break;
			case 'hour':
			    break;
			case 'minute':
			    break;
			case 'second':
			    break;
			default:;
		}
		src.select();
	}
	return true;
}
function dp_blur(srcType)
{
	var src=event.srcElement;
	var dp=getParentFromSrc(src,"SPAN")
	if(src && src.tagName=="INPUT" && dp && dp.className=="DPFrame")
	{
		var lYear=dp.curDate.getFullYear();
		var lMonth=dp.curDate.getMonth()+1;
		var lDay=dp.curDate.getDate();
		var lHour=dp.curDate.getHours();
		var lMinute=dp.curDate.getMinutes();
		var lSecond=dp.curDate.getSeconds();

		var val=parseInt(src.value,10);
		if(isNaN(val))
			val=-1;
		switch(srcType)
		{
			case 'year':
				lYear=val==-1?lYear:val;
				break;
			case 'month':
				lMonth=val==-1?lMonth:val;
				break;
			case 'day':
				lDay=val==-1?lDay:val;
				break;
			case 'hour':
				lHour=val==-1?lHour:val;
				break;
			case 'minute':
				lMinute=val==-1?lMinute:val;
				break;
			case 'second':
				lSecond=val==-1?lSecond:val;
				break;
			default:;
		}
		dp.setCurDate(lYear,lMonth,lDay,lHour,lMinute,lSecond);
		if(val==-1)
			dp.refreshView();
	}
	return true;
}
function dp_keyDown(srcType)
{
	var src=event.srcElement;
	var dp=getParentFromSrc(src,"SPAN")
	var bRefresh=true;
	if(dp && dp.className=="DPFrame")
	{
		var lYear=dp.curDate.getFullYear();
		var lMonth=dp.curDate.getMonth();
		var lDay=dp.curDate.getDate();
		var lHour=dp.curDate.getHours();
		var lMinute=dp.curDate.getMinutes();
		var lSecond=dp.curDate.getSeconds();

		var lStep=0;
		switch(event.keyCode)
		{
			case 38:
				lStep=1;
				break;
			case 40:
				lStep=-1;
				break;
			case 13:
				event.keyCode=9;
				break;
			default:
				bRefresh=false;
		}
		switch(srcType)
		{
			case 'year':
				lYear+=lStep;
				break;
			case 'month':
				lMonth+=lStep;
				break;
			case 'day':
				lDay+=lStep;
				break;
			case 'hour':
				lHour+=lStep;
				break;
			case 'minute':
				lMinute+=lStep;
				break;
			case 'second':
				lSecond+=lStep;
				break;

			default:;
		}
		if(bRefresh)
		{
			dp.setCurDate(lYear,lMonth+1,lDay,lHour,lMinute,lSecond);
		}
	}
	return true;
}
function dp_monthChange(lStep)
{
	var src=event.srcElement;
	if(src)
	{
		var ddt=getDropDownTable();
		if(ddt && ddt.dp)
		{
			var dt=ddt.dp.curDate.clone();
			var lOldMonth=dt.getMonth();
			var lOldDay=dt.getDate();
			dt.setDate(1);
			dt.setMonth(lOldMonth+lStep+1);
			dt.setDate(0);
			if(dt.getDate()>lOldDay)
				dt.setDate(lOldDay);
			if(ddt.dp.setCurDate(dt.getFullYear(),dt.getMonth()+1,dt.getDate(),dt.getHours(),dt.getMinutes(),dt.getSeconds()))
				ddt.dp.initDropDown();
		}
	}
}
function dp_yearChange(lStep)
{
	var src=event.srcElement;
	if(src)
	{
		var ddt=getDropDownTable();
		if(ddt && ddt.dp)
		{
			var dt=ddt.dp.curDate.clone();
			var lOldYear=dt.getFullYear();
			var lOldDay=dt.getDate();
			dt.setYear(lOldYear+lStep);
			if(dt.getDate()>lOldDay)
				dt.setDate(lOldDay);
			if(ddt.dp.setCurDate(dt.getFullYear(),dt.getMonth()+1,dt.getDate(),dt.getHours(),dt.getMinutes(),dt.getSeconds()))
				ddt.dp.initDropDown();
		}
	}
}
function dp_ddt_click()
{
	var src=event.srcElement;
	if(src && src.tagName=="TD")
	{
		var ddt=getDropDownTable();
		if(ddt && ddt.dp)
		{
			var lOldMonth=ddt.dp.curDate.getMonth();
			if(ddt.dp.setCurDate(src.year,parseInt(src.month,10)+1,parseInt(src.day,10)))
			{
				if(src.month!=lOldMonth)
					ddt.dp.initDropDown();
				else
					dp_onCell(src);
			}
		}
	}
}
function dp_onCell(src)
{
	var row=src.parentElement;
	if(row && row.tagName=="TR" && row.rowIndex>1)
	{
		var ddt=getDropDownTable();
		if(ddt)
		{
			if(ddt.curCell)
				ddt.curCell.className=ddt.curCellOldClass;
			ddt.curCellOldClass=src.className;
			src.className="DPCellSelect";
			ddt.curCell=src;
		}
	}
}
function dp_ddt_dblclick()
{
	var src=event.srcElement;
	if(src && src.tagName=="TD")
	{
		var ddt=getDropDownTable();
		if(ddt && ddt.dp)
		{
			var lOldMonth=ddt.dp.curDate.getMonth();
			var lHour=ddt.dp.curDate.getHours();
			var lMinute=ddt.dp.curDate.getMinutes();
			var lSecond=ddt.dp.curDate.getSeconds();
			
			
			if(ddt.dp.setCurDate(src.year,parseInt(src.month,10)+1,parseInt(src.day,10),lHour,lMinute,lSecond))
			{
				ddt.dp.hideDropDown();
			}
		}
		
	}
}
function dp_sub_docClick()
{
	var src=event.srcElement;
	var ddt=getParentFromSrc(src,"TABLE");
	if(!ddt || ddt.id!="dpDropDownTable")
	{
		dp_hideDropDown();
	}
	event.cancelBubble=true;
	event.returnValue=false;
	return false;
}
function dp_sub_dockeydown()
{
	dp_hideDropDown();
	return true;
}
function hideElement(elmID,intLeft,intTop,intWidth,intHeight)
{
	for (i = 0; i < document.all.tags(elmID).length; i++)
	{
		obj = document.all.tags(elmID)[i];
		if (! obj || ! obj.offsetParent)
			continue;
		// Find the element's offsetTop and offsetLeft relative to the BODY tag.
		objLeft   = obj.offsetLeft;
		objTop    = obj.offsetTop;
		objParent = obj.offsetParent;
		while (objParent.tagName.toUpperCase() != "BODY")
		{
			objLeft  += objParent.offsetLeft;
			objTop   += objParent.offsetTop;
			objParent = objParent.offsetParent;
		}
		// Adjust the element's offsetTop relative to the dropdown menu
		if (intLeft > (objLeft + obj.offsetWidth) || objLeft > (intLeft + intWidth))
			;
		else if (objTop < (intTop))  // 要隐藏的控件在日期控件的上方
			;
		else if (objTop > (intTop + intHeight))  // 要隐藏的控件在日期控件显示范围的下方
			;
		else
		  {
			obj.style.visibility = "hidden";
		  }
	}
}
function showElement(elmID)
{
	for (i = 0; i < document.all.tags(elmID).length; i++)
	{
		obj = document.all.tags(elmID)[i];
		if (! obj || ! obj.offsetParent)
			continue;
			obj.style.visibility = "";
	}
}
function KeyFilter(type)
{
	var berr=false;
	
	switch(type)
	{
		case 'date':
			if (!(event.keyCode == 45 || event.keyCode == 47 || (event.keyCode>=48 && event.keyCode<=57)))
				berr=true;
			break;
		case 'number':
			if (!(event.keyCode>=48 && event.keyCode<=57))
				berr=true;
			break;
		case 'cy':
			if (!(event.keyCode == 46 || (event.keyCode>=48 && event.keyCode<=57)))
				berr=true;
			break;
		case 'long':
			if (!(event.keyCode == 45 || (event.keyCode>=48 && event.keyCode<=57)))
				berr=true;
			break;
		case 'double':
			if (!(event.keyCode == 45 || event.keyCode == 46 || (event.keyCode>=48 && event.keyCode<=57)))
				berr=true;
			break;
		default:
			if (event.keyCode == 35 || event.keyCode == 37 || event.keyCode==38)
				berr=true;
	}
	return !berr;
}
function getParentFromSrc(src,parTag)
{
	if(src && src.tagName!=parTag)
		src=getParentFromSrc(src.parentElement,parTag);
	return src;
}
function switchToOption(sel,newOption,byWhat)
{
	newOption=newOption.toString();
	if(newOption && sel && sel.tagName=="SELECT")
	{
		newOption=trim(newOption);
		var opts=sel.options;
		for(var i=0;i<opts.length;i++)
		{
			if(trim(opts[i][byWhat].toString())==newOption)
			{
				sel.selectedIndex=i;
				break;
			}
		}
	}
}
function isElementVisible(src)
{
	if(src)
	{
		var x=getOffsetLeft(src)+2-document.body.scrollLeft;
		var y=getOffsetTop(src)+2-document.body.scrollTop;
		if(ptIsInRect(x,y,0,0,document.body.offsetWidth,document.body.offsetHeight))
		{
			var e=document.elementFromPoint(x,y);
			return src==e;
		}
	}
			
	return false;
}
function ptIsInRect(x,y,left,top,right,bottom)
{
	return (x>=left && x<right) && (y>=top && y<bottom);
}
function getOffsetLeft(src)
{
	var set=0;
	if(src)
	{
		if (src.offsetParent)
			set+=src.offsetLeft+getOffsetLeft(src.offsetParent);
		
		if(src.tagName!="BODY")
		{
			var x=parseInt(src.scrollLeft,10);
			if(!isNaN(x))
				set-=x;
		}
	}
	return set;
}
function getOffsetTop(src)
{
	var set=0;
	if(src)
	{
		if (src.offsetParent)
			set+=src.offsetTop+getOffsetTop(src.offsetParent);
		
		if(src.tagName!="BODY")
		{
			var y=parseInt(src.scrollTop,10);
			if(!isNaN(y))
				set-=y;
		}
	}
	return set;
}
function isAnyLevelParent(src,par)
{
	var hr=false;
	if(src==par)
		hr=true;
	else if(src!=null)
		hr=isAnyLevelParent(src.parentElement,par);
	
	return hr;
}


//-------------------------------------------------------------
function isIE(version)
{
	var i0=navigator.appVersion.indexOf("MSIE")
	var i1=-1;
	var ver=0;
	if(i0>=0)
	{
		i1=navigator.appVersion.indexOf(" ",i0+1);
		if(i1>=0)
		{
			i0=i1;
			i1=navigator.appVersion.indexOf(";",i0+1);
			if(i1>=0)
			{
				ver=parseFloat(navigator.appVersion.substring(i0+1,i1));
				if(isNaN(ver))
					ver=0;
			}
		}
	}
	
	return (navigator.userAgent.indexOf("MSIE")!= -1
		&& navigator.userAgent.indexOf("Windows")!=-1
		&& ((ver<(version+1) && ver>=version) || version==0));
}
function getValidDate(str)
{
	var sDate=str.replace(/\//g,"-");
	var vArr=sDate.split("-");
	var sRet="";
	
	if(vArr.length>=3)
	{
		var year=parseInt(vArr[0],10);
		var month=parseInt(vArr[1],10);
		var day=parseInt(vArr[2],10);
		if(!(isNaN(year) || isNaN(month) || isNaN(day)))
			if(year>=1900 && year<9999 && month>=1 && month<=12)
			{
				var dt=new Date(year,month-1,day);
				year=dt.getFullYear();
				month=dt.getMonth()+1;
				day=dt.getDate();
				sRet=year+"-"+(month<10?"0":"")+month+"-"+(day<10?"0":"")+day;
			}
	}
	
	return sRet;
}
function getSafeValue(val,def)
{
	if(typeof(val)=='undefined' || val==null)
		return def;
	else
		return val;
}
function createSelectPicker(sName, sType, sOldStr, sOldIds, bMultiSelect, sFieldName, sWhereValue, sMessage, iWidth)
{
    if(sOldStr==null || sOldStr == "null") sOldStr = "";
    if(sOldIds==null || sOldIds == "null") sOldIds = "";
    if(sOldStr=="") sOldIds = "";
    if(bMultiSelect==null) bMultiSelect=false;
    if(sFieldName==null || sWhereValue==null) {
        sFieldName=null;
        //sWhereValue="";
    }
    if(iWidth==null) iWidth = (bMultiSelect ? 60 : 25);
	var spID="sp_"+(m_iPickerCount++);
    var sDescHeight = getDescription(sType);
    var sDesc = sDescHeight.Desc;
	document.write("<span class=SPFrame id="+spID+">");
	document.write("<input class=SPShow type=text value=\""+sOldStr+"\" size="+iWidth+" name=\""+sName+"_str\" onkeydown=\"javascript:return sp_CancelChange()\" onmouseup=\"javascript:return sp_CancelChange()\">");
	document.write("<input class=SPButton type=\"button\" value=\"选择"+sDesc+"\" onclick=\"return sp_OpenPane();\">");
	document.write("<input type=hidden size=4 value=\""+sOldIds+"\" name=\""+sName+"\">");
	document.write("</span>");
	var sp=document.all(spID);
	sp_initSelectPicker(sp, sName, sType, sDesc, bMultiSelect, sFieldName, sWhereValue, sMessage,
	        sDescHeight.dlgHeight, sDescHeight.dlgWidth);
	return sp;
}
function getDescription(sType)
{
    var retval = new Object();
    retval.dlgWidth = 500;
    switch (sType) {
        case 'customer':
            retval.Desc = '客户';
            retval.dlgHeight = 310;
            break;
        case 'salesman':
            retval.Desc = '客户经理';
            retval.dlgHeight = 340;
            break;
        case 'salessupport':
            retval.Desc = '客户支持';
            retval.dlgHeight = 340;
            break;
        case 'vipservice':
            retval.Desc = 'VIP服务人员';
            retval.dlgHeight = 340;
            break;
        case 'vipmaker':
            retval.Desc = 'VIP制作人员';
            retval.dlgHeight = 340;
            break;
        case 'assistant':
            retval.Desc = '客户经理助手';
            retval.dlgHeight = 340;
            break;
        case 'linkman':
            retval.Desc = '联系人';
            retval.dlgHeight = 320;
            break;
        case 'category':
            retval.Desc = '行业';
            retval.dlgHeight = 320;
            retval.dlgWidth = 760;
            break;
        case 'category1':
            retval.Desc = '行业';
            retval.dlgHeight = 440;
            retval.dlgWidth = 600;
            break;
        case 'intent':
            retval.Desc = '购买意向';
            retval.dlgHeight = 460;
            break;
        case 'contract':
            retval.Desc = '合同';
            retval.dlgHeight = 420;
            break;
    }
    return retval;
}
function sp_initSelectPicker(sp, sName, sType, sDesc, bMultiSelect, sFieldName, sWhereValue,
        sMessage, sDlgHeight, sDlgWidth)
{
    if(sp)
    {
        sp.ctrlName = sName;
        sp.ctrlType = sType;
        sp.description = sDesc;
        sp.multiSelect = bMultiSelect;
        sp.fieldName = sFieldName;
        sp.whereValue = sWhereValue;
        sp.message = sMessage;
        sp.dlgHeight = sDlgHeight;
        sp.dlgWidth = sDlgWidth;
        sp.showPaneWindow = sp_showPaneWindow;
    }
}
function sp_OpenPane()
{
    var src=event.srcElement;
    var sp=getParentFromSrc(src,"SPAN")
	if(src && src.tagName=="INPUT" && sp && sp.className=="SPFrame")
	{
        sp.showPaneWindow();
    }
    return true;
}
function sp_CancelChange()
{
    var src=event.srcElement;
	if(src && src.tagName=="INPUT" && src.className=="SPShow")
	{
	    if("keydown"==event.type){
    		switch (event.keyCode){
    			case 35:		//home	
		   		case 36:		//end
    			case 37:		//left
	    		case 39:		//right
    				return true;
    			default:
    		}
    	}
        event.returnValue = false;
        return false;
    }
}
function sp_showPaneWindow()
{
	var sp=this;
	if(sp.fieldName!=null && sp.whereValue!=null) {
        var wVal = eval(sp.whereValue);
        if(wVal == "") {
	        alert(sp.message);
	        return false;
	    }
	    if(sp.ctrlType == "category" || sp.ctrlType == "category1" ) {
            if(wVal.indexOf("a") != 0 && wVal.indexOf("b") != 0 && wVal.indexOf("c2") != 0 ) {
	            alert("该产品没有行业类目。");
	            return false;
            }
	    }
	}
	var src1=sp.children[0];
    var src2=sp.children[2];
    if(src1 && src1.tagName=="INPUT" && src2 && src2.tagName=="INPUT")
    {
        var dArgs = new Object();
        dArgs.description = sp.description;
        dArgs.ctrlType = sp.ctrlType
        dArgs.oldName = src1.value;
        dArgs.oldValue = src2.value;
        if(sp.fieldName!=null) dArgs.fieldName = sp.fieldName;
        if(sp.whereValue!=null) dArgs.whereValue = eval(sp.whereValue);
        dArgs.multiSelect = sp.multiSelect;
        var ret;
        if(sp.ctrlType == "category1"){
            ret = window.showModalDialog("/bin/selectpicker/category?style=1&ali_site=2&parent="+src2.value, dArgs, "dialogHeight: "+sp.dlgHeight+"px; dialogWidth: "+sp.dlgWidth+"px; dialogTop: px; dialogLeft: px; edge: Raised; center: Yes; help: No; resizable: No; status: No;");
        }else{
            ret = window.showModalDialog("/js/SelectPane.html", dArgs, "dialogHeight: "+sp.dlgHeight+"px; dialogWidth: "+sp.dlgWidth+"px; dialogTop: px; dialogLeft: px; edge: Raised; center: Yes; help: No; resizable: No; status: No;");
        }
        if(ret && ret.returnName!=null && ret.returnID != null)
        {
            src1.value = ret.returnName;
            src2.value = ret.returnID;
        }
    }
    return true;
}
function createCheckBoxPicker()
{
    var args=createCheckBoxPicker.arguments;
    if(args.length < 3) return null;
    var sName = args[0];
    var sOldValue = (isNaN(args[1]) ? 0 : parseInt(args[1], 10));
    var sPutValue = (sOldValue<=0) ? 0 : sOldValue;
    sOldValue = (sOldValue<=0) ? -1 : sOldValue;
	var sNewLine = (args.length >= 3 && args[2]) ? "<br>" : "&nbsp;";
	var cbpID="cbp_"+(m_iPickerCount++);
    document.write("<span class=CBPFrame id="+cbpID+">");
	for(var i=4; i<args.length; i+=2)
	{
        var val = (isNaN(args[i-1]) ? 0 : parseInt(args[i-1], 10));
        document.write("<input class=CBPINPUT type=\"checkbox\" value=\""+val+"\" "+((val & sPutValue)==val?"checked":"")+" onclick=\"return cbp_CheckBoxClick()\">"+args[i]);
        document.write(sNewLine);
	}
	document.write("<input type=hidden value=\""+sOldValue+"\" name=\""+sName+"\">");
	document.write("</span>");
    var cbp = document.all(cbpID);
    cbp.refreshValue = cbp_refreshValue;
    return cbp;
}
function cbp_CheckBoxClick()
{
    var src=event.srcElement;
    var cbp=getParentFromSrc(src,"SPAN")
	if(src && src.tagName=="INPUT" && cbp && cbp.className=="CBPFrame")
	{
        cbp.refreshValue();
    }
    return true;
}
function cbp_refreshValue()
{
    var cbp = this;
    var val = 0;
    for(var i=0; i<cbp.children.length-1; i++) {
        var src=cbp.children[i];
        if(src && src.className == "CBPINPUT" && src.checked) {
            val = val + parseInt(src.value, 10);
        }
    }
    src = cbp.children[cbp.children.length-1];
    if(src)
        src.value = (val<=0?-1:val);
}

function createCheckBoxPicker2()
{
    var args=createCheckBoxPicker2.arguments;
    if(args.length < 4) return null;
    var sName = args[0];
    var sOldValue = (isNaN(args[1]) ? 0 : parseInt(args[1], 10));
    var sPutValue = (sOldValue<=0) ? 0 : sOldValue;
    sOldValue = (sOldValue<=0) ? -1 : sOldValue;
    var sNewLine = (args.length >= 3 && args[2]) ? "<br>" : "&nbsp;";
    var disableMask = (args.length >= 4 && args[3]) ? args[3] : 0;
    var cbpID="cbp_"+(m_iPickerCount++);
    document.write("<span class=CBPFrame id="+cbpID+">");
    var count=0;
	for(var i=5; i<args.length; i+=2)
	{
        var val = (isNaN(args[i-1]) ? 0 : parseInt(args[i-1], 10));
        if((disableMask & val )!=0 ){
          document.write("<input class=CBPINPUT type=\"checkbox\" value=\""+val+"\" "+((val & sPutValue)==val?"checked":"")+" disabled><font color=gray>"+args[i]+"</font>");
        }else{
          document.write("<input class=CBPINPUT type=\"checkbox\" value=\""+val+"\" "+((val & sPutValue)==val?"checked":"")+" onclick=\"return cbp_CheckBoxClick()\">"+args[i]);
        }
        document.write(sNewLine);
        count++;
	}
	document.write("<input type=hidden value=\""+sOldValue+"\" name=\""+sName+"\">");
	document.write("</span>");
    var cbp = document.all(cbpID);
    cbp.refreshValue = cbp_refreshValue;
    return cbp;
}

function showCheckBoxPicker()
{
    var args=showCheckBoxPicker.arguments;
    if(args.length < 2) return null;
    var sOldValue = (isNaN(args[0]) ? 0 : parseInt(args[0], 10));
    if(sOldValue <= 0) sOldValue=0;
	var sNewLine = (args.length >= 2 && args[1]) ? "<br>" : "&nbsp;";
	for(var i=3; i<args.length; i+=2)
	{
        var val = (isNaN(args[i-1]) ? 0 : parseInt(args[i-1], 10));
        if( (val & sOldValue) == val ) {
            document.write(args[i]);
            document.write(sNewLine);
        }
	}
}
/////////////////////////////////////////////////////////////////////////////////////////////
// Scroll Table
/////////////////////////////////////////////////////////////////////////////////////////////
function createScrollTable(tableObj, thisMaxCols, startCols) {
    if(tableObj == null) return null;
    var iRowsCount = tableObj.rows.length;
    if(iRowsCount <= 0) return null;
    var iColsCount = tableObj.rows(0).cells.length;
    if(iColsCount <= thisMaxCols) return null;
    iStartCols = (startCols==null) ? 0 : startCols;
    var stID="st_"+(m_iPickerCount++);
    document.write("<span id=\"" + stID + "\"></span>");
    var oData = document.all(stID);
    var aElement=document.createElement("<a style='cursor:hand' onclick='javascript:return st_LeftRight(-1);'></a>");
    aElement.innerHTML="<img src='/images/left_arrow.gif' border=0>";
    oData.appendChild(aElement);
    aElement=document.createElement("<span></span>");
    aElement.innerHTML="&nbsp;&nbsp;";
    oData.appendChild(aElement);
    aElement=document.createElement("<a style='cursor:hand' onclick='javascript:return st_LeftRight(1);'></a>");
    aElement.innerHTML="<img src='/images/right_arrow.gif' border=0>";
    oData.appendChild(aElement);
    oData.appendChild(tableObj);
    oData.maxCols = thisMaxCols - iStartCols;
    oData.startCol = iStartCols;
    oData.curCol = oData.startCol;
    oData.tabObj = tableObj;
    oData.tabRowsCount = iRowsCount;
    oData.tabColsCount = iColsCount;
    oData.hiddenCells = st_HiddenCells;
    oData.hiddenCells();
    return oData;
}
function st_LeftRight(f)
{
    var src=event.srcElement;
	var st=getParentFromSrc(src,"SPAN")
    st.curCol += f * st.maxCols;
    if(st.curCol < st.startCol) st.curCol = st.startCol;
    if(st.curCol > st.tabColsCount - 1) st.curCol = st.curCol - st.maxCols;
    st.hiddenCells();
    return false;
}
function st_HiddenCells()
{
    var st = this;
    if(st.tabRowsCount <= 0) return;
    //if(st.tabColsCount < st.curCol) return;
    for(var i=0; i<st.tabRowsCount; i++) {
        for(var j=st.startCol; j<st.curCol; j++) {
            st.tabObj.rows(i).cells(j).style.display = "none";
        }
        for(var j=st.curCol; j<st.curCol + st.maxCols && j<st.tabColsCount; j++) {
            st.tabObj.rows(i).cells(j).style.display = "";
        }
        for(var j=st.curCol + st.maxCols; j<st.tabColsCount; j++) {
            st.tabObj.rows(i).cells(j).style.display = "none";
        }
    }
}
