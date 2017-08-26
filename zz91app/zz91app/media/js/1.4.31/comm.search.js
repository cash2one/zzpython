// 完成首页初始化
$(".clearinputcontent").on("click",function(){
	//UIInput = api.require('UIInput');
	UIInput.value({
		id:UIInputid,
	    msg: ''
	});
});
function openuiinput(){
	UIInput = api.require('UIInput');
	var type = api.pageParam.type;
	UIInput.open({
	    rect: {
	        x: $(".backicon").width()+50,
	        y: 15,
	        w: $("#search-input").width(),
	        h: 20
	    },
	    styles: {
	        bgColor: '#fff',
	        size: 14,
	        color: '#000',
	        placeholder: {
	            color: '#ccc'
	        }
	    },
	    autoFocus: true,
	    maxRows: 1,
	    placeholder: '输入你感兴趣的关键词',
	    keyboardType: 'default',
	    fixedOn: api.frameName
	}, function(ret, err) {
	
	    if (ret) {
	        //alert(JSON.stringify(ret));
	        UIInputid=ret.id;
	        if (ret.status==true){
	        	if (ret.eventType=="change"){
	        		//alert(2)
			        UIInput.value({
			        id:UIInputid
			        },function(ret1, err) {
					    if (ret1) {
					    	if (ret1.status==true && ret1.msg!=""){
					    		api.execScript({
									frameName : 'search_body',
									script : "searchtis('" + ret1.msg + "')"
								});
					    	}
					        //alert(JSON.stringify(ret1));
					    } else {
					        //alert(JSON.stringify(err));
					    }
					});
				}
			}
	    } else {
	        //alert(JSON.stringify(err));
	    }
	});
	
}
$(".searchbotton").on("click", function() {
	var keywords;
	openuiinput();
	UIInput.value({id:UIInputid},function(ret, err) {
		//alert(JSON.stringify(ret))
	    if (ret) {
	    	if (ret.msg==""){
	    		zzalert("请输入搜索内容！")
	    		return;
	    	}
	    	keywords = ret.msg;
	    	UIInput.close({id:UIInputid});
	    	
	    	
	    	//供求搜索
			if (!type) {
				var pageParam = {
					type : "trade-list",
					label_hex : keywords,
					label : keywords
				};
				type== "trade-list";
				openWin("trade-list", "../trade/trade-list.html", pageParam);
				//return;
			}else{
				if (type== "trade-list") {
					api.execScript({
						name : 'trade-list',
						frameName : 'trade-list_',
						script : "keywordssearch('" + keywords + "')"
					});
				}
			}
			//行情报价搜索
			if (type== "offer-list") {
				var pageParam = {
					type : "offer-list",
					keywords : keywords
				};
				openWin("offer-list", "../price/price.html", pageParam);
				api.execScript({
					name : 'offer-list',
					frameName : 'offer-list_',
					script : "searchprice('" + keywords + "')"
				});
			}
			//行情报价搜索
			if (type== "company-list") {
				var pageParam = {
					type : "company-list",
					keywords : keywords
				};
				api.execScript({
					name : 'company-list',
					frameName : 'company-list_',
					script : "searchkeywords('" + keywords + "')"
				});
			}
			//厂家直购搜索
			if (type== "vender") {
				var pageParam = {
					type : "vender",
					keywords : keywords,
					showbottom : 1
				};
				openWin("vender", "../zhigou/vender.html", pageParam);
				api.execScript({
					name : 'vender',
					frameName : 'vender_',
					script : "searchkeywords('" + keywords + "')"
				});
			}
			//互助社区搜索
			//zzalert(type)
			if (type== "community" || type=='huzhu-list') {
				var pageParam = {
					type : "huzhu-list",
					keywords : keywords
				};
				openWin("huzhu-list", "../huzhu/hudong-list.html", pageParam);
				api.execScript({
					name : 'huzhu-list',
					frameName : 'huzhu-list_',
					script : "keywordssearch('" + keywords + "')"
				});
			}
			var data={
		    	keywords:keywords,
		    	ktype:type,
		    }
		    zzappajax("get",hosturl+"keywords/savekeywords.html",data,function(){
		    	
		    },function(){
		    })
		    
			api.closeWin();
	    	
			//
	    } else {
	        //alert(JSON.stringify(err));
	    }
	});
})
//openuiinput();