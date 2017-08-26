(function($) {
	//全局配置(通常所有页面引用该配置，特殊页面使用mui.init({})来覆盖全局配置)
	$.initGlobal({
		optimize: true,
		swipeBack: true,
		showAfterLoad: true,
		titleBar: false,
		back: function() {
			//			return {
			//				preload : true//TODO 默认启用预加载等show，hide事件，动画都完成后放开预加载
			//			}
		},
		show: {
			aniShow: 'slide-in-right',
			duration: 400
		}
	});
	/**
	 * hyperlink
	 */
	$.ready(function() {
		$('body').on('tap', 'a', function(e) {
			var id = this.getAttribute('href');
			if (id && ~id.indexOf('.html')) {
				if (window.plus) {
					//alert(1);
					$.openWindow({
						id: id,
						url: this.href,
						preload: true //TODO 等show，hide事件，动画都完成后放开预加载
					});
				} else {
					document.location.href = this.href;
				}
			}
		});
	});
})(mui);

/**
 * toggle
 */
window.addEventListener('toggle', function(event) {
	if (event.target.id === 'M_Toggle') {
		var isActive = event.detail.isActive;
		var table = document.querySelector('.mui-table-view');
		var card = document.querySelector('.mui-card');
		if (isActive) {
			card.appendChild(table);
			card.style.display = '';
		} else {
			var content = document.querySelector('.mui-content');
			content.insertBefore(table, card);
			card.style.display = 'none';
		}
	}
});
//简单处理label点击触发radio或checkbox
window.addEventListener('tap', function(event) {
	var target = event.target;
	for (; target && target !== document; target = target.parentNode) {
		if (target.tagName && target.tagName === 'LABEL') {
			var parent = target.parentNode;
			if (parent.classList && (parent.classList.contains('mui-radio') || parent.classList.contains('mui-checkbox'))) {
				var input = parent.querySelector('input');
				if (input) {
					input.click();
				}
			}
		}
	}
});
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