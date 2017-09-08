from django.conf.urls import *
import settings

urlpatterns = patterns('zz91otherweb.views',
	#(r'^$', 'feiliao'),
	(r'^listmore(?P<typeid>\w+).html$', 'listmore'),
	(r'^verifycode/$', 'verifycode'),
	#--feiliao123改版
	(r'^$', 'index'),#首页
	(r'^feiliao123_more(?P<typeid>\w+).html$', 'feiliao123_more'),#更多
	(r'^trade/$', 'trade'),#交易
	(r'^news/$','news'),#资讯
)
urlpatterns += patterns('zz91otherweb.exhibit',
    (r'^feiliao123/zh/list.html$','list'),
    (r'^feiliao123/zh-add.html$','add'),
    (r'^feiliao123/zh-edit.html$','zhedit'),
    (r'^feiliao123/zh/add_save.html$','add_save'),
    (r'^feiliao123/doDelete.do$','doDelete'),
    (r'^feiliao123/zh-upload.html','zhupload'),
    (r'^feiliao123/zh/del.html','del_zh'),
)
#业务工单
urlpatterns += patterns('zz91otherweb.gd',
	#---后台
	(r'^feiliao123/gd/list.html$','gd_list'),#所有工单
	(r'^feiliao123/gd/add.html$','gd_add'),#添加工单
	(r'^feiliao123/gd/reply.html$','gd_reply'),
	(r'^feiliao123/gd/replysave.html$','gd_replysave'),
	(r'^feiliao123/gd/details.html$','gd_details'),#工单详情
	(r'^feiliao123/gd/station.html$','gd_station'),#工单状态
	(r'^feiliao123/gd/answer.html$','gd_answer'),#回复
)
#----设备信息搜索和删除，啊啊啊啊
urlpatterns += patterns('zz91otherweb.zzshebei',
    (r'^feiliao123/list/$','listl'),
    (r'^feiliao123/listl/$','listl'),
    (r'^feiliao123/doDelete.do$','doDelete'),
)
urlpatterns += patterns('zz91otherweb.dacong',
    (r'^adminmobile/dacong_add.html$','dacongadd'),
    (r'^adminmobile/dacong_list.html$','daconglist'),
    (r'^adminmobile/dacong_content.html$','editcontent'),
    (r'^adminmobile/dacong_savenews.html$','savenews'),
    (r'^adminmobile/dacong_edit.html$','editnews'),
    (r'^adminmobile/dacong_savecontent.html$','savecontent'),
    (r'^adminmobile/dacong_delnews.html$','dacong_delnews'),
    (r'^adminmobile/dacong_view.html$','dacong_view'),
)
#再生汇
urlpatterns += patterns('zz91otherweb.zsh',
    (r'^adminmobile/zsh/zshlist.html$','zshlist'),
    (r'^adminmobile/zsh/$','zshlist'),
    (r'^adminmobile/zsh/changepay.html$','changepay'),
    (r'^adminmobile/zsh/changezheng.html$','changezheng'),
    (r'^adminmobile/zsh/addcompany.html$','addcompany'),
    (r'^adminmobile/zsh/modify.html$','modify'),
    (r'^adminmobile/zsh/add.html$','zshadd'),
    (r'^adminmobile/zsh/mod.html$','zshmod'),
    (r'^adminmobile/zsh/save.html$','zshsave'),
    (r'^adminmobile/zsh/tv.html$','qiandaotv'),
    (r'^adminmobile/zsh/qiandaolist.html$','qiandaolist'),
    (r'^adminmobile/zsh/newqiandao.html$','newqiandao'),
    (r'^adminmobile/zsh/zshdel.html$','zshdel'),
    
)

