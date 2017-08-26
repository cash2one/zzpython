// JavaScript Document
 function clickselect(liofselect,content) {
		$(liofselect).mousedown(
             function () {
				$(liofselect).css({
                      "background-color":"#FFF",
                      "font-size":"16px",
                      "padding":"0px",
					  "list-style-image":"url(images/help/help_05.jpg)"
				});
				$(this).css({
                      "background-color":"#ccc",
                      "font-size":"16px",
                      "padding":"2px",
					  "list-style-image":"url(images/help/help_06.jpg)"
				});
				$(content).fadeOut(1000);
				var inout=$(this).attr("class");
				for(var i=0;i<$(liofselect).size()+1;i++){
					if(inout=="tab"+i){
						$(".content"+i).fadeIn(1000);
					}
				}
             }
        )
 }
 
 function opacityer(opacity,over_opacity,out_opacity,time) {
    $(opacity).css("opacity",out_opacity)
        .hover(
             function () {
             	$(this).animate({opacity:over_opacity},time); 
             },
             function () {
             	$(this).animate({opacity:out_opacity},time); 
             }
        )
 }
 function opacity(opacity,over_opacity,out_opacity,outer,time,other) {
 	if (other!=undefined) {
 		$(other).css("opacity",out_opacity);
 	} 
    $(opacity).css("opacity",outer)
        .hover(
               function () {
				 if($(other).css("opacity")==over_opacity){
				 }else{
             	     if ($(this).next('img')!=undefined){
             		    $(this).next('img').animate({opacity:over_opacity},time);
             	     }else{
             		    $(this).animate({opacity:over_opacity},time);
              	     } 
		         }
             },
             function () {
             	if ($(this).next("img")!=undefined){
             		  $(this).next("img").animate({opacity:out_opacity},time);
             	}else{
             		$(this).animate({opacity:out_opacity},time);
             	}  
             }
        )
 }
 
 function tip(sel,obj,x,y){
		var x = x;
		var	y = y;
		$(sel).mouseover(function(event){
			this.newTitle = this.title
			this.title = ''	
			$('body').append('<div class='+obj+'><div class="tolltipcur">'+this.newTitle+'</div></div>')
			$('.'+obj).css({
				left  : event.pageX+x,
				top   : event.pageY+y	
			}).show()
		}).mousemove(function(event){
			$('.'+obj).css({
				left  : event.pageX+x,
				top   : event.pageY+y	
			})
		}).mouseout(function(){
			$('.'+obj).remove(),
			this.title = this.newTitle	
		})	
	}
	/*
**input输入框的value值
**/
function labal(input,label,value){
	_value = $(input).val();
	if(_value !== ''){
		$(label).html('');	
	}
	$(input).focus(function(){
	$(label).text('')
	}).blur(function(){
		$(label).text(value)
		phone = $(input).val().length;
		if (phone > 0){
			$(label).text('')
		}
	})
	$(label).click(function(){
		$(this).text('');
		$(input).focus();
	});
}
/*textareat*/
function labal_text(input,label,value){
	_value = $(input).html();
	
	if(_value !== ''){
		$(label).html(value);	
	}
	$(input).focus(function(){
		$(label).text('')
	}).blur(function(){
		
		$(label).html(value);
		
		phone = $(input).val().length;
		
		if (phone > 0){
			$(label).html('');
		}
	})
	$(label).click(function(){
		$(this).text('');
		$(input).focus();
	})
	
}
 $(document).ready(function() {
    clickselect(".ulhelp li",".contentbody div");
    opacityer(".hiden",1,0.6,12);
	opacityer(".icon1",0.6,0,1,12);
	opacityer(".icon2",0.6,0,12,1);
	opacityer(".ico",0.6,0,12,1);
	opacityer(".icon",0.6,0,12,1);
	opacityer(".iconer",0.6,0,12,1);
    opacityer(".iconers",0.6,0,12,1);
    opacityer(".icons",0.6,0,12,1);
	opacityer(".iconerons",0.6,0,12,1);

	opacity(".showout",0.6,0,1,12,".icon1");
	opacity(".showout",0.6,0,1,12,".icon2");
	opacity(".showout",0.6,0,1,12,".ico");
	opacity(".showout",0.6,0,1,12,".icon");
	opacity(".showout",0.6,0,1,12,".iconer");
    opacity(".showout",0.6,0,1,12,".iconers");
    opacity(".showout",0.6,0,1,12,".icons");
    opacity(".showout",0.6,0,1,12,".iconeron");
	tip('.telephone','tolltip',-100,17)//调用函数 1当前选择器,2选择器 X, Y
	tip('.weixin','tolltip2',-100,17)//调用函数 1当前选择器,2选择器 X, Y
	tip('.qq','tolltip',-100,17)//调用函数 1当前选择器,2选择器 X,
	labal('.textarea','.ppostion','如果你有其他需求，请一并告诉我，方便给你安排:)');
	$("#goup").click()=function(){
		$('body,html').animate({scrollTop:1600},12);
	}

});
window.onload = function(){
  var oTop = document.getElementById("goup");
  var screenw = document.documentElement.clientWidth || document.body.clientWidth;
  var screenh = document.documentElement.clientHeight || document.body.clientHeight;
  oTop.style.left = screenw - oTop.offsetWidth +"px";
  oTop.style.top = screenh - oTop.offsetHeight + "px";
  window.onscroll = function(){
    var scrolltop = document.documentElement.scrollTop || document.body.scrollTop;
    oTop.style.top = screenh - oTop.offsetHeight + scrolltop +"px";
  }
  oTop.onclick = function(){
    document.documentElement.scrollTop = document.body.scrollTop =1100;
  }
}  
// var OUT_OPACITY = 0.6;
// var OVER_OPACITY = 1.0;

