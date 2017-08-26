// JavaScript Document
AliMobile.Util = (function() {
	function wzHide(wzid) {
		jQuery("#" + wzid).hide();
		var date = new Date();
		var expireDays = 5;
		date.setTime(date.getTime() + expireDays * 24 * 3600 * 1000);
		document.cookie = wzid + "=0; path=/; expires=" + date.toGMTString();
	}
	function navPageGoto(totalPage, currPage) {
		var pageIndex = document.getElementById('pageIndex').value;
		if (pageIndex < 1 || pageIndex == null) {
			alert("请输入正确的页码！");
			return;
		}
		if (pageIndex > 0 && pageIndex <= totalPage) {
			var href = window.location.href;
			var url = href;
			if (href.indexOf("p-") == -1) {
				url = href.replace(".htm", "_p-" + pageIndex + ".htm");
			} else {
				url = href.replace("p-" + currPage, "p-" + pageIndex);
				}
			window.location.href = url;
		}
	}

	/* 注册暂时使用 */
	var xmlHttp = false;
	try {
		xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
	} catch (e) {
		try {
			xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
		} catch (e2) {
			xmlHttp = false;
		}
	}
	if (!xmlHttp && typeof XMLHttpRequest != 'undefined') {
		xmlHttp = new XMLHttpRequest();
	}
	/* register */
	function callServer() {
		var mobile = document.getElementById("mobile").value;
		var myFunc = "callback";
		if (mobile == "") {
			alert("请输入11位手机号！");
			return false;
		}
		var url = "/touch/member/mRegister.htm";
		var paramStr = "action=member/RegisterHandler&event_submit_do_send_mobile_verify_code4_touch=aa&mobile="
				+ escape(mobile) + "&callback =" + escape(myFunc);

		xmlHttp.open("POST", url, true);
		xmlHttp.setRequestHeader("Content-type",
				"application/x-www-form-urlencoded");
		xmlHttp.onreadystatechange = evalCallback;
		xmlHttp.send(paramStr);
	}
	function evalCallback() {
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			var result = xmlHttp.responseText.replace(/&quot;/g, "\"");
			eval(result);
		}
	}
	function callback(jsonObj) {
		var info = document.getElementById("info");
		if (jsonObj.success == true) {
			info.innerHTML = " 验证码已发送到您的手机，请立即查收。没有收到？";
		} else {
			switch (jsonObj.data.resultCode) {
			case "MOBILE_IDENTITY_CODE_TOO_FREQUENTLY":
				info.innerHTML = "手机获取验证码过于频繁,请一分钟之后再试。";
				break;
			case "MOBILE_HAS_VALIDATED":
				info.innerHTML = "此手机目前已验证";
				break;
			case "DATA_ERROR":
				info.innerHTML = "手机号码不合法";
				break;
			case "MEMBER_MP_VALIDATE_MP_ERR":
				info.innerHTML = "手机号码不合法";
				break;
			default:
				info.innerHTML = jsonObj.data.resultCode;
			}
		}
	}
	function checkAgree(obj, target) {
		if (obj.checked == false) {
			target.setAttribute("class", "grayBtn");
			target.disabled = true;
		} else {
			target.setAttribute("class", "commonBtn");
			target.disabled = false;
		}
	}
	var favParentNode;
	function favDel(tobj) {
		var obj = jQuery(tobj);
		jQuery("#favDelUrl").attr("value", obj.attr("ahref"));
		jQuery("#favDelTitle").html(obj.attr("atitle"));
		var adel = obj.attr("adel") || "div";
		favParentNode = obj.parent(adel);
		favDeleteDialogHidden("#favDelReturn");
		favDeleteDialogShow("#favDelConfirm");

		jQuery("#cancel").bind("click", function(e) {
			favDeleteDialogHidden("#favDelConfirm");
		});
		jQuery("#ok").bind("click", function(e) {
			favDeleteAjaxRequest();
		});
	}

	function favDeleteDialogShow(id, time) {
		var fdc = jQuery(id);
		fdc.css('display', '');
		fdc.css('top', document.body.scrollTop + 200 + 'px');
		if (time) {
			setTimeout(function() {
				favDeleteDialogHidden(id)
			}, time);
		}
	}

	function favDeleteDialogHidden(id) {
		var fdc = jQuery(id);
		fdc.css('display', 'none');
	}

	function favDeleteAjaxRequest() {
		jQuery("#favDelReturnMsg").html("处理中...");
		var ajaxurl = jQuery("#favDelUrl").attr("value");
		jQuery.ajax({
			url : ajaxurl + "&ajaxport=1",
			type : "GET",
			dataType : "html",
			error : function() {
				jQuery("#favDelReturnMsg").html("删除失败");
				favDeleteDialogHidden("#favDelConfirm");
				favDeleteDialogShow("#favDelReturn", 1500);
			},
			success : function(responseText) {

				if (responseText.trim() == "noLogined") {
					window.location.href = url;
					return;
				}
				jQuery("#favDelReturnMsg").html(responseText);
				if (responseText.indexOf("成功") !== -1) {
					favParentNode.remove();
					favDeleteDialogHidden("#favDelConfirm");
					favDeleteDialogShow("#favDelReturn", 1500);
				}
			}
		});
	}

	function addFav(ajaxurl) {
		jQuery.ajax({
			url : ajaxurl + "&ajaxport=1",
			type : "GET",
			dataType : "html",
			error : function() {
				alert("收藏失败！");
			},
			success : function(responseText) {
				if (responseText.trim() == "noLogined") {
					window.location.href = ajaxurl;
				} else {
					alert("温馨提示：" + responseText);
				}
			}
		});
	}
	function showOfferBigPicDialog(bigUrl) {
		// 显示大图
		document.getElementById('showImg').setAttribute("src", bigUrl);
		document.getElementById('disFilter').style.display = "block";
		document.getElementById('dialogClose').style.display = "block";
		document.getElementById('fadelayer').style.display = "block";

		document.getElementById('showImg').onload = function() {
			var totalHeight = document.getElementsByTagName("body")[0].scrollHeight;

			document.getElementById('fadelayer').style.height = totalHeight
					+ "px";
		}
	}
	function closeOfferBigPicDialog() {
		document.getElementById('fadelayer').style.display = "none";
		document.getElementById('disFilter').style.display = "none";
		document.getElementById('dialogClose').style.display = "none";
	}

	function getPositionSuccess(position) {
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;
		document.getElementById("long").value = lng;
		document.getElementById("lati").value = lat;
		var lngStr = "" + lng;
		var index = lngStr.indexOf(".");
		if (index != -1 && lngStr.length > index + 4) {
			lngStr = lngStr.substring(0, index + 4);
		}
		var latStr = "" + lat;
		index = latStr.indexOf(".");
		if (index != -1 && latStr.length > index + 4) {
			latStr = latStr.substring(0, index + 4);
		}
		document.getElementById("longSpan").innerHTML = lngStr;
		document.getElementById("latiSpan").innerHTML = latStr;
		display(1);
		var url = '/touch/offer/ajaxGeo/?lati=' + lat + "&long=" + lng;
		var script = jQuery.getScript(url, function() {
			getGeoInfo();
		});
	}

	function getGeoInfo() {
		if (_geo_result_ && _geo_result_.result) {
			var province = _geo_result_.result.province;
			var city = _geo_result_.result.city;
			var town = _geo_result_.result.town;
			var street = _geo_result_.result.street;
			var nearLocation = _geo_result_.result.location;
			var curLoc = province;
			if (province.indexOf('市') == -1) {
				curLoc += city;
			}
			if (city != town) {
				curLoc += town;
			}
			curLoc += street;
			document.getElementById('tempLocation').style.display = "none";
			document.getElementById('realLocation').innerHTML = curLoc;
		}
	}

	function getPositionError(error) {
		switch (error.code) {
		case error.TIMEOUT:
			showErrorMsg("位置获取失败");
			break;
		case error.PERMISSION_DENIED:
			showErrorMsg("位置获取失败");
			break;
		case error.POSITION_UNAVAILABLE:
			showErrorMsg("位置获取失败");
			break;
		}
	}

	function display(type) {
		if (type == 1) {
			document.getElementById("div1").style.display = "none";
			document.getElementById("div2").style.display = "block";
			document.getElementById("div3").style.display = "none";
			document.getElementById("distance").style.height = "192px";
		} else if (type == 2) {
			document.getElementById("div1").style.display = "none";
			document.getElementById("div2").style.display = "none";
			document.getElementById("div3").style.display = "block";
			document.getElementById("distance").style.height = "96px";
		} else {
			document.getElementById("div1").style.display = "block";
			document.getElementById("div2").style.display = "none";
			document.getElementById("div3").style.display = "none";
		}
	}

	function showErrorMsg(msg) {
		document.getElementById("errormsg").innerHTML = msg;
		display(2);
	}

	function init() {
		if (navigator.geolocation) {
			display(0);
			navigator.geolocation.getCurrentPosition(getPositionSuccess,
					getPositionError);
		} else {
			showErrorMsg('非常抱歉，可能由于设备原因，我们暂时无法获取您的当前位置');
		}
	}

	function showDisList() {
		var evt = document.createEvent('MouseEvents');
		evt.initEvent('click', true, true);
		evt.clientX = 580;
		evt.clientY = 230;
		document.getElementById('disSelect').dispatchEvent(evt);
	}
	function showFilterDiv(flag) {

		if (document.getElementById("mobileUserAgent").value != "android") {
			document.getElementById('bgDiv').style.display = "block";
			document.getElementById('popDiv').style.display = "block";
			document.getElementById('dialogClose').style.display = "block";
			document.getElementById('filterContent').style.display = "block";
		} else {
			document.getElementById('popDiv').setAttribute("class", "");
			document.getElementById('dialogClose').setAttribute("class",
					"filter-close-android");
			document.getElementById('filterContent').setAttribute("class",
					"filter-content-android");
			document.getElementById('popDiv').style.display = "block";
			document.getElementById('dialogClose').style.display = "block";
			document.getElementById('filterContent').style.display = "block";
		}

		if (flag == 1) {
			document.getElementById('cate').style.display = "block";
			document.getElementById('area').style.display = "none";
			if (document.getElementById('distance') != null) {
				document.getElementById('distance').style.display = "none";
			}
		} else if (flag == 2) {
			document.getElementById('cate').style.display = "none";
			document.getElementById('area').style.display = "block";
			if (document.getElementById('distance') != null) {
				document.getElementById('distance').style.display = "none";
			}
		} else if (flag == 3) {
			document.getElementById('cate').style.display = "none";
			document.getElementById('area').style.display = "none";
			document.getElementById('distance').style.display = "block";
			init();
		}

		if (document.getElementById("mobileUserAgent").value != "android") {
			var totalHeight = jQuery("body")[0].scrollHeight;
			document.getElementById('bgDiv').style.height = totalHeight + 100
					+ "px";
			document.getElementById('popDiv').style.height = totalHeight + "px";
		}

	}
	function closeDialog() {
		if (document.getElementById('bgDiv') != null) {
			document.getElementById('bgDiv').style.display = "none";
		}
		document.getElementById('popDiv').style.display = "none";
		document.getElementById('dialogClose').style.display = "none";
		document.getElementById('filterContent').style.display = "none";

		document.getElementById('cate').style.display = "none";
		document.getElementById('area').style.display = "none";
		if (document.getElementById('distance') != null) {
			document.getElementById('distance').style.display = "none";
		}
	}
	function submitPriceFilter(id) {
		var select = document.getElementById(id);
		if (select.options[select.options.selectedIndex] != "") {
			window.location.href = select.options[select.options.selectedIndex].value;
		} else {
			closeDialog();
		}
	}

	function showSubCate(cateId, keywords) {
		if (cateId != "0") {
			document.getElementById("categoryId").value = cateId;
			document.getElementById("ajaxDiv").innerHTML = "<div class='wait'><img src='/images/load.gif'/>正在获取数据，请稍后...</div>";
			var ajaxurl = "/touch/offer/ajaxCategory.htm?categoryId=" + cateId
					+ "&keywords=" + keywords;
			jQuery.ajax({
				url : ajaxurl,
				type : "GET",
				dataType : "html",
				error : function() {
					return false
				},
				success : function(html) {
					document.getElementById("ajaxDiv").innerHTML = html;
				}
			});
		}
	}

	function submitCate() {
		var subCateDiv = document.getElementById("subCate");
		var url = "";
		var param = "";
		
		var fValue = "";
		var featurelist = document.getElementsByName("featurelist");
		if (featurelist != null) {
			var pos = document.getElementById("featurelist").options;
			for ( var i = 0; i < pos.length; i++) {
				var po = pos[i];
				if (po.selected == true) {
					fValue = po.value;
					break;
				}
			}
			document.getElementById("feature").value = fValue;
		}
		

		if (fValue == "") {
			closeDialog();
		} else {
			window.location.href = "/offerlist/?keywords="+ fValue +"";
			//document.getElementById("cateForm").action="/offerlist/?keywords="+ fValue +"";
			//document.getElementById("cateForm").submit();
		}

	}

	var isShow = false;
	function showSearch() {
		var obj = jQuery("#searchBar");
		if (obj != null) {
			if (isShow == false) {
				obj.css('display', 'block');
				isShow = true;
			} else {
				obj.css('display', 'none');
				isShow = false;
			}
		}
	}

	function gotoPage(totalPage, currentPage, pageName) {
		var pageIndex = $('#pageIndex').val();
		if (pageIndex > 0 && pageIndex <= totalPage) {
			var href = window.location.href;
			var url = "";
			if (pageName == "fav") {
				url = href.replace("beginPage=" + currentPage, "beginPage=" + pageIndex);
				if (url.indexOf("beginPage=") == -1) {
					url += "&beginPage=" + pageIndex;
				}
			} else {
				url = href.replace("p-" + currentPage, "p-" + pageIndex);
				if (url.indexOf("p-") == -1) {
					url = url.replace(".htm", "_p-" + pageIndex + ".htm");
				}
			}
			window.location.href = url;
		}
	}

	function showMore(obj, short, long) {
		var shortDiv = document.getElementById(short);
		var longDiv = document.getElementById(long);
		if (obj.value == "更 多") {
			obj.style.display = "none";
			shortDiv.style.display = "none";
			longDiv.style.display = "block";
		} else {
			obj.value = "更 多";
			shortDiv.style.display = "block";
			longDiv.style.display = "none";
		}
	}
	return {
		version : "1.0",
		getPositionSuccess : getPositionSuccess,
		getGeoInfo : getGeoInfo,
		getPositionError : getPositionError,
		display : display,
		showErrorMsg : showErrorMsg,
		init : init,
		showDisList : showDisList,
		showFilterDiv : showFilterDiv,
		closeDialog : closeDialog,
		submitPriceFilter : submitPriceFilter,
		showSubCate : showSubCate,
		submitCate : submitCate,
		showOfferBigPicDialog : showOfferBigPicDialog,
		closeOfferBigPicDialog : closeOfferBigPicDialog,
		addFav : addFav,
		favDel : favDel,
		callServer : callServer,
		showSearch : showSearch,
		gotoPage : gotoPage,
		showMore : showMore,
		wzHide : wzHide,
		navPageGoto : navPageGoto
	};
})();

