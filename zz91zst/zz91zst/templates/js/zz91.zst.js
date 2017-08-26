// JavaScript Document

$(document).ready(function(event) {
	var telbtn	=$("#tel_btn"),
		netbtn	=$("#net_btn"),
	 	telcont	=$("#telcont"),
	 	netcont	=$("#netcont"),
		viewservterms = $("#viewservterms"),
		zz91terms = $("#zz91terms"),
		zz91termsbg=$(".zz91termsbg"),
		printArea = $("#printArea"),
		closetermsDetail = $("#closetermsDetail"),
		online_apply = $("#online_apply"),
		valueadd_servive = $("#valueadd_servive");
		
    telbtn.click(function(){
			if($(this).attr("class")=="apply_tabsbox_nav_btnt"){
				$(this).attr({"class":"apply_tabsbox_nav_btntis"});
				netbtn.attr({"class":"apply_tabsbox_nav_btnn"});
				telcont.fadeIn(300);
				netcont.hide();
			}
		});
		
	 netbtn.click(function(){
			if($(this).attr("class")=="apply_tabsbox_nav_btnn"){
				telbtn.attr({"class":"apply_tabsbox_nav_btnt"});
				$(this).attr({"class":"apply_tabsbox_nav_btnnis"});
				telcont.hide();
				netcont.fadeIn(300);
			}
		});
	
	viewservterms.click(function(){
			zz91terms.fadeIn(500);
			zz91termsbg.css({"height":$("body").height()+"px"})
			printArea.css({"left":($("body").width()/2-420)+"px","top":"120px"});
		});
	
	closetermsDetail.click(function(){zz91terms.fadeOut(200)});
	
	zz91termsbg.click(function(){zz91terms.fadeOut(200)});
	
	$(".surepaybtn").mouseover(function(){
			$(this).css({"background-position":"left -35px"})
		}).mouseout(function(){
			$(this).css({"background-position":"left top"})
			})
			
	
	$(".queding_btn").mouseover(function(){
			$(this).css({"background-position":"left -26px"})
		}).mouseout(function(){
			$(this).css({"background-position":"left top"})
			})
			
	$(".shenqing_btn").mouseover(function(){
			$(this).css({"background-position":"left -26px"})
		}).mouseout(function(){
			$(this).css({"background-position":"left top"})
			})		
			
	var payment_net = $("#payment_net"),
        payment_zfb = $("#payment_zfb"),
		payment_gw  = $("#payment_gw");
		
		payment_net.click(function(){
		
			payment_net.attr({"class":"payment_netis"});
        	payment_zfb.attr({"class":"payment_zfb"});
			payment_gw.attr({"class":"payment_gw"});
			
			$(".paytabs_cont_method1").slideDown(500);
			$(".paytabs_cont_method2").slideUp(500);
			$(".paytabs_cont_method3").slideUp(500);
		})
		
		
		payment_zfb.click(function(){
			payment_net.attr({"class":"payment_net"});
        	payment_zfb.attr({"class":"payment_zfbis"});
			payment_gw.attr({"class":"payment_gw"});
			
			$(".paytabs_cont_method1").slideUp(500);
			$(".paytabs_cont_method2").slideDown(500);
			$(".paytabs_cont_method3").slideUp(500);
		})
		
		
		payment_gw.click(function(){
			payment_net.attr({"class":"payment_net"});
        	payment_zfb.attr({"class":"payment_zfb"});
			payment_gw.attr({"class":"payment_gwis"});
			
			$(".paytabs_cont_method1").slideUp(500);
			$(".paytabs_cont_method2").slideUp(500);
			$(".paytabs_cont_method3").slideDown(500);
		})
		
		
		

		new zz91slide(
					config={
						conter:"#zz91slide",
						spd:500,
						toggleImg:'.toggleImg img',
						intval:3000
					}
				);
				
				
		online_apply.click(function(){
			
				online_apply.attr({"class":"apply_servleader_is"});
				valueadd_servive.attr({"class":"apply_servleader_no"});
				$(".apply_tabsbox").slideDown(500);
				$(".apply_leaderbox").slideUp(500);
			})
		
		valueadd_servive.click(function(){
			
				online_apply.attr({"class":"apply_servleader_no"});
				valueadd_servive.attr({"class":"apply_servleader_is"});
				$(".apply_tabsbox").slideUp(500);
				$(".apply_leaderbox").slideDown(500);
			})
        
});


/**
     ctner 容器
     spd 切换速度
     intval 切换间隔
     toggleImg 图片列
     toggleBtn 按钮列
**/
var zz91slide = function(config){
    zz91slide = this;
    config = config || {};
    var conter = config.conter || "#zz91slide",
        conterBtn = config.conterBtn ||".toggleBtn",
        spd = config.spd || 300,
        intval = config.intval || 1000,
        toggleImg = config.toggleImg||".toggleImg img",
        toggleBtn = config.toggleBtn||".toggleBtn a";
        nowP = config.nowP || 0;
    
    //initilzation  turnBtn
    creatBtn($(toggleImg).length,conterBtn);
    
    var pic=$(toggleImg),
        turnBt=$(toggleBtn);
    
    pic.eq(0).css({"display":"block"});
    
    var os = function(){
        nowP=nowP>(pic.length-2)?0:nowP=nowP+1;
        if($(toggleImg).length>1){
            toggleBtnF(nowP);
            toggleImgF(nowP);
        }
    };
    
    var t=setInterval(os,intval);
    
    //检测鼠标位置
    $(conter).bind({
        mouseover:function(){clearInterval(t);},
        mouseout:function(){t=setInterval(os,intval);}
    }); 
    
    //切换
    turnBt.click(function(event){
            event.preventDefault();
            nowP=$(this).index();       
            toggleBtnF(nowP);
            toggleImgF(nowP);
    })
    
    //toggle images
    function toggleImgF(i){pic.fadeOut(spd).eq(i).fadeIn(spd);}
    
    //toggle button
    function toggleBtnF(i){turnBt.removeClass("selected").eq(i).addClass("selected");}
    
    //add turn btn
    function creatBtn(leg,contBtn){
        leg = leg || 0;
        var b = document.createElement('a');
        if(leg > 1) $(contBtn).append("<a class='selected' href='javascript:void(0)'></a>");
        for(var i = 2; i <= leg; i++){      
                $(contBtn).append("<a href='javascript:void(0)'></a>");
        }
    }
}