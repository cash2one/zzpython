(function( env ) {
'use strict';
var configs = {
resolve: function( id ) {
var rStyle = /\.css(?:\?|$)/,
parts = id.split('/'),
root = parts[0],
type = rStyle.test( id ) ? 'css/' : 'js/';
switch ( root ){
case 'widget':
id = 'http://static.c.aliimg.com/' + type + 'list/'  + id;
break;
}
return id;
},
alias: {
'Tips':'cml/widget/tip',
'ImageLoader':'cml/widget/imageLazyload'
},
/**
* 配置baseUrl，如果是static分支，请配置成 http://static.c.aliimg.com，
* 请勿直接配置 CDN 域名，除非你想清楚了清除文件缓存的机制（比如加时间戳）
* 请使用 styleCombine 来帮你处理 CDN 缓存的问题。
*/
baseUrl:"http://style.c.aliimg.com/",
/**
* 打开 AMD 异步加载功能。
*/
amd:true
};
if( typeof env.lofty !== 'undefined' ) {
// for lofty
env.lofty.config(configs);
}
if( typeof exports !== 'undefined' && env === exports ) {
// for node.js
exports.configs = configs;
}
})(this);

/*! Copyright (c) 2013 Brandon Aaron (http://brandon.aaron.sh)
* Licensed under the MIT License (LICENSE.txt).
*
* Version: 3.1.11
*
* Requires: jQuery 1.2.2+
*/
!function(a){"function"==typeof define&&define.amd?define(["jquery"],a):"object"==typeof exports?module.exports=a:a(jQuery)}(function(a){function b(b){var g=b||window.event,h=i.call(arguments,1),j=0,l=0,m=0,n=0,o=0,p=0;if(b=a.event.fix(g),b.type="mousewheel","detail"in g&&(m=-1*g.detail),"wheelDelta"in g&&(m=g.wheelDelta),"wheelDeltaY"in g&&(m=g.wheelDeltaY),"wheelDeltaX"in g&&(l=-1*g.wheelDeltaX),"axis"in g&&g.axis===g.HORIZONTAL_AXIS&&(l=-1*m,m=0),j=0===m?l:m,"deltaY"in g&&(m=-1*g.deltaY,j=m),"deltaX"in g&&(l=g.deltaX,0===m&&(j=-1*l)),0!==m||0!==l){if(1===g.deltaMode){var q=a.data(this,"mousewheel-line-height");j*=q,m*=q,l*=q}else if(2===g.deltaMode){var r=a.data(this,"mousewheel-page-height");j*=r,m*=r,l*=r}if(n=Math.max(Math.abs(m),Math.abs(l)),(!f||f>n)&&(f=n,d(g,n)&&(f/=40)),d(g,n)&&(j/=40,l/=40,m/=40),j=Math[j>=1?"floor":"ceil"](j/f),l=Math[l>=1?"floor":"ceil"](l/f),m=Math[m>=1?"floor":"ceil"](m/f),k.settings.normalizeOffset&&this.getBoundingClientRect){var s=this.getBoundingClientRect();o=b.clientX-s.left,p=b.clientY-s.top}return b.deltaX=l,b.deltaY=m,b.deltaFactor=f,b.offsetX=o,b.offsetY=p,b.deltaMode=0,h.unshift(b,j,l,m),e&&clearTimeout(e),e=setTimeout(c,200),(a.event.dispatch||a.event.handle).apply(this,h)}}function c(){f=null}function d(a,b){return k.settings.adjustOldDeltas&&"mousewheel"===a.type&&b%120===0}var e,f,g=["wheel","mousewheel","DOMMouseScroll","MozMousePixelScroll"],h="onwheel"in document||document.documentMode>=9?["wheel"]:["mousewheel","DomMouseScroll","MozMousePixelScroll"],i=Array.prototype.slice;if(a.event.fixHooks)for(var j=g.length;j;)a.event.fixHooks[g[--j]]=a.event.mouseHooks;var k=a.event.special.mousewheel={version:"3.1.11",setup:function(){if(this.addEventListener)for(var c=h.length;c;)this.addEventListener(h[--c],b,!1);else this.onmousewheel=b;a.data(this,"mousewheel-line-height",k.getLineHeight(this)),a.data(this,"mousewheel-page-height",k.getPageHeight(this))},teardown:function(){if(this.removeEventListener)for(var c=h.length;c;)this.removeEventListener(h[--c],b,!1);else this.onmousewheel=null;a.removeData(this,"mousewheel-line-height"),a.removeData(this,"mousewheel-page-height")},getLineHeight:function(b){var c=a(b)["offsetParent"in a.fn?"offsetParent":"parent"]();return c.length||(c=a("body")),parseInt(c.css("fontSize"),10)},getPageHeight:function(b){return a(b).height()},settings:{adjustOldDeltas:!0,normalizeOffset:!0}};a.fn.extend({mousewheel:function(a){return a?this.bind("mousewheel",a):this.trigger("mousewheel")},unmousewheel:function(a){return this.unbind("mousewheel",a)}})});

