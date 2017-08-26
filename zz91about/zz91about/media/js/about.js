// JavaScript Document
$(document).ready(function() {
	var lm=$(".navli");
	lm.mouseover(function(){
		var self = $(this);
		var firsta=self.find('a').first()
		firsta.addClass("nav_on");
		//self.find("#nav_a").removeClass("nav_arr");
		var navxl=self.find(".nav_xl");
		if (self){
			navxl.css("display","");
			//navxl.fadeIn("slow");
		}
	});
	lm.mouseout(function(){
		var self = $(this);
		var firsta=self.find('a').first()
		//firsta.addClass("nav_arr");
		firsta.removeClass("nav_on");
		var navxl=self.find(".nav_xl");
		if (self){
			navxl.css("display","none");
			//navxl.fadeOut("slow");
		}
	});
})