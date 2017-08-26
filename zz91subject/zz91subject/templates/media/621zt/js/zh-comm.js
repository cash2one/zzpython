$(function(){
    var list = ["江苏超喜加塑料科技有限公司 A17展位","北京市京元物环认证咨询有限公司（杭州分公司） A19展位","扬州市海达塑料科技有限公司 A18展位","揭阳市美之达五金塑胶实业有限公司 A16展位","辽阳胜达再生资源利用有限公司 A15展位","余姚市低塘东达塑料厂 报名观展","常州勤益塑料有限公司 报名观展","郑州星辉塑业有限公司 报名观展","昆山合志塑料科技有限公司 报名观展","个体经营(王辉) 报名观展","台州市融科塑胶有限公司 报名观展","山东中胤环保科技有限公司 报名观展","平湖市驰新塑胶有限公司 报名观展","浙江凯王塑业有限公司 报名观展","嘉兴市赛腾新材料科技有限公司 报名观展"]
    var moveul = $(".fh-info-ul");
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
    

    $(".fh-info-box").on({
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


   
    $(".c-content-left ul li").on("click",function(){
        $(this).addClass("c-active").siblings().removeClass('c-active');
        $(".c-content-right-con").eq($(this).index()).addClass("c-on").siblings().removeClass('c-on');
    });

    $(".c-pingmiantu p,.c-pingmiantu img").click(function(){
        $(".c-pingmiantu-bigimg").toggle();
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
    $(".c-content-left ul li").eq(pageIndex).click();


    var d=new Date(),str='';
    str +=d.getFullYear()+"-"; //获取当前年份
    str +=(d.getMonth()+1<10?("0"+(d.getMonth()+1)):d.getMonth()+1)+"-"; //获取当前月份（0——11）
    str +=d.getDate()<10?"0"+d.getDate():d.getDate(); 

    var dayObj = DateDiff(str, "2017-06-21");
    var lastDay = dayObj.Days;
    $(".lastday").text(lastDay)
    function DateDiff(sDate1, sDate2){ //sDate1和sDate2是字符串 yyyy-MM-dd格式 
        var aDate, oDate1, oDate2, iDays, ihours, iminutes, iseconds;
        aDate = sDate1.split("-");
        var OsObject = "";  
        
       
            oDate1 = new Date(aDate[1] + '/' + aDate[2] + '/' + aDate[0]);//转换为MM-dd-yyyy格式 
            aDate = sDate2.split("-");
            oDate2 = new Date(aDate[1] + '/' + aDate[2] + '/' + aDate[0]);
       
        
        var timeSpan = {};

        var TotalMilliseconds = Math.abs(oDate1 - oDate2);//相差的毫秒数
        timeSpan.Days = parseInt(TotalMilliseconds / 1000 / 60 / 60 /24);
        timeSpan.TotalHours = parseInt(TotalMilliseconds / 1000 / 60 / 60);
        timeSpan.Hours = timeSpan.TotalHours % 24;
        timeSpan.TotalMinutes = parseInt(TotalMilliseconds / 1000 / 60);
        timeSpan.Minutes = timeSpan.TotalMinutes % 60;
        timeSpan.TotalSeconds = parseInt(TotalMilliseconds / 1000);
        timeSpan.Seconds = timeSpan.TotalSeconds % 60;
        timeSpan.TotalMilliseconds = TotalMilliseconds;
        timeSpan.Milliseconds = TotalMilliseconds % 1000;
        return timeSpan;
    }
    $(".lastday").hide()
})