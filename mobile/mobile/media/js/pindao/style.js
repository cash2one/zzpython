
$(function(){
	$('.r_box').click(function(e){
		$('#reply_div').lightbox_me({
					overlaySpeed:0,
					lightboxSpeed:0,
            		centered: true, 
            		onLoad: function() { 
						var target = $.event.fix(e).currentTarget;
						
            		}
        	});
		e.preventDefault();
	});
});


function dismiss(){
	$('#reply_div').trigger('close');
}

function mySwitch(){
    document.getElementById('nav_1').style.display = document.getElementById('nav_1').style.display=='none'?'block':'none';
	document.getElementById('nav_2').style.display = 'none';
	document.getElementById('nav_3').style.display = 'none';
}

function mySwitch1(){
    document.getElementById('nav_2').style.display = document.getElementById('nav_2').style.display=='none'?'block':'none';
	document.getElementById('nav_1').style.display = 'none';
	document.getElementById('nav_3').style.display = 'none';
}
function mySwitch2(){
    document.getElementById('nav_3').style.display = document.getElementById('nav_3').style.display=='none'?'block':'none';
	document.getElementById('nav_2').style.display = 'none';
	document.getElementById('nav_1').style.display = 'none';
}

$(function(){
	$('.btn_confirm').click(function(){
		var area=$("#area1").val();
		var timearg=$("#timearg1").val();
		var keywords=$("#keywords").val();
		var ptype=$("#ptype").val();
		var haveprice=$("#haveprice").val();
		var havepic=$("#havepic").val();
		window.location.href='?keywords='+keywords+'&province='+area+'&timearg='+timearg+'&ptype='+ptype+'&haveprice='+haveprice+'&havepic='+havepic;
	});
});

$(document).ready(function() {
	$("#b1_ul li").click(function(){
		var self=$(this);
		var cssvalue=self.css("background-color");

		if (cssvalue=="rgb(219, 219, 219)"){
		self.css("background-color","#fff");
		$("#area1").val("");
		}else{
		$("#b1_ul li").css("background-color","#fff");
		self.css("background-color","#dbdbdb");
		$("#area1").val(self.attr("area"));
		}
		
	});	
	$("#b1_ul2 li").click(function(){
		var self=$(this);
		var cssvalue2=self.css("background-color");
		if (cssvalue2=="rgb(219, 219, 219)"){
		self.css("background-color","#fff");
		$("#timearg1").val("");
		}else{
		$("#b1_ul2 li").css("background-color","#fff");
		self.css("background-color","#dbdbdb");
		$("#timearg1").val(self.attr("timearg"));
		}
	});	
});

function telclick(url){
	$.ajax({
	   type: "GET",
	   url: url,
	   data: '',
	   success:function(data){},
	   error:function(data){}
	}); 
}











