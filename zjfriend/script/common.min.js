function GetComments(n) {
	var t = $("#hiddenType").val();
	t == 2 && n > 1 || ($("#more_comments").show(), $.ajax({
		type : "POST",
		url : "/comment/commentsjson.ashx",
		data : {
			tid : $("#hiddenTid").val(),
			type : t,
			page : n,
			orderby : commentorderby
		},
		dataType : "text",
		timeout : 1e4,
		success : function(data) {
			var review = eval("(" + data + ")"), result = TrimPath.processDOMTemplate("_mycomments_", review), myTemplateObj = TrimPath.parseDOMTemplate("_mycomments_"), result = myTemplateObj.process(review), ReviewCount;
			n > 1 ? $("#MyComments").append(result) : $("#MyComments").html(result);
			$("#fixed").hide();
			ReviewCount = review.Count[0].ReviewCount;
			$("#span_reviewcount,#div_reviewcount").html(ReviewCount);
			ReviewCount == 0 ? (t == 3 ? $("#MyComments").html('<div style="color:red;text-align:center;">还没有你的评论，赶紧来吧<\/div>') : $("#MyComments").html('<div style="color:red;text-align:center;">还没有评论，赶快来抢沙发吧<\/div>'), stoploading = !0, $("#more_comments").hide()) : (review.All.length < 20 && ( stoploading = !0, $("#more_comments").hide()), t == 2 && $("#more_comments").hide())
		},
		error : function() {
		}
	}))
}

function GetNewsViewComments(n) {
	$("#fixed").show();
	var t = $("#hiddenType").val();
	$.ajax({
		type : "POST",
		url : "/comment/commentsjson.ashx",
		data : {
			tid : $("#hiddenTid").val(),
			type : t,
			page : n,
			pagesize : 10
		},
		dataType : "text",
		timeout : 1e4,
		success : function(data) {
			var review = eval("(" + data + ")"), result = TrimPath.processDOMTemplate("_mycomments_", review), myTemplateObj = TrimPath.parseDOMTemplate("_mycomments_"), result = myTemplateObj.process(review), ReviewCount;
			$("#MyComments").html(result);
			$("#fixed").hide();
			ReviewCount = review.Count[0].ReviewCount;
			$("#span_reviewcount,#div_reviewcount").html(ReviewCount);
			ReviewCount == 0 && (t == 3 ? $("#MyComments").html('<div style="color:red;text-align:center;">还没有你的评论，赶紧来吧<\/div>') : $("#MyComments").html('<div style="color:red;text-align:center;">还没有评论，赶快来抢沙发吧<\/div>'))
		},
		error : function() {
		}
	})
}

function setAPPLink() {
	$("span").each(function() {
		$(this).hasClass("dev") && ($(this).html().indexOf("Android") > 0 || $(this).hasClass("android") ? $(this).html("<a class='from' target='_blank' href='http://app.mydrivers.com/download/kkeji-m.apk'>" + $(this).html() + "<\/a>") : ($(this).html().indexOf("iPhone") > 0 || $(this).hasClass("iphone") || $(this).hasClass("ios")) && $(this).html("<a class='from' target='_blank' href='https://itunes.apple.com/cn/app/qu-jia-xin-wen/id796040119?mt=8'>" + $(this).html() + "<\/a>"))
	})
}

function GetMyComments(n) {
	$("#fixed").show();
	$.ajax({
		type : "POST",
		url : "/comment/mycommentsjson.ashx",
		data : {
			type : $("#hiddenType").val(),
			page : n
		},
		dataType : "text",
		timeout : 1e4,
		success : function(n) {
			var t = n.split("wwgmydrivers||");
			t.length == 2 && ($("#MyComments").html(t[0]), $("#fixed").hide())
		},
		error : function() {
		}
	})
}

