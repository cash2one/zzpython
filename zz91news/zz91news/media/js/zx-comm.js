$(function(){
	var input = document.createElement('input');
    if("placeholder" in input){
        //支持
    }
    else{
        searchVal();
        function searchVal(){
            $(".j_searchipt").each(function(i,item){
                var sipt_val = $(item).attr("placeholder");
                $(item).val(sipt_val).css("color","#bfbfbf");
            })
            $(".j_searchipt").bind(
                {
                    focus:function(){
                        $(this).css("color","#000")
                        sipt_val = $(this).attr("placeholder");
                        var sipt_Nval = $(this).val();
                        if(sipt_Nval==sipt_val){
                            $(this).val("")
                        }
                    },
                    blur:function(){
                        sipt_val = $(this).attr("placeholder");
                        var sipt_Nval = $(this).val();
                        if(sipt_Nval.length==0){
                            $(this).val(sipt_val).css("color","#bfbfbf")
                        }
                    }
                }
            )
        }
    }
	
	var fixed=$(".zx-rmdy"); //得到导航对象
	
	var win=$(window) //得到窗口对象
	
	var rmHeight=$(".zx-rmdy").height(); 
	
	var fixedHmin=$(".zx-rmdy").offset().top;//距离文档顶部距离
	
	var fixedHmax=$(".footbox").offset().top-(rmHeight+100);
	
	var sc=$(document);//得到document文档对象。
	
	win.scroll(function(){
	  if(sc.scrollTop()>=fixedHmin&&sc.scrollTop()<=fixedHmax){
	    fixed.addClass("zx-rmdy-fixed"); 
	   
	  }else{
	   fixed.removeClass("zx-rmdy-fixed");
	  
	  }
	})  
	
	
})