###
#----废料123后台
urlpatterns += patterns('zz91otherweb.admin123',
	(r'^feiliao123/visiturl.html$', 'visiturl'),
	(r'^feiliao123/admin.html$', 'default'),
	(r'^feiliao123/webtype.html$', 'webtype'),
	(r'^feiliao123/deletetype.html$', 'deletetype'),
	(r'^feiliao123/addwebtype.html$', 'addwebtype'),
	(r'^feiliao123/addwebtypeok.html$', 'addwebtypeok'),
	(r'^feiliao123/updatetype.html$', 'updatetype'),
	(r'^feiliao123/updatetypeok.html$', 'updatetypeok'),
	(r'^feiliao123/website.html$', 'website'),
	(r'^feiliao123/addwebsite.html$', 'addwebsite'),
	(r'^feiliao123/addwebsiteok.html$', 'addwebsiteok'),
	(r'^feiliao123/deleteweb.html$', 'deleteweb'),
	(r'^feiliao123/updateweb.html$', 'updateweb'),
	(r'^feiliao123/reduction.html$', 'reduction'),
	(r'^feiliao123/recommend.html$', 'recommend'),
	(r'^feiliao123/cancelrecommend.html$', 'cancelrecommend'),
	(r'^feiliao123/returnpage.html$', 'returnpage'),
	(r'^feiliao123/upload.html$', 'upload'),
	(r'^feiliao123/imgload.html$', 'imgload'),
	#---来电宝,可添加文章
	(r'^feiliao123/webartical.html$', 'webartical'),
	(r'^feiliao123/addwebartical.html$', 'addwebartical'),
	(r'^feiliao123/addwebarticalok.html$', 'addwebarticalok'),
	(r'^feiliao123/update_artical.html$', 'update_artical'),
	#----数据分析
	(r'^feiliao123/dataout.html$', 'dataout'),
	(r'^feiliao123/analyse.html$', 'analyse'),
	(r'^feiliao123/analysischart.html$', 'analysischart'),
	(r'^feiliao123/analyse_pageout.html$', 'analyse_pageout'),
	(r'^feiliao123/analyse_page.html$', 'analyse_page'),
	(r'^feiliao123/analyse_type.html$', 'analyse_type'),
	(r'^feiliao123/add_type.html$', 'add_type'),
	(r'^feiliao123/add_typeok.html$', 'add_typeok'),
	(r'^feiliao123/del_type.html$', 'del_type'),
	(r'^feiliao123/jumpout.html$', 'jumpout'),
	(r'^feiliao123/datalogin.html$', 'datalogin'),
	(r'^feiliao123/logdetail.html$', 'logdetail'),
	(r'^feiliao123/deldata.html$', 'deldata'),
	(r'^feiliao123/sendmials.html$', 'sendmials'),
	(r'^feiliao123/mailto.html$', 'mailto'),
	(r'^feiliao123/dialogs/image/image.html$', 'mailimg'),
	(r'^feiliao123/mailloadimg.html$', 'mailloadimg'),
	(r'^feiliao123/deldatasis.html$', 'deldatasis'),
	(r'^feiliao123/ipvisit.html$', 'ipvisit'),
	(r'^feiliao123/ipvisitout.html$', 'ipvisitout'),
	(r'^feiliao123/delipvisit.html$', 'delipvisit'),
	(r'^feiliao123/pagedetail.html$', 'pagedetail'),
	
	
	#----图表
	(r'^feiliao123/tongji_chart.html$', 'tongji_chart'),
	#----百度收录查询
	(r'^feiliao123/baiduincluded.html$', 'baiduincluded'),
	(r'^feiliao123/baiduincluded2.html$', 'baiduincluded2'),
	
	(r'^feiliao123/page404.html$', 'page404'),
	(r'^feiliao123/deletepage404.html$', 'deletepage404'),
	#上传文件
	(r'^feiliao123/uploadfileadmin.html$', 'uploadfileadmin'),
	(r'^feiliao123/uploadfileok.html$', 'uploadfileok'),
	#删除已上传的文件
	(r'^feiliao123/del_this_file.html$', 'del_this_file'),
	#敏感词
	(r'^feiliao123/mingang.html$', 'mingang'),
)
#----互助
urlpatterns += patterns('zz91otherweb.huzhu',
	(r'^feiliao123/huzhu_artical.html$', 'artical'),
	(r'^feiliao123/huzhu_arttype.html$', 'arttype'),
	(r'^feiliao123/huzhu_detail.html$', 'detail'),
	(r'^feiliao123/huzhu_addartical.html$', 'addartical'),
	(r'^feiliao123/huzhu_addarticalok.html$', 'addarticalok'),
	(r'^feiliao123/huzhu_updateartical.html$', 'updateartical'),
	(r'^feiliao123/huzhu_delartical.html$', 'delartical'),
)
#----资讯中心
urlpatterns += patterns('zz91otherweb.news',
	(r'^feiliao123/getquickart.html$', 'getquickart'),
	(r'^feiliao123/updatequickok.html$', 'updatequickok'),
	(r'^feiliao123/update_aqsiq.html$', 'update_aqsiq'),
	(r'^feiliao123/artical.html$', 'artical'),
	(r'^feiliao123/aqsiqdetail(?P<id>\d+).htm$', 'aqsiqdetail'),
	(r'^feiliao123/del_aqsiq.html$', 'del_aqsiq'),
	(r'^feiliao123/addartical.html$', 'addartical'),
	(r'^feiliao123/addarticalok.html$', 'addarticalok'),
	(r'^feiliao123/newsadmin.html$', 'newsadmin'),
	(r'^feiliao123/newsadmin2.html$', 'newsadmin2'),
	(r'^feiliao123/newstype.html$', 'newstype'),
	(r'^feiliao123/addnews.html$', 'addnews'),
	(r'^feiliao123/addnewsok.html$', 'addnewsok'),
	(r'^feiliao123/addnewstype.html$', 'addnewstype'),
	(r'^feiliao123/addnewstypeok.html$', 'addnewstypeok'),
	(r'^feiliao123/delete_newstype.html$', 'delete_newstype'),
	(r'^feiliao123/delete_newstype.html$', 'delete_newstype'),
	(r'^feiliao123/update_newstype.html$', 'update_newstype'),
	(r'^feiliao123/delnews.html$', 'delnews'),
	(r'^feiliao123/newsout.html$', 'newsout'),
	(r'^feiliao123/updateartical.html$', 'updateartical'),
	(r'^feiliao123/del_all_zz91.html$', 'del_all_zz91'),#zz91资讯一键删除
	(r'^feiliao123/back_newsall.html$', 'back_newsall'),
	#----报价资讯
	(r'^feiliao123/source_list.html$', 'source_list'),
	(r'^feiliao123/source_type.html$', 'source_type'),
)
#----手机站
urlpatterns += patterns('zz91otherweb.mobile',
	(r'^feiliao123/delastdbsimp.html$', 'delastdbsimp'),
	#----互助
	(r'^feiliao123/huzhu.html$', 'huzhu'),
	(r'^feiliao123/replylist.html$', 'replylist'),
	(r'^feiliao123/pushtype.html$', 'pushtype'),
	(r'^feiliao123/add_bbs_post.html$', 'add_bbs_post'),
	(r'^feiliao123/add_bbs_postok.html$', 'add_bbs_postok'),
	(r'^feiliao123/update_bbs_post.html$', 'update_bbs_post'),
	(r'^feiliao123/del_bbs_post.html$', 'del_bbs_post'),
    #展会直播
    (r'^feiliao123/zhibo.html$', 'zhibo'),
    (r'^feiliao123/zhibo_add.html$', 'zhibo_add'),
    (r'^feiliao123/zhibo_save.html$', 'zhibo_save'),
    (r'^feiliao123/zhibo_mod.html$', 'zhibo_mod'),
    (r'^feiliao123/zhibo_del.html$', 'zhibo_del'),
	#---支付订单
	(r'^feiliao123/pay_order.html$', 'pay_order'),
	#----微信
	(r'^feiliao123/weixinscore.html$', 'weixinscore'),
	(r'^feiliao123/scoreexchange.html$', 'scoreexchange'),
	(r'^feiliao123/accountscore.html$', 'accountscore'),
	(r'^feiliao123/addweixinscore.html$', 'addweixinscore'),
	(r'^feiliao123/addweixinscoreok.html$', 'addweixinscoreok'),
	(r'^feiliao123/exchangetype.html$', 'exchangetype'),
	(r'^feiliao123/addexchangetype.html$', 'addexchangetype'),
	(r'^feiliao123/addexchangetypeok.html$', 'addexchangetypeok'),
	(r'^feiliao123/updatexchangetype.html$', 'updatexchangetype'),
	(r'^feiliao123/delexchangetype.html$', 'delexchangetype'),
	(r'^feiliao123/upchangetype_close.html$', 'upchangetype_close'),
	#----手机钱包
	(r'^feiliao123/paytype.html$', 'paytype'),
	(r'^feiliao123/addpaytype.html$', 'addpaytype'),
	(r'^feiliao123/addpaytypeok.html$', 'addpaytypeok'),
	(r'^feiliao123/updatepaytype.html$', 'updatepaytype'),
	(r'^feiliao123/delpaytype.html$', 'delpaytype'),
	(r'^feiliao123/addchongzhi.html$', 'addchongzhi'),
	(r'^feiliao123/addchongzhiok.html$', 'addchongzhiok'),
	(r'^feiliao123/delqbyzm.html$', 'delqbyzm'),
	(r'^feiliao123/redelqb.html$', 'redelqb'),
	
	(r'^feiliao123/getcompanyid.html$', 'getcompanyid'),
	(r'^feiliao123/getfromaccounttocompanyid.html$', 'getfromaccounttocompanyid'),
	#----手机钱包商城
	(r'^feiliao123/shop_product.html$', 'shop_product'),
	(r'^feiliao123/addshop_product.html$', 'addshop_product'),
	(r'^feiliao123/addshop_productok.html$', 'addshop_productok'),
	(r'^feiliao123/delshop_product.html$', 'delshop_product'),
	(r'^feiliao123/updateshop_product.html$', 'updateshop_product'),
	
	(r'^feiliao123/shop_llb_keywords.html$', 'shop_llb_keywords'),
	(r'^feiliao123/delshop_llb_keywords.html$', 'delshop_llb_keywords'),
	
	(r'^feiliao123/shop_reflush.html$', 'shop_reflush'),
	(r'^feiliao123/addshop_reflush.html$', 'addshop_reflush'),
	(r'^feiliao123/addshop_reflushok.html$', 'addshop_reflushok'),
	(r'^feiliao123/delshop_reflush.html$', 'delshop_reflush'),
	(r'^feiliao123/updateshop_reflush.html$', 'updateshop_reflush'),
	
	(r'^feiliao123/update_prorank.html$', 'update_prorank'),
	(r'^feiliao123/update_prorankok.html$', 'update_prorankok'),
	(r'^feiliao123/del_prorank.html$', 'del_prorank'),
	(r'^feiliao123/upshop_product2.html$', 'upshop_product2'),
	(r'^feiliao123/shop_baoming.html$', 'shop_baoming'),
	#钱包充值广告
	(r'^feiliao123/qianbao_gg.html$', 'qianbao_gg'),
	(r'^feiliao123/updateqbgg.html$', 'updateqbgg'),
	(r'^feiliao123/updateqbggok.html$', 'updateqbggok'),
	#----举报信息
	(r'^feiliao123/report.html$', 'report'),
	#----充值,消费金额
	(r'^feiliao123/outfee.html$', 'outfee'),
	#----充值金额走势图
	(r'^feiliao123/chongzhichart.html$', 'chongzhichart'),
	(r'^feiliao123/chongzhicharturl.html$', 'chongzhicharturl'),
	(r'^feiliao123/sunfeechart.html$', 'sunfeechart'),
	#----账户余额
	(r'^feiliao123/blance.html', 'blance'),
	
	#----2016双11砍价
	(r'^feiliao123/kanjia-index.html', 'kanjia_prolist'),
	(r'^feiliao123/kanjia-baoming.html', 'kanjia_baoming'),
	(r'^feiliao123/kanjia-history.html', 'kanjia_history'),
)
#----手机app
urlpatterns += patterns('zz91otherweb.app',
	(r'^feiliao123/messagelist.html$', 'messagelist'),
	(r'^feiliao123/addmessage.html$', 'addmessage'),
	(r'^feiliao123/addmessageok.html$', 'addmessageok'),
	(r'^feiliao123/updatemessage.html$', 'updatemessage'),
	(r'^feiliao123/delmessage.html$', 'delmessage'),
	(r'^feiliao123/appinstalluser.html$', 'appinstalluser'),
	(r'^feiliao123/telchecklist.html$', 'telchecklist'),
	(r'^feiliao123/installchart.html$', 'installchart'),
	(r'^feiliao123/installcharturl.html$', 'installcharturl'),
    
    (r'^feiliao123/installchart.html$', 'installchart'),
    (r'^feiliao123/installcharturl.html$', 'installcharturl'),
    (r'^feiliao123/activechart.html$', 'activechart'),
    (r'^feiliao123/activecharturl.html$', 'activecharturl'),
    
    #微信后台管理
    (r'^feiliao123/weixinlist.html$', 'weixinlist'),
    (r'^feiliao123/send_service_message.html$', 'send_service_message'),
    (r'^feiliao123/send_other_message.html$', 'send_other_message'),
    
    
	(r'^feiliao123/userKeywords.html$', 'userKeywords'),
	
	#抢购首页
	(r'^feiliao123/qianggou.html$', 'qianggou'),
	#-----以下是抢购商品表(goods)
	#增加抢购商品
	(r'^feiliao123/add_goods.html$', 'add_goods'),
	(r'^feiliao123/add_goods_ok.html$','add_goods_ok'),
	#查看抢购商品表
	(r'^feiliao123/list_goods.html$', 'list_goods'),
	(r'^feiliao123/edit_goods.html$', 'edit_goods'),
	(r'^feiliao123/edit_goods_ok.html$','edit_goods_ok'),
	#上架操作
	(r'^feiliao123/turn_on.html$', 'turn_on'),
	(r'^feiliao123/delgoods.html$', 'delgoods'),
	#下架操作
	(r'^feiliao123/turn_off.html$', 'turn_off'),
	#推荐操作
	(r'^feiliao123/tuijian_on.html$', 'tuijian_on'),
	#取消推荐操作
	(r'^feiliao123/tuijian_off.html$', 'tuijian_off'),
	
	#-----以下是抢购订单表(orderForm)
	#查看订单
	(r'^feiliao123/list_order.html$', 'list_order'),
	#退回订单操作
	(r'^feiliao123/tuihui.html$', 'tuihui'),
	#成功订单操作
	(r'^feiliao123/success.html$', 'success'),
	
	#-----以下是app推送
	(r'^feiliao123/app_pushlist.html$', 'app_pushlist'),
	(r'^feiliao123/add_push.html$', 'add_push'),
	(r'^feiliao123/add_pushok.html$', 'add_pushok'),
	(r'^feiliao123/update_app_push.html$', 'update_app_push'),
	(r'^feiliao123/delthispush.html$', 'delthispush'),
	
	#---钱包优惠管理	
	(r'^feiliao123/list_qianbao_gg.html$', 'list_qianbao_gg'),
	#--添加
	(r'^feiliao123/add_qianbao_gg.html$', 'add_qianbao_gg'),
	(r'^feiliao123/add_qianbao_ggok.html$', 'add_qianbao_ggok'),
	#--编辑
	(r'^feiliao123/edit_this_gg.html$', 'edit_this_gg'),
	(r'^feiliao123/edit_this_ggok.html$', 'edit_this_ggok'),
	#--删除
	(r'^feiliao123/del_this_gg.html$', 'del_this_gg'),
	#--钱包广告开关操作
	(r'^feiliao123/flag_on.html$', 'flag_on'),#开
	(r'^feiliao123/flag_off.html$', 'flag_off'),#关
	#移动抽奖
	(r'^feiliao123/choujiang.html$', 'choujiang'),
	(r'^feiliao123/add_choujiang.html$', 'add_choujiang'),#手动添加
	(r'^feiliao123/add_choujiangok.html$', 'add_choujiangok'),#手动添加确认
	(r'^feiliao123/edit_this_cj.html$', 'edit_this_cj'),#编辑
	(r'^feiliao123/del_this_cj.html$', 'del_this_cj'),#删除
)