function PostComment(n) {
	var r = getCookie("mydrivers_userid"), o = getCookie("mydrivers_usernumid"), i;
	if (r == null || r == "") {
		ShowAjaxTip("CommentsTip" + n, "不允许匿名评论！", "AjaxTipWarning");
		return
	}
	var t = "", u = $("#txtContent" + n).val(), f = $("#hiddenTid").val(), e = 0;
	if (u.length < 1) {
		ShowAjaxTip("CommentsTip" + n, "评论内容不得少于1个字符！", "AjaxTipWarning");
		$("#txtContent" + n).focus();
		return
	}
	i = getCookie("mydrivers_userid");
	i != null && i != "" && ( e = 1);
	$.ajax({
		type : "POST",
		url : "/comment/post.ashx",
		data : {
			cid : 1,
			tid : f,
			rid : n,
			content : Replace(u),
			usertype : e
		},
		success : function(i) {
			switch(i) {
				case"0":
					t = "您要评论的主题不存在";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"1":
					t = "验证码不正确";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"2":
					t = "15秒内不允许再次评论";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"4":
					t = "评论内容不得少于 5 字多于 1000 字";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"5":
					t = "发送评论成功.";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipComplete");
					$("#txtContent" + n).val("");
					$("#hiddenPage").val() == "newsview" ? window.location.href = "/comment/review.aspx?tid=" + f : GetComments(1);
					break;
				case"6":
					t = "您的评论中含有被系统禁止的内容，请修改后再发表";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"7":
					t = "页面超时请刷新页面后再发表";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"9":
					t = "暂时不允许发表评论";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"10":
					t = "您的IP地址被屏蔽，请联系管理员";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"12":
					t = "找不到验证码";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"13":
					t = "60天以前的新闻评论被禁止,感谢您对本网站的支持";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"14":
					t = "此新闻不允许发表评论,感谢您对本网站的支持";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"15":
					t = "此新闻不允许匿名用户发表评论,感谢您对本网站的支持";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"16":
					t = "此新闻的评论内容不允许重复,感谢您对本网站的支持";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				case"17":
					t = "用户不存在，请重新登录重试";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning");
					break;
				default:
					t = "未知错误";
					ShowAjaxTip("CommentsTip" + n, t, "AjaxTipWarning")
			}
		},
		complete : function() {
		},
		error : function() {
			ShowAjaxTip("CommentsTip" + n, "出错误了，请稍后重试！", "AjaxTipWarning")
		}
	})
}

function GetRelatedNews(n, t) {
	$.ajax({
		type : "GET",
		url : "/m/relatednews.ashx",
		data : {
			q : t,
			tid : n
		},
		dataType : "text",
		timeout : 1e4,
		success : function(n) {
			$("#ul_relatednews").html(n)
		},
		error : function() {
		}
	})
}

function changetab(n, t) {
	if ($("#fixed").show(), stoploading = !1, page = 1, $("#li_comments1").removeClass("act"), $("#li_comments2").removeClass("act"), $("#li_comments3").removeClass("act"), $("#li_comments" + n).addClass("act"), $("#hiddenType").val(n), $("#a_allreviews").attr("href", "/comment/review.aspx?tid=" + t + "&type=" + n), n == 3) {
		$("#div_seeall").html("查看所有我的评论");
		var i = getCookie("mydrivers_userid"), r = getCookie("mydrivers_usernumid");
		i != null && i != "" ? $("#a_allreviews").attr("href", "/comment/myreview.aspx") : window.location.href = "/login.aspx?ReturnUrl=" + window.location.href + "&t=2"
	} else
		$("#div_seeall").html('查看所有<span id="span_reviewcount">0<\/span>条评论');
	n == 2 && $("#more_comments").hide();
	GetComments(1)
}

function seeallreviews(n) {
	var t = $("#hiddenType").val(), i = getCookie("mydrivers_userid"), r = "/comment/review.aspx?tid=" + n + "&type=" + t;
	t == 3 && ( r = i == null || i == "" ? "/login.aspx?ReturnUrl=" + window.location.href + "&t=2" : "/comment/myreview.aspx");
	window.location.href = r
}

function weibologin(n, t) {
	n == "qq" ? window.location.href = "http://passport.mydrivers.com/qq/qqlogin.aspx?reurl=" + t : n == "sina" && (window.location.href = "http://passport.mydrivers.com/weibo/sinaweibo.aspx?reurl=" + t)
}

