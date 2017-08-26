//图片上传
var server = "http://app.zz91.com/tradeimgupload.html";
var files = [];
var index = 1;
 // 上传文件
function upload(p) {
		if (index > 5) {
			alert("最多上传5张图片");
			return false;
		}
		var wt = plus.nativeUI.showWaiting();
		var task = plus.uploader.createUpload(server, {
				method: "POST"
			},
			function(t, status) { //上传完成
				if (status == 200) {
					//plus.storage.setItem("uploader",t.responseText);
					wt.close();
					//document.getElementById("mark").style.display="none";
					alert("上传成功！")
					index += 1;
					document.getElementById("imglist").innerHTML += "<img src='" + t.responseText + "' width=80 height=80>";
				} else {
					wt.close();
				}
			}
		);
		task.addData("randid", getRandid());
		task.addFile(p, {
			key: 'uploadkey'
		});
		task.start();
	}
	// 拍照添加文件

function appendByCamera() {
		plus.camera.getCamera().captureImage(function(p) {
			upload(p);
		});
	}
	// 从相册添加文件

function appendByGallery() {
		plus.gallery.pick(function(p) {
			upload(p)
		});
	}
	// 产生一个随机数

function getRandid() {
	//alert(document.getElementById("randid").value)
	return document.getElementById("randid").value;
	//return Math.floor(Math.random() * 100000000 + 10000000).toString();
}
//发布供求弹窗选择
function getselectvalue(obj){
	var selectname=obj.parentNode.title;
	document.getElementById(selectname).value=obj.title;
	closeoverlay();
}
function getpricevalue(obj){
	var selectname=obj.parentNode.title;
	var pricevalue=obj.parentNode.childNodes[1].value;
	//alert(pricevalue)
	document.getElementById(selectname).value=pricevalue;
	closeoverlay();
}
//关闭窗口
function closewindow(){
	closeoverlay()
	var ws = plus.webview.currentWebview();
	ws.close();
}