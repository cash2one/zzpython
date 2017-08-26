$(function(){
    var list = ["江苏超喜加塑料科技有限公司 A17展位","北京市京元物环认证咨询有限公司（杭州分公司） A19展位","扬州市海达塑料科技有限公司 A18展位","揭阳市美之达五金塑胶实业有限公司 A16展位","辽阳胜达再生资源利用有限公司 A15展位","余姚市低塘东达塑料厂 报名观展","常州勤益塑料有限公司 报名观展","郑州星辉塑业有限公司 报名观展","昆山合志塑料科技有限公司 报名观展","个体经营(王辉) 报名观展","台州市融科塑胶有限公司 报名观展","山东中胤环保科技有限公司 报名观展","平湖市驰新塑胶有限公司 报名观展","浙江凯王塑业有限公司 报名观展","嘉兴市赛腾新材料科技有限公司 报名观展"]
    var moveul = $(".band-info-ul");
    var moveliHtml="";
    $.each(list,function(i,item){
        moveliHtml +='<li class="fl">'+ item +'</li>';
    })
    moveul.html(moveliHtml);
    var moveli = moveul.find("li");
    var ulWidth = 0;
    $.each(moveli,function(i,item){
        ulWidth += $(item).outerWidth();
    })
    moveul.width(ulWidth*2);
    var moveHtml = moveul.html();
    moveul.append(moveHtml);
    
    var startNum = 0;
    var starttime;
    startMove();
    function startMove(){
        starttime = setInterval(function(){
            if(startNum == ulWidth){
                startNum = 0;
            }
            startNum += 1;
            moveul.css("marginLeft",-startNum+"px");
        },30)
    }
    

    $(".band-infomain").on({
        mouseenter:function(){
            clearInterval(starttime)
        },
        mouseleave:function(){
            startMove()
        }
    })
    
    $(".fh-nav-ul").on("mouseleave",function(){
        $(".fh-nav-xian").animate({"width":"0","left":"0"})
    })


    $(".fh-nav-ul li").on({
        mouseenter:function(){
            $(this).find(".fh-nav-smallbox").show();
            var index = $(this).index();
            $(".fh-nav-xian").stop().animate({"width":"120px","left":index*120+"px"})
        },
        mouseleave:function(){
            $(this).find(".fh-nav-smallbox").hide()
        }
    })
    
    $(".conmain-list li").on("click",function(){
        $(this).addClass("conmain-list-this").siblings().removeClass('conmain-list-this');
        $(".conmain-rbox").eq($(this).index()).addClass("conmain-block").siblings().removeClass('conmain-block');
    });


	function GetQueryString(name) { 
      var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
      var r = window.location.search.substr(1).match(reg); //获取url中"?"符后的字符串并正则匹配
      var context = ""; 
      if (r != null) 
         context = r[2]; 
      reg = null; 
      r = null; 
      return context == null || context == "" || context == "undefined" ? "" : context; 
    }
    var pageIndex = GetQueryString("page");
    $(".conmain-list li").eq(pageIndex).click();
})