function sndReq(n, t, i, r) {
	i == "support" ? $("#s_" + t).html("支持[" + (parseInt(r) + 1) + "]") : $("#o_" + t).html("反对[" + (parseInt(r) + 1) + "]");
	var u = getCookie("Vote" + n + t);
	u == null && $.ajax({
		type : "POST",
		url : "/comment/vote.ashx",
		data : {
			act : i,
			tid : n,
			rid : t
		},
		dataType : "text",
		timeout : 1e4,
		success : function() {
			setCookie("Vote" + n + t, i)
		},
		error : function() {
		}
	})
}

function userReport(n, t) {
	($("#span_jubao_" + n).html("已举报"), getCookie("report_" + n) != "yes") && $.ajax({
		type : "POST",
		url : "/comment/usereport.ashx",
		data : {
			ID : n,
			Tid : t
		},
		dataType : "text",
		timeout : 1e4,
		success : function() {
		},
		error : function() {
		}
	})
}

function ShowReply(n) {
	var t, i, r;
	if ($("#div_reply_" + n).html().length > 0) {
		$("#div_reply_" + n).html("");
		return
	}
	t = "";
	t += '<div style="padding-top: 5px;">';
	t += '\t<div class="plun_input"><a name="post0"><\/a>';
	i = getCookie("mydrivers_userid");
	r = getCookie("mydrivers_usernumid");
	t += i != null && i != "" ? '<ul><li style="float:left;" class="ydl">' + decodeURI(i) + "，" + sayhi() + '<\/li><li onclick="ShowReply(' + n + ')"><a href="javascript:;">×<\/a><\/li><\/ul>' : '<ul><li style="float:left;" class="fbpl">发表评论：<\/li><li onclick="gourl(\'reg\')"><a href="javascript:;">注册<\/a><\/li><li style="color:#dcdcdc;">|<\/li><li onclick="gourl(\'login\')"><a href="javascript:;">登 录<\/a><\/li><\/ul>';
	t += "\t<\/div>";
	t += '\t<div class="plunxx_in">';
	t += i != null && i != "" ? '<div id="div_contentbg" class="write1"><p>我来说两句...<\/p><\/div>' : '<div class="write"><p>请<a onclick="gourl(\'login\')" href="javascript:;">登录<\/a>后发表评论<\/p><\/div>';
	t += '\t\t<textarea name="txtContent' + n + '" id="txtContent' + n + '" onclick="$(\'#div_contentbg\').hide();" cols="45" rows="5" class="plun_login_textarea"><\/textarea>';
	t += "\t<\/div>";
	t += '\t<div class="plun_bt_tj_button"><div style=\'float:left;width:150px;\'><div id="CommentsTip' + n + '" class="AjaxTipWarning"><\/div><\/div>';
	t += '\t\t<input type="button" name="btnlogin" id="btnlogin" value="发表评论" onclick="PostComment(' + n + ')" class="button_style1">';
	t += "\t<\/div>";
	t += "<\/div>";
	$("#div_reply_" + n).html(t)
}

function sayhi() {
	var t = new Date, n = t.getHours(), i = parseInt(n);
	return n >= 0 && n < 6 ? "凌晨好" : n >= 6 && n < 9 ? "早上好" : n >= 9 && n < 11 ? "上午好" : n >= 11 && n < 13 ? "中午好" : n >= 13 && n < 17 ? "下午好" : n >= 17 && n < 19 ? "傍晚好" : n >= 19 && n < 24 ? "晚上好" :
	void 0
}

function shoucang(n, t) {
	var i = getCookie("mydrivers_userid");
	i != null && i != "" ? $.ajax({
		type : "POST",
		url : "/shoucang.ashx",
		data : {
			tid : n,
			title : t
		},
		dataType : "text",
		timeout : 1e4,
		success : function(n) {
			n == "收藏成功" ? ($("#div_shoucang").removeAttr("class").addClass("sc2"), alert("收藏成功")) : n == "取消成功" && ($("#div_shoucang").removeAttr("class").addClass("sc"), alert("取消成功"))
		},
		error : function() {
		}
	}) : window.location.href = "/login.aspx?ReturnUrl=" + window.location.href + "&t=1"
}

function ShowAjaxTip(n, t, i) {
	$("#" + n).html('<div style="float: right"><img src="http://11.mydrivers.com/comments/images/v20130509/' + i + '.gif" style="margin: 7px 7px;cursor:pointer;" onclick="HideAxajTip(this);"><\/div><div>' + t + "<div>").removeAttr("class").addClass(i).show()
}

