function bookmarks() {
    $('body,html').animate({
        scrollTop: '0px'
    },
    "slow")
}
$(document).ready(function(e) {
    $(".item-title-icon2").click(function(){
		$(this).parent().next(".item-div").fadeToggle();
	});
	$(".item-title-icon").click(function(){
		$(this).parent().next(".item-block").fadeToggle();
		
		
	});
	$(".item-div-box").click(function(){
		var str=$(this).find(".item-div-icon").css("display");
		if(str==="none"){
			$(this).removeClass("item-div-style");
			$(this).addClass("item-div-click");
			$(this).find(".item-div-icon").css("display","block");
			//alert($(this).find(".item_div_i").attr("checked"))
			//$(this).find(".item_div_i").val("1");
			$(this).find(".item_div_i").attr("checked",'true');
		}else{
			$(this).removeClass("item-div-click");
			$(this).addClass("item-div-style");
			$(this).find(".item-div-icon").css("display","none");
			//$(this).find(".item_div_i").val("0");
			$(this).find(".item_div_i").removeAttr("checked");
		}
		$("#formorder").submit();
	});
	
	$(".box-nav table tr td").click(function(){
		$(".box-nav table tr td").removeClass("box-table-click");
		$(".box-nav table tr td").addClass("box-table-bg");
		$(".box-nav table tr td div").removeClass("box-click");
		$(".box-nav table tr td div").addClass("box-bg");
		$(".box-nav table tr td").find("img").attr("src","http://img0.zz91.com/zz91/mobile/images/type_bg.jpg");
		$(this).find("img").attr("src","http://img0.zz91.com/zz91/mobile/images/type_click.jpg");
		$(this).removeClass("box-table-bg");
		$(this).addClass("box-table-click");
		$(this).children("div").removeClass("box-bg");
		$(this).children("div").addClass("box-click");
		
		var categorycode = $(this).attr("categorycode");
		$(".box-div").html("<img src='/images/load.gif'>");
		var ajaxurl="http://m.zz91.com/categoryinfo.html?categorycode="+categorycode;
		$.getScript(ajaxurl, function() {
				var result = categorylist;
				$(".box-div").html(result);
				return false;
		});
		
	});
	$(".box-nav ul li").click(function(){
		$(".box-nav ul li").removeClass("box-table-click");
		$(".box-nav ul li").addClass("box-table-bg");
		$(".box-nav ul li div").removeClass("box-click");
		$(".box-nav ul li div").addClass("box-bg");
		$(this).removeClass("box-table-bg");
		$(this).addClass("box-table-click");
		$(this).children("div").removeClass("box-bg");
		$(this).children("div").addClass("box-click");
		
		var categorycode = $(this).attr("categorycode");
		$(".box-div").html("<img src='/images/load.gif'>");
		var ajaxurl="http://m.zz91.com/categoryinfo.html?categorycode="+categorycode;
		$.getScript(ajaxurl, function() {
				var result = categorylist;
				$(".box-div").html(result);
				return false;
		});
		
	});
	
	$("#category").click(function(){
		$("#toplist").stop(true,true).slideToggle("show");
	});
	$("#slideup").click(function(){
		$("#toplist").stop(true,true).slideToggle("show");
	});
	
	
	$(".item-title-img").click(function(){
		var str=$(this).children("img").css("display");
		if(str==="none"){
			$(this).children("img").css("display","block");
			$(this).parent().next(".item-block").children(".item-title2").children(".item-title-img2").children("img").css("display","block");
			$(this).parent().next(".item-block").find(".item-div-box").removeClass("item-div-style");
			$(this).parent().next(".item-block").find(".item-div-box").addClass("item-div-click");
			$(this).parent().next(".item-block").find(".item-div-box").find(".item-div-icon").css("display","block");
			//$(this).parent().next(".item-block").find(".item-div-box").children(".item_div_i").val("1");
			//$(this).parent().next(".item-block").children(".all").val("1");
			$(this).parent().next(".item-block").find(".item-div-box").find(".item_div_i").attr("checked",'true');
			$(this).parent().find("#itemparent").attr("checked",'true');
			//var categorycode = $(this).attr("categorycode");
			//var ajaxurl="/order/save_collect.html?categorycode="+categorycode+"&collect_type=1";
			//$.ajax({url:ajaxurl,async:false});
		}else{
			$(this).children("img").css("display","none");
			$(this).parent().next(".item-block").children(".item-title2").children(".item-title-img2").children("img").css("display","none");
			$(this).parent().next(".item-block").find(".item-div-box").removeClass("item-div-click");
			$(this).parent().next(".item-block").find(".item-div-box").addClass("item-div-style");
			$(this).parent().next(".item-block").find(".item-div-box").find(".item-div-icon").css("display","none");
			//$(this).parent().next(".item-block").find(".item-div-box").children(".item_div_i").val("0");
			$(this).parent().next(".item-block").find(".item-div-box").find(".item_div_i").removeAttr("checked");
			$(this).parent().find("#itemparent").removeAttr("checked");
			//$(this).parent().next(".item-block").children(".all").val("0");
		}
		$("#formorder").submit();
	});
	$(".item-title-img2").click(function(){
		var str=$(this).parent().next(".item-div").children(".all").val();
		if(str==="0"){
			$(this).children("img").css("display","block");
			$(this).parent().next(".item-div").children(".item-div-box").removeClass("item-div-style");
			$(this).parent().next(".item-div").children(".item-div-box").addClass("item-div-click");
			$(this).parent().next(".item-div").children(".item-div-box").find(".item-div-icon").css("display","block");
			//$(this).parent().next(".item-div").children(".item-div-box").children(".item_div_i").val("1");
			$(this).parent().next(".item-div").children(".all").val("1");
		}else{
			$(this).children("img").css("display","none");
			$(this).parent().next(".item-div").children(".item-div-box").removeClass("item-div-click");
			$(this).parent().next(".item-div").children(".item-div-box").addClass("item-div-style");
			$(this).parent().next(".item-div").children(".item-div-box").find(".item-div-icon").css("display","none");
			//$(this).parent().next(".item-div").children(".item-div-box").children(".item_div_i").val("0");
			$(this).parent().next(".item-div").children(".all").val("0");
		}
	});
	
});
