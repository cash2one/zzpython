function getNav(opts,fction){
			this.moveBox = opts.obj; //滑动菜单
			this.fction  = fction;
			//构造三步奏
			this.init();
			this.renderDOM();
			this.bindDOM();
		}
		getNav.prototype.init = function(){
			this.width_w = this.moveBox.width();	   				//页面科室宽度
			this.moveMain = this.moveBox.find(".j_movemian")		//滑动主
			this.moveLi  = this.moveMain.find("li"); 				//滑动菜单选项
			this.LiWidth =  this.moveLi.outerWidth(); 		
			this.LiNum   = this.moveLi.length;		   				//滑动菜单选项个数
		}
		getNav.prototype.renderDOM = function(){
			var moveMain = this.moveMain;
			var moveLi  = this.moveLi;
			var LiNum   = this.LiNum;
			var LiWidth   = this.LiWidth;
			var width_w = this.width_w;
			var moveBd  = this.moveBd;

			this.mBoxWidth   = LiNum*LiWidth;
			moveMain.width(this.mBoxWidth);
		}
		getNav.prototype.bindDOM = function(){
			var self     = this;
			var moveBox  = self.moveBox;
			var moveMain = self.moveMain;
			var moveLi  = self.moveLi;
			var LiNum    = self.LiNum;
			var mLiWidth = self.mLiWidth;

			var moveBd  = self.moveBd;

			var endRight = -(this.mBoxWidth-this.width_w); //最右侧划动位置

			//手指按下的处理事件
			var startHandler = function(evt){
				self.mgLeftStart = parseInt(moveMain.css("marginLeft"));
				//记录手指按下的坐标
				self.startX = evt.touches[0].pageX;
			};

			//手指移动的处理事件
			var moveHandler = function(evt){
				//兼容chrome android，阻止浏览器默认行为
				evt.preventDefault();

				//计算手指的偏移量
				self.offsetX = evt.targetTouches[0].pageX - self.startX;

				self.mgLeftEnd = self.mgLeftStart + self.offsetX;  //手机滑动的距离

				if(self.mgLeftEnd>0){				//判断是否拉到最左端
					self.mgLeftEnd = self.mgLeftEnd/3
				}
				else if( self.mgLeftEnd < endRight){
					self.mgLeftEnd = endRight - (endRight - self.mgLeftEnd)/3   //判断是否拉到最左端
				}
				moveMain.animate({"marginLeft":self.mgLeftEnd +"px"},0)
			};

			//手指抬起的处理事件
			var endHandler = function(evt){
				// evt.preventDefault();
				self.mgLeft = parseInt(moveMain.css("marginLeft"));
				if(self.mgLeft>0){								//判断是否拉到最左端
					moveMain.animate({"marginLeft":0},500)
				}else if(self.mgLeft<endRight){					//判断是否拉到最右端
					moveMain.animate({"marginLeft":endRight},500)
				}
			};

			self.thisNav = moveMain.find(".thisNav")
			//手指抬起的处理事件
			

			//绑定事件
			moveBox.get(0).addEventListener('touchstart', startHandler);
			moveBox.get(0).addEventListener('touchmove', moveHandler);
			moveBox.get(0).addEventListener('touchend', endHandler);
			
		}

//查看案例
$(".zz-bg-white").on("click",".zz-jieshao-anli",function(){
	var anlibox  =  $(this);
	var iconUp    = anlibox.find(".zz-anli-more .aui-iconfont");
	var imgbox    = anlibox.find(".zz-anli-imgbox");
	var anlibox_h = anlibox.offset().top;

	if(!iconUp.hasClass("aui-icon-fold")){
		iconUp.addClass("aui-icon-fold");
		imgbox.show();
		$("body").animate({"scrollTop":anlibox_h-50+"px"},500)
		anlibox.find(".zz-brev-iconbox").hide();
		anlibox.find(".aui-ellipsis-1").removeClass("aui-ellipsis-1").attr("aui-ellipsis","aui-ellipsis-1");
		anlibox.find(".aui-ellipsis-2").removeClass("aui-ellipsis-2").attr("aui-ellipsis","aui-ellipsis-2");
	}
})
$(".zz-bg-white").on("click",".zz-anli-more",function(event){
	event.stopPropagation();
	var iconUp    = $(this).find(".aui-iconfont");
	var anlibox   = $(this).parents(".zz-jieshao-anli");
	var imgbox    = $(this).parents(".zz-jieshao-anli").find(".zz-anli-imgbox");
	var anlibox_h = anlibox.offset().top;
	if(iconUp.hasClass("aui-icon-fold")){
		iconUp.removeClass("aui-icon-fold");
		imgbox.slideUp();
		anlibox.find(".zz-brev-iconbox").show();
		anlibox.find("[aui-ellipsis]").addClass(anlibox.find("[aui-ellipsis]").attr("aui-ellipsis"))

	}else{
		iconUp.addClass("aui-icon-fold");
		imgbox.show();
		$("body").animate({"scrollTop":anlibox_h-50+"px"},500)
		anlibox.find(".zz-brev-iconbox").hide();
		anlibox.find(".aui-ellipsis-1").removeClass("aui-ellipsis-1").attr("aui-ellipsis","aui-ellipsis-1");
		anlibox.find(".aui-ellipsis-2").removeClass("aui-ellipsis-2").attr("aui-ellipsis","aui-ellipsis-2");
	}
})