(function($) {
	'use strict';
	$(function() {
		var $fullText = $('.admin-fullText');
		$('#admin-fullscreen').on('click', function() {
			$.AMUI.fullscreen.toggle();
		});

		$(document).on($.AMUI.fullscreen.raw.fullscreenchange, function() {
			$fullText.text($.AMUI.fullscreen.isFullscreen ? '退出全屏' : '开启全屏');
		});
	});
})(jQuery);

function selectOption(menuname, value) {
	var menu = document.getElementById(menuname);
	if (menu) {
		for (var i = 0; i <= menu.options.length; i++) {
			if (value) {
				if (menu.options[i].value == value) {
					menu.options[i].selected = true;
					break;
				}
			}
		}
	}
}

function selectCheckBox(boxname, thevalue) {
	if (thevalue) {
		var boxes = document.getElementsByName(boxname);
		for (var i = 0; i < boxes.length; i++) {
			if (thevalue) {
				if (thevalue.toString() == boxes[i].value.toString()) {
					boxes[i].checked = true;
				}
			}
		}
	}
}
//标题提交提示
function hint(ts) {
	$(".hint").remove()
	var hintHtml = '<div class="hint" style="position:fixed;color:#fff;line-height:18px;font-size:14px;width:100%;z-index:100000">' + '<span style="display:block;margin:0 8px;background:#000;opacity:0.8;border-radius:5px;padding:10px 10px;text-align:center">' + ts + '<span>' + '</div>';
	$("body").append(hintHtml);
	var hint_height = $(".hint").height();
	var wd_height = $(window).height();
	var top_height = (wd_height - hint_height) / 2
	$(".hint").css("top", top_height + "px");
	setTimeout(function() {
		$(".hint").fadeOut("slow", function() {
			$(".hint").remove()
		})
	}, 2000)
}