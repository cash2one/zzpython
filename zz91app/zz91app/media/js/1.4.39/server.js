if (location.href.indexOf("/html/index-frame.html")>=0){
	(function(d, t) {
		var r = d.createElement(t),
			s = d.getElementsByTagName(t)[0];
		r.async = 1;
		r.src = hosturl + '/js/1.4.39/index-frame.js?' + (new Date()).getTime().toString();
		s.parentNode.insertBefore(r, s);
	})(document, "script");
}