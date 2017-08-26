


$(document).ready(function() {
    $("#FeiLiaoLeiMu_nav li").mouseover(function(){
		//$(this).css("background","#f5f5f5");
		$(this).children("ul").css("display","block");
		//$(this).children(".zi21").css("background","url(http://img0.zz91.com/zz91/tradelist/images/areaDown1.png) no-repeat");
		});
	$("#FeiLiaoLeiMu_nav li").mouseout(function(){
		//$(this).css("background","none");
		$(this).children("ul").css("display","none");
		//$(this).children(".zi21").css("background","url(http://img0.zz91.com/zz91/tradelist/images/areaDown0.png) no-repeat");
		});
	
	$("#FeiLiaoLeiMu_nav2 li").mouseover(function(){
		//$(this).css("background","#f5f5f5");
		});
	$("#FeiLiaoLeiMu_nav2 li").mouseout(function(){
		//$(this).css("background","none");
		});
		
	$("#FeiLiaoLeiMu").mouseover(function(){
		$(".FeiLiaoLeiMu_nav").css("display","block");
		});
	$("#FeiLiaoLeiMu").mouseout(function(){
		$(".FeiLiaoLeiMu_nav").css("display","none");
		});
	$(".FeiLiaoLeiMu_nav").mouseover(function(){
		$(".FeiLiaoLeiMu_nav").css("display","block");
		});
	$(".FeiLiaoLeiMu_nav").mouseout(function(){
		$(".FeiLiaoLeiMu_nav").css("display","none");
		});
	$("#FaBu").mouseover(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/fabu2_hover.jpg) no-repeat 20px 10px");
		});
	$("#FaBu").mouseout(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/fabu2.jpg) no-repeat 20px 10px");
		});
	$("#zi9").mouseover(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/fabu_hover.jpg) no-repeat");
		});
	$("#zi9").mouseout(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/fabu.jpg) no-repeat");
		});
		
	$(".zi15").mouseover(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/liuyan_hover.jpg) no-repeat");
		});
	$(".zi15").mouseout(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/liuyan.jpg) no-repeat");
		});
	
	//$("#small li").mouseover(function(){
//		$(this).children("ul").css("display","block");
//		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/icon6.jpg) no-repeat 55px 12px");
//		});
//	$("#small li").mouseout(function(){
//		$(this).children("ul").css("display","none");
//		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/icon5.jpg) no-repeat 55px 12px");
//		});
//	$("#small li ul li").mouseover(function(){
//		$(this).css("background","none");
//		});
//	$("#small li ul li").mouseout(function(){
//		$(this).css("background","none");
//		});
	$("#address").mouseover(function(){
		$(".address_block").css("display","block");
		});
	$("#address").mouseout(function(){
		$(".address_block").css("display","none");
		});
	$(".address_block").mouseover(function(){
		$(".address_block").css("display","block");
		});
	$(".address_block").mouseout(function(){
		$(".address_block").css("display","none");
		});
	$("#time").mouseover(function(){
		$(".time_block").css("display","block");
		});
	$("#time").mouseout(function(){
		$(".time_block").css("display","none");
		});
	$(".time_block").mouseover(function(){
		$(".time_block").css("display","block");
		});
	$(".time_block").mouseout(function(){
		$(".time_block").css("display","none");
		});
	$("#page_ok").mouseover(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/page_ok.jpg) no-repeat");
		});
	$("#page_ok").mouseout(function(){
		$(this).css("background","none");
		});
	
	
	
		
});


$(document).ready(function() {
	$(".mainblock3 .item").mouseover(function(){
		$(this).css("background","#f2f2f2");						  
	});
	$(".mainblock3 .item").mouseout(function(){
		$(this).css("background","#fff");
	});
	$("a").click(function(){
			var self=$(this);
			if (self.attr("target")=="" || !self.attr("target"))
			{
				if (!self.attr("data")){
					$("#page_cover").css("display","");
					$("#page_cover").css("height",$("#bodymain").height());
					$("#page_cover_loading").css("display","");
				}
			}
	});
});
$(window).scroll(function(){
		
	var obj = $("#topBar"); //获取店招的高度
	var height = obj.height();
	var innerHeight=window.innerHeight  //获取显示窗口高度
	|| document.documentElement.clientHeight
	|| document.body.clientHeight;
	
	//判断滚动条是否滚动了230PX+店招高度
	if ($(document).scrollTop() >= ($("#BiaoQian").height()+ $("#gold_wk").height() +$("#gold_wk1").height() +$("#logosearch").height()+ $("#header").height() + $("#topBar").height()+ $("#mainBlock").height() + $(".mainblock1").height() + $("#companyprice").height()+300 ))
	{
		$("#postscroll").addClass("post_right");
	}else{
		$("#postscroll").removeClass("post_right");
	}
	//判断滚动显示窗口高度	
	if ($(document).scrollTop() > (innerHeight))
		$("#top").css("display","block");
	else
	    $("#top").hide();
});

