// 注册页面


$(document).ready(function() {
	/*提示信息导航按钮特效*/
	$("#content-nav li").mouseover(function(){
		$(this).css("background","url(images/button_hover.jpg) no-repeat");
	});
    $("#content-nav li").mouseout(function(){
		$(this).css("background","url(images/button.jpg)  no-repeat");
	});
	
	/*注册页面提交按钮特效*/
	$("#button").mouseover(function(){
		$(this).css("background","url(images/ok_hover.jpg) no-repeat");
	});
	$("#button").mouseout(function(){
		$(this).css("background","url(images/ok.jpg) no-repeat");
	});
	$(".sf-service").click(function(){
		art.dialog({
			zIndex:999,
			title:'中国环保网服务条款',
			width:'600px',
			height:'500px',
			content: "<iframe src='service.html' width='580px' height='500px' border=0></iframe>"
		});
	});
	
	
	$("#industry").click(function(){
		$(this).next(".select1-block").css("display","block");
	});
	$("#industry").mouseout(function(){
		$(this).next(".select1-block").css("display","none");
	});
	$("#industry-block").mouseout(function(){
		$(this).css("display","none");
	});
	$("#industry-block").mouseover(function(){
		$(this).css("display","block");
	});
	$("#industry-block ul li").click(function(){
		$("#industry").val($(this).html());
		$("#industry-block").css("display","none");
	});
	
	
	$("#company").click(function(){
		$(this).next(".select1-block").css("display","block");
	});
	$("#company").mouseout(function(){
		$(this).next(".select1-block").css("display","none");
	});
	$("#company-block").mouseout(function(){
		$(this).css("display","none");
	});
	$("#company-block").mouseover(function(){
		$(this).css("display","block");
	});
	$("#company-block ul li").click(function(){
		$("#company").val($(this).html());
		$("#company-block").css("display","none");
	});
	
	$("#regions").click(function(){
		$(this).next(".select1-block").css("display","block");
	});
	$("#regions").mouseout(function(){
		$(this).next(".select1-block").css("display","none");
	});
	$("#regions-block").mouseout(function(){
		$(this).css("display","none");
	});
	$("#regions-block").mouseover(function(){
		$(this).css("display","block");
	});
	$("#regions-block ul li").click(function(){
		$("#regions").val($(this).html());
		$("#regions-block").css("display","none");
	});
	$("#countries").click(function(){
		$(this).next(".select1-block").css("display","block");
	});
	$("#countries").mouseout(function(){
		$(this).next(".select1-block").css("display","none");
	});
	$("#countries-block").mouseout(function(){
		$(this).css("display","none");
	});
	$("#countries-block").mouseover(function(){
		$(this).css("display","block");
	});
	$("#countries-block ul li").click(function(){
		$("#countries").val($(this).html());
		$("#countries-block").css("display","none");
	});
});



/*单选按钮点文字选中*/
function SfRadio(num,n)
{  	
	for(var id=0;id<2;id++){
		if(id===num){
			if(n===0)
			{
				document.getElementById("SfRadio"+id).checked=true;
			}else{
				document.getElementById("NameRadio"+id).checked=true;
			}
		}else{
			if(n===0)
			{
				document.getElementById("SfRadio"+id).checked=false;
			}else{
				document.getElementById("NameRadio"+id).checked=false;
			}
		}
	}
}