$(function(){
	$("#nav li").each(function(){
		$(this).click(function(){
			$("#nav li").each(function(){
				$(this).removeClass("on");
        			var idx = $(this).attr("name");
          			$("#"+idx).hide();
    		});
				$(this).addClass("on");
     			var ids=$(this).attr("name");
    			$("#"+ids).show();
		});
	});
});