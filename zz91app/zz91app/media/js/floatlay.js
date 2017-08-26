// JavaScript Document

function openoverlay(url,title,html,overlayheight,obj)
{
	if (obj!=""){
		html=$(obj).html()
	}
	var overlaywidth=$("body").width()/2+100;
	if (overlayheight==""){
		overlayheight=$(window).height()/2;
	}
	var simpleWindown_html = new String;
	simpleWindown_html ="<div id=\"TB_overlayBG\" >&nbsp;</div>";
	simpleWindown_html += "<center><div class=\"overlaybox\" style=\"display:none\">";
	simpleWindown_html += "<div class=\"nbox\">";
	if (title!=""){
		simpleWindown_html += "<h2><span id=otitle>"+title+"</span><a class=\"overlayclose\" href=\"javascript:closeoverlay();\">×</a></h2>";
	}else{
		simpleWindown_html += "<h2><a class=\"overlayclose\" href=\"javascript:closeoverlay();\">×</a></h2>";
	}
	
	simpleWindown_html += "<div class=\"mainlist\">";
	if (html!=0){
		simpleWindown_html += html
	}else{
		simpleWindown_html += "<iframe id=\"overlaylink\" name=\"overlaylink\"  frameborder=\"0\" src=''></iframe>";
	}
	simpleWindown_html += "</div></div></div></center>";
	if (!document.getElementById("TB_overlayBG"))
	{
		$("body").append(simpleWindown_html);
	}else{
		if(html!=0){
			$(".mainlist").html(html);
			$("#otitle").html(title)
		}else{
			$("#otitle").html(title)
			$(".mainlist").html("<iframe id=\"overlaylink\" name=\"overlaylink\"  frameborder=\"0\" src=''></iframe>");
		}
	}
	
	$("#TB_overlayBG").css({
		display:"block",
		height:$(document).height(),
		zIndex:6
	});
	$(".overlaybox").css({
		//left:($("body").width()-$(".overlaybox").width())/2-20+"px",
		left:($("body").width()-overlaywidth)/2+"px",
		top:$(window).scrollTop()+80+"px",
		//top:($(window).height()-overlayheight)/2+$(window).scrollTop()+"px",
		display:"block"
	});
	$(".overlaybox").css("width",overlaywidth+5);
	$(".overlaybox").css("height",overlayheight+38);
	$(".mainlist").css("height",overlayheight-10);
	$("#overlaylink").css("width",overlaywidth);
	$("#overlaylink").css("height",overlayheight);
	if (document.getElementById("overlaylink")){
		document.getElementById("overlaylink").src=url;
	}
	minwindow=true
}
function openimglayer(html,overlayheight){
	var overlaywidth=$("body").width()/2+100;
	if (overlayheight==""){
		overlayheight=$(window).height()/2;
	}
	var simpleWindown_html = new String;
	simpleWindown_html ="<div id=\"TB_overlayBG\">&nbsp;</div>";
	simpleWindown_html += "<center><div class=\"overlayboximg\" style=\"display:none\">";
	simpleWindown_html += "<h2><a class=\"overlaycloseimg\" href=\"javascript:closeoverlayimg();\">×</a></h2>";
	simpleWindown_html += "<div class=\"mainlistimg\">";
	if (html!=0){
		simpleWindown_html += "<center>"+html+"</center>";
	}
	simpleWindown_html += "</div></div></center>";
	
	if (!document.getElementById("TB_overlayBG"))
	{
		$("body").append(simpleWindown_html);
	}else{
		if(html!=0){
			$(".mainlistimg").html("<center>"+html+"</center>");
		}
	}
//	$("#TB_overlayBG").css({
//		display:"block",
//		height:$(document).height(),
//		zIndex:6
//	});
	$(".overlayboximg").css({
		//left:($("body").width()-$(".overlaybox").width())/2-20+"px",
		left:($("body").width()-overlaywidth)/2-20+"px",
		top:($(window).height()-overlayheight)/2+$(window).scrollTop()+"px",
		display:"block"
	});
	$(".overlayboximg").css("width",overlaywidth+5);
	$(".overlayboximg").css("height",overlayheight+38);
	minwindow=true
	
}

function closeoverlay()
{
	$("#TB_overlayBG").css("display","none");
	$(".overlaybox ").css("display","none");
	if (document.getElementById("overlaylink")){
		document.getElementById("overlaylink").src="";
	}
	minwindow=null
}
function closeoverlayimg()
{
	$("#TB_overlayBG").css("display","none");
	$(".overlayboximg ").css("display","none");
	inwindow=null
}