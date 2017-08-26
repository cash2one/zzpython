/**
 * 全局js
 * Autor: Fhua
 * Date: 16-11-25
 */

//Layui 扩展组件入口

var pay_html='<div class="shang_box" style="display: block;"><div class="shang_tit"><p>感谢您的支持，我会继续努力的!</p></div><div class="shang_payimg"style="width:80%"><img src="/WebSystems/images/pay1.png" alt="扫码支持" title="扫一扫" style="float:left"/><img src="/WebSystems/images/pay2.png" alt="扫码支持"title="扫一扫"style="float:right"/></div><div class="pay_explain">扫码打赏，你说多少就多少</div><div class="shang_info"><p>打开<span id="shang_pay_txt">支付宝</span>扫一扫，即可进行扫码打赏哦</p></div></div>';

layui.config({
    base: '/WebSystems/Js/Content/layui/lay/modules/extendplus/' //自定义layui组件的目录
}).extend({//设定组件别名
    common: 'common',
    navbar: 'navbar/navbar',
    tab: 'navbar/tab',
    icheck: 'icheck/icheck'
});



layui.use(['layer', 'element', 'util','common'], function () {
    var $ = layui.jquery
    , layer = layui.layer
	, common = layui.common
    , device = layui.device()//设备信息
    , element = layui.element();

    //阻止IE7以下访问
    if (device.ie && device.ie < 9) {
        layer.alert('最低支持ie9，您当前使用的是古老的 IE' + device.ie + '！');
    }

	//
    //手机设备的简单适配
    var treeMobile = $('.site-tree-mobile')
    , shadeMobile = $('.site-mobile-shade')

    treeMobile.on('click', function () {
        $('body').addClass('site-mobile');
    });

    shadeMobile.on('click', function () {
        $('body').removeClass('site-mobile');
    });

    //捐赠
    $('.juanzen').on('click', function () {
        layer.open({
            type: 1,
			shadeClose:true,
            title: false,
            area: ['562px', '450px'],
            content: pay_html
        });
    });
    //weixin、weibo
    $('#git,#weibo,#weixin').on('click', function () {
        layer.tips('暂时没有哦!', this)
    });

	
	
    var globalActive = {
        doRefresh: function () {
            var url = $(this).data('href');
            if (url) {
                location.href = url;
            }
            else {
                location.href = location.href;
            }
        },
        doGoTop: function () {
            $(this).click(function () {
                $('body,html').animate({ scrollTop: 0 }, 100);
                return false;
            });
        },
        doGoBack: function () {
            history.go(-1);
        },
		close_parent: function () {
		var index = parent.layer.getFrameIndex(window.name); //获取窗口索引
		parent.layer.close(index);
		return false;
        }
    };

    $('.do-action').on('click', function (e) {
        var type = $(this).data('type');
        globalActive[type] ? globalActive[type].call(this) : '';
        layui.stope(e);//阻止冒泡事件
		return false;
    });
	
	
	
	
//删除菜单
$('.mar_delete').bind('click', function() {
var Param  = $(this).attr("Param");
var id     = $(this).attr("id");
	$.ajax({ 
	type:"POST", 
	dataType:'json', 
	async: false,
	url:"/WebSystems/Include/Class_Menu.php", 
	data:"Param="+Param+"&id="+id, 
	cache:false, //不缓存此页面 
	success:function(data){ 

	if(data.status=='y'){
	layer.msg(data.info); 	
	location.reload(); 
	}else{
		layer.msg(data.info); 
	}

	} 
	}); 
	

});



//增加相册

$('#creat_xiangce').bind('click', function() {
var rel=$(this).attr("rel");
layer.open({
  type: 2,
  skin: 'layui-layer-molv', //样式类名
  closeBtn: 0, //不显示关闭按钮
  anim: 2,
  shadeClose: true, //开启遮罩关闭
  area: ['50%','380px'],
  content: rel //iframe的url
});

});




//删除相册
$('.del_friendlink').live('click', function() {
var id=$(this).parent().parent().attr("id");
var rel=$(this).parent().parent().attr("rel");
var Param="del_friendlink";
	$.ajax({ 
	type:"POST", 
	dataType:'json', 
	async: false,
	url:"/WebSystems/Include/Class_Menu.php", 
	data:"Param="+Param+"&id="+rel, 
	cache:false, //不缓存此页面 
	success:function(data){ 
	if(data.status=='y'){
	layer.msg(data.info); 	
	$("#"+id).remove();
	}else{
		layer.msg(data.info); 
	}

	} 
	}); 
	
});



//修改相册
$('.edt_friendlink').live('click', function() {
	var rel=$(this).attr("rel");
	layer.open({
	  type: 2,
	  skin: 'layui-layer-molv', //样式类名
	  closeBtn: 0, //不显示关闭按钮
	  anim: 2,
	  shadeClose: true, //开启遮罩关闭
	  area: ['50%','380px'],
	  content: rel //iframe的url
	});

});









//删除相册里面的图片
$('.del_mar_pic').live('click', function() {
var id=$(this).parent().parent().attr("id");
var rel=$(this).parent().parent().attr("rel");
var Param="del_mar_pic2";
	$.ajax({ 
	type:"POST", 
	dataType:'json', 
	async: false,
	url:"/WebSystems/Include/Class_Menu.php", 
	data:"Param="+Param+"&id="+rel, 
	cache:false, //不缓存此页面 
	success:function(data){ 
	if(data.status=='y'){
	layer.msg(data.info); 	
	$("#"+id).remove();
	}else{
		layer.msg(data.info); 
	}

	} 
	}); 
	
});



	
//添加分类
$('#mar_add_menu').bind('click', function() {
var rel="Sys_Sort_add.php"+window.location.search+"&id=";
layer.open({
  type: 2,
  title: '添加分类',
  shadeClose: true,
  shade: 0.8,
  area: ['80%', '60%'],
  content: rel //iframe的url
}); 
	
});

//修改分类
$('.edit_menu').live('click', function() {
var id=$(this).attr("rel");
var rel="Sys_Sort_add.php"+window.location.search+"&id="+id;
layer.open({
  type: 2,
  title: '添加分类',
  shadeClose: true,
  shade: 0.8,
  area: ['80%', '60%'],
  content: rel //iframe的url
}); 
	
});



//删除分类
$('.del_menu').live('click', function() {
var id=$(this).attr("rel");
var rel="Sys_Sort_add.php"+window.location.search+"&id="+id+"&action=del";

	$.ajax({ 
	type:"POST", 
	dataType:'json', 
	async: false,
	url:rel, 
	data:"", 
	cache:false, //不缓存此页面 
	success:function(data){ 
            if(data.status=='y'){
				layer.msg(data.info);
				doSearch();

			}else{
				layer.msg(data.info);
			}
	} 
	}); 
	
	

	
});


	
	
	
	
});



