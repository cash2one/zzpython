$(function() {
	$('#stick_buy').click(function(e) {
		var proid2 = $('#proid2').val();
		$('#proid').val(proid2);
		$('#buyTipp2').lightbox_me({
			overlaySpeed: 0,
			lightboxSpeed: 0,
			centered: true,
			onLoad: function() {}
		});
		e.preventDefault();
	})
});
$(function() {
	$('#stick_buy3').click(function(e) {
		$('#contact1').lightbox_me({
			overlaySpeed: 0,
			lightboxSpeed: 0,
			centered: true,
			onLoad: function() {}
		});
		e.preventDefault();
	})
});
$(function() {
	$('#stick_buy2').click(function(e) {
		var mobile = $('#mobile').val();
		if (mobile.length == 11) {
			var qianbaoblance = $('#qianbaoblance').val();
			var proid = $('#proid').val();
			//alert(qianbaoblance);
			if (parseInt(qianbaoblance) >= 15) {
				$.ajax({
					type: "GET",
					url: "qianbaopay.html",
					data: "paytype=9" + "&proid=" + proid + "&mobile=" + mobile,
					success: function(data) {
						//alert(data);
						if (data == '1') {
							qianbaoblance = parseInt(qianbaoblance) - 15
							$('#qianbaoblance').val(qianbaoblance);
							$('#sucess1').lightbox_me({
								overlaySpeed: 0,
								lightboxSpeed: 0,
								centered: true,
								onLoad: function() {}
							});
							e.preventDefault();
						}
						if (data == '2') {
							$('#sucess2').lightbox_me({
								overlaySpeed: 0,
								lightboxSpeed: 0,
								centered: true,
								onLoad: function() {}
							});
							e.preventDefault();
						}
					},
					error: function(data) {
						//alert("错误!青重试.");
					}
				});
			} else {
				//alert(qianbaoblance);
				$('#bal').lightbox_me({
					overlaySpeed: 0,
					lightboxSpeed: 0,
					centered: true,
					onLoad: function() {}
				});
				e.preventDefault();
			}
		} else {
			alert('请填写正确的手机号');
			$('#contact1').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#extend_buy').click(function(e) {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = 300;
		if (parseInt(qianbaoblance) >= money) {
			$('#extendTipp').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		} else {
			$('#bal').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#chk_link').click(function(e) {
		$('#bal').lightbox_me({
			overlaySpeed: 0,
			lightboxSpeed: 0,
			centered: true,
			onLoad: function() {}
		});
		e.preventDefault();
	})
});
$(function() {
	$('#chk_link1').click(function(e) {
		$('#bal').lightbox_me({
			overlaySpeed: 0,
			lightboxSpeed: 0,
			centered: true,
			onLoad: function() {}
		});
		e.preventDefault();
	})
});
$(function() {
	$('#buyprotop').click(function(e) {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = $('input[name="stick"]:checked').val()
		var proid = $('#proid').val();
		if (parseInt(qianbaoblance) >= parseInt(money)) {
			//alert(money);
			//alert(qianbaoblance);
			$.ajax({
				type: "GET",
				url: "qianbaopay.html",
				data: "money=" + money + "&paytype=9" + "&proid=" + proid,
				success: function(data) {
					//alert(data);
					if (data == '1') {
						$('#sucess').lightbox_me({
							overlaySpeed: 0,
							lightboxSpeed: 0,
							centered: true,
							onLoad: function() {}
						});
						e.preventDefault();
					}
				},
				error: function(data) {
					//alert("错误!青重试.");
				}
			});
		} else {
			//alert(qianbaoblance);
			$('#bal').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#wxtgclk').click(function(e) {
		$('#contact2').lightbox_me({
			overlaySpeed: 0,
			lightboxSpeed: 0,
			centered: true,
			onLoad: function() {}
		});
		e.preventDefault();
	})
});
$(function() {
	$('#contact3').click(function(e) {
		var mobile1 = $('#mobile1').val();
		if (mobile1.length == 11) {
			var qianbaoblance = $('#qianbaoblance').val();
			//var proid=$('#proid').val();
			if (parseInt(qianbaoblance) >= 300) {
				//alert(money);
				//alert(qianbaoblance);
				$.ajax({
					type: "GET",
					url: "qianbaopay.html",
					data: "money=300" + "&mobile=" + mobile1 + "&paytype=10",
					success: function(data) {
						//alert(data);
						if (data == '1') {
							qianbaoblance = parseInt(qianbaoblance) - 300
							$('#qianbaoblance').val(qianbaoblance);
							$('#sucess1').lightbox_me({
								overlaySpeed: 0,
								lightboxSpeed: 0,
								centered: true,
								onLoad: function() {}
							});
							e.preventDefault();
						}
						if (data == '2') {
							$('#sucess3').lightbox_me({
								overlaySpeed: 0,
								lightboxSpeed: 0,
								centered: true,
								onLoad: function() {}
							});
							e.preventDefault();
						}
					},
					error: function(data) {
						//alert("错误!青重试.");
					}
				});
			} else {
				//alert(qianbaoblance);
				$('#bal').lightbox_me({
					overlaySpeed: 0,
					lightboxSpeed: 0,
					centered: true,
					onLoad: function() {}
				});
				e.preventDefault();
			}
		} else {
			alert('请填写正确的手机号');
			$('#contact2').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#showphone').click(function(e) {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = 300;
		if (parseInt(qianbaoblance) >= money) {
			$('#showphone1').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		} else {
			$('#bal').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#buybook').click(function(e) {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = 300;
		if (parseInt(qianbaoblance) >= money) {
			$('#huangye').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		} else {
			$('#bal').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#buytradead').click(function(e) {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = 1200;
		if (parseInt(qianbaoblance) >= money) {
			$('#tradead').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		} else {
			$('#bal').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});
$(function() {
	$('#huangye_buy').click(function(e) {
		var contact=$('#huangye_contact').val();
		contact=contact.replace("#","");
		var person=$('#huangye_person').val();
		person=person.replace("#","");
		var address=$('#huangye_address').val();
		address=address.replace("#","号");
		if (contact==""){
			alert("请输入联系方式");
			return false;
		}
		if (person==""){
			alert("请输入联系人");
			return false;
		}
		if (address==""){
			alert("请输入收货地址");
			return false;
		}
		$.ajax({
			type: "GET",
			url: "qianbaopay.html",
			data: "baoming='联系方式：" + contact + "联系人："+person+"联系地址："+address+"'&paytype=16",
			success: function(data) {
				if (data == 'baoming') {
					dismiss();
					$('#sucess1').lightbox_me({
						overlaySpeed: 0,
						lightboxSpeed: 0,
						centered: true,
						onLoad: function() {}
					});
					e.preventDefault();
				} else if (data == '0') {
					dismiss();
					$('#terror').lightbox_me({
						overlaySpeed: 0,
						lightboxSpeed: 0,
						centered: true,
						onLoad: function() {}
					});
					e.preventDefault();
				} else if (data == 'nomoney') {
					dismiss();
					$('#bal').lightbox_me({
						overlaySpeed: 0,
						lightboxSpeed: 0,
						centered: true,
						onLoad: function() {}
					});
					e.preventDefault();
				}
			},
			error: function(data) {
				alert("错误!请重试.");
			}
		});
	})
});
$(function() {
	$('#tradead_buy').click(function(e) {
		var contact=$('#tradead_contact').val();
		contact=contact.replace("#","");
		var person=$('#tradead_person').val();
		person=person.replace("#","");
		var tradead_keywords=$('#tradead_keywords').val();
		tradead_keywords=tradead_keywords.replace("#","");
		if (contact==""){
			alert("请输入联系方式");
			return false;
		}
		if (person==""){
			alert("请输入联系人");
			return false;
		}
		if (tradead_keywords==""){
			alert("请输入广告词");
			return false;
		}
		$.ajax({
			type: "GET",
			url: "qianbaopay.html",
			data: "baoming=联系方式：" + contact + "联系人："+person+"广告词："+tradead_keywords+"&paytype=17",
			success: function(data) {
				if (data == 'baoming') {
					dismiss();
					$('#sucess1').lightbox_me({
						overlaySpeed: 0,
						lightboxSpeed: 0,
						centered: true,
						onLoad: function() {}
					});
					e.preventDefault();
				} else if (data == '0') {
					dismiss();
					$('#terror').lightbox_me({
						overlaySpeed: 0,
						lightboxSpeed: 0,
						centered: true,
						onLoad: function() {}
					});
					e.preventDefault();
				} else if (data == 'nomoney') {
					dismiss();
					$('#bal').lightbox_me({
						overlaySpeed: 0,
						lightboxSpeed: 0,
						centered: true,
						onLoad: function() {}
					});
					e.preventDefault();
				}
			},
			error: function(data) {
				alert("错误!请重试.");
			}
		});
	})
});
$(function() {
	$('#showphone2').click(function(e) {
		$('#showphone3').lightbox_me({
			overlaySpeed: 0,
			lightboxSpeed: 0,
			centered: true,
			onLoad: function() {}
		});
		e.preventDefault();
	})
});
$(function() {
	$('#showphone4').click(function(e) {
		var qianbaoblance = $('#qianbaoblance').val();
		var money = $('input[name="shownumb"]:checked').val()
		if (parseInt(qianbaoblance) >= parseInt(money)) {
			$.ajax({
				type: "GET",
				url: "qianbaopay.html",
				data: "money=" + money + "&paytype=11",
				success: function(data) {
					//alert(data);
					if (data == '1') {
						$('#sucess4').lightbox_me({
							overlaySpeed: 0,
							lightboxSpeed: 0,
							centered: true,
							onLoad: function() {}
						});
						e.preventDefault();
					} else if (data == '2') {
						$('#sucess5').lightbox_me({
							overlaySpeed: 0,
							lightboxSpeed: 0,
							centered: true,
							onLoad: function() {}
						});
						e.preventDefault();
					}
				},
				error: function(data) {
					//alert("错误!青重试.");
				}
			});
		} else {
			$('#bal').lightbox_me({
				overlaySpeed: 0,
				lightboxSpeed: 0,
				centered: true,
				onLoad: function() {}
			});
			e.preventDefault();
		}
	})
});

function dismiss() {
	$('#buyTipp').trigger('close');
	$('#buyTipp2').trigger('close');
	$('#extendTipp').trigger('close');
	$('#bal').trigger('close');
	$('#sucess').trigger('close');
	$('#sucess1').trigger('close');
	$('#sucess2').trigger('close');
	$('#sucess3').trigger('close');
	$('#contact1').trigger('close');
	$('#contact2').trigger('close');
	$('#showphone1').trigger('close');
	$('#showphone3').trigger('close');
	$('#sucess4').trigger('close');
	$('#sucess5').trigger('close');
	$('#huangye').trigger('close');
	$('#terror').trigger('close');
	$('#tradead').trigger('close');
}