AliMobile.Area = (function() {

	var bindEvent = function(id) {
		jQuery(id).bind('change', function(e) {
			for ( var i = 0; i < this.options.length; i++) {
				var o = this.options[i];
				if (o.selected == true) {
					var prov = o.value;
					if (prov != "0") {
						enableCity();
						getData(prov, doSomething);
					} else {
						initCity(new Array());
						disableCity();
					}
					break
				}
			}
		});
	};
	bindEvent("#province");

	var getData = function(province, callback) {
		var url = '/touch/shortcut/ajaxCityList.htm?province=' + province;
		var script = jQuery.getScript(url, function() {
			callback();
		});
	};
	var doSomething = function() {
		if (_city_result_.result && _city_result_.result.length > 0) {
			initCity(_city_result_.result);
			enableCity();
		} else {
			initCity(new Array());
			disableCity();
		}
	};
	var initCity = function(list) {
		var cs = jQuery('#city');
		var opts = cs[0].options;
		if (opts.length > 1) {
			cs.empty();
			cs.append('<option value="0">所有城镇</option>');
		}
		for ( var i = 0; i < list.length; i++) {
			var str = '<option value="' + list[i] + '">' + list[i]
					+ '</option>';
			cs.append(str);
		}
	};
	var disableCity = function() {
		jQuery('#city').css('disabled', true);
		jQuery('#city').css('class', 'disableSelect');
	};
	var enableCity = function() {
		jQuery('#city').css('disabled', false);
		jQuery('#city').css('class', 'areaSelect');
	};

	var clearSelectArea = function() {
		document.getElementById("city").options[0].selected = true;
		document.getElementById("province").options[0].selected = true;
		document.getElementById("areaFiltFrm").submit();
	};

	var selectArea = function() {
		var province = null, city = null, showProvince = null;
		if (document.getElementById("province").options[0].selected != true) {
			var pos = document.getElementById("province").options;
			for ( var i = 0; i < pos.length; i++) {
				var po = pos[i];
				if (po.selected == true) {
					province = po.value;
					showProvince = province;
					break;
				}
			}
			//var cos = document.getElementById("city").options;
//			if (cos[0].selected != true) {
//				for ( var i = 0; i < cos.length; i++) {
//					var co = cos[i];
//					if (co.selected == true) {
//						// province = null;
//						city = co.value;
//						showProvince = city;
//						break;
//					}
//				}
//			}
		}
		if (province != null) {
			document.getElementById("hiddenProv").value = province;
		}
		if (city != null) {
			document.getElementById("hiddenCity").value = city;
		}
		if (showProvince != null) {
			document.getElementById("hiddenShowProv").value = showProvince;
		}
		document.getElementById("areaFiltFrm").submit();
	};
	return {
		version : "1.0",
		clearSelectArea : clearSelectArea,
		selectArea : selectArea
	};
})();

