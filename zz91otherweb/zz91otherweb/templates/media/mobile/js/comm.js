function selectOption(menuname, values) {
	$("#"+menuname).val(values);
//	var menu = document.getElementById(menuname);
//	if (menu) {
//		for (var i = 0; i <= menu.options.length; i++) {
//			if (value) {
//				if (menu.options[i].value == value) {
//					menu.options[i].selected = true;
//					break;
//				}
//			}
//		}
//	}
}

function selectCheckBox(boxname, thevalue) {
	if (thevalue){
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