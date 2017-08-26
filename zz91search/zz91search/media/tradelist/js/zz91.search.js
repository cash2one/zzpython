function zz91newsearch(frm,s)
{
	var type=$("#TopSeaType").val();
	var searcfrm=frm.keywords
	if (searcfrm){
		var searchvalue=searcfrm.value;
	}

	if (searchvalue=="" || searchvalue=="请输入搜索关键字")
	{
		alert("请输入搜索关键字！");
		frm.search_text.focus();
		return false;
	}
	if (searchvalue!="")
	{
		
		//searchvalue=searchvalue.replace(/\//gm,"astoxg");
//		searchvalue=searchvalue.replace(/\%/gm,"astoxf");
//		searchvalue=searchvalue.replace(/\\/gm,"astoxl");
//		searchvalue=searchvalue.replace(/-/gm,"astohg");
//		searchvalue=searchvalue.replace(/\(/gm,"astokhl");
//		searchvalue=searchvalue.replace(/\)/gm,"astokhr");
		searchvalue=encodeURI(searchvalue)
	}
	if (type=="1")
	{
		
		frm.action="http://www.zz91.com/trade/searchfirst/?keywords="+searchvalue+"";
		window.location=frm.action;
		return false;
		//frm.action="http://trade.zz91.com/offerlist--a1--p--"+searchvalue+".htm";
		frm.target="_self"
	}
	if (type=="2")
	{
		frm.action="http://www.zz91.com/trade/searchfirst/?keywords="+searchvalue+"&ptype=2";
		window.location=frm.action;
		return false;
		//frm.action="http://trade.zz91.com/offerlist--a2--p--"+searchvalue+".htm";
		frm.target="_self";
	}
	if (type=="3")
	{
		frm.action="http://price.zz91.com/priceSearch.htm?title="+searchvalue+"";
		frm.target="_blank";
	}
	if (type=="5")
	{
		frm.action="http://www.zz91.com/photo/searchPic.htm?searchKey="+searchvalue+"";
		frm.target="_blank";
	}
	if (type=="4")
	{
		frm.action="http://company.zz91.com/index-p-"+searchvalue+".htm";
		frm.target="_blank";
	}
	if (type=="6")
	{
		frm.action="http://xianhuo.zz91.com/spot.htm?title="+searchvalue+"";
		frm.target="_blank";
	}
	
	if (s==1){
		frm.submit();
		//return false
	}
}

$(document).ready(function() {
	$(".search_bar li").click(function() {
		var no = $(this).attr("value");
		$("#TopSeaType").val(no);
		$(".search_bar li").removeClass("searchnav_on");
		$(this).addClass("searchnav_on");
	});	
	$.focusblur = function(focusid) {
		var focusblurid = $(focusid);
		var defval = focusblurid.val();
		alert(defval)
		focusblurid.focus(function(){
			var thisval = $(this).val();
			if(thisval==defval){
				//$(this).val("");
				$(this).css("color","#00a44b");
			}
		});
		focusblurid.blur(function(){
			var thisval = $(this).val();
			if(thisval==""){
				$(this).val(defval);
				$(this).css("color","#CCC");
			}
		});
	};
	$("#search_a1").click(function(){
		zz91newsearch(document.getElementById("searchForm1"),1);
	})
	$("#search_a2").click(function(){
		zz91newsearch(document.getElementById("searchForm2"),1);
	})
	//////////////////////////////////////////////////
	
});




/*搜索导航的字体变色*/