AliMobile.SearchBar = (function() {
	var input = function(t, m, c) {
		AliMobile.SearchBar.showCleanIcon(t);
		AliMobile.SearchBar.getSuggestData(t, m, c);
	}
	var submit = function(t) {
		if (chkSearchInput(t)) {
			jQuery(t + " form").submit();
		}
	};
	var showCleanIcon = function(t) {
		if (jQuery(t + " .searchKey").val() != "") {
			jQuery(t + " .clear").show();
		} else {
			jQuery(t + " .clear").hide();
		}
	};
	var cleanSearchInput = function(t) {
		jQuery(t + " .searchKey").val('');
		jQuery(t + " .clear").hide();
		jQuery(t + " .t-search-suggest").remove();
	};
	var chkSearchInput = function(t) {
		if (jQuery(t + " .searchKey").val() == "") {
			alert("请输入关键字！");
			return false;
		} else {
			return true;
		}
	};
	var setSearchType = function(t, m, text, type, msg) {
		if (m == "2")
			jQuery(t + " .selection").addClass("selection-b");
		if (type) {
			jQuery(t + " .selection").hide();
			jQuery(t + " .type").text(text);
			jQuery(t + " .searchKey").attr("placeholder", msg);
			jQuery(t + " .searchType").val(type);
		} else {
			jQuery(t + " .selection").toggle()
			jQuery(t + " .t-search-suggest").remove();
		}
	};
	var getSuggestData = function(t, m, c) {
		var type = jQuery(t + " .searchType").val();
		var query = jQuery(t + " .searchKey").val();
		if (query.lenght < 2)
			return;
		var ajaxurl = "http://suggest.china.alibaba.com/bin/suggest?type="
				+ type + "&q=" + query;
		//var _suggest_result_={result:[['_pp%裤','7620'], ['_pp%板','12819'], ['_pp%再生料','20295'], ['聚丙烯_pp%','47968'], ['品牌','55651114'], ['_pp%s','84613'], ['透明_pp%','102503'], ['再生_pp%','17495'], ['_pp%袋','277377'], ['阻燃_pp%','15857']],category:[{query:"pp",name:"PP", id:"1034889"}]};
		jQuery.getScript(ajaxurl, function() {
			var result = _suggest_result_.result;
			if (jQuery.isArray(result) && result.length > 0) {
				jQuery(t + " .selection").hide();
				jQuery(t + " .t-search-suggest").remove();
				var suggestion = '<div class="suggestion"><ul>';
				var n = 0;
				if (m == "2")
					suggestion += '<li class="ac close">\u5173\u95ed</li>';
				jQuery.each(result, function(i, it) {
					var key = it[0].replace('_', '').replace('%', '')
					var li = '<li class="item"><span class="num">' + it[1]
							+ '\u6761</span><span class="key">' + key
							+ '</span></li>';
					if (n++ < 4) {
						suggestion += li;
					}
				});
				if (m == "1")
					suggestion += '<li class="ac close">\u5173\u95ed</li>';
				suggestion += "</ul></div>";
				jQuery(t + " " + (c || ".t-search-bar")).append(
						'<div class="t-search-suggest"></div>');
				if (m == "2")
					jQuery(t + " .t-search-suggest").addClass(
							result.length > 1 ? "t-search-suggest-b"
									: "t-search-suggest-b2");
				jQuery(t + " .t-search-suggest").append(suggestion);
				jQuery(t + " .suggestion .close").bind('click', function(e) {
					jQuery(t + " .t-search-suggest").hide();
				});
				jQuery(t + " .suggestion .item").bind('click', function(e) {
					var k = e.target.childNodes[1] || e.target;
					jQuery(t + " .searchKey").val(k.innerText);
					jQuery(t + " form").submit();
				});
			}
		});
	};
	function showQuickSearch() {
		jQuery(".t-quick-hidden").css('display', 'none');
		jQuery("#quickSearch").css('display', 'block');

	}

	function hideQuickSearch() {
		jQuery(".t-quick-hidden").css('display', 'block');
		jQuery("#quickSearch").css('display', 'none');

	}
	return {
		version : "1.0",
		submit : submit,
		getSuggestData : getSuggestData,
		setSearchType : setSearchType,
		chkSearchInput : chkSearchInput,
		cleanSearchInput : cleanSearchInput,
		showCleanIcon : showCleanIcon,
		submit : submit,
		input : input,
		showQuickSearch : showQuickSearch,
		hideQuickSearch : hideQuickSearch
	};
})();

