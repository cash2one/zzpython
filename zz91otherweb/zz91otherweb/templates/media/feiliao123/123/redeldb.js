$(function() {
	$(".delectdata").click(function(e) {
		var deldataid = $(this).attr('deldataid');
		//alert(deldataid)
		$('#deldataid').val(deldataid)
		if(confirm("是否确认删除")) {
			//alert(qianbaoid)
			$('#isdel').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		} else {
			return false;
		}
	});
});
$(function() {
	$("#yzma").click(function() {
		var yzmatxt = $('#yzmatxt').val()
		var deldataid = $('#deldataid').val()
		var deldbname = $('#deldbname').val()
			//alert(yzmatxt)
		$.ajax({
			type: "GET",
			url: "delqbyzm.html",
			data: "yzmatxt=" + yzmatxt,
			success: function(data) {
				//alert(data);
				if(data == '1') {
					window.location.href = "redelqb.html?deldataid=" + deldataid + "&yzmatxt=" + yzmatxt + "&deldbname=" + deldbname;
					//alert('成功!')
				} else {
					alert('密码错误!')
				}
			},
			error: function(data) {
				//alert("错误!青重试.");
			}
		});
	});
});

function dismiss() {
	$('#isdel').trigger('close');
}