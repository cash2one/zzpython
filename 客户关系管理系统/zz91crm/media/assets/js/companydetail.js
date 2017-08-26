//选择国家
function selectcountry(id) {
	if(id == "1") {
		document.getElementById("othercountrys").style.display = "none"
		document.getElementById("mycountry").style.display = ""
	} else {
		document.getElementById("othercountrys").style.display = ""
		document.getElementById("mycountry").style.display = "none"
	}
}
//