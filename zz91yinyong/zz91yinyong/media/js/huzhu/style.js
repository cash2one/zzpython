function gotoReply(){
	$('.d-reply')[0].scrollIntoView(true);
	$('.d-reply').find('textarea').focus();
}

function dismiss(){
	$('#reply_div_cz').trigger('close');
	$('.d-reply').trigger('close');
	$('#reply_div_').trigger('close');
	$('#reply_div_nick').trigger('close');
	
}


function check() { 
	var regC = /[^ -~]+/g; 
	var regE = /\D+/g; 
	var str = t1.value; 
	
	if (regC.test(str)){ 
		t1.value = t1.value.substr(0,5); 
	} 
	
	if(regE.test(str)){ 
		t1.value = t1.value.substr(0,10); 
	} 
} 
















