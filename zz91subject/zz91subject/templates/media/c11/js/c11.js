
     $(document).ready(function(){  
           $("#c1").click(function(){ 
                $("#c2").removeClass("mb_c2");
				$("#c2").addClass("mb_g2");
                $("#c3").removeClass("mb_c3"); 
				$("#c3").addClass("mb_g3");
				$("#c4").removeClass("mb_c4"); 
				$("#c4").addClass("mb_g4");
            }); 
			$("#c2").click(function(){ 
                $("#c1").removeClass("mb_c1");
				$("#c1").addClass("mb_g1");
                $("#c3").removeClass("mb_c3"); 
				$("#c3").addClass("mb_g3");
				$("#c4").removeClass("mb_c4"); 
				$("#c4").addClass("mb_g4");
            });
			$("#c3").click(function(){ 
                $("#c2").removeClass("mb_c2");
				$("#c2").addClass("mb_g2");
                $("#c1").removeClass("mb_c1"); 
				$("#c1").addClass("mb_g1");
				$("#c4").removeClass("mb_c4"); 
				$("#c4").addClass("mb_g4");
            });
			$("#c4").click(function(){ 
                $("#c2").removeClass("mb_c2");
				$("#c2").addClass("mb_g2");
                $("#c3").removeClass("mb_c3"); 
				$("#c3").addClass("mb_g3");
				$("#c1").removeClass("mb_c1"); 
				$("#c1").addClass("mb_g1");
            });
        }); 
		
$(function(){
	$('#c1').click(function(e){
		$('#coupons1').lightbox_me({
					overlaySpeed:0,
					lightboxSpeed:0,
            		centered: true, 
            		onLoad: function() { 
            		}
        	});
		e.preventDefault();
	})
});

$(function(){
	$('#suc_login').click(function(e){
		$('#coupons2').lightbox_me({
					overlaySpeed:0,
					lightboxSpeed:0,
            		centered: true, 
            		onLoad: function() { 
            		}
        	});
		e.preventDefault();
	})
});

function dismiss(){
	$('#coupons1').trigger('close');
	$('#suc_draw').trigger('close');
	
}