//自定义增加
layui.config({
    base: '/WebSystems/Js/Content/layui/lay/modules/extendplus/' //自定义layui组件的目录
}).use(['element', 'layer', 'navbar', 'tab'], function() {
	var element = layui.element(),
		$ = layui.jquery,
		layer = layui.layer,
		navbar = layui.navbar(),
		tab = layui.tab({
			elem: '.admin-nav-card' //设置选项卡容器
		});
  
    $('.frame_Add').on('click', function (e) {

        var icon = $(this).attr('icon');
		var title = $(this).attr('title');
		var href = $(this).attr('url');
		var obj = {
		icon :icon,
		title : title,
		href : href
		};
		tab.tabAdd(obj);
		return false;
		
	});    
  

});
	
	
	
	
//将form转为AJAX提交
function ajaxSubmit(frm, fn) {
    var dataPara = getFormJson(frm);
    $.ajax({
        url: frm.action,
		dataType:'json',
        type: frm.method,
        data: dataPara,
        success: fn
    });
}


function ajaxSubmit(frm, fn) {
    var dataPara = getFormJson(frm);
    $.ajax({
        url: frm.action,
		dataType:'json',
        type: frm.method,
        data: dataPara,
        success: fn
    });
}







//将form中的值转换为键值对。
function getFormJson(frm) {
    var o = {};
    var a = $(frm).serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });

    return o;
}


function parent_close(index) {
var index = parent.layer.getFrameIndex(window.name); //获取窗口索引
parent.layer.close(index);
return false;
}