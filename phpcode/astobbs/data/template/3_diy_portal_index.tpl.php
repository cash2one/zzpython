<?php if(!defined('IN_DISCUZ')) exit('Access Denied'); hookscriptoutput('index');
block_get('16,17');?><?php include template('common/header'); ?><style id="diy_style" type="text/css"></style>
<script src="template/xinrui_iuni/js/jquery.min.js" type="text/javascript" type="text/javascript"></script>
<script type="text/javascript"> jQuery.noConflict();</script>
<script src="template/xinrui_iuni/js/jquery.SuperSlide.js" type="text/javascript" type="text/javascript"></script>
<div class="wp cl mtw">
<div class="col1 z">
<div class="portal_slide bp">
<!--[diy=diy1]--><div id="diy1" class="area"><div id="framePK5JoH" class="frame move-span cl frame-1-1"><div class="title frame-title"><span class="titletext">1-1框架</span></div><div id="framePK5JoH_left" class="column frame-1-1-l"><div id="framePK5JoH_left_temp" class="move-span temp"></div><?php block_display('16');?></div><div id="framePK5JoH_center" class="column frame-1-1-r"><div id="framePK5JoH_center_temp" class="move-span temp"></div><?php block_display('17');?></div></div><div id="frame5T4bc7" class="frame move-span cl frame-1"><div class="title frame-title"><span class="titletext">1框架</span></div><div id="frame5T4bc7_left" class="column frame-1-c"><div id="frame5T4bc7_left_temp" class="move-span temp"></div></div></div></div><!--[/diy]-->
</div>
<div class="today_focus bp">
<!--[diy=diy2]--><div id="diy2" class="area"></div><!--[/diy]-->
</div>
<div class="essence bp">
<!--[diy=diy11]--><div id="diy11" class="area"></div><!--[/diy]-->
</div>
<div class="news_portal bp">
<!--[diy=diy9]--><div id="diy9" class="area"></div><!--[/diy]-->
<div class="jquery_pagnation"></div>
<script type="text/javascript"> jQuery.noConflict();</script>
<script src="template/xinrui_iuni/js/jquery.pagnation.js" type="text/javascript"></script> 
<script type="text/javascript">
(function(dfsj_jq){
var dfsj_items = dfsj_jq('.newest li');
var dfsj_items2 = 10;
var total = dfsj_items.size();
total>0 && dfsj_jq('.jquery_pagnation').pagination({pagetotal:total,target:dfsj_items,perpage:dfsj_items2});
})(jQuery);
</script>
</div>
</div>
<div class="col2 y">
<div class="sd_btn bp">
<a onclick="showWindow('nav', this.href, 'get', 0)" href="forum.php?mod=misc&amp;action=nav" class="post_btn">发表新帖</a>
<a href="plugin.php?id=dsu_paulsign:sign" target="_blank" class="signin">马上签到</a>
</div>
<div class="colu bp"><!--[diy=diy3]--><div id="diy3" class="area"></div><!--[/diy]--></div>
<div class="hot_act bp">
<!--[diy=diy10]--><div id="diy10" class="area"></div><!--[/diy]-->
</div>
<div class="weibo bp" style="display:none;">
<!--[diy=diy8]--><div id="diy8" class="area"></div><!--[/diy]-->
</div>
<div class="fans bp"><!--[diy=diy4]--><div id="diy4" class="area"></div><!--[/diy]--></div>
<div class="about bp"><!--[diy=diy5]--><div id="diy5" class="area"></div><!--[/diy]--></div>
<div class="mbm"><!--[diy=diy6]--><div id="diy6" class="area"></div><!--[/diy]--></div>
<div class="mbm"><!--[diy=diy7]--><div id="diy7" class="area"></div><!--[/diy]--></div>
</div>
</div>

<!-- Baidu Button BEGIN -->
<script type="text/javascript" id="bdshare_js" data="type=tools&mini=1" ></script> 
<script type="text/javascript" id="bdshell_js"></script> 
<script type="text/javascript">
var bds_config = {};
document.getElementById('bdshell_js').src = "http://bdimg.share.baidu.com/static/js/shell_v2.js?cdnversion=" + new Date().getHours();
</script>
<!-- Baidu Button END --><?php include template('common/footer'); ?>