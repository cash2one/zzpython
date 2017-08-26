// JavaScript Document

function openoverlay(url,title,html,overlayheight)
{
	overlaywidth=$("body").width()/2+100;
	if (overlayheight==""){
		overlayheight=$(window).height()/2;
	}
	var simpleWindown_html = new String;
	simpleWindown_html ="<div id=\"TB_overlayBG\">&nbsp;</div>";
	simpleWindown_html += "<center><div class=\"overlaybox\" style=\"display:none\">";
	simpleWindown_html += "<div class=\"nbox\">";
	simpleWindown_html += "<h2><span id=otitle>"+title+"</span><a class=\"overlayclose\" href=\"javascript:closeoverlay();\">×</a></h2>";
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
		left:($("body").width()-overlaywidth)/2-20+"px",
		top:($(window).height()-overlayheight)/2+$(window).scrollTop()+"px",
		display:"block"
	});
	$(".overlaybox").css("width",overlaywidth+5);
	$(".overlaybox").css("height",overlayheight+38);
	$("#overlaylink").css("width",overlaywidth);
	$("#overlaylink").css("height",overlayheight);
	if (document.getElementById("overlaylink")){
		document.getElementById("overlaylink").src=url;
	}
}

function closeoverlay()
{
	$("#TB_overlayBG").css("display","none");
	$(".overlaybox ").css("display","none");
	if (document.getElementById("overlaylink")){
	document.getElementById("overlaylink").src="";
	}
}