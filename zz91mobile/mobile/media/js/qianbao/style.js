(function(d,D,v){d.fn.responsiveSlides=function(h){var b=d.extend({auto:!0,speed:1E3,timeout:7E3,pager:!1,nav:!1,random:!1,pause:!1,pauseControls:!1,prevText:"Previous",nextText:"Next",maxwidth:"",controls:"",namespace:"rslides",before:function(){},after:function(){}},h);return this.each(function(){v++;var e=d(this),n,p,i,k,l,m=0,f=e.children(),w=f.size(),q=parseFloat(b.speed),x=parseFloat(b.timeout),r=parseFloat(b.maxwidth),c=b.namespace,g=c+v,y=c+"_nav "+g+"_nav",s=c+"_here",j=g+"_on",z=g+"_s",
o=d("<ul class='"+c+"_tabs "+g+"_tabs' />"),A={"float":"left",position:"relative"},E={"float":"none",position:"absolute"},t=function(a){b.before();f.stop().fadeOut(q,function(){d(this).removeClass(j).css(E)}).eq(a).fadeIn(q,function(){d(this).addClass(j).css(A);b.after();m=a})};b.random&&(f.sort(function(){return Math.round(Math.random())-0.5}),e.empty().append(f));f.each(function(a){this.id=z+a});e.addClass(c+" "+g);h&&h.maxwidth&&e.css("max-width",r);f.hide().eq(0).addClass(j).css(A).show();if(1<
f.size()){if(x<q+100)return;if(b.pager){var u=[];f.each(function(a){a=a+1;u=u+("<li><a href='#' class='"+z+a+"'>"+a+"</a></li>")});o.append(u);l=o.find("a");h.controls?d(b.controls).append(o):e.after(o);n=function(a){l.closest("li").removeClass(s).eq(a).addClass(s)}}b.auto&&(p=function(){k=setInterval(function(){var a=m+1<w?m+1:0;b.pager&&n(a);t(a)},x)},p());i=function(){if(b.auto){clearInterval(k);p()}};b.pause&&e.hover(function(){clearInterval(k)},function(){i()});b.pager&&(l.bind("click",function(a){a.preventDefault();
b.pauseControls||i();a=l.index(this);if(!(m===a||d("."+j+":animated").length)){n(a);t(a)}}).eq(0).closest("li").addClass(s),b.pauseControls&&l.hover(function(){clearInterval(k)},function(){i()}));if(b.nav){c="<a href='javascript:' class='"+y+" prev'>"+b.prevText+"</a><a href='javascript:' class='"+y+" next'>"+b.nextText+"</a>";h.controls?d(b.controls).append(c):e.after(c);var c=d("."+g+"_nav"),B=d("."+g+"_nav.prev");c.bind("click",function(a){a.preventDefault();if(!d("."+j+":animated").length){var c=f.index(d("."+j)),
a=c-1,c=c+1<w?m+1:0;t(d(this)[0]===B[0]?a:c);b.pager&&n(d(this)[0]===B[0]?a:c);b.pauseControls||i()}});b.pauseControls&&c.hover(function(){clearInterval(k)},function(){i()})}}if("undefined"===typeof document.body.style.maxWidth&&h.maxwidth){var C=function(){e.css("width","100%");e.width()>r&&e.css("width",r)};C();d(D).bind("resize",function(){C()})}})}})(jQuery,this,0);
$(function() {
    $(".f426x240").responsiveSlides({
        auto: true,
        pager: true,
        nav: true,
        speed: 700
    });
    $(".f160x160").responsiveSlides({
        auto: true,
        pager: true,
        speed: 700
    });
});


function change(dex){
		var id=document.getElementById("menu");
		var taga=id.getElementsByTagName("div");
		var len=taga.length;
		for(var i=0;i<len;i++){
			var divname='JKDiv_'+i.toString();
		if(i==(parseInt(dex))){
			taga[i].style.backgroundColor='#009944';
			taga[i].style.color='#fff';
			taga[i].style.fontWeight='900';
			taga[i].style.height='41px';
			taga[i].style.top='0'
			document.getElementById(divname).style.display="block";
	    }else{
			taga[i].style.backgroundColor='#fff';
			taga[i].style.color='#303030';
			taga[i].style.fontWeight='normal';
			taga[i].style.height='38px';
			taga[i].style.top='3px';
			document.getElementById(divname).style.display="none"; 
		}
	}
}



$(function(){
	$('.jbbox').click(function(e){
		$('#tippOff_').lightbox_me({
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
	$('#tipp_link2').click(function(e){
		$('#tippOff_').lightbox_me({
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
	$('#tipp_link').click(function(e){
		var chk_value =[];    
		$('input[name="report"]:checked').each(function(){    
			chk_value.push($(this).val());    
		});
		var company_id=$(this).attr("company_id")
		var forcompany_id=$(this).attr("forcompany_id")
		var product_id=$(this).attr("product_id")
		//alert(chk_value);
		
		if (chk_value.length>0){
		
			$.ajax({
			   type: "GET",
			   url: "/trade/pro_report.html",
			   data: 'company_id='+company_id+'&forcompany_id='+forcompany_id+'&product_id='+product_id+'&chk_value='+chk_value,
			   success:function(data){
					//alert(data);
			   },
			   error:function(data){
					//alert("错误!青重试.");
			   }
			}); 
			
			$('#jb3').html('举报正在处理');
			$('#jb4').html('举报正在处理');
			
			$('#tippOff').lightbox_me({
						overlaySpeed:0,
						lightboxSpeed:0,
						centered: true, 
						onLoad: function() { 
						}
				});
			e.preventDefault();
		}
		else{
		
			$('#tippOff2').lightbox_me({
				overlaySpeed:0,
				lightboxSpeed:0,
				centered: true, 
				onLoad: function() { 
				}
			});
		
		}
	})
});


$(function(){
	$('#block_info_item_chk').click(function(e){
		$('#chk').lightbox_me({
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
	$('#chk_link').click(function(e){
		$('#chk1').lightbox_me({
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
	$('#chk1_link').click(function(e){
		$('#bal').lightbox_me({
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
	$('#chk2_link').click(function(e){
		$('#bal').lightbox_me({
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
	$('#inline_chk').click(function(e){
		$('#inline_chk_Div').lightbox_me({
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
	$('#tippOff').trigger('close');
	$('#tippOff_').trigger('close');
	$('#tippOff2').trigger('close');
	$('#chk').trigger('close');
	$('#chk1').trigger('close');
	$('#bal').trigger('close');
	$('#inline_chk_Div').trigger('close');
}

$(function(){
		$('#inlineChk').click(function(e){
			$('#inline_chk').css('display','none');
			$('.block_info_item_phone').css('display','inline');
			$('.info_item_phone').css('display','block');
			$('.info_item_phone_').css('display','block');
			$('.block_info_tel').css('display','block');
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