function HideAxajTip(n) {
	n.parentNode.parentNode.style.display = "none"
}

function gohome() {
	window.location.href = "/"
}

function GoTop() {
	window.scrollTo(0, 0)
}

function Replace(n) {
	return re = /%/g, n = n.replace(re, "％"), re = /\+/g, n.replace(re, "＋")
}

function logout() {
	var n = "http://passport.mydrivers.com/logout.aspx?ReturnUrl=" + window.location.href;
	parent.location = n
}

function gourl(n) {
	var t = "";
	n == "login" ? t = "/login.aspx?ReturnUrl=" + window.location.href : n == "reg" && ( t = "/reg.aspx?ReturnUrl=" + window.location.href);
	parent.location = t
}

function userslogin() {
	var n = $("#txtUserName").val();
	if ($("#txtUserName").val() == "")
		return alert("用户名不能为空"), $("#txtUserName").focus(), !1;
	if ($("#txtPwd").val() == "")
		return alert("密码不能为空"), $("#txtPwd").focus(), !1;
	document.charset = "gb2312";
	userlogin.action = "http://passport.mydrivers.com/comments/check_login.aspx?ReturnUrl=" + $("#hiddenReturnUrl").val()
}

function NewsAppADClose() {
	$(".newsappad").hide();
	setCookie2("newsappad", "1")
}

function getNewsAppAD() {
	var n = navigator.userAgent.toLowerCase();
	n.indexOf("ipad") > -1 || n.indexOf("iphone") > -1 || n.indexOf("ipod") > -1 ? getCookie("newsappad") == null && $("#div_iosad").show() : n.indexOf("Windows Phone") > -1 || getCookie("newsappad") == null && $("#div_androidad").show()
}

function getCookie(n) {
	var t;
	if (n && ( t = document.cookie.indexOf(n + "="), t != -1)) {
		var i = document.cookie.substring(t + n.length + 1, document.cookie.length), r = i.split(";");
		return r[0]
	}
}

function setCookie(n, t) {
	var i = new Date;
	i.setTime(i.getTime() + 2592e6);
	document.cookie = n + "=" + escape(t) + ";expires=" + i.toGMTString()
}

function setCookie2(n, t) {
	var i = new Date;
	i.setTime(i.getTime() + 18e5);
	document.cookie = n + "=" + escape(t) + ";expires=" + i.toGMTString()
}

function setFontSize(n) {
	n == 22 ? ($("#content").addClass("big").removeClass("small"), $("#contentFontp18").html("<a id='contentFont18' href='javascript:setFontSize(18);' class='f-small f-click'>A<\/a>"), $("#contentFontp18").addClass("f-small"), $("#contentFontp22").html("<a id='contentFont22'>A<\/a>"), $("#contentFontp22").addClass("f-big f-gray"), setCookie("fontsize", 22)) : ($("#content").addClass("small").removeClass("big"), $("#contentFontp22").html("<a id='contentFont22' href='javascript:setFontSize(22);' class='f-click'>A<\/a>"), $("#contentFontp22").addClass("f-big"), $("#contentFontp18").html("<a id='contentFont18' class='f-small'>A<\/a>"), $("#contentFontp18").addClass("f-small f-gray"), setCookie("fontsize", 18))
}

function StringBuffer() {
	this._strings_ = []
}

function getPager(n, t) {
	var i = new StringBuffer, h = "", u = 5, e = 20, o, s, f, r;
	for ( pagecount = t % e != 0 ? parseInt(t / e) + 1 : parseInt(t / e), n < 1 && ( n = 1), pagecount < 1 && ( pagecount = 1), n > pagecount && ( n = pagecount), o = n - 1, s = n + 1, o < 1 ? i.append(' <span class="sinfo">上一页<\/span>') : i.append(' <a href="javascript:GetComments(' + o + ')">上一页<\/a>'), f = n % u == 0 ? n - (u - 1) : n - parseInt(n % u) + 1, f > u && i.append('<a href="javascript:GetComments(' + (f - 1) + ')">...<\/a>'), r = f; r < f + u; r++) {
		if (r > pagecount)
			break;
		r == n ? i.append(' <span class="pagecurr" title="Page ' + r + '">' + r + "<\/span>") : i.append(' <a href="javascript:GetComments(' + r + ')">' + r + "<\/a>")
	}
	pagecount >= n + u && i.append('<a href="javascript:GetComments(' + (f + u) + ')">...<\/a>');
	s > pagecount ? i.append(' <span class="sinfo">下一页<\/span>') : i.append(' <a href="javascript:GetComments(' + s + ')">下一页<\/a>');
	i.append("<br />");
	h = i.toString();
	pagecount > 1 ? $(".postpage").html(h).show() : $(".postpage").hide()
}