#----微门户关键词库
urlpatterns += patterns('zz91otherweb.weimenhu',
	#所有关键字
	(r'^feiliao123/key_list.html$', 'key_list'),
	(r'^feiliao123/key_daoru.html$', 'key_daoru'),
	(r'^feiliao123/key_mod.html$', 'key_mod'),
	(r'^feiliao123/key_save.html$', 'key_save'),
	(r'^feiliao123/key_listsave.html$', 'key_listsave'),
	(r'^feiliao123/key_tongji.html$', 'key_tongji'),
	(r'^feiliao123/key_list_del.html$', 'key_list_del'),
	(r'^feiliao123/huifu_ok_all.html$', 'huifu_ok_all'),
	(r'^feiliao123/shenhe_ok.html$', 'shenhe_ok'),
	(r'^feiliao123/shenhe_no.html$', 'shenhe_no'),
	(r'^feiliao123/delthis.html$', 'delthis'),
    (r'^feiliao123/shenhe_ok_all.html$', 'shenhe_ok_all'),#一键审核
    (r'^feiliao123/del_all1.html$', 'del_all1'),#一键删除1
	
	#未审核客户搜索关键字
	(r'^feiliao123/key_nocheck.html$', 'key_nocheck'),
	(r'^feiliao123/status_ok.html$', 'status_ok'),
	(r'^feiliao123/status_no.html$', 'status_no'),
	(r'^feiliao123/del_this.html$', 'del_this'),
	(r'^feiliao123/pushtype1.html$', 'pushtype1'),
    (r'^feiliao123/shenhe_ok_all2.html$', 'shenhe_ok_all2'),#一键审核2
    (r'^feiliao123/del_all2.html$', 'del_all2'),#一键删除2
    
    #导出数据
    (r'^feiliao123/deleted_keywords_export.html$', 'deleted_keywords_export'),#导出回收战数据（按时间）
    (r'^feiliao123/export_who_selected.html$', 'export_who_selected'),#导出回收战数据（按时间）
)
#----zz91帮助中心
urlpatterns += patterns('zz91otherweb.help',
	(r'^feiliao123/help_artical.html$', 'help_artical'),#帮助中心列表页
	(r'^feiliao123/help_column.html$', 'help_column'),#栏目页
	(r'^feiliao123/add_father_column.html$', 'add_father_column'),#添加父栏目
	(r'^feiliao123/add_father_columnok.html$', 'add_father_columnok'),#添加父栏目成功
	(r'^feiliao123/help_returnpage.html$', 'help_returnpage'),#返回列表页
	(r'^feiliao123/delete_column.html$', 'delete_column'),#删除栏目
	(r'^feiliao123/addhelpartical.html$', 'addhelpartical'),#添加或修改页面
	(r'^feiliao123/addhelparticalok.html$', 'addhelparticalok'),#添加或修改页面确认
	(r'^feiliao123/deletehelpartical.html$', 'deletehelpartical'),#删除确认
)

