var flag=false; 
function DrawImage(ImgD,width,height){ 
	var image=new Image(); 
	image.src=ImgD.src; 
	if(image.width>0 && image.height>0){ 
		flag=true; 
		if(image.width/image.height>1){ 
			if(image.width>width){
				ImgD.width=width; 
				ImgD.height=(image.height*width)/image.width; 
			}else{ 
				ImgD.width=image.width;
				ImgD.height=image.height; 
			} 
		}else{ 
			if(image.height>height){
				ImgD.height=height; 
				ImgD.width=(image.width*height)/image.height;
				if(ImgD.width>width){ 
					ImgD.width=width;
					ImgD.height=(width*image.height)/image.width;
				}
			}else{ 
				ImgD.width=image.width;
				ImgD.height=image.height; 
			} 
		//ImgD.alt="点击查看大图片"; 
		}
		if(ImgD.width>width){ ImgD.width=width;ImgD.height=(width*image.height)/image.width;}
		if(ImgD.height>height){ ImgD.height=height;ImgD.width=(image.width*height)/image.height;}
	}
}

//jquery图片成比例缩放
function jDrawImage(ImgD,width,height){ 
	var image=new Image(); 
	var rzwidth,rzheight;
	image.src=ImgD.attr("src"); 
	if(image.width>0 && image.height>0){ 
		flag=true; 
		if(image.width/image.height>1){ 
			if(image.width>width){
				rzwidth=width;
				rzheight=(image.height*width)/image.width;
			}else{
				rzwidth=image.width;
				rzheight=image.height;
			} 
			
		}else{ 
			if(image.height>height){
				rzwidth=(image.width*height)/image.height;
				rzheight=height;
			}else{
				rzwidth=image.width;
				rzheight=image.height;
			} 
		//ImgD.alt="点击查看大图片"; 
		}
		if(rzwidth>width){ rzwidth=width;rzheight=(image.height*width)/image.width;}
		if(rzheight>height){ rzheight=height;rzwidth=(image.width*height)/image.height;}
		ImgD.width(rzwidth);
		ImgD.height(rzheight); 
	}
}
function setImgSize(dom,width,height){
	for(var i=0;i<dom.length;i++){
		jDrawImage(dom.eq(i),width,height);
	}
}