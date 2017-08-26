/*coolapp@163.com,2012-12-7*/
(function($){
  $.fn.floatfly=function(options){
    var opts=$.extend({},$.fn.floatfly.defaults,options);
    return this.each(function(){
      var $ff=$("<div></div>").append(this);
      $('body').append($ff);

      var $ctrl=$('<div><a>¡Á</a><div>').css({'cursor':'pointer','display':'block','font-size':'12px','width':'14px','height':'14px','line-height':'14px'});
      if(opts.ctrlPos=='top')$ff.prepend($ctrl);
      else $ff.append($ctrl);

      if(opts.imgBorder=='none'||opts.imgBorder=='0')$ff.find('*').css('border','none');

      var D=document;var DE=D.documentElement;var A=3
      $ff.css('position','absolute');

      var ffw=$ff.width(),ffh=$ff.height();
      var rw=DE.clientWidth-ffw,rh=DE.clientHeight-ffh;
      var ffl=Math.round(rw*Math.random()+DE.scrollLeft);
      var fft=Math.round((rh)* Math.random()+DE.scrollTop);
      $ff.css({'left':ffl+'px','top':fft+'px'});
      var ffxa=(Math.random()*A+.3),ffya=(Math.random()*A+.3);
      if(Math.random()>.5)ffxa=-ffxa;if(Math.random()>.5)ffya=-ffya;
      setInterval(function(){
        ffxa*=(1.5-Math.random());if(Math.abs(ffxa)<.1)ffxa=ffxa>0?.5:-.5;else if(Math.abs(ffxa)>A)ffxa=ffxa>0?A:-A;
        ffya*=(1.5-Math.random());if(Math.abs(ffya)<.1)ffxa=ffya>0?.5:-.5;else if(Math.abs(ffya)>A)ffya=ffya>0?A:-A;
      },3000);
      var floatfly=function(){
        rw=DE.clientWidth-ffw+DE.scrollLeft,rh=DE.clientHeight-ffh+DE.scrollTop;
        ffl+=ffxa;if(ffl>rw){ffl=rw-ffxa;ffxa=-ffxa}else if(ffl<DE.scrollLeft){ffl=DE.scrollLeft-ffxa;ffxa=-ffxa;}
        fft+=ffya;if(fft>rh){fft=rh-ffya;ffya=-ffya}else if(fft<DE.scrollTop){fft=DE.scrollTop-ffya;ffya=-ffya;}
        $ff.css({'top':Math.round(fft)+'px','left':Math.round(ffl)+'px','display':'block','visibility':'visible'});
      }
      var hdl=setInterval(floatfly,100);


      $ctrl.click(function(){
        clearInterval(hdl);$ff.fadeOut(99,function(){$ff.reomve();});
        floatfly=null;
        return false;
  }).mouseover(function(){clearInterval(hdl);}).mouseout(function(){clearInterval(hdl);hdl=setInterval(floatfly,100);});
      $ff.mouseover(function(){clearInterval(hdl);}).mouseout(function(){clearInterval(hdl);hdl=setInterval(floatfly,100);});
    });
  };
  $.fn.floatfly.defaults={
    ctrlPos:'top',
    imgBorder:'none'
  };

  $.fn.floatfly.setDefaults=function(settings){
    $.extend( $.fn.floatfly.defaults,settings);
  };
})(jQuery);