#----数据分析
urlpatterns += patterns('zz91otherweb.data',
	(r'^feiliao123/delcompro.html$', 'delcompro'),
	(r'^feiliao123/delkwdsearch.html$', 'delkwdsearch'),
	(r'^feiliao123/compro_check.html$', 'compro_check'),
	(r'^feiliao123/upcompro_check.html$', 'upcompro_check'),
	(r'^feiliao123/search_keywords.html$', 'search_keywords'),
	(r'^feiliao123/loadfile.html$', 'loadfile'),
	(r'^feiliao123/logindata.html$', 'logindata'),
	(r'^feiliao123/getpublishdata.html$', 'getpublishdata'),
	(r'^feiliao123/publishdata.html$', 'publishdata'),
	(r'^feiliao123/publishdetaildata.html$', 'publishdetaildata'),
	(r'^feiliao123/keywordssearchdata.html$', 'keywordssearchdata'),
	(r'^feiliao123/keywordsscreening.html$', 'keywordsscreening'),
	(r'^feiliao123/huanbaolist.html$', 'huanbaolist'),
	(r'^feiliao123/del_all_huanbaolist.html$', 'del_all_huanbaolist'),#环保资讯一键删除
	(r'^feiliao123/huanbaodetail(?P<id>\d+).htm$', 'huanbaodetail'),
	#---非法关键词
	(r'^feiliao123/feifa_list.html$','feifa_list'),
	(r'^feiliao123/feifa_add.html$','feifa_add'),
	(r'^feiliao123/feifa_save.html$','feifa_save'),
	(r'^feiliao123/feifa_mod.html$','feifa_mod'),
	(r'^feiliao123/feifa_del.html$','feifa_del'),
	(r'^feiliao123/feifa_daoru.html$','feifa_daoru'),
	(r'^feiliao123/feifa_update.html$','feifa_update'),
	(r'^feiliao123/feifa_daochu.html$','feifa_daochu'),
	(r'^feiliao123/feifa_listsave.html$','feifa_listsave'),
	
)
#----抓取日志
urlpatterns += patterns('zz91otherweb.log',
	(r'^feiliao123/log_type.html$', 'log_type'),
	(r'^feiliao123/log_list.html$', 'log_list'),
	(r'^feiliao123/del_log.html$', 'del_log'),
	(r'^feiliao123/addlogtype.html$', 'addlogtype'),
	(r'^feiliao123/addlogtypeok.html$', 'addlogtypeok'),
	(r'^feiliao123/updatelogtype.html$', 'updatelogtype'),
	(r'^feiliao123/lognews.html$', 'lognews'),
	(r'^feiliao123/addlognews.html$', 'addlognews'),
	(r'^feiliao123/addlognewsok.html$', 'addlognewsok'),
	(r'^feiliao123/updatelognews.html$', 'updatelognews'),
	(r'^feiliao123/updlog_isok.html$', 'updlog_isok'),
	(r'^feiliao123/updlog_isok2.html$', 'updlog_isok2'),
	#来电宝日志
	(r'^feiliao123/ppc/log.html$', 'ppc_log'),
	
	(r'^feiliao123/appUserlog.html$', 'appUserlog'),
	(r'^feiliao123/zz91logall.html$', 'zz91logall'),
	(r'^feiliao123/errlog.html$', 'errlog'),
)

