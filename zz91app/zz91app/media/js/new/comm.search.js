// 完成首页初始化
$("#searchbutton").hide();
$(".topbar").append('<div class="swipe fr" id="searchbutton1">搜索</div>');
document.getElementById("keywords").focus();
$("#searchbutton1").on("click", function() {
	//供求搜索
	var keywords = $("#keywords").val()
	if (!keywords || keywords==""){
		zzalert("请输入关键字！");
		return false;
	}
	//供求搜索
	var type = api.pageParam.type;
	if (!type) {
		
		var pageParam = {
			type: "trade-list",
			label_hex: keywords,
			label: keywords
		};
		type == "trade-list";
		openWin("trade-list", "../trade/trade-list.html", pageParam);
		api.closeWin({
			name: 'search'
		});
		return false;
	} else {
		if (type == "trade-list") {
			api.execScript({
				name: 'trade-list',
				frameName: 'trade-list_',
				script: "keywordssearch('" + $("#keywords").val() + "')"
			});
		}
	}
	//行情报价搜索
	if (type == "offer-list") {
		var keywords = $("#keywords").val()
		var pageParam = {
			type: "offer-list",
			keywords: keywords
		};
		openWin("offer-list", "../price/price.html", pageParam);
		api.execScript({
			name: 'offer-list',
			frameName: 'offer-list_',
			script: "searchprice('" + $("#keywords").val() + "')"
		});
		//隐藏左边筛选按钮
		//api.execScript({
		//name : 'offer-list',
		//script : "hidrightbutton()"
		//});
	}
	//行情报价搜索
	if (type == "company-list") {
		var keywords = $("#keywords").val()
		var pageParam = {
			type: "company-list",
			keywords: keywords
		};
		api.execScript({
			name: 'company-list',
			frameName: 'company-list_',
			script: "searchkeywords('" + $("#keywords").val() + "')"
		});
	}
	//厂家直购搜索
	if (type == "vender") {
		var keywords = $("#keywords").val();
		//alert(keywords)
		var pageParam = {
			type: "vender",
			keywords: keywords,
			showbottom: 1
		};
		openWin("vender", "../zhigou/vender.html", pageParam);
		api.execScript({
			name: 'vender',
			frameName: 'vender_',
			script: "searchkeywords('" + $("#keywords").val() + "')"
		});
	}
	//互助社区搜索
	//zzalert(type)
	if (type == "community" || type == 'huzhu-list') {
		var keywords = $("#keywords").val()
		var pageParam = {
			type: "huzhu-list",
			keywords: keywords
		};
		openWin("huzhu-list", "../huzhu/hudong-list.html", pageParam);
		api.execScript({
			name: 'huzhu-list',
			frameName: 'huzhu-list_',
			script: "keywordssearch('" + $("#keywords").val() + "')"
		});
	}
	//localStorage.removeItem('seartext');
	//保存搜索历史纪录
	var seartext = $api.getStorage("seartext");
	if (!seartext) {
		seartext = "";
	}
	if ($("#keywords").val() != "") {
		if (seartext != "") {
			$.each(seartext, function(index, item) {
				if (item.type == type) {
					if (item.value != $("#keywords").val()) {
						var seartexta = "{'type' : '" + type + "','value' : '" + $("#keywords").val() + "'}";
						seartext = seartext + seartexta + ",";
						$api.setStorage("seartext", seartext)
					}
				}
			});
		} else {
			var seartexta = "{'type' : '" + type + "','value' : '" + $("#keywords").val() + "'}";
			seartext = seartext + seartexta + ",";
			$api.setStorage("seartext", seartext)
		}
	}
	api.closeWin({
		name: 'search'
	});
})
apiready = function() {
	var thridHeader = $api.byId('thridHeader');
	var header = $api.byId('wrap');
	//$api.fixStatusBar(header);
	var thridHeader = $api.offset(header);
	var type = api.pageParam.type;

	api.openFrame({
		name: 'search_body',
		url: './search_body.html',
		rect: {
			x: 0,
			y: thridHeader.h,
			w: 'auto',
			h: 'auto'
		},
		pageParam: api.pageParam,
		bounces: false,
		delay: 200
	});
	document.getElementById("keywords").focus();
	$("#searchbutton").on("click", function() {
		//供求搜索
		var keywords = $("#keywords").val();
		if (!keywords || keywords==""){
			zzalert("请输入关键字！")
			return false;
		}
		//供求搜索
		if (!type) {
			var pageParam = {
				type: "trade-list",
				label_hex: keywords,
				label: keywords
			};
			type == "trade-list";
			openWin("trade-list", "../trade/trade-list.html", pageParam);
			api.closeWin({
				name: 'search'
			});
			return false;
		} else {
			if (type == "trade-list") {
				api.execScript({
					name: 'trade-list',
					frameName: 'trade-list_',
					script: "keywordssearch('" + $("#keywords").val() + "')"
				});
			}
		}
		//行情报价搜索
		if (type == "offer-list") {
			var keywords = $("#keywords").val()
			var pageParam = {
				type: "offer-list",
				keywords: keywords
			};
			openWin("offer-list", "../price/price.html", pageParam);
			api.execScript({
				name: 'offer-list',
				frameName: 'offer-list_',
				script: "searchprice('" + $("#keywords").val() + "')"
			});
			//隐藏左边筛选按钮
			//api.execScript({
			//name : 'offer-list',
			//script : "hidrightbutton()"
			//});
		}
		//行情报价搜索
		if (type == "company-list") {
			var keywords = $("#keywords").val()
			var pageParam = {
				type: "company-list",
				keywords: keywords
			};
			api.execScript({
				name: 'company-list',
				frameName: 'company-list_',
				script: "searchkeywords('" + $("#keywords").val() + "')"
			});
		}
		//厂家直购搜索
		if (type == "vender") {
			var keywords = $("#keywords").val();
			//alert(keywords)
			var pageParam = {
				type: "vender",
				keywords: keywords,
				showbottom: 1
			};
			openWin("vender", "../zhigou/vender.html", pageParam);
			api.execScript({
				name: 'vender',
				frameName: 'vender_',
				script: "searchkeywords('" + $("#keywords").val() + "')"
			});
		}
		//互助社区搜索
		//zzalert(type)
		if (type == "community" || type == 'huzhu-list') {
			var keywords = $("#keywords").val()
			var pageParam = {
				type: "huzhu-list",
				keywords: keywords
			};
			openWin("huzhu-list", "../huzhu/hudong-list.html", pageParam);
			api.execScript({
				name: 'huzhu-list',
				frameName: 'huzhu-list_',
				script: "keywordssearch('" + $("#keywords").val() + "')"
			});
		}
		//return false;
		//localStorage.removeItem('seartext');
		//保存搜索历史纪录
		var seartext = $api.getStorage("seartext");
		if (!seartext) {
			seartext = "";
		}
		if ($("#keywords").val() != "") {
			if (seartext != "") {
				$.each(seartext, function(index, item) {
					if (item.type == type) {
						if (item.value != $("#keywords").val()) {
							var seartexta = "{'type' : '" + type + "','value' : '" + $("#keywords").val() + "'}";
							seartext = seartext + seartexta + ",";
							$api.setStorage("seartext", seartext)
						}
					}
				});
			} else {
				var seartexta = "{'type' : '" + type + "','value' : '" + $("#keywords").val() + "'}";
				seartext = seartext + seartexta + ",";
				$api.setStorage("seartext", seartext)
			}
		}
		api.closeWin({
			name: 'search'
		});
	})
};