$(document).ready(function(){
	$("#message").mouseover(function(){
		$("#message1").css("background","url(http://img0.zz91.com/zz91/tradelist/images/message_hover.jpg) no-repeat");
		$("#message1").css("display","")
		$("#message1").stop().animate({width:"64px"});
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/message1.jpg) no-repeat");
		$(this).css("border-color","#00632b");
	});
	$("#message").mouseout(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/message.jpg) no-repeat");
		$(this).css("border-color","#ccc");
		$("#message1").css("background","none");
		$("#message1").stop().animate({width:"0px"});
		$("#message1").css("display","none")
	});
	$("#message1").mouseover(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/message_hover.jpg) no-repeat");
		$(this).stop().animate({width:"64px"});
		$("#message").css("background","url(http://img0.zz91.com/zz91/tradelist/images/message1.jpg) no-repeat");
		$("#message").css("border-color","#00632b");
		$("#message1").css("display","")
	});
	$("#message1").mouseout(function(){
		$("#message").css("background","url(http://img0.zz91.com/zz91/tradelist/images/message.jpg) no-repeat");
		$("#message").css("border-color","#ccc");
		$(this).css("background","none");
		$(this).stop().animate({width:"0px"});
		$("#message1").css("display","none")
	});
	$("#join").mouseover(function(){
		$("#join1").css("background","url(http://img0.zz91.com/zz91/tradelist/images/join_hover.jpg) no-repeat");
		$("#join1").stop().animate({width:"78px"});
		$("#join1").css("display","")
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/join1.jpg) no-repeat");
		$(this).css("border-color","#00632b");
	});
	$("#join").mouseout(function(){
		
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/join.jpg) no-repeat");
		$(this).css("border-color","#ccc");
		$("#join1").css("background","none");
		$("#join1").stop().animate({width:"0px"});
		$("#join1").css("display","none");
	});
	$("#join1").mouseover(function(){
		$(this).css("background","url(http://img0.zz91.com/zz91/tradelist/images/join_hover.jpg) no-repeat");
		$(this).stop().animate({width:"78px"});
		$("#join").css("background","url(http://img0.zz91.com/zz91/tradelist/images/join1.jpg) no-repeat");
		$("#join").css("border-color","#00632b");	
		$("#join1").css("display","")
	});
	$("#join1").mouseout(function(){
		$("#join1").css("background","url(http://img0.zz91.com/zz91/tradelist/images/join.jpg) no-repeat");
		$("#join1").css("border-color","#ccc");
		$(this).css("background","none");
		$(this).stop().animate({width:"0px"});
		$("#join1").css("display","none")
	});
	
	$("#top").mouseover(function(){
		$("#top1").stop().animate({width:"64px"});
		$("#top1").css("display","")
	});
	$("#top").mouseout(function(){
		$("#top1").stop().animate({width:"0px"});
		$("#top1").css("display","none")
	});
	$("#top1").mouseover(function(){
		$(this).stop().animate({width:"64px"});
		$("#top1").css("display","");
	});	
	$("#top1").mouseout(function(){
		$(this).stop().animate({width:"0px"});
		$("#top1").css("display","none");
	});
	var ii=0;
	$("#searchForm1 #keywords").keyup(function(event){
		var thisval = $(this).val();
		var ajaxurl="http://pyapp.zz91.com/keywordsearch/?keywords="+thisval;
		$.getScript(ajaxurl, function() {
				if(event.keyCode != 40 && event.keyCode != 38){ 
					var result = _suggest_result_.result;
					var myobj = eval('(' + result + ')');
					var value="<ul>"
					for(var i=0;i<myobj.length-1;i++){
						value+="<li>"+myobj[i].keyword+"</li>"
					}
					value+="</ul>";
					$("#searchresult").css({'position':'absolute','width':($("#keywords").width()+10).toString()+'px','height':(myobj.length*24+20).toString()+'px','display':'','z-index':'800'});
					$("#searchresult").html(value);
					ii=0;
				}
				
				$("#searchresult li").mouseover(function(){
					$(this).css("background","#f2f2f2");						  
				});
				$("#searchresult li").click(function(){
					$("#searchresult").css("display","none")
					$("#keywords").val($(this).html());						  
				});
				$("#searchresult li").mouseout(function(){
					$(this).css("background","#fff");
				});
				if(event.keyCode == 40 || event.keyCode == 38){
					var searchdroplist=$("#searchresult li");
					if (event.keyCode==38){
						ii-=1;
					}else{
						ii+=1;
					}
					if (ii<=0){
						ii=1;
					}
					if (ii>searchdroplist.length){
						ii=searchdroplist.length;
					}
					$("#keywords").val($(searchdroplist[ii-1]).html());
					$("#searchresult li").css("background","#fff");
					$(searchdroplist[ii-1]).css("background","#f2f2f2");
					return false;
				}
		});
		$("body").click(function(){
			$("#searchresult").css("display","none")			  				 	
		});	
	});	
});



function displaySubMenu11(li)
{
	var subMenu = li.getElementsByTagName("div")[1];
	subMenu.style.display = "block";
	var subMenu1 = li.getElementsByTagName("div")[0];
	subMenu1.className="baibaoxiang_on";
	
}
function hideSubMenu11(li){
	var subMenu = li.getElementsByTagName("div")[1];
	subMenu.style.display = "none";
	var subMenu1 = li.getElementsByTagName("div")[0];
	subMenu1.className="baibaoxiang_off";
}
	
function searchin(frm)
{
	if (frm.keywords.value=="")
	{
		return false;
	}
}
	