urlpatterns += patterns('zz91otherweb.myrc',
	(r'^feiliao123/operatype.html$', 'operatype'),
	(r'^feiliao123/operadata.html$', 'operadata'),
	(r'^feiliao123/delopera.html$', 'delopera'),
)
urlpatterns += patterns('zz91otherweb.vote',
	(r'^feiliao123/vote_list.html$', 'vote_list'),
	(r'^feiliao123/vote_add.html$', 'vote_add'),
	(r'^feiliao123/vote_save.html$', 'vote_save'),
	(r'^feiliao123/vote_edit.html$', 'vote_edit'),
	(r'^feiliao123/vote_del.html$', 'vote_del'),
	(r'^feiliao123/vote_log.html$', 'vote_log'),
	(r'^feiliao123/vote_addnum.html$', 'vote_addnum'),
	(r'^feiliao123/vote_log_del.html$', 'vote_log_del'),
	(r'^feiliao123/ybp_admin_userlist.html$', 'ybp_admin_userlist'),
	(r'^feiliao123/ybp_vote_detail.html$', 'ybp_vote_detail'),
	
)
#----行情报价
urlpatterns += patterns('zz91otherweb.price',
	(r'^feiliao123/price_category.html$', 'price_category'),
	(r'^feiliao123/price_category_attr.html$', 'price_category_attr'),
	(r'^feiliao123/price_table_header.html$', 'price_table_header'),
	
	(r'^feiliao123/add_priceattr.html$', 'add_priceattr'),
	(r'^feiliao123/add_priceattrok.html$', 'add_priceattrok'),
	(r'^feiliao123/update_priceattr.html$', 'update_priceattr'),
	(r'^feiliao123/del_priceattr.html$', 'del_priceattr'),
	(r'^feiliao123/getc_label.html$', 'getc_label'),
	(r'^feiliao123/price_category_field.html$', 'price_category_field'),
	(r'^feiliao123/add_pricefield.html$', 'add_pricefield'),
	(r'^feiliao123/add_pricefieldok.html$', 'add_pricefieldok'),
	(r'^feiliao123/update_pricefield.html$', 'update_pricefield'),
	(r'^feiliao123/del_pricefield.html$', 'del_pricefield'),
)
#----地磅系统
urlpatterns += patterns('zz91otherweb.dibang',
	#公司列表
	(r'^feiliao123/dibang/company_list.html$', 'company_list'),
	(r'^feiliao123/dibang/company_add.html$', 'company_add'),
	(r'^feiliao123/dibang/company_del.html$', 'company_del'),
	(r'^feiliao123/dibang/company_mod.html$', 'company_mod'),
	(r'^feiliao123/dibang/company_save.html$', 'company_save'),
	#人员管理
	(r'^feiliao123/dibang/user_list.html$', 'user_list'),
	(r'^feiliao123/dibang/user_add.html$', 'user_add'),
	(r'^feiliao123/dibang/user_del.html$', 'user_del'),
	(r'^feiliao123/dibang/user_mod.html$', 'user_mod'),
	(r'^feiliao123/dibang/user_save.html$', 'user_save'),
	#入库管理
	(r'^feiliao123/dibang/storage_list.html$', 'storage_list'),
	(r'^feiliao123/dibang/storage_add.html$', 'storage_add'),
	(r'^feiliao123/dibang/storage_del.html$', 'storage_del'),
	(r'^feiliao123/dibang/storage_mod.html$', 'storage_mod'),
	(r'^feiliao123/dibang/storage_save.html$', 'storage_save'),
	#集团管理
	(r'^feiliao123/dibang/group_list.html$', 'group_list'),
	(r'^feiliao123/dibang/group_add.html$', 'group_add'),
	(r'^feiliao123/dibang/group_del.html$', 'group_del'),
	(r'^feiliao123/dibang/group_mod.html$', 'group_mod'),
	(r'^feiliao123/dibang/group_save.html$', 'group_save'),
	#供应商管理
	(r'^feiliao123/dibang/supplier_list.html$', 'supplier_list'),
	(r'^feiliao123/dibang/supplier_add.html$', 'supplier_add'),
	(r'^feiliao123/dibang/supplier_del.html$', 'supplier_del'),
	(r'^feiliao123/dibang/supplier_mod.html$', 'supplier_mod'),
	(r'^feiliao123/dibang/supplier_save.html$', 'supplier_save'),
	#产品信息管理
	(r'^feiliao123/dibang/product_list.html$', 'product_list'),
	(r'^feiliao123/dibang/product_add.html$', 'product_add'),
	(r'^feiliao123/dibang/product_del.html$', 'product_del'),
	(r'^feiliao123/dibang/product_mod.html$', 'product_mod'),
	(r'^feiliao123/dibang/product_save.html$', 'product_save'),
	#废品类别管理
	(r'^feiliao123/dibang/category_list.html$', 'category_list'),
	(r'^feiliao123/dibang/category_add.html$', 'category_add'),
	(r'^feiliao123/dibang/category_del.html$', 'category_del'),
	(r'^feiliao123/dibang/category_mod.html$', 'category_mod'),
	(r'^feiliao123/dibang/category_save.html$', 'category_save'),
	
)

