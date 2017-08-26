// JavaScript Document
	  (function slide(config){
		config = config || {};
		var conter = config.conter || "#slide",//容器
			conterBtn = ".toggleBtn" || {}
			,
			spd = 500,//切换速度
			intval = 5000,//切换间隔
			toggleImg = ".toggleImg img"|| {},//图片列
			toggleBtn = ".toggleBtn a" || {};//按钮列
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
			if(leg > 1) $(contBtn).append("<a class='selected' href='javascript:void(0)'>1</a>");
			for(var i = 2; i <= leg; i++){      
					$(contBtn).append("<a href='javascript:void(0)'>"+i+"</a>");
			}
		}	
	})();