/*$(function(){
	$(".atlast img").css("opacity",0.6)
        .hover(
             function () {
                  $(this).animate({opacity:1.0},10);
             },
             function () {
                 $(this).animate({opacity:0.6},10);
             }
        )
});


$(function(){
	$(".ico").css("opacity",0);
	$(".showout").hover(
             function () {
                  $(this).next(0).animate({opacity:0.6},10);
             },
             function () {
                 $(this).next(0).animate({opacity:0},10);
             }
        )
});

$(function(){
	$(".icon").css("opacity",0);
	$(".showout").hover(
             function () {
                  $(this).next(0).animate({opacity:0.6} ,1);
             },
             function () {
                 $(this).next(0).animate({opacity:0} ,1);
             }
        )
});
  
 $(function(){
	$(".icon1").css("opacity",0);
	$(".showout").hover(
             function () {
                  $(this).next(0).animate({opacity:0.6},1);
             },
             function () {
                 $(this).next(0).animate({opacity:0},1);
             }
        )
});

$(function(){
	$(".iconer").css("opacity",0);
	$(".showout").hover(
             function () {
                  $(this).next(0).animate({opacity:0.6},1);
             },
             function () {
                 $(this).next(0).animate({opacity:0},1);
             }
        )
});

$(function(){
	$(".icon2").css("opacity",0);
	$(".showout").hover(
             function () {
                  $(this).next(0).animate({opacity:0.6},1);
             },
             function () {
                 $(this).next(0).animate({opacity:0},1);
             }
        )
});
$(function(){
	$(".iconers").css("opacity",0);
	$(".showout").hover(
             function () {
                  $(this).next(0).animate({opacity:0.6},10);
             },
             function () {
                 $(this).next(0).animate({opacity:0},10);
             }
        )
});*/

/*$(function(){
	 var i =50;
	 $(".chinesenav li a").hover(
          function () { 
			  var timer = setInterval(function(){
	             $(this).css("width", i + "%").css({"background": "black"});
	                i++;
	             if (i >100) {clearInterval(timer);}
              }, 100);
		 },
         function () {
           $(".chinesenav li").css({"background": "white"},{"width":"100%"});
         }
     )
});
 */
  
/*$(function(){
	 var i = 0;
	 $(".chinesenav li").hover(
          function (event) { 
			 if(event.target==this){
			 $(this).parent().css({"width":"0px"});
			  var timer = setInterval(function(){
	             $(this).css("width", i + "%").css({"background": "black"});
	                i++;
	             if (i >100) {clearInterval(timer);}
              }, 100);
			  event.stopPropagation();
			 }
		 },
         function () {
           $(".chinesenav li").css({"background": "white"},{"width":"100%"});
         }
     )
});
*/