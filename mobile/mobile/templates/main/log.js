function loadjavascript(url, d, t) {
	var r = d.createElement(t),
		s = d.getElementsByTagName(t)[0];
	r.async = false;
	r.src = url + '?' + (new Date()).getTime().toString();
	s.parentNode.insertBefore(r, s);
}
loadjavascript("http://img0.zz91.com/lib/jquery/jquery-1.6.2.min.js", document, "script");
loadjavascript("http://img0.zz91.com/lib/jquery/jquery.cookie.js", document, "script");
var ajaxurl="http://www.zz91.com/getLoginStatus.htm";
var companyId;
$.getScript(ajaxurl, function() {
	if (companyId){
		var userid=companyId;
	}else{
		userid=0;
	}
	var title=$(document).attr("title");
	var url= window.location.href
	var myDate=new Date();
	var mytime=myDate.toString();
	var equip=navigator.platform;
	var preurl=document.referrer
	
	var posturl="http://pyapp.zz91.com/log/saveloginfo.html?userid="+userid+"&title="+title+"&url="+url+"&mytime="+mytime+"&equip="+equip+"&preurl="+preurl   
	$.getScript(posturl, function() {
		
	});
})