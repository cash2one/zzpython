(function(w) {
	// 空函数
	function shield() {
		return false;
	}
	document.addEventListener('touchstart', shield, false); //取消浏览器的所有事件，使得active的样式在手机上正常生效
	document.oncontextmenu = shield; //屏蔽选择函数
	// H5 plus事件处理
	var ws = null,
		at = 100;

	function plusReady() {
		ws = plus.webview.currentWebview();
		// Android处理返回键
		plus.key.addEventListener('backbutton', function() {
			//if(confirm('确认退出1？')){
			//plus.navigator.closeSplashscreen();
			//plus.runtime.quit();
			//back();
			//}
		}, false);
		compatibleAdjust();
	}
	if (w.plus) {
		plusReady();
	} else {
		document.addEventListener('plusready', plusReady, false);
	}
	// DOMContentLoaded事件处理
	var domready = false;
	document.addEventListener('DOMContentLoaded', function() {
		domready = true;
		gInit();
		document.body.onselectstart = shield;
		compatibleAdjust();
	}, false);
	// 处理返回事件
	w.back = function(hide) {
		if (w.plus) {
			ws || (ws = plus.webview.currentWebview());
			if (hide || ws.preate) {
				ws.hide('auto', at);
			} else {
				ws.close();
			}
		} else if (history.length > 1) {
			history.back();
		} else {
			w.close();
		}
	};
	// 处理点击事件
	var openw = null,
		waiting = null;
	/**
	 * 打开新窗口
	 * @param {URIString} id : 要打开页面url
	 * @param {boolean} wa : 是否显示等待框
	 * @param {boolean} ns : 是否不自动显示
	 */
	w.clicked = function(id, wa, ns) {
		if (openw) { //避免多次打开同一个页面
			return;
		}
		if (w.plus) {
			wa && (waiting = plus.nativeUI.showWaiting());
			var pre = ''; //'http://192.168.1.178:8080/h5/';
			openw = plus.webview.create(pre + id, id, {
				scrollIndicator: 'none',
				scalable: false
			});
			ns || openw.addEventListener('loaded', function() { //页面加载完成后才显示
				setTimeout(function() { //延后显示避免低端机上闪屏
					openw.show('slide-in-right', at);
					closeWaiting();
				}, 500);
			}, false);
			openw.addEventListener('close', function() { //页面关闭后可再次打开
				openw = null;
			}, false);
		} else {
			w.open(id);
		}
	};
	/**
	 * 关闭等待框
	 */
	w.closeWaiting = function() {
			waiting && waiting.close();
			waiting = null;
		}
		// 兼容性样式调整
	var adjust = false;

	function compatibleAdjust() {
		if (adjust || !w.plus || !domready) {
			return;
		}
		// iOS平台使用滚动的div
		if ("iOS" == plus.os.name) {
			at = 300;
			var t = document.getElementById("dcontent");
			t && (t.className = "sdcontent");
			t = document.getElementById("content");
			t && (t.className = "scontent");
		}
		adjust = true;
	};
	// 通用元素对象
	var _dout_ = null,
		_dcontent_ = null;
	w.gInit = function() {
		_dout_ = document.getElementById("output");
		_dcontent_ = document.getElementById("dcontent");
	};
	// 清空输出内容
	w.outClean = function() {
		_dout_.innerHTML = "";
	};
	// 输出内容
	w.outSet = function(s) {
		_dout_.innerHTML = s + "<br/>";
		_dout_.scrollTop = 0;
	};
	// 输出行内容
	w.outLine = function(s) {
		_dout_.innerHTML += s + "<br/>";
	};
	// 格式化时长字符串，格式为"HH:MM:SS"
	w.timeToStr = function(ts) {
		if (isNaN(ts)) {
			return "--:--:--";
		}
		var h = parseInt(ts / 3600);
		var m = parseInt((ts % 3600) / 60);
		var s = parseInt(ts % 60);
		return (ultZeroize(h) + ":" + ultZeroize(m) + ":" + ultZeroize(s));
	};
	// 格式化日期时间字符串，格式为"YYYY-MM-DD HH:MM:SS"
	w.dateToStr = function(d) {
		return (d.getFullYear() + "-" + ultZeroize(d.getMonth() + 1) + "-" + ultZeroize(d.getDate()) + " " + ultZeroize(d.getHours()) + ":" + ultZeroize(d.getMinutes()) + ":" + ultZeroize(d.getSeconds()));
	};
	/**
	 * zeroize value with length(default is 2).
	 * @param {Object} v
	 * @param {Number} l
	 * @return {String}
	 */
	w.ultZeroize = function(v, l) {
		var z = "";
		l = l || 2;
		v = String(v);
		for (var i = 0; i < l - v.length; i++) {
			z += "0";
		}
		return z + v;
	};
})(window);
//下载新的app
function downloadnewapp() {
	plus.runtime.launchApplication({
		pname: "com.zz91.app2",
		extra: {
			url: "http://m.zz91.com"
		}
	}, function(e) {
		$("#mainbody").html("<div class=midload>ZZ91再生网app已全新改版</div>");
		$(".mui-bar").css("display","none");
		plus.ui.confirm("ZZ91再生网app已全新改版，请更新最新版。", function(i) {
			if (0 == i.index) {
				var appUrl = zzweburl + "/app/zz91-1.3.0.apk?" + (new Date()).getTime().toString();
				//mui.toast('下载新版应用中...');
				showdowninfo();
				
				var options = {
					method: "GET",
					filename: "_downloads/zz91-1.3.0.apk",
				};
				showdowninfo();
				var url = "_downloads/zz91-1.3.0.apk";       // 这个url是你的文件路径，文件路径怎么获取就不用多说了吧
				plus.io.resolveLocalFileSystemURL(url, function( entry ) {
				    entry.remove( function ( e ) {
				        console.log( "删除成功" );
				    }, function ( e ) {
				        console.log( "删除失败" );
				    });
				});
				var dtask = plus.downloader.createDownload(appUrl, options);
				dtask.addEventListener("statechanged", function(task, status) {
					showdowninfopercent((parseInt(task.downloadedSize/ 1024) / 1000).toString())
					if ( task.state == 4) {
						// 下载完成 
						$(".hint").remove();
						plus.downloader.clear();
						plus.runtime.openFile("_downloads/zz91-1.3.0.apk", {}, function(e) {
							plus.nativeUI.alert("升级失败：" + e.emssage);
						});
						plus.runtime.quit();
					}  
				});
				dtask.start();
				
			} else {
				return false;
			}
			
		}, "提示", ["立即更新", "取　　消"]);

	});
}
//下载提示框
function showdowninfo() {
	var ts = "正在下载应用...";
	$(".hint").remove()
	var hintHtml = '<div class="hint" style="position:fixed;color:#fff;line-height:18px;font-size:14px;width:100%">' + '<span style="display:block;margin:0 8px;background:#000;opacity:0.8;border-radius:5px;padding:10px 10px;text-align:center" id="downloadstate">' + ts + '<span>' + '</div>';
	$("body").append(hintHtml);
	$(".hint").css("bottom", "80px");
}

function showdowninfopercent(percent) {
	$("#downloadstate").html("正在下载应用 已下载" + percent + "M");
	if (percent == 100) {
		$(".hint").remove()
	}
}
mui.plusReady(function() {
	downloadnewapp()
})