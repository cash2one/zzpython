$(".ptop").hide();
$(".ptop").find("font").html("免费开通流量宝，送<font color='#FFFF00'>88</font>元流量钱包。 ")
$(".ptop").find(".aui-ellipsis-1").hide()
//保存错误日志信息
function saveerrlog(content) {
	//return;
	var data = {
		content : content,
	}
	api.hideProgress();
}
function zz91adopen(){
	openwindows("noorder",hosturl+"app/html/ad/hongbao/gg.html");
	$(".opensmallad").remove();
}
//缩小到小广告
function closetosmallad(){
	$(".opensmallad").remove();
	var hintHtml = '<div class="opensmallad" onclick="zz91adopen()" style="position:fixed;bottom:80px;right:0px;line-height:25px;font-size:12px;width:50px;height:50px;border-radius:50%;text-align:center;z-index:999999;background-color:#ff0000"><span style="text-align:center;color:#fff;margin-top:8px;line-height:16px;"><i class="aui-iconfont aui-icon-redpacket"></i><br />红包</span></div>';
	$(".hotnews").append(hintHtml);
}