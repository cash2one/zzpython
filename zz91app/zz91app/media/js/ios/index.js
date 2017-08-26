var netconect=reloadiosapp();
if (netconect==true){
	loadfirsthtml();
}
plus.push.addEventListener("click", function(msg) {
	if (msgchickurl==""){
		gotourl(msg.payload,"messages");
		msgchickurl=msg.payload;
	}
	if (msg.payload!=msgchickurl){
		msgchickurl="";
	}
}, false);
// 监听在线消息事件
plus.push.addEventListener("receive", function(msg) {
	if (msg.aps) { // Apple APNS message

	} else {

	}
}, false);