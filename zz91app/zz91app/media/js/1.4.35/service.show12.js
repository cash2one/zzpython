$(".pricetitle").html("价格：<span>￥ 300 / 月</span>");
$(".serverdate").find(".aui-radio-name").eq(0).html("￥300/1个月");
$(".serverdate").find(".aui-radio-name").eq(1).html("￥600/2个月");
$(".serverdate").find(".aui-radio-name").eq(2).html("￥1800/6个月");
$(".serverdate").find(".aui-radio-name").eq(3).html("￥2400/8个月");
$(".serverdate").find(".aui-radio-name").eq(4).html("￥3600/1年");
$(".serverdate").find(".aui-radio-name").eq(5).html("￥7200/2年");

$(".serverdate").find(".aui-radio").eq(0).attr("money","300");
$(".serverdate").find(".aui-radio").eq(1).attr("money","600");
$(".serverdate").find(".aui-radio").eq(2).attr("money","1800");
$(".serverdate").find(".aui-radio").eq(3).attr("money","2400");
$(".serverdate").find(".aui-radio").eq(4).attr("money","3600");
$(".serverdate").find(".aui-radio").eq(5).attr("money","7200");