
$(function(){
	
	var _wrap=$('ul.mulitline');	
	var _interval=3000;	
	var _moving;
	
	_wrap.hover(function(){
		
		clearInterval(_moving);
		
	},function(){
		
		_moving=setInterval(function(){
			
			var _field=_wrap.find('li:first');
			
			var _h=_field.height();
			
			_field.animate({marginTop:-_h+'px'},600,function(){
				
				_field.css('marginTop',0).appendTo(_wrap);
				
			})
			
		},_interval)
		
	}).trigger('mouseleave');
	
});