/*!!cmd:compress=true*/
/*!!cmd:jsCompressOpt=["--disable-optimizations"]*/
define(["jquery","downloadbox"],function(e,h){e(document).ready(function(){h.init()});
var c=e(document.body).hasClass("buyer");
function i(l,k){var m,n;return function(){
	var p=+new Date,o=[].slice.call(arguments);
	if(m&&p<m+k){return;n&&clearTimeout(n);
	n=setTimeout(function(){
		m=p;l.apply(this,o)
		}
		,k)}else{
			m=p;var q=l.apply(this,o);
			if(!q){
				m-=(k+1)
				}
				}
				}
				}
				var b=e(window).innerHeight(),
				g=(e("body").scrollTop()||e("html").scrollTop()||0)+b,
				j=e(".section-feature4").offset().top;
				e(".navbar").css("opacity",0);
				e(window).on("resize",function(){b=e(window).innerHeight();
				j=e(".section-feature4").offset().top});
				e("body, html").on("mousewheel",
				i(function(k){b=e(window).innerHeight();
				if(!k.deltaY){k.deltaY=(-k.originalEvent.wheelDelta||k.originalEvent.deltaY)>0?-1:1}g=(e("body").scrollTop()||e("html").scrollTop()||0)+b-k.deltaY*100;
				j=e(".section-feature4").offset().top;e(".navbar").stop();
				if(g<=j-3*b||g>j+b){e("body, html").animate({
					scrollTop:(k.deltaY>0?"-":"+")+"=100"},0);
					e(".navbar").animate({opacity:0},300);return false}e(".navbar").animate({opacity:1},300);
					k.preventDefault();f(k.deltaY>0?1:-1)},250));
					e(document).on("keydown",function(k){var l=-1,m;
					switch(k.keyCode){
						case 33:m=-100;
								l=1;
								break;
						case 34:m=100;break;
						case 38:m=-100;l=1;break;
						case 40:m=100;break}g=(e("body").scrollTop()||e("html").scrollTop()||0)+b+m;
						if(g<=j-3*b||g>j+b){e("body, html").animate({scrollTop:"+="+m},0);return false}f(l)});
						e(".navbar").delegate("li","click",function(){d(e(this).data("index")+1)});
						e(".navbar").delegate("button","click",function(){e(".navbar li").removeClass("current");
						e("body, html").animate({scrollTop:0},800);
						e(".navbar").animate({opacity:0},300)});
						e(".feature-nav").delegate("li","click",function(){d(e(this).index(".feature-nav li")+1)});
						function f(l){for(var k=0;k<4;k++){if(g>=j-b*k){if(l>0){d(3-k)}else{d(4-k)}break}}}function d(k){e("body, html").stop();
						e(".navbar li").removeClass("current");
						e("body, html").animate({scrollTop:j-b*(4-k)},800,"swing");
						a(k);
						e('.navbar li[data-index="'+(k-1)+'"]').addClass("current")}function a(k){setTimeout(function(){e(".animated").removeClass("fadeInDown fadeInUp bounce fadeInLeft fadeInRight rotateIn rotateScaleIn swing");
						e(".animation").removeClass("animation");
						if(c){switch(k){
							case 1:e(".section-feature1 .section-feature-title i").addClass("swing");break;
							case 2:e(".section-feature2 .section-feature-images").addClass("fadeInUp");break;
							case 3:e(".section-feature3 .section-feature-title").addClass("fadeInRight");
							e(".section-feature3 .section-feature-desc").addClass("fadeInLeft");break;
							case 4:e(".section-feature5 .section-feature-images").addClass("rotateScaleIn");break}}else{switch(k){
								case 1:e(".section-feature1 .section-feature-title").addClass("fadeInDown");e(".section-feature1 .section-feature-desc").addClass("fadeInUp");e(".section-feature1 .section-feature-images").addClass("animation");break;
								case 2:e(".section-feature2 .section-feature-title i").addClass("bounce");e(".section-feature2 .section-feature-images").addClass("animation");break;
								case 3:e(".section-feature3 .section-feature-title").addClass("fadeInLeft");e(".section-feature3 .section-feature-desc").addClass("fadeInRight");break;
								case 4:e(".section-feature4 .section-feature-title").addClass("fadeInDown");e(".section-feature4 .section-feature-desc").addClass("fadeInUp");break}}},800)}});