function getMyPager(n, t) {
	var i = new StringBuffer, h = "", u = 5, e = 20, o, s, f, r;
	for ( pagecount = t % e != 0 ? parseInt(t / e) + 1 : parseInt(t / e), n < 1 && ( n = 1), pagecount < 1 && ( pagecount = 1), n > pagecount && ( n = pagecount), o = n - 1, s = n + 1, o < 1 ? i.append(' <span class="sinfo">上一页<\/span>') : i.append(' <a href="javascript:GetMyComments(' + o + ')">上一页<\/a>'), f = n % u == 0 ? n - (u - 1) : n - parseInt(n % u) + 1, f > u && i.append('<a href="javascript:GetMyComments(' + (f - 1) + ')">...<\/a>'), r = f; r < f + u; r++) {
		if (r > pagecount)
			break;
		r == n ? i.append(' <span class="pagecurr" title="Page ' + r + '">' + r + "<\/span>") : i.append(' <a href="javascript:GetMyComments(' + r + ')">' + r + "<\/a>")
	}
	pagecount >= n + u && i.append('<a href="javascript:GetMyComments(' + (f + u) + ')">...<\/a>');
	s > pagecount ? i.append(' <span class="sinfo">下一页<\/span>') : i.append(' <a href="javascript:GetMyComments(' + s + ')">下一页<\/a>');
	i.append("<br />");
	h = i.toString();
	pagecount > 1 ? $(".postpage").html(h).show() : $(".postpage").hide()
}! function(n) {
	"function" == typeof define && define.amd ? define(["jquery"], n) : n(window.jQuery || window.Zepto)
}(function(n) {
	function i() {
	}

	function o(n, i) {
		var u;
		return u = i._$container == t ? ("innerHeight" in r ? r.innerHeight : t.height()) + t.scrollTop() : i._$container.offset().top + i._$container.height(), u <= n.offset().top - i.threshold
	}

	function l(i, u) {
		var f;
		return f = u._$container == t ? t.width() + (n.fn.scrollLeft ? t.scrollLeft() : r.pageXOffset) : u._$container.offset().left + u._$container.width(), f <= i.offset().left - u.threshold
	}

	function s(n, i) {
		var r;
		return r = i._$container == t ? t.scrollTop() : i._$container.offset().top, r >= n.offset().top + i.threshold + n.height()
	}

	function a(i, u) {
		var f;
		return f = u._$container == t ? n.fn.scrollLeft ? t.scrollLeft() : r.pageXOffset : u._$container.offset().left, f >= i.offset().left + u.threshold + i.width()
	}

	function u(n, t) {
		var i = 0;
		n.each(function(r) {
			function f() {
				u.trigger("_lazyload_appear");
				i = 0
			}

			var u = n.eq(r);
			if (!t.skip_invisible || u.width() || u.height() || "none" === u.css("display"))
				if (t.vertical_only) {
					if (!s(u, t))
						if (o(u, t)) {
							if (++i > t.failure_limit)
								return !1
						} else
							f()
				} else if (!s(u, t) && !a(u, t))
					if (o(u, t) || l(u, t)) {
						if (++i > t.failure_limit)
							return !1
					} else
						f()
		})
	}

	function h(n) {
		return n.filter(function(t) {
			return !n.eq(t)._lazyload_loadStarted
		})
	}

	var f, r = window, t = n(r), e = {
		threshold : 0,
		failure_limit : 0,
		event : "scroll",
		effect : "show",
		effect_params : null,
		container : r,
		data_attribute : "original",
		data_srcset_attribute : "original-srcset",
		skip_invisible : !0,
		appear : i,
		load : i,
		vertical_only : !1,
		minimum_interval : 300,
		use_minimum_interval_in_ios : !1,
		url_rewriter_fn : i,
		no_fake_img_loader : !1,
		placeholder_data_img : "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC",
		placeholder_real_img : "http://ditu.baidu.cn/yyfm/lazyload/0.0.1/img/placeholder.png"
	}, c = /(?:iphone|ipod|ipad).*os/gi.test(navigator.appVersion), v = c && /(?:iphone|ipod|ipad).*os 5/gi.test(navigator.appVersion);
	f = function() {
		var n = Object.prototype.toString;
		return function(t) {
			return n.call(t).replace("[object ", "").replace("]", "")
		}
	}();
	n.fn.hasOwnProperty("lazyload") || (n.fn.lazyload = function(o) {
		var l, a, p, s = this, y = null;
		return n.isPlainObject(o) || ( o = {}), n.each(e, function(i, u) {
			-1 != n.inArray(i, ["threshold", "failure_limit", "minimum_interval"]) ? o[i] = "String" == f(o[i]) ? parseInt(o[i], 10) : u : "container" == i ? (o._$container = o.hasOwnProperty(i) ? o[i] == r || o[i] == document ? t : n(o[i]) : t,
			delete o.container) : !e.hasOwnProperty(i) || o.hasOwnProperty(i) && f(o[i]) == f(e[i]) || (o[i] = u)
		}), l = "scroll" == o.event, a = l || "scrollstart" == o.event || "scrollstop" == o.event, s.each(function(t) {
			var f = this, r = s.eq(t), c = r.attr("src"), l = r.attr("data-" + o.data_attribute), u = o.url_rewriter_fn == i ? l : o.url_rewriter_fn.call(f, r, l), e = r.attr("data-" + o.data_srcset_attribute), v = r.is("img");
			return 1 == r._lazyload_loadStarted || c == u ? (r._lazyload_loadStarted = !0, s = h(s),
			void 0) : (r._lazyload_loadStarted = !1, v && !c && r.one("error", function() {
				r.attr("src", o.placeholder_real_img)
			}).attr("src", o.placeholder_data_img), r.one("_lazyload_appear", function() {
				function c() {
					t && r.hide();
					v ? (e && r.attr("srcset", e), u && r.attr("src", u)) : r.css("background-image", 'url("' + u + '")');
					t && r[o.effect].apply(r, l ? o.effect_params : []);
					s = h(s)
				}

				var t, l = n.isArray(o.effect_params);
				r._lazyload_loadStarted || ( t = "show" != o.effect && n.fn[o.effect] && (!o.effect_params || l && 0 == o.effect_params.length), o.appear != i && o.appear.call(f, s.length, o), r._lazyload_loadStarted = !0, o.no_fake_img_loader || e ? (o.load != i && r.one("load", function() {
					o.load.call(f, s.length, o)
				}), c()) : n("<img />").one("load", function() {
					c();
					o.load != i && o.load.call(f, s.length, o)
				}).attr("src", u))
			}), a || r.on(o.event, function() {
				r._lazyload_loadStarted || r.trigger("_lazyload_appear")
			}),
			void 0)
		}), a && ( p = 0 != o.minimum_interval, o._$container.on(o.event, function() {
			return !l || !p || c && !o.use_minimum_interval_in_ios ? u(s, o) : (y || ( y = setTimeout(function() {
				u(s, o);
				y = null
			}, o.minimum_interval)),
			void 0)
		})), t.on("resize load", function() {
			u(s, o)
		}), v && t.on("pageshow", function(n) {
			n.originalEvent && n.originalEvent.persisted && s.trigger("_lazyload_appear")
		}), n(function() {
			u(s, o)
		}), this
	})
});
StringBuffer.prototype.append = function(n) {
	this._strings_.push(n)
};
StringBuffer.prototype.toString = function() {
	return this._strings_.join("")
};
$(function() {
	$(".eloginbar").click(function() {
		var n = getCookie("mydrivers_userid"), t = getCookie("mydrivers_usernumid");
		n == null && gourl("login")
	})
}); 