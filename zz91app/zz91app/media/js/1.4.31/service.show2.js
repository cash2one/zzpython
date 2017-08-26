$(".buybutton").on("click",function() {
	event.stopPropagation();
	if (havelogin()) {
		paysubmit();
	}
})