AliMobile.Support = (function() {
	function doSupport(obj, type, id) {
		var num = document.getElementById("num" + id);

		var ajaxurl = "/touch/wiki/ajaxSupport/?type=" + type + "&id=" + id;
		jQuery
				.ajax({
					url : ajaxurl,
					type : "GET",
					dataType : "html",
					error : function() {
						return false
					},
					success : function(html) {
						if (html == "fail") {
							alert("\u60a8\u5df2\u7ecf\u53c2\u4e0e\u8fc7\u8bc4\u4ef7\uff0c\u65e0\u9700\u91cd\u590d\u64cd\u4f5c\uff01");
						} else {
							if (num != null) {
								num.innerHTML = parseInt(num.innerHTML)
										+ parseInt(1);
							}
						}
						obj.setAttribute("class", obj.getAttribute("class")
								+ "Dis");
						obj.disabled = true;
					}
				});
	}

	return {
		version : "1.0",
		doSupport : doSupport
	};
})();

AliMobile.WikiSubCate = (function() {
	var lastId = 0;
	function showWikiSubCate(id) {
		if (id == "" || id == null) {
			return;
		}
		
		if (lastId != id) {
			var lastSub = document.getElementById(lastId + "sub");
			var lastArrow = document.getElementById(lastId + "arrow");
			var lastPare = document.getElementById(lastId + "pare");
			if (lastSub != null) {
				lastSub.style.display = "none";
				lastArrow.setAttribute("class", "cate-down");
				lastPare.setAttribute("class", "cate-title");
			}
		}

		var sub = document.getElementById(id + "sub");
		var arrow = document.getElementById(id + "arrow");
		var pare = document.getElementById(id + "pare");

		if (sub != null) {
			lastId = id;
			if (sub.getAttribute("isopen") == "1") {
				sub.style.display = "block";
				sub.setAttribute("isopen", "0");
			} else {
				var ajaxurl = "/ajaxSubCate/?categoryId=" + id;
				jQuery.ajax({
					url : ajaxurl,
					type : "GET",
					dataType : "html",
					error : function() {
						return false
					},
					success : function(html) {
						sub.innerHTML = html;
						arrow.setAttribute("class", "cate-up");
						sub.setAttribute("isopen", "1");
					}
				});
			}
			pare.setAttribute("class", "cate-title-now");
		}
	}

	return {
		version : "1.0",
		showWikiSubCate : showWikiSubCate
	};
})();

