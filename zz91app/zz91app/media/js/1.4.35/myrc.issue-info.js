$(".prototop").find(".aui-input-row").html('<input class="aui-checkbox aui-checkbox-info" type="checkbox"  name="protop" id="protop" checked  value="1" onclick="selectshowcontact()">开通供求置顶服务， ￥ 1200元/次<br /> <a class="color-green seetopservice">查看详情</a><span style="color:#ff0000;font-size:12px">让更多的客户联系您。</span>')

//获取余额
		function getbalance(){
			//获得余额
			zzappajax("get",hosturl+"qianbao/qianbaobaoblance.html","",function(ret){
				if (ret){
					var blance=ret.blance;
					var showphpne=ret.showphone;
					$(".balancenum").html(blance);
					var showcontactnum=0;
					var contact_see = $(".see-contact input:checked").val();
					if (parseInt(contact_see)==1){
						showcontactnum=$("#showcontactnum").val();
						if (showcontactnum){
							showcontactnum=parseInt(showcontactnum)
						}
					}
					
					var protopchecked = $("#protop:checked").val();
					if (protopchecked){
						showcontactnum+=1200;
					}
					if (blance>=parseInt(showcontactnum)){
						$(".nomeny").hide();
					}else{
						$(".nomeny").show();
					}
					//高会或已经购买显示联系方式直接隐藏
					if (showphpne){
						$(".see-contact").hide();
						$(".showcontact").hide();
					}else{
						$(".see-contact").show();
						//$(".showcontact").show();
					}
				}else{
					$(".see-contact").hide();
					$(".showcontact").hide();
				}
			},function(){
				zzalert("读取余额错误！")
			})
		}
		
		//选择付费类型
		function selectshowcontact(){
			var showcontactnum=$("#showcontactnum").val();
			if (showcontactnum){
				showcontactnum=parseInt(showcontactnum)
			}else{
				showcontactnum=0
			}
			selectvalue=showcontactnum;
			var contact_see = $(".see-contact input:checked").val();
			if (contact_see==0){
				selectvalue=0;
			}
			var balancenum=$(".balancenum").text();
			var protopchecked = $("#protop:checked").val();
			var showcontactnum=parseInt(selectvalue);
			if (protopchecked){
				showcontactnum+=1200;
			}
			if (parseInt(showcontactnum)>parseInt(balancenum)){
				$(".nomeny").show();
			}else{
				$(".nomeny").hide();
			}
		}
