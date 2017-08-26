// JavaScript Document
//  built by hetao138@gmail.com 2011-1-25
//  zz91.com regsiter page function 2011
var onsubmitErr=0;	
	$(function(){
		//页面重新载入,清空input值
		//$(".fillDomain :input").val("");
		
		//change border-color when input focus 
		$(".fillDomain input").focus(function (){
			$(this).css({ "border":"1px solid #F67F03","background-color":"#F2FFE6" });	
			$(this).next("label").fadeOut(500);
		});
		
		$(".fillDomain input").blur(function (){
			$(this).css({"border":"1px solid #ADC397","background-color":"#FFF"});	
			if($(this).val()==""){
				$(this).next("label").fadeIn(500);
			}	
		});

		//zz91 service hide or show
		$("#viewTermsService").click(function(){
			$("#zz91TermsService").slideDown(800);
			$(".termsServiceClose").show();
			});
			
		$(".termsServiceClose").click(function(){
			$(this).hide();
			$("#zz91TermsService").slideUp(800);
			});

		//input focus default information
		$("#zz91_regemailname").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请填写有效电子邮箱,便于找回密码.<br>没有邮箱? <a href='http://mail.163.com/' target='_blank'>注册网易邮箱</a></em>");
			});
			
		$("#zz91_regemailadr").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请填写有效电子邮箱,便于找回密码.<br>没有邮箱? <a href='http://mail.163.com/' target='_blank'>注册网易邮箱</a></em>");
			});	
			
		$("#zz91_memberName").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>会员登录名由4-20个英文字母或者数字组成,不能使用中文,注册成功后不可修改</em>");
			});
			
		$("#zz91_password").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请填写有效的会员密码,密码由6-20个字符组成,不能使用中文</em>");
			});
			
		$("#zz91_passwordConfirm").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请在输入一遍密码!</em>");
			});
			
		$("#zz91_regProducts").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请填写您所经营的主要商品，有助于快速的找到匹配客户</em>");
			});
			
		$("#zz91_trueName").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请填写真实姓名,方便客户联系您</em>");
			});
			
		$("#zz91_regCompName").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>注册企业请填写在工商局注册全称,个体经营者请填写营业执照上的全称,并标注个体经营。如:个体经营（张三）</em>");
			});
			
		$("#zz91_telcountry").focus(function(){
			$(this).val("086");
			$(this).parent().find("em").replaceWith("<em class='notice'>请在输入国家区号,例如:中国(086)</em>");
			});
			
		$("#zz91_telcity").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请在输入城市区号,例如:北京(010)</em>");
			});
			
		$("#zz91_tel").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请在输入7-8位电话号码</em>");
			});	
				
		$("#zz91_mobile").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请填写11位的手机号码</em>");
			});
			
		$("#zz91_verifyInfo").focus(function(){
			$(this).parent().find("em").replaceWith("<em class='notice'>请将左边图片里的内容填入此处</em>");
			});				
				
				
		
		// email check	
		$("#zz91_regemailname").blur(function(){
			if( $(this).val() != "" && !/^(\w+[\.-]?\w+)*$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>您的电子邮箱格式有误</em>");
				onsubmitErr=1;
				return false;
				}
			else if($(this).val() == ""){
					$(this).parent().find("em").replaceWith("<em class='error'>请填写您有效电子邮箱,便于找回密码</em>");
					return false;
				}
			else{	
					//$(this).parent().find("em").replaceWith("<em class='success'>您的电子邮箱格式正确</em>");
					emailAllFiler();
				}
				
			});
		// email@ check	
		$("#zz91_regemailadr").blur(function(){
				if( $(this).val() != "" && !/^\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($(this).val())){
					$(this).parent().find("em").replaceWith("<em class='error'>您的电子邮箱错误!</em>");
					onsubmitErr=1;
					return false;
					}
				else if($(this).val()==""){
					$(this).parent().find("em").replaceWith("<em class='notice'>请填写电子邮箱!</em>");
					return false;
					}
				else{
					//$(this).parent().find("em").replaceWith("<em class='success'>邮箱服务器地址填写正确!</em>");
					emailAllFiler();
					}
					
			});		
		function emailAllFiler(){
				if($("#zz91_regemailname").val()!="" && $("#zz91_regemailadr").val()!="")
				{
					$("#zz91_regemailname").parent().find("em").replaceWith("<em class='notice'>正在检测，请稍后...</em>");
					var AllEmail=$("#zz91_regemailname").val()+"@"+$("#zz91_regemailadr").val();
					//alert("getemail.asp?email="+AllEmail);
					$.get("/zz91regGetemail/",{email:AllEmail},function(data){
																		
						if (data=="err")
						{
							var url="http://www.zz91.com/cn/login.asp?url=/myrc/default.asp";
							var errtxt="您输入的邮箱已经被使用，请重新输入或使用该邮箱<a href="+url+" target=_blank>登录</a><br><a href=http://www.zz91.com/cn/forgetpass.asp target=_blank>忘记密码？</a>我们将会把您的密码发到您要注册的邮箱里!";
					  		$("#zz91_regemailadr").parent().find("em").replaceWith("<em class='error'>"+errtxt+"</em>");
							onsubmitErr=1;
						}else if (data=="succ")
						{
							$("#zz91_regemailadr").parent().find("em").replaceWith("<em class='success'>填写正确！</em>");
							onsubmitErr=0;
						}
					});
				}
		}
		
		//regname check
		$("#zz91_memberName").blur(function(){
			if( $(this).val() != "" && !/^[a-zA-Z]{1}([a-zA-Z\d]){3,19}$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>会员登录名有误,登录名是能是以字母开头的4-20个字母或者数字组成!</em>");
				onsubmitErr=1;
				return false;
			}
			else if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>会员登录名必须填写!</em>");
				return false;
				}
			else{
				//$(this).parent().find("em").replaceWith("<em class='success'>会员登录名格式正确!</em>");
				usernameFilter();
				}
			});
		function usernameFilter()
		{
			if ($("#zz91_memberName").val()!="")
			{
				var memberName=$("#zz91_memberName").val();
				$("#zz91_memberName").parent().find("em").replaceWith("<em class='notice'>正在检测，请稍后...</em>");
				//alert("getemail.asp?email="+AllEmail);
				$.get("/zz91regGetusername/",{username: memberName}, function(data){
					if (data=="err")
					{
						var errtxt="该会员名已经存在，请重新输入";
						onsubmitErr=1;
						$("#zz91_memberName").parent().find("em").replaceWith("<em class='error'>"+errtxt+"</em>");
					}else if (data=="succ")
					{
						$("#zz91_memberName").parent().find("em").replaceWith("<em class='success'>填写正确！</em>");
						onsubmitErr=0;
					}
				});
			}
		}
		//password check
		$("#zz91_password").blur(function(){
			if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>请填写会员密码</em>");
				return false;
			}
			else if( $(this).val() != "" && /^[\x80-\xff]?$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>会员密码不能使用中文</em>");
				onsubmitErr=1;
				return false;
				}
			else if( $(this).val() != "" && ($(this).val().length < 6 || $(this).val().length >20)){
				$(this).parent().find("em").replaceWith("<em class='error'>密码长度应在6-20个字母之间</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>密码格式正确</em>");
				onsubmitErr=0;
				}
			});
			
		//password confirm
		$("#zz91_passwordConfirm").blur(function(){
			if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>请再次填写您的密码</em>");
				onsubmitErr=1;
				return false;
			}
			else if( $(this).val() != "" && $(this).val()!= $("#zz91_password").val()){
				$(this).parent().find("em").replaceWith("<em class='error'>第二次输入和第一次不一样,请重新输入</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>密码第二次输入正确</em>");
				onsubmitErr=0;
				}
			});
	
		//products check
		$("#zz91_regProducts").blur(function(){
			if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>请填写经营产品</em>");
				onsubmitErr=1;
				return false;
			}
			else if( $(this).val() != "" && ($(this).val().length < 1 || $(this).val().length >40) ){
				$(this).parent().find("em").replaceWith("<em class='error'>请简短的描述你的产品,4请将控制在20个字以内</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>经营产品填写正确</em>");
				onsubmitErr=0;
				}
			});
		
		//reg username  check
		$("#zz91_trueName").blur(function(){
			if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>请填写真实姓名</em>");
				onsubmitErr=1;
				return false;
			}
			else if( $(this).val() != "" && /^[a-zA-Z\x80-\xff]{2,8}$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>您的姓名输入格式有误</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>填写的姓名格式正确</em>");
				onsubmitErr=0;
				}
			});
			
		//reg Company check
		$("#zz91_regCompName").blur(function(){
			if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>请填写公司名称,或者个体经营者名称</em>");
				onsubmitErr=1;
				return false;
			}
			else if( $(this).val() != "" && ($(this).val().length < 4 || $(this).val().length >40) ){
				$(this).parent().find("em").replaceWith("<em class='error'>填写的公司名称太长或者太短,请控制在2-20个字数以内</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>公司名称填写正确</em>");
				onsubmitErr=0;
				}
			});	
		
		
		//telcountry check
		$("#zz91_telcountry").blur(function(){
			if($(this).val()==""){
				//$(this).parent().find("em").replaceWith("<em class='error'>请填写国家区号,国家区号默认为:中国(086)</em>");
				//onsubmitErr=1;
				//return false;
			}
			else if( $(this).val() != "" && !/^\d{1,6}$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>国家区号填写错误,国家区号是1-6位的数字</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>国家区号格式填写正确</em>");
				onsubmitErr=0;
				}
			});	
			
		//telcity check
		$("#zz91_telcity").blur(function(){
			if($(this).val()==""){
				//$(this).parent().find("em").replaceWith("<em class='error'>请填写城市区号</em>");
				//onsubmitErr=1;
				//return false;
			}
			else if( $(this).val() != "" && !/^0{1}[\d]{2,3}$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>城市区号填写错误,城市区号是以0开头的3-4位的数字</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>城市区号格式填写正确</em>");
				onsubmitErr=0;
				}
			});	
			
		//tel check
		$("#zz91_tel").blur(function(){
			if($(this).val()==""){
				//$(this).parent().find("em").replaceWith("<em class='error'>请填写电话号码</em>");
				//onsubmitErr=1;
				//return false;
			}
			else if( $(this).val() != "" && !/^[\d]{7,8}$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>电话号码填写错误,电话号码是7-8位的数字</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				$(this).parent().find("em").replaceWith("<em class='success'>电话号码格填写式正确</em>");
				onsubmitErr=0;
				}
			});	
		
		// mobilephone check
		$("#zz91_mobile").blur(function(){
			if($(this).val()==""){
				$(this).parent().find("em").replaceWith("<em class='error'>请填写手机号码</em>");
				onsubmitErr=1;
				return false;
			}
			else if( $(this).val() != "" && !/^1[3,5,8]{1}[\d]{9}$/.test($(this).val())){
				$(this).parent().find("em").replaceWith("<em class='error'>手机号码格式不正确</em>");
				onsubmitErr=1;
				return false;
				}
			else{
				//$(this).parent().find("em").replaceWith("<em class='success'>手机号码格式填写正确</em>");
				commobileFilter();
				}
			});
		function commobileFilter()
		{
			if ($("#zz91_mobile").val()!="")
			{
				var mobile=$("#zz91_mobile").val();
				$("#zz91_mobile").parent().find("em").replaceWith("<em class='notice'>正在检测，请稍后...</em>");
				$.get("/zz91regGetmobile/",{mobile:mobile}, function(data){
					if (data!="")
					{
						var errtxt="此手机号码已被注册，请填写其它号码";
						onsubmitErr=1;
						$("#zz91_mobile").parent().find("em").replaceWith("<em class='error'>"+errtxt+"</em>");
					}else if (data=="")
					{
						$("#zz91_mobile").parent().find("em").replaceWith("<em class='success'>填写正确！</em>");
						document.getElementById("mobileflag").value="1";
						onsubmitErr=0;
						//return false;
					}
				});
			}
		}
			
	});
	
	
	// alertBox build
	function alertBox(alertInfo){
		$("body").append("<div class='isfillformbc'></div><div class='isfillform'><div class='isfillformArea'><div class='close'>关闭提示</div><div class='zz91_warning'></div></div></div>");
		$(".isfillformbc,.isfillform").fadeIn(20);
		$(".zz91_warning").append(alertInfo);				
		$(".close").click(function(){
			$(".isfillformbc,.isfillform").fadeOut(20,function(){$("div").remove(".isfillformbc, .isfillform")});
		});
		
	}
			
	//mobile & tel 	fill one of them
	$(function(){
		$("form").submit(function(){
		var emailName="电子邮箱没有填写!";
		var emailAdr="电子邮箱没有填写!";
		var member="会员登录名没有填写!";
		var password="密码没有填写!";
		var passwordConfirm="密码没有确认!";
		var regProducts="主营产品没有填写";
		var trueName="您的姓名没有填写!";
		var company="公司名称没有填写!";
		var mobileTel="固定电话或者手机号码必填一项";
		var verifyInfo="验证码没有填写!";
		var mobiletxt="你注册的手机号码已经存在！请重新填写！";
		var memberNametxt="会员登录名已经存在！请重新填写！";
		var emailtxt="你注册的电子邮箱已经存在！请重新填写！"
		var verifyInfo="验证码没有填写";
		var success="祝贺您!您已经成功注册为ZZ91再生网会员,系统将自动跳转到注册第二步,您可以进一步完善自己的个人资料,待完善个人资料后,ZZ91将快速的为你匹配相应客户,立刻开始网上贸易!";
		if($("#zz91_regemailname").val()==""){
			alertBox(emailName);
			return false;
			}
		else if($("#zz91_regemailadr").val()==""){
			alertBox(emailAdr);
			return false;
			}
		else if($("#zz91_memberName").val()==""){
			alertBox(member);
			return false;
			}
		else if($("#zz91_password").val()==""){
			alertBox(password);
			return false;
			}
		
		else if($("#zz91_passwordConfirm").val()==""){
			alertBox(passwordConfirm);
			return false;
			}
		else if($("#zz91_regProducts").val()==""){
			alertBox(regProducts);
			return false;
			}
		else if($("#zz91_trueName").val()==""){
			alertBox(trueName);
			return false;
			}
		else if($("#zz91_regCompName").val()==""){
			alertBox(company);
			return false;
			}
		
		else if($("#zz91_mobile").val()==""){
			alertBox(mobileTel);
			return false;
			}
		else if($("#zz91_verifyInfo").val()==""){
			alertBox(verifyInfo);
			return false;
			}
		else if(onsubmitErr==1){
			return false;
			}
		//alert(onsubmitErr);
		document.getElementById("Submitsave").disabled=true
		document.getElementById("Submitsave").value="正在上传数据，请稍候..."
		errtimeout();
		});
	});
var tt=0;
function errtimeout()
{
	if (tt>100)
	{
		alert("提交信息出现错误，前检查你提交的信息是否有误,请重新提交！");
		document.getElementById('Submitsave').disabled=false;
		document.getElementById('Submitsave').value='提交注册信息';
		tt=0;
		return false;
	}
	tt=tt+1;
	setTimeout("errtimeout()",1000);
}
function changeVerifyImage()
{
	document.getElementById("yzpic").src="/zz91verifycode/"+Math.random()
}