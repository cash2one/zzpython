(function($){
$.fn.extend({
        Scroll:function(opt,callback){
                //参数初始化
                if(!opt) var opt={};
                var _this=this.eq(0).find("ul:first");
                var lineH=_this.find("li:first").height(), //获取行高
                        line=opt.line?parseInt(opt.line,10):parseInt(this.height()/lineH,10),
                        speed=opt.speed?parseInt(opt.speed,10):5000, //卷动速度，数值越大，速度越慢（毫秒）
                        timer=opt.timer?parseInt(opt.timer,10):3000; //滚动的时间间隔（毫秒）
                if(line==0) line=1;
                var upHeight=0-line*lineH;
                //滚动函数
                scrollUp=function(){
                        _this.animate({
                                marginTop:upHeight
                        },speed,function(){
                                for(i=1;i<=line;i++){
                                        _this.find("li:first").appendTo(_this);
                                }
                                _this.css({marginTop:0});
                        });
                }
                //鼠标事件绑定
                _this.hover(function(){
                        clearInterval(timerID);
                },function(){
                        timerID=setInterval("scrollUp()",timer);
                }).mouseout();
        }       
})
})(jQuery);

function Marquee(){
  this.ID=document.getElementById(arguments[0]);
  this.Direction=arguments[1];
  this.Step=arguments[2];
  this.Width=arguments[3];
  this.Height=arguments[4];
  this.Timer=arguments[5];
  this.WaitTime=arguments[6];
  this.StopTime=arguments[7];
  if(arguments[8]){this.ScrollStep=arguments[8];}else{this.ScrollStep=this.Direction>1?this.Width:this.Height;}
  this.CTL=this.StartID=this.Stop=this.MouseOver=0;
  this.ID.style.overflowX=this.ID.style.overflowY="hidden";
  this.ID.noWrap=true;
  this.ID.style.width=this.Width;
  this.ID.style.height=this.Height;
  this.ClientScroll=this.Direction>1?this.ID.scrollWidth:this.ID.scrollHeight;
  this.ID.innerHTML+=this.ID.innerHTML;
  this.Start(this,this.Timer,this.WaitTime,this.StopTime);
  }
Marquee.prototype.Start=function(msobj,timer,waittime,stoptime){
  msobj.StartID=function(){msobj.Scroll();}
  msobj.Continue=function(){
    if(msobj.MouseOver==1){setTimeout(msobj.Continue,waittime);}
    else{clearInterval(msobj.TimerID); msobj.CTL=msobj.Stop=0; msobj.TimerID=setInterval(msobj.StartID,timer);}
    }
  msobj.Pause=function(){msobj.Stop=1; clearInterval(msobj.TimerID); setTimeout(msobj.Continue,waittime);}
  msobj.Begin=function(){
    msobj.TimerID=setInterval(msobj.StartID,timer);
    msobj.ID.onmouseover=function(){msobj.MouseOver=1; clearInterval(msobj.TimerID);}
    msobj.ID.onmouseout=function(){msobj.MouseOver=0; if(msobj.Stop==0){clearInterval(msobj.TimerID); msobj.TimerID=setInterval(msobj.StartID,timer);}}
    }
  setTimeout(msobj.Begin,stoptime);
  }
Marquee.prototype.Scroll=function(){
  switch(this.Direction){
    case 0:
      this.CTL+=this.Step;
      if(this.CTL>=this.ScrollStep&&this.WaitTime>0){this.ID.scrollTop+=this.ScrollStep+this.Step-this.CTL; this.Pause(); return;}
      else{if(this.ID.scrollTop>=this.ClientScroll) this.ID.scrollTop-=this.ClientScroll; this.ID.scrollTop+=this.Step;}
      break;
    case 1:
      this.CTL+=this.Step;
      if(this.CTL>=this.ScrollStep&&this.WaitTime>0){this.ID.scrollTop-=this.ScrollStep+this.Step-this.CTL; this.Pause(); return;}
      else{if(this.ID.scrollTop<=0) this.ID.scrollTop+=this.ClientScroll; this.ID.scrollTop-=this.Step;}
      break;
    case 2:
      this.CTL+=this.Step;
      if(this.CTL>=this.ScrollStep&&this.WaitTime>0){this.ID.scrollLeft+=this.ScrollStep+this.Step-this.CTL; this.Pause(); return;}
      else{if(this.ID.scrollLeft>=this.ClientScroll) this.ID.scrollLeft-=this.ClientScroll; this.ID.scrollLeft+=this.Step;}
      break;
    case 3:
      this.CTL+=this.Step;
      if(this.CTL>=this.ScrollStep&&this.WaitTime>0){this.ID.scrollLeft-=this.ScrollStep+this.Step-this.CTL; this.Pause(); return;}
      else{if(this.ID.scrollLeft<=0) this.ID.scrollLeft+=this.ClientScroll; this.ID.scrollLeft-=this.Step;}
      break;
    }
  }

$(document).ready(function(){
	new Marquee(
    "toppic",  //容器ID<br />
    0,  //向上滚动(0向上 1向下 2向左 3向右)<br />
    1,  //滚动的步长<br />
    914,  //容器可视宽度<br />
    112,  //容器可视高度<br />
    30,  //定时器 数值越小，滚动的速度越快(1000=1秒,建议不小于20)<br />
    5000,  //间歇停顿时间(0为不停顿,1000=1秒)<br />
    1000,  //开始时的等待时间(0为不等待,1000=1秒)<br />
    110 //间歇滚动间距(可选)<br />
    );
	
	new Marquee(
    "topinfo",  //容器ID<br />
    2,  //向上滚动(0向上 1向下 2向左 3向右)<br />
    1,  //滚动的步长<br />
    160,  //容器可视宽度<br />
    21,  //容器可视高度<br />
    40,  //定时器 数值越小，滚动的速度越快(1000=1秒,建议不小于20)<br />
    0,  //间歇停顿时间(0为不停顿,1000=1秒)<br />
    0,  //开始时的等待时间(0为不等待,1000=1秒)<br />
    10 //间歇滚动间距(可选)<br />
    );
});