$(".buybutton").css("z-index",99999)
$(".buybutton").on("click", function() {
	event.stopPropagation();
	if (havelogin()) {
		paysubmit();
	}
})