
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
}

function mySwitch1(){
    document.getElementById('nav_2').style.display = document.getElementById('nav_2').style.display=='none'?'block':'none';
}
function mySwitch2(){
    document.getElementById('nav_3').style.display = document.getElementById('nav_3').style.display=='none'?'block':'none';
}


window.onload = function(){
				var id = document.getElementById('b1_ul');
				var lis = id.getElementsByTagName('li');
				var len = lis.length;
				for(var i=0;i<len;i++){
				lis[i].onclick = function(){
				for(var j=0;j<len;j++){
					lis[j].style.backgroundColor = "#fff";
				}
				this.style.backgroundColor = "#dbdbdb";
			};
		}
	};












