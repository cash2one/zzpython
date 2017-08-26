$(function(){
	var w_height = $(window).height(); 
	$(window).on("scroll",function(){
		var w_scrollHeight = $(document).scrollTop();
		if(w_scrollHeight>w_height){
			$(".j_gotop").css("display","block")
		}else{
			$(".j_gotop").hide()
		}
	})
	$(".j_gotop").on("click",function(){
		 $("html,body").animate({scrollTop:0},500)
	})
	var zzajax = function(method, url, data, successCallback, errorCallback) {
		$.ajax({
			type: method,
			url: url,
			data: data,
			dataType: "json",   //返回格式为json
			traditional: true,
			cache:false, 
			success: function(ret) {
				successCallback && successCallback(ret);
			},
			error: function(err) {
				errorCallback && errorCallback(err);
			}
		});
	}
})