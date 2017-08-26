// JavaScript Document

	$(function(){
    	$("#back").click(function(){
        	$('body,html').animate({scrollTop:0},1000);
        });
		$("#f1").click(function(){
           	$('html,body').animate({scrollTop:$('#1F').offset().top},1000);
        });
		$("#f2").click(function(){
          	$('html,body').animate({scrollTop:$('#2F').offset().top},1000);
        });
		$("#f3").click(function(){
           	$('html,body').animate({scrollTop:$('#3F').offset().top},1000);
        });
    });
	
	$(function(){
		$("ul.tag01 li a").each(function(){
			$(this).click(function(){
      			$("ul.tag01 li a").each(function(){
					$(this).removeClass("on");
         			var idx = $(this).attr("name");
          			$("#"+idx).hide();
    			});
				$(this).addClass("on");
     			var ids=$(this).attr("name");
     			$("#"+ids).show();
  			});
		});
		$("ul.tag02 li a").each(function(){
			$(this).click(function(){
      			$("ul.tag02 li a").each(function(){
					$(this).removeClass("on");
         			var idx = $(this).attr("name");
          			$("#"+idx).hide();
    			});
				$(this).addClass("on");
     			var ids=$(this).attr("name");
     			$("#"+ids).show();
  			});
		});
		$("ul.tag03 li a").each(function(){
			$(this).click(function(){
      			$("ul.tag03 li a").each(function(){
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