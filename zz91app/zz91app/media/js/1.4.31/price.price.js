apiready = function() {
	var type = api.pageParam.type;
	if (type != "price") {
		$(".box").hide();
		var moreList;
		switch(type) {
			case "gedi":
				moreList = [{
					title : {
						name : "网上报价",
						categoryId : "137"
					},
					list : [{
						name : "河北",
						categoryId : "138",
						mSrc : ""
					}, {
						name : "广东",
						categoryId : "130",
						mSrc : ""
					}, {
						name : "浙江",
						categoryId : "127",
						mSrc : ""
					}, {
						name : "上海",
						categoryId : "115",
						mSrc : ""
					}, {
						name : "齐鲁",
						categoryId : "126",
						mSrc : ""
					}, {
						name : "东莞",
						categoryId : "111",
						mSrc : ""
					}, {
						name : "顺德",
						categoryId : "120",
						mSrc : ""
					}, {
						name : ""
					}, {
						name : ""
					}]
				}];
				break;
			case "quanguo":
				var moreList = [{
					title : {
						name : "网上报价",
						categoryId : "20"
					},
					list : [{
						name : "PET",
						categoryId : "20",
						mSrc : "&assist_id=290"
					}, {
						name : "PP",
						categoryId : "20",
						mSrc : "&assist_id=291"
					}, {
						name : "PC",
						categoryId : "20",
						mSrc : "&assist_id=293"
					}, {
						name : "PS",
						categoryId : "20",
						mSrc : "&assist_id=294"
					}, {
						name : "PVC",
						categoryId : "20",
						mSrc : "&assist_id=297"
					}, {
						name : "ABS",
						categoryId : "20",
						mSrc : "&assist_id=296"
					}, {
						name : "HDPE",
						categoryId : "20",
						mSrc : "&assist_id=295"
					}, {
						name : "LDPE",
						categoryId : "20",
						mSrc : "&assist_id=292"
					}, {
						name : "PA",
						categoryId : "20",
						mSrc : "&assist_id=298"
					}, {
						name : "PMMA",
						categoryId : "20",
						mSrc : "&assist_id=299"
					}, {
						name : ""
					}, {
						name : ""
					}]
				}];
				break;
			case "zaishen":
				var moreList = [{
					title : {
						name : "塑料再生料价格",
						ccategoryId : "98"
					},
					list : [{
						name : "中部地区",
						categoryId : "98",
						mSrc : "&keywords=e4b8ade983a8e59cb0e58cba"
					}, {
						name : "山东",
						categoryId : "98",
						mSrc : "&keywords=e5b1b1e4b89c"
					}, {
						name : "河北",
						categoryId : "98",
						mSrc : "&keywords=e6b2b3e58c97"
					}, {
						name : "江苏",
						categoryId : "98",
						mSrc : "&keywords=e6b19fe88b8f"
					}, {
						name : "浙江",
						categoryId : "98",
						mSrc : "&keywords=e6b599e6b19f"
					}, {
						name : "广东",
						categoryId : "98",
						mSrc : "&keywords=e5b9bfe4b89c"
					}]
				}];
				break;
				break;
			case "usa":
				var moreList = [{
					title : {
						name : "美国废塑料价格",
						categoryId : "62"
					},
					list : [{
						name : "PET",
						categoryId : "62",
						mSrc : "&assist_id=290"
					}, {
						name : "ABS",
						categoryId : "62",
						mSrc : "&assist_id=296"
					}, {
						name : "HDPE",
						categoryId : "62",
						mSrc : "&assist_id=295"
					}, {
						name : "LDPE",
						categoryId : "62",
						mSrc : "&assist_id=292"
					}, {
						name : "PP",
						categoryId : "62",
						mSrc : "&assist_id=291"
					}, {
						name : "PVC",
						categoryId : "62",
						mSrc : "&assist_id=297"
					}]
				}];
				break;
			case "ouzhou":
				var moreList = [{
					title : {
						name : "欧洲废塑料价格",
						categoryId : "63"
					},
					list : [{
						name : "PET",
						categoryId : "63",
						mSrc : "&assist_id=290"
					}, {
						name : "LEPE",
						categoryId : "63",
						mSrc : "&assist_id=292"
					}, {
						name : "HDPE",
						categoryId : "63",
						mSrc : "&assist_id=295"
					}, {
						name : "ABS",
						categoryId : "63",
						mSrc : "&assist_id=296"
					}, {
						name : "PP",
						categoryId : "63",
						mSrc : "&assist_id=291"
					}, {
						name : "PVC",
						categoryId : "63",
						mSrc : "&assist_id=297"
					}, {
						name : "PA",
						categoryId : "63",
						mSrc : "&assist_id=298"
					}, {
						name : ""
					}, {
						name : ""
					}]
				}];
				break;
			case "xinliao":
				var moreList = [{
					title : {
						name : "余姚塑料城",
						categoryId : "324"
					},
					list : [{
						name : "PS",
						categoryId : "324",
						mSrc : "&assist_id=294"
					}, {
						name : "PVC",
						categoryId : "324",
						mSrc : "&assist_id=297"
					}, {
						name : "LDPE",
						categoryId : "324",
						mSrc : "&assist_id=292"
					}, {
						name : "HDPE",
						categoryId : "324",
						mSrc : "&assist_id=295"
					}, {
						name : "LLDPE",
						categoryId : "324",
						mSrc : "&assist_id=304"
					}, {
						name : "PP",
						categoryId : "324",
						mSrc : "&assist_id=291"
					}, {
						name : "ABS",
						categoryId : "324",
						mSrc : "&assist_id=296"
					}, {
						name : ""
					}, {
						name : ""
					}]
				}, {
					title : {
						name : "国内石化出厂价",
						categoryId : "61"
					},
					list : [{
						name : "LDPE",
						categoryId : "61",
						mSrc : "&assist_id=292"
					}, {
						name : "HDPE",
						categoryId : "61",
						mSrc : "&assist_id=295"
					}, {
						name : "PP",
						categoryId : "61",
						mSrc : "&assist_id=291"
					}, {
						name : "PS",
						categoryId : "61",
						mSrc : "&assist_id=294"
					}, {
						name : "PVC",
						categoryId : "61",
						mSrc : "&assist_id=297"
					}, {
						name : "ABS",
						categoryId : "61",
						mSrc : "&assist_id=296"
					}, {
						name : "LLDPE",
						categoryId : "61",
						mSrc : "&assist_id=304"
					}, {
						name : ""
					}, {
						name : ""
					}]
				}, {
					title : {
						name : "国内石化企业出厂价",
						categoryId : "61"
					},
					list : [{
						name : "LDPE",
						categoryId : "61",
						mSrc : "&assist_id=292"
					}, {
						name : "PP",
						categoryId : "61",
						mSrc : "&assist_id=291"
					}, {
						name : "HDPE",
						categoryId : "61",
						mSrc : "&assist_id=295"
					}, {
						name : "PVC",
						categoryId : "61",
						mSrc : "&assist_id=297"
					}, {
						name : "ABS",
						categoryId : "61",
						mSrc : "&assist_id=296"
					}, {
						name : "LLDPE",
						categoryId : "61",
						mSrc : "&assist_id=304"
					}]
				}, {
					title : {
						name : "东莞市场价",
						categoryId : "111"
					}
				}, {
					title : {
						name : "北京市场价",
						categoryId : "112"
					}
				}, {
					title : {
						name : "广州市场价",
						categoryId : "113"
					}
				}, {
					title : {
						name : "常州市场价",
						categoryId : "114"
					}
				}, {
					title : {
						name : "上海市场价",
						categoryId : "115"
					}
				}, {
					title : {
						name : "汕头市场价",
						categoryId : "118"
					}
				}, {
					title : {
						name : "杭州市场价",
						categoryId : "119"
					}
				}, {
					title : {
						name : "顺德市场价",
						categoryId : "120"
					}
				}, {
					title : {
						name : "临沂市场价",
						categoryId : "121"
					}
				}, {
					title : {
						name : "齐鲁市场价",
						categoryId : "126"
					}
				}];
				break;
			case "qihuo":
				var moreList = [{
					title : {
						name : "国际市场收盘价",
						categoryId : "233"
					},
					list : [{
						name : "PE",
						categoryId : "233",
						mSrc : "&assist_id=300"
					}, {
						name : "PP",
						categoryId : "233",
						mSrc : "&assist_id=291"
					}, {
						name : ""
					}]
				}, {
					title : {
						name : "香港美金报价",
						categoryId : "233"
					},
					list : [{
						name : "PE",
						categoryId : "233",
						mSrc : "&assist_id=291"
					}, {
						name : "PP",
						categoryId : "233",
						mSrc : "&assist_id=296"
					}, {
						name : "PP",
						categoryId : "233",
						mSrc : "&assist_id=294"
					}]
				}];
				break;
		}
		getMore(moreList);
	}
	//行情报价
	$(".type-small").on("click", "span", function() {
		var categoryId = $(this).attr("category-id");
		var mSrc = $(this).attr("mSrc");
		if (categoryId) {
			var pageParam = {
				type : "offer-list",
				categoryId : categoryId,
				mSrc : mSrc
			};
			openWin("offer-list", "../price/offer-list.html", pageParam);
		} else {
			var oType = $(this).attr("type");
			if (oType) {
				var pageParam = {
					type : oType,
					wintitle: $(this).text(),
					bounces : false
				};
				openWin(oType, "../price/price.html", pageParam);
			}
		}
	})
}