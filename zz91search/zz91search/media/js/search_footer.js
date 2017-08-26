function zz91newsearch(frm) {
    var type = frm.TopSeaType.value;
    var searcfrm = frm.search
    if (searcfrm) {
        var searchvalue = searcfrm.value
    } else {
        var searcbutton = frm.search_text
        if (searcbutton) {
            var searchvalue = searcbutton.value
        }
    }
    if (searchvalue == "" || searchvalue == "请输入内容") {
        alert("请输入搜索关键字！");
		return false
    }
    if (searchvalue != "") {
        searchvalue = searchvalue.replace(/\//gm, "astoxg");
        searchvalue = searchvalue.replace(/\%/gm, "astoxf");
        searchvalue = searchvalue.replace(/\\/gm, "astoxl");
        searchvalue = searchvalue.replace(/-/gm, "astohg");
        searchvalue = searchvalue.replace(/\(/gm, "astokhl");
        searchvalue = searchvalue.replace(/\)/gm, "astokhr");
        searchvalue = encodeURI(searchvalue)
    }
    if (type == "1") {
        frm.action = "http://trade.zz91.com/offerlist--a1--p--" + searchvalue + ".htm";
        frm.target = "_blank"
    }
    if (type == "2") {
        frm.action = "http://trade.zz91.com/offerlist--a2--p--" + searchvalue + ".htm";
        frm.target = "_blank"
    }
    if (type == "3") {
        frm.action = "http://price.zz91.com/priceSearch.htm?title=" + searchvalue + "";
        frm.target = "_blank"
    }
    if (type == "5") {
        frm.action = "http://www.zz91.com/photo/searchPic.htm?searchKey=" + searchvalue + "";
        frm.target = "_blank"
    }
    if (type == "4") {
        frm.action = "http://company.zz91.com/index-p-" + searchvalue + ".htm";
        frm.target = "_blank"
    }
    if (type == "6") {
        frm.action = "http://xianhuo.zz91.com/spot.htm?title=" + searchvalue + "";
        frm.target = "_blank"
    }
}
$(document).ready(function() {
    var ii = 0;
    $("#searchForm1_footer #TopKeywords_footer").keyup(function(event) {
        var thisval = $(this).val();
        var ajaxurl = "http://pyapp.zz91.com/keywordsearch/?keywords=" + thisval;
        $.getScript(ajaxurl,
        function() {
            if (event.keyCode != 40 && event.keyCode != 38) {
                var result = _suggest_result_.result;
                var myobj = eval('(' + result + ')');
                var value = "<ul>"
                for (var i = 0; i < myobj.length - 1; i++) {
                    value += "<li>" + myobj[i].keyword + "</li>"
                }
                value += "</ul>";
                $("#searchresult_footer").css({
                    'position': 'absolute',
                    'width': ($("#TopKeywords_footer").width() + 10).toString() + 'px',
                    'height': (myobj.length * 24 + 20).toString() + 'px',
                    'display': '',
                    'z-index': '800'
                });
                $("#searchresult_footer").html(value);
                ii = 0
            }
            $("#searchresult_footer li").mouseover(function() {
                $(this).css("background", "#f2f2f2")
            });
            $("#searchresult_footer li").click(function() {
                $("#searchresult_footer").css("display", "none");
				$("#TopKeywords_footer").val($(this).html())
            });
            $("#searchresult_footer li").mouseout(function() {
                $(this).css("background", "#fff")
            });
            if (event.keyCode == 40 || event.keyCode == 38) {
                var searchdroplist = $("#searchresult_footer li");
                if (event.keyCode == 38) {
                    ii -= 1
                } else {
                    ii += 1
                }
                if (ii <= 0) {
                    ii = 1
                }
                if (ii > searchdroplist.length) {
                    ii = searchdroplist.length
                }
                $("#TopKeywords_footer").val($(searchdroplist[ii - 1]).html());
                $("#searchresult_footer li").css("background", "#fff");
                $(searchdroplist[ii - 1]).css("background", "#f2f2f2");
                return false
            }
        });
        $("body").click(function() {
            $("#searchresult_footer").css("display", "none")
        })
    });
    $(".search_bar li").click(function() {
        var no = $(this).attr("value");
        $("#TopSeaType_footer").val(no);
        var self = $(this);
        var searchbartxt = $(".search_bar li");
        var TopKeywords = $("#TopKeywords_footer");
        searchbartxt.removeClass("searchnav_on");
        $(this).addClass("searchnav_on");
        var txt = ""
        for (var p = 0; p <= searchbartxt.length - 1; p++) {
            txt += $(searchbartxt[p]).attr("s-data")
        }
        var alertvalue = $("#TopKeywords_footer").val();
        if (txt.indexOf(alertvalue) >= 0 || TopKeywords.val() == "") {
            TopKeywords.val(self.attr("s-data"));
            TopKeywords.css("color", "#999")
        }
    });
    $("#TopKeywords_footer").click(function() {
        var self = $(this);
        var searchbartxt = $(".search_bar li");
        var TopKeywords = $("#TopKeywords_footer");
        var txt = ""
        for (var p = 0; p <= searchbartxt.length - 1; p++) {
            txt += $(searchbartxt[p]).attr("s-data")
        }
        if (txt.indexOf(self.val()) >= 0 || TopKeywords.val() == "") {
            TopKeywords.val("");
            TopKeywords.css("color", "#000")
        }
    });
    $("#TopKeywords_footer").blur(function() {
        var searchbartxt = $(".search_bar li");
        var TopKeywords = $("#TopKeywords_footer");
        var nowtxt = $(searchbartxt[$("#TopSeaType_footer").val() - 1]).attr("s-data");
        var alertvalue = $("#TopKeywords_footer").val();
        var txt = ""
        for (var p = 0; p <= searchbartxt.length - 1; p++) {
            txt += $(searchbartxt[p]).attr("s-data")
        }
        if (txt.indexOf(TopKeywords.val) >= 0 || TopKeywords.val() == "") {
            TopKeywords.val(nowtxt);
            TopKeywords.css("color", "#999")
        }
    });
    $("#search_a1_footer").click(function() {
        zz91searchindex(document.getElementById("searchForm1"), 1)
    })
});
function zz91searchindex(frm, s) {
    var type = $("#TopSeaType_footer").val();
    var searchbartxt = $(".search_bar li");
    var TopKeywords = $("#TopKeywords_footer");
    var searchvalue = encodeURI(TopKeywords.val());
    var nowtxt = $(searchbartxt[$("#TopSeaType_footer").val() - 1]).attr("s-data");
    var alertvalue = $("#TopKeywords_footer").val();
    var txt = ""
    for (var p = 0; p <= searchbartxt.length - 1; p++) {
        txt += $(searchbartxt[p]).attr("s-data")
    }
    if (txt.indexOf(TopKeywords.val) >= 0 || TopKeywords.val() == "") {
        TopKeywords.val(nowtxt);
        TopKeywords.css("color", "#999");
        return false
    }
    if (type == "1") {
        frm.action = "http://s.zz91.com/trade/searchfirst/?keywords=" + searchvalue + "";
        frm.target = "_blank"
    }
    if (type == "2") {
        frm.action = "http://s.zz91.com/trade/searchfirst/?keywords=" + searchvalue + "&ptype=2";
        frm.target = "_blank"
    }
    if (type == "3") {
        frm.action = "http://price.zz91.com/priceSearch.htm?title=" + searchvalue + "";
        frm.target = "_blank"
    }
    if (type == "5") {
        frm.action = "http://www.zz91.com/photo/searchPic.htm?searchKey=" + searchvalue + "";
        frm.target = "_blank"
    }
    if (type == "4") {
        frm.action = "http://company.zz91.com/index-p-" + searchvalue + ".htm";
        frm.target = "_blank"
    }
    if (s == 1) {
        frm.submit()
    }
}