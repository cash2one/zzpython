//顶部滚动图片
function showscrollpic() {
	var UIScrollPicture = api.require('UIScrollPromptView');
	UIScrollPicture.open({
		rect : {
			x : 0,
			y : 0,
			w : api.winWidth,
			h : 230
		},
		data : {
			paths : picpath,
			captions: piccaptions
		},
		styles : {
			caption : {//（可选项）JSON对象；说明文字区域样式
				height : 25.0, //（可选项）数字类型；说明文字区域高度；默认：35.0
				color : 'rgba(255,255,255,0.5)', //（可选项）字符串类型；说明文字字体颜色；默认：'#E0FFFF'
				size : 16.0, //（可选项）数字类型；说明文字字体大小；默认：13.0
				bgColor : 'rgba(0,0,0,0.5)', //（可选项）说明文字区域的背景色，支持rgb、rgba、#；默认'#696969'
				position : 'overlay' //（可选项）字符串类型；说明文字区域的显示位置，取值范围：overlay（悬浮在图片上方，底部与图片底部对齐），bottom（紧跟在图片下方，顶部与图片底部对齐）；默认：'bottom'
			},
			indicator : {//（可选项）JSON对象；指示器样式；不传则不显示指示器
				align : 'center', //(可选项)字符串类型；指示器位置，center（居中），left（靠左），right（靠右）；默认：center
				//color : 'rgba(0,200,0,0.9)', //(可选项)指示器颜色 ，支持rgb、rgba、#；默认：'#FFFFFF'
				activeColor : 'rgba(0,0,0,0.7)' //(可选项)当前指示器颜色，支持rgb、rgba、#；默认：'#DA70D6'
			}
		},
		placeholderImg : "widget://image/loadimg0.png",
		contentMode : "scaleAspectFit",
		interval : 6,
		auto : true,
		loop : true,
		fixedOn : api.frameName,
		fixed : false
	}, function(ret, err) {
		//zzalert(JSON.stringify(ret));
	});
}