AliMobile.WikiSearch = (function() {
	function submitFrm() {
		if (chkNull()) {
			document.getElementById('wikiSearchFrm').submit();
		}
	}

	function showClear() {
		var wikik = document.getElementById("wikik");
		var wikic = document.getElementById("wikiClear");

		if (wikik.value != "") {
			wikic.style.display = "block";
		} else {
			wikic.style.display = "none";
		}
	}

	function clearData() {
		document.getElementById('wikik').value = '';
		document.getElementById("wikiClear").style.display = "none";
	}

	function chkNull() {
		if (document.getElementById('wikik').value == '') {
			alert("\u8bf7\u8f93\u5165\u641c\u7d22\u5173\u952e\u5b57");
			return false;
		} else {
			return true;
		}
	}

	return {
		version : "1.0",
		submitFrm : submitFrm,
		showClear : showClear,
		clearData : clearData
	};
})();

AliMobile.NewsPicsIndex = (function() {
	var built = function(id) {
		var eles = jQuery(id + " ul.ajaxTab");
		eles.each(function(i, ele) {
			var ele = jQuery(ele);
			var toEle;
			if (id == "#newsIndex") {
				toEle = jQuery(id + " ul.ajaxTabUl").get(i);
			} else if (id == "#picsSummary") {
				toEle = jQuery(id + " div.ajaxTabUl").get(i);
			}
			var lis = ele.find("li");
			lis.each(function(j, it) {
				var li = jQuery(it);
				li.bind("click", function() {
					var da = eval("(" + li.attr("data") + ")");
					switchClass(ele, li);
					startAjax(toEle, id, da);
				});
			});
		});
	};
	built("#newsIndex");
	built("#picsSummary");

	var switchClass = function(ele, li) {
		var lis = ele.find("li");
		lis.each(function(i, it) {
			var li = jQuery(it);
			li.removeClass("chk");
		});
		li.addClass("chk");
	};

	var startAjax = function(toEleT, id, da) {
		jQuery.ajax({
			type : "GET",
			url : da.url,
			dataType : "json",
			beforeSend : function() {
				var toEle = jQuery(toEleT);
				toEle.html('<p class="ac f16 m15">loading...</p>');
			},
			success : function(o) {
				insertUl(toEleT, id, o);
			}
		});
	};

	var insertUl = function(toEleT, id, o) {
		var toEle = jQuery(toEleT);
		toEle.html('');
		var html = '';
		if (id == "#newsIndex") {
			jQuery.each(o, function(index, it) {
				html += '<li><a href="' + it.url + '"><div class="desc">'
						+ it.title + '</div></a></li>';
			});
		} else if (id == "#picsSummary") {
			var i = 0;
			var lis = '';
			var descDiv = '';
			jQuery.each(o, function(index, it) {
				if (index < o.length - 1) {
					lis += '<li><a href="' + it.url + '"><div class="desc">'
							+ it.title + '</div></a></li>';
				} else {
					descDiv = '<div class="more"><a href="' + it.url
							+ '"><div class="morebtn">' + it.title
							+ '</div></a></div>';
				}
				i++;
			});
			html = '<ul class="picsList2">' + lis + '</ul>' + descDiv;
		}
		toEle.html(html);
	};

	return {
		version : "1.0"
	}
})();

