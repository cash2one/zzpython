function myfun()
{
//alert(window.location.href);
var weburl=window.location.href;

$.ajax({
   type: "get",
   url: "/addrecordeddata/",
   data: "weburl="+weburl,
}); 
//window.location.href="/addrecordeddata/?weburl="+weburl
}
window.onload=myfun;
