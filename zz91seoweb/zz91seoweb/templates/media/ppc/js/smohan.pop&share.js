/*
弹出插件 AND 分享插件
autho：smohan
http://www.smohan.net
*/


;(function($){$.fn.SmohanPopLayer=function(options){var Config={Shade:true,Event:"click",Content:"Content",Title:"Smohan.net"};var options=$.extend(Config,options);var layer_width=$('#'+options.Content).outerWidth(true);var layer_height=$('#'+options.Content).outerHeight(true)
var layer_top=(layer_height+40)/2;var layer_left=(layer_width+40)/2;var load_left=(layer_width-36)/2;var load_top=(layer_height-100)/2;var layerhtml="";if(options.Shade==true){layerhtml+='<div class="Smohan_Layer_Shade" style="display:none;"></div>';}
layerhtml+='<div class="Smohan_Layer_box" style="/* width:'+layer_width+'px;height:'+layer_height+'px; */margin-top:-'+layer_top+'px;margin-left:-'+layer_left+'px;display:none;" id="layer_'+options.Content+'">';layerhtml+='<h3><b class="text">'+options.Title+'</b><a href="javascript:void(0)" class="close"></a></h3>';layerhtml+='<div class="layer_content">';layerhtml+='<div class="loading" style="left:'+load_left+'px;top:'+load_top+'px;"></div>';layerhtml+='<div id="'+options.Content+'" style="display:block;">'+$("#"+options.Content).html()+'</div>';layerhtml+='</div>';layerhtml+='</div>';$('body').prepend(layerhtml);if(options.Event=="unload"){$('#layer_'+options.Content).animate({opacity:'show',marginTop:'-'+layer_top+'px'},"slow",function(){$('.Smohan_Layer_Shade').show();$('.Smohan_Layer_box .loading').hide();});}else{$(this).live(options.Event,function(e){$('#layer_'+options.Content).animate({opacity:'show',marginTop:'-'+layer_top+'px'},"slow",function(){$('.Smohan_Layer_Shade').show();$('.Smohan_Layer_box .loading').hide();});});}
$('.Smohan_Layer_box .close').click(function(e){$('.Smohan_Layer_box').animate({opacity:'hide',marginTop:'-300px'},"slow",function(){$('.Smohan_Layer_Shade').hide();$('.Smohan_Layer_box .loading').show();});});};})(jQuery);

//表单	
$(document).ready(function(e) {
	var share_html = "";
	share_html += '<div id="Share">';
	share_html += '<form method="post" action="http://www.zz91.com/zt/baomingsave/">';
	share_html += '<div class="s-main"><div class="sm-txt">公司名称：</div> <div class="sm-input"><input name="textfield" type="text" id="textfield" value="" title="*公司名称" /></div> </div>';
	share_html += '<div class="s-main"><div class="sm-txt">联系人：</div> <div class="sm-input"><input name="textfield2" type="text" id="textfield2" value="" title="*联系人"/></div> </div>';
	share_html += '<div class="s-main"><div class="sm-txt">性别：</div><div class="sm-radio"><input type="radio" name="radio" id="radio" value="radio" title="性别：女士" checked /><span>女士</span>  <input type="radio" name="radio" id="radio" value="radio" title="性别：男士" /><span>男士</span> </div></div>';
	share_html += '<div class="s-main"><div class="sm-txt">联系电话 ：</div> <div class="sm-input"><input name="textfield3" type="text" id="textfield3" value="" title="*联系电话"/></div> </div>';
	share_html += '<div class="s-main"><div class="sm-txt">手机：</div> <div class="sm-input"><input name="textfield4" type="text" id="textfield4" value="" title="*手机"/></div> </div>';
	share_html += '<div class="s-main"><center><div class="sm-btn">提交</div></center></div>';
	share_html += '</form>';
	share_html += '</div>';
	
	var share_html_ ="";
	share_html_ += '<div id="Share_">';
	share_html_ += '<span>您的信息已提交，客服会尽快联系您办理！</span>';
	share_html_ += '</div>';
	
	$('body').prepend(share_html);
	$('body').prepend(share_html_);
    $('.share').SmohanPopLayer({Shade : true,Event:'click',Content : 'Share', Title : ''});
	$('.sm-btn').SmohanPopLayer({Shade : true,Event:'click',Content : 'Share_', Title : ''});
	$('.sm-btn').click(function(frm){
	
	
		varlulfs="";
		for(var i=0;i<frm.length;i++)
		{
			var objinput=frm[i];
			if (objinput.title!="")
			{
				if (objinput.type=="radio")
				{
					if(objinput.checked==true)
					{
						varlulfs=varlulfs+objinput.title+"\n";
					}
				}else{
					varlulfs=varlulfs+objinput.title+":"+objinput.value+"\n";
				}
				if (objinput.title.substring(0,1)=="*")
				{
					if (objinput.value=="")
					{
						alert(objinput.title.substring(1)+"不能为空！");
						objinput.focus();
						return false
					}
					
				}
			}
		}
		frm.contents.value = varlulfs;
	
	
		$('.Smohan_Layer_box .close').trigger('click');
	});
});
