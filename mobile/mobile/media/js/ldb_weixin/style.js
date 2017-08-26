// JavaScript Document

		
	
	
	
	
	
	
	
	
	
		
//支付成功弹出框	
	$(function(){
	$('.box-btn').click(function(e){
		$('#suc_div').lightbox_me({
					overlaySpeed:0,
					lightboxSpeed:0,
            		centered: true, 
            		onLoad: function() { 
						var target = $.event.fix(e).currentTarget;
            		}
        	});
		e.preventDefault();
	})
});

//支付失败弹出框
    $(function(){
	$('.box-logo').click(function(e){
		$('#fail_div').lightbox_me({
					overlaySpeed:0,
					lightboxSpeed:0,
            		centered: true, 
            		onLoad: function() { 
						var target = $.event.fix(e).currentTarget;
            		}
        	});
		e.preventDefault();
	})
});


      function dismiss(){
		$('#suc_div').trigger('close');
		$('#fail_div').trigger('close');
	}
	
	
	
	
	
	
	
	
	