urlpatterns += patterns('zz91otherweb.automation',
	(r'^feiliao123/automation.html$', 'feisuliao'),
	(r'^feiliao123/feisuliao.html$', 'feisuliao'),
	(r'^feiliao123/suliao_price.html$', 'suliao_price'),
	(r'^feiliao123/suliao_net_price.html$', 'suliao_net_price'),
	(r'^feiliao123/suliao_zaocanwanbao.html$', 'zaocanwanbao'),
	(r'^feiliao123/net_price.html$', 'net_price'),
	(r'^feiliao123/suliao_duanxin_price.html$', 'duanxin_price'),
	(r'^feiliao123/huanbao.html$', 'huanbao'),
	(r'^feiliao123/huanbao_check.html$', 'huanbao_check'),
	(r'^feiliao123/suliao_week_price.html$', 'week_price'),
	(r'^feiliao123/chartdata.html$', 'chartdata'),
	(r'^feiliao123/area_price.html$', 'area_price'),
)

urlpatterns += patterns('zz91otherweb.useradmin',
	(r'^feiliao123/login.html$', 'login'),
	(r'^feiliao123/logout.html$', 'logout'),
	(r'^feiliao123/loginpage.html$', 'loginpage'),
)

urlpatterns += patterns('zz91otherweb.adminmobile',
	(r'^adminmobile/index.html$', 'index'),
	(r'^adminmobile/login.html$', 'login'),
	(r'^adminmobile/loginsave.html$', 'loginsave'),
	(r'^adminmobile/logout.html$', 'logout'),
	(r'^adminmobile/loginpage.html$', 'loginpage'),
	
	(r'^adminmobile/trade.html$', 'trade'),
	(r'^adminmobile/editpro.html$', 'editpro'),
	(r'^adminmobile/editcompany.html$', 'editcompany'),
	(r'^adminmobile/procontent.html$', 'procontent'),
	(r'^adminmobile/editpic.html$', 'editpic'),
	(r'^adminmobile/category.html$', 'category'),
	(r'^adminmobile/savecontent.html$', 'savecontent'),
	(r'^adminmobile/companycontent.html$', 'companycontent'),
	(r'^adminmobile/companybusiness.html$', 'companybusiness'),
	
	(r'^adminmobile/paylist.html$', 'paylist'),
	(r'^adminmobile/chongzhi.html$', 'chongzhi'),
	(r'^adminmobile/savechongzhi.html$', 'savechongzhi'),
	(r'^adminmobile/outfee.html$', 'outfee'),
	(r'^adminmobile/huzhu.html$', 'huzhu'),
	(r'^adminmobile/del_bbs_post.html$', 'del_bbs_post'),
	
	(r'^adminmobile/shop_product.html$', 'shop_product'),
	(r'^adminmobile/update_prorank.html$', 'update_prorank'),
	(r'^adminmobile/update_prorankok.html$', 'update_prorankok'),
	
	(r'^adminmobile/chongzhisearch.html$', 'chongzhisearch'),
	(r'^adminmobile/servicelist.html$','servicelist'),
	
)

#----留言速配服务管理
urlpatterns += patterns('zz91otherweb.qunfa',
	(r'^feiliao123/qunfa_list.html$', 'qunfa_list'),
	(r'^feiliao123/qunfa_record.html$', 'qunfa_record'),
	(r'^feiliao123/qunfa_manage.html$', 'qunfa_manage'),
	(r'^feiliao123/qunfa_match_keywords.html$', 'match_keywords'),
	(r'^feiliao123/qunfa_add_task.html$', 'add_task'),
	(r'^feiliao123/qunfa_fix_task.html$', 'fix_task'),
)

#---css引入
urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)