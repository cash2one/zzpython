var popShow = function(obj){
    this.window_h = $(window).height();
    this.window_w = $(window).width();
    this.obj_h    = obj.height();
    this.obj_w    = obj.width();
    this.Top      = (window_h - obj_h)/2;
    this.Left     = (window_w-obj_w)/2;
    if($(".wdpop").length>0){
        $(".wdpop").show();
    }else{
        this.wdpopHtml = "<div class='wdpop' style='background:#000;height:100%;width:"+ this.window_w +"px;position:fixed;z-index:1000;opacity: 0.80;filter:Alpha(opacity=80);left:0;top:0;'><div>"
        $("body").append(this.wdpopHtml);
    }
    obj.css({"top":-this.obj_h+"px","left":this.Left+"px","zIndex":"1001","position":"fixed"}).show();
    obj.animate({"top":this.Top+"px"},300,"swing")
}

var closePop = function(obj){
    obj.hide();
    $(".wdpop").hide();
}


scrollBottomTest =function(fn){
     $(window).scroll(function(){
         var $this =$(this),
         viewH =$(this).height(),//可见高度
         contentH =$(document).height(),//内容高度
         scrollTop =$(this).scrollTop();//滚动高度
        if(contentH - viewH - scrollTop <= 100) { //到达底部100px时,加载新内容
        // if(scrollTop/(contentH -viewH)>=0.95){ //到达底部100px时,加载新内容
        // 这里加载数据..
            fn&&fn();
        }
     });
}