AliMobile.GetMore = (function() {

	var getMore = function() {
		var obj = jQuery("#moreButton");
		var more = jQuery("#moreDiv");
		var pageName = obj.attr("pageName");
		var url = obj.attr("url");
		var pageIndex = obj.attr("pageIndex");

		if (pageName == "clubSummary" && parseInt(pageIndex) >= 3) {
			return;
		}

		if (more != null) {
			obj.html("\u6b63\u5728\u52a0\u8f7d...");

			if (obj.attr("type") != "app") {
				jQuery("#moreTable").attr("class", "moreTable-loading");
				jQuery("#moreLeft").attr("class", "moreLeft-loading");
				jQuery("#moreRight").attr("class", "moreRight-loading");
				jQuery("#moreButton").attr("class", "moreButton-loading");
			} else {
				jQuery("#moreButton").attr("class", "more-app-loading");
			}

			var ajaxUrl = url + "beginPage=" + (parseInt(pageIndex) + 1);
			jQuery.ajax({
				url : ajaxUrl,
				type : "GET",
				dataType : "html",
				error : function() {
					return false
				},
				success : function(html) {
					if (jQuery.trim(html) == "") {
						jQuery("#moreTable").css("display", "none");
					} else if (obj.attr("type") == "app") {
						jQuery("#moreButton").attr("class", "more-app");
						jQuery("#moreDiv").html(
								jQuery("#moreDiv").html() + html);
						obj.html("\u66f4\u591a...");
						jQuery("#moreButton").attr("pageIndex", parseInt(pageIndex) + 1);
					} else {
						jQuery("#moreDiv").html(jQuery("#moreDiv").html() + html);
						obj.html("\u66f4\u591a...");
						jQuery("#moreTable").attr("class", "moreTable");
						jQuery("#moreLeft").attr("class", "moreLeft");
						jQuery("#moreRight").attr("class", "moreRight");
						jQuery("#moreButton").attr("class", "moreButton");
						jQuery("#moreButton").attr("pageIndex",
								parseInt(pageIndex) + 1);
					}
				}
			});
		}

		if (pageName == "clubSummary" && parseInt(pageIndex) == 1) {
			jQuery("#moreTable").css("display", "none");
		}
	};

	return {
		version : "1.0",
		getMore : getMore
	};
})();
