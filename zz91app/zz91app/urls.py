#from django.conf.urls import patterns, include, url
from django.conf.urls import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#----首页消息推送
urlpatterns = patterns('zz91app.views',
    (r'^getuser/$', 'getuser'),
    (r'^$', 'default'),
    (r'^index.html$', 'index'),
    (r'^index_ios.html$', 'index_ios'),
    (r'^index_new.html$', 'index_new'),
    (r'^bottom.html$', 'bottom'),
    (r'^top.html$', 'top'),
    (r'^trade.html$', 'trade'),
    (r'^question/list.html$', 'question'),
    
    (r'^appbody.html$', 'appbody'),
    (r'^newslist/$', 'newslist'),
    (r'^messagesindex.html$', 'messagesindex'),
    (r'^messagesnoview.html$', 'messagesnoview'),
    (r'^messagelist/$', 'messagesindex'),
    (r'^messagelistmongo.html$', 'messagelistmongo'),
    (r'^messagelist.html$', 'messagelist'),
    (r'^messagelistview/$', 'messagelistview'),
    (r'^messagescount.html$', 'messagescount'),
    (r'^messagesreadall.html$', 'messagesreadall'),
    (r'^qianbaolist/$', 'qianbaolist'),
    (r'^orderlist/$', 'orderlist'),
    (r'^changeidview/$', 'changeidview'),
    (r'^fk.html$', 'fk'),
    (r'^feedbacksave.html$', 'feedbacksave'),
    (r'^load.html$', 'load'),
    (r'^set.html$', 'set'),
    (r'^set_ios.html$', 'set_ios'),
    (r'^tongji/t.html$', 'tongji'),
    
    #--留言
    (r'^msg/list.html$', 'leavewordslist'),
    (r'^msg/chatimgupload.html$', 'chatimgupload'),
    
    
    
    (r'^robots.txt$', 'robots'),
    (r'^gethtml.html', 'gethtml'),
    (r'^getuserkeywords.html', 'getuserkeywords'),
    (r'^getweburl.html', 'getweburl'),
    (r'^invite/invite.html', 'invite'),
    (r'^invite/invite_save.html', 'invite_save'),
    (r'^invite/myinvite.html', 'myinvite'),
    
    #app推送
    (r'^app_pushlist.html$', 'app_pushlist'),
    (r'^app_choice_industry.html$', 'app_choice_industry'),
    (r'^app_choice_industryok.html$', 'app_choice_industryok'),
    (r'^updateerrlog.html$', 'updateerrlog'),
    
)
#业务工单
urlpatterns += patterns('zz91app.gd',
    #---后台
    (r'^gd/list.html$','gd_list'),#所有工单
    (r'^gd/add.html$','gd_add'),#添加工单
    (r'^gd/reply.html$','gd_reply'),
    (r'^gd/replysave.html$','gd_replysave'),
    (r'^gd/save.html$','gd_save'),#添加工单
    (r'^gd/details.html$','gd_details'),#工单详情
    (r'^gd/station.html$','gd_station'),#工单状态
    (r'^gd/answer.html$','gd_answer'),#回复
    (r'^gd/noview.html$','gd_noview'),#
    
)
#服务中心
urlpatterns += patterns('zz91app.help',
    (r'^help/$','index'),#
    (r'^help/index.html$','index'),#
    (r'^help/list.html$','list'),#
    (r'^help/detail.html$','detail'),#
)
#----来电宝
urlpatterns+=patterns('zz91app.ldb_weixin',
    #----来电宝首页
    (r'^laidianbao/$', 'laidianbao'),
    (r'^laidianbao/list-(?P<page>\d+).html$', 'laidianbao'),
    #----来电宝微信
    (r'^ldb_weixin/product_introduction.html$', 'product_introduction'),
    (r'^ldb_weixin/about.html$', 'about'),
    (r'^ldb_weixin/contact.html$', 'contact'),
    (r'^ldb_weixin/callanalysis.html$', 'callanalysis'),
    (r'^ldb_weixin/businessearch.html$', 'businessearch'),
    (r'^ldb_weixin/businessearchmore.html$', 'businessearchmore'),
    (r'^ldb_weixin/balance.html$', 'balance'),
    (r'^ldb_weixin/phonerecords.html$', 'phonerecords'),
    (r'^ldb_weixin/phonerecords-(?P<datearg>\d+).html$', 'phonerecords'),
    (r'^ldb_weixin/phonerecordsmore.html$', 'phonerecordsmore'),
    (r'^ldb_weixin/phoneclick.html$', 'phoneclick'),
    (r'^ldb_weixin/phoneclickmore.html$', 'phoneclickmore'),
    (r'^ldb_weixin/lookcontact.html$', 'lookcontact'),
    #---来电宝钱包首页
    (r'^ldb_weixin/index.html$', 'index'),
)
#----供求
urlpatterns += patterns('zz91app.trade',
    (r'^category/$', 'category'),
    (r'^detail/$', 'detail'),
    (r'^offerlist/$', 'offerlist'),
    (r'^leavewords_save/$', 'leavewords_save'),
    (r'^favorite/$', 'favorite'),
    (r'^fj.html$', 'fj'),
    (r'^post.html$', 'post'),
    (r'^products_save.html$', 'products_save'),
    
    (r'^post_save.html$', 'post_save'),
    
    (r'^tradeimgupload.html$', 'tradeimgupload'),
    (r'^otherimgupload.html$', 'otherimgupload'),
    (r'^msg/leavewordsuploadimg.html$', 'leavewordsuploadimg'),
    
    (r'^trade/pricelist.html$', 'pricelist'),
    (r'^viewcontact.html$', 'viewcontact'),
    (r'^pro_report.html$', 'pro_report'),
    (r'^offerlistside.html$', 'offerlistside'),
    (r'^offerlistside_cate.html$', 'offerlistside_cate'),
    (r'^productsimglist.html$', 'productsimglist'),
    (r'^trade/xgkeywords.html$', 'xgkeywords'),
    (r'^trade/viewhistory.html$', 'viewhistory'),
    (r'^trade/user_tongjidata.html$', 'user_tongjidata'),
    (r'^trade/showcontact.html$', 'showcontact'),
    
)
#----报价
urlpatterns += patterns('zz91app.price',
    (r'^priceviews/$', 'details'),
    (r'^priceindex/$', 'index'),
    (r'^price/$', 'pricelist'),
    (r'^price/companypricelist.html$', 'companypricelist'),
    (r'^price/companyprice_detail.html$', 'companyprice_detail'),
    (r'^price/companycategory.html$', 'companycategory'),
    (r'^price/companyprice_save.html$', 'companyprice_save'),
    
    
    (r'^pricemore/$', 'pricemore'),
    (r'^price/pricechart.html$', 'pricechart'),
    (r'^price/pricechartdata.html$', 'pricechartdata'),
    (r'^price/studylist.html$', 'studylist'),
    (r'^price/study_detail.html$', 'study_detail'),
    
    
    
    (r'^price/(?P<category_id>\d+).html$', 'pricelist'),
    (r'^price/p(?P<assist_id>\d+).html$', 'pricelist'),
    (r'^pricemore/(?P<category_id>\d+).html$', 'pricemore'),
    (r'^pricemore/p(?P<assist_id>\d+).html$', 'pricemore'),
    
    (r'^priceindex/jinshuarea/$', 'jinshuarea'),
    (r'^priceindex/qihuo/$', 'qihuo'),
    (r'^priceindex/youse/$', 'youse'),
    (r'^priceindex/suliaoarea/$', 'suliaoarea'),
    (r'^priceindex/suliaoxinliao/$', 'suliaoxinliao'),
    (r'^priceindex/areasuliao/$', 'areasuliao'),
    (r'^priceindex/suliaoqihuo/$', 'suliaoqihuo'),
    (r'^priceindex/suliaozaishengliao/$', 'suliaozaishengliao'),
    (r'^priceindex/meiguosuliao/$', 'meiguosuliao'),
    (r'^priceindex/ouzhousuliao/$', 'ouzhousuliao'),
    (r'^priceindex/suliaozaishengliao/$', 'suliaozaishengliao'),
    (r'^priceindex/feizhidongtai/$', 'feizhidongtai'),
    (r'^priceindex/feizhiarea/$', 'feizhiarea'),
    (r'^priceindex/feizhiriping/$', 'feizhiriping'),
    (r'^compriceviews/$', 'compdetails'),
)
#----资讯
urlpatterns += patterns('zz91app.news',
    (r'^news/$', 'newsindex'),
    (r'^news/columnlist.html$', 'newscolumnlist'),
    (r'^news/list.html$', 'news_list'),
    (r'^news/list-(?P<typeid>\w+).html$', 'news_list'),
    (r'^news/search.html$', 'news_search'),
    (r'^news/search-(?P<page>\d+).html$', 'news_search'),
    (r'^news/list-(?P<typeid>\w+)-(?P<page>\d+).html$', 'news_list'),
    (r'^news/newsdetail(?P<id>\d+).html$', 'newsdetail'),
    (r'^news/newsdetail(?P<id>\d+).htm$', 'newsdetail'),
)
#----sex
urlpatterns += patterns('zz91app.sex',
    (r'^sex/$', 'newsindex'),
    (r'^sex/list.html$', 'news_list'),
    (r'^sex/navlist.html$', 'navlist'),
    (r'^sex/mynavlist.html$', 'mynavlist'),
    (r'^sex/order.html$', 'order'),
    (r'^sex/list-(?P<typeid>\w+).html$', 'news_list'),
    (r'^sex/search.html$', 'news_search'),
    (r'^sex/search-(?P<page>\d+).html$', 'news_search'),
    (r'^sex/list-(?P<typeid>\w+)-(?P<page>\d+).html$', 'news_list'),
    (r'^sex/newsdetail(?P<id>\d+).html$', 'newsdetail'),
    #dedecms测试
    (r'^sex/show_memebe_stom.html$', 'show_memebe_stom'),#收藏夹显示
    (r'^sex/show_feedback.html$','show_feedback'),#评论表显示
    (r'^sex/show_myorder.html$', 'show_myorder'),#我的订阅显示
    (r'^sex/show_view_history.html$', 'show_view_history'),#最近浏览
    (r'^sex/show_member.html$', 'show_member'),
    (r'^sex/insert_member_guestbook.html$', 'insert_member_guestbook'),#插入至留言溥
    (r'^sex/insert_view_history.html$', 'insert_view_history'),#插入至浏览历史
    (r'^sex/insert_dede_feedback.html$', 'insert_dede_feedback'),
    (r'^sex/insert_myorder.html$', 'insert_myorder'),
    (r'^sex/insert_dede_member_stow.html$', 'insert_dede_member_stow'),
    (r'^sex/login.html$', 'login'),#登录
    (r'^sex/reg.html$', 'reg'),#注册
    (r'^sex/modinfo.html$', 'modinfo'),#
    (r'^sex/insert_feedback_goodbad.html$', 'insert_feedback_goodbad'),#
    (r'^sex/uploadface.html$', 'upload'),
)
#----互助
urlpatterns += patterns('zz91app.huzhu',
    (r'^huzhu/$', 'huzhu'),
    (r'^huzhumore/$', 'huzhumore'),
    (r'^huzhupost/$', 'huzhupost'),
    (r'^huzhu_imgload/$', 'huzhu_imgload'),
    (r'^huzhu_upload/$', 'huzhu_upload'),
    (r'^huzhupostsave/$', 'huzhupostsave'),
    (r'^huzhuview/(?P<id>\d+).htm$', 'huzhuview'),
    (r'^huzhuview/viewReply(?P<id>\d+).htm$', 'huzhuview'),
    (r'^huzhureplymore/$', 'replymore'),
    (r'^huzhu_replay/$', 'huzhu_replay'),
    (r'^reply_reply/$', 'reply_reply'),
    (r'^huzhu/recommend_add.html$', 'recommend_add'),
    (r'^huzhu/sharetoquan.html$', 'sharetoquan'),
    (r'^huzhu/newspinlun.html$', 'newspinlun'),
    (r'^huzhu/newspinlunsave.html$', 'newspinlunsave'),
    (r'^huzhu/app_quan.html$', 'app_quan'),
    
    
)
#----公司黄页
urlpatterns += patterns('zz91app.company',
    (r'^company/$', 'company'),
    (r'^companydetail/$', 'companydetail'),
    (r'^companyinfo/$', 'companyinfo'),
    (r'^companyproducts/$', 'companyproducts'),
    (r'^company/companyshop.html$', 'companyshop'),
    (r'^company/compinfo.html$', 'compinfo'),
    (r'^company/companyproductslist.html$', 'companyproductslist'),
    (r'^company/getcompanyidfromdomain.html$', 'getcompanyidfromdomain'),
)
#----生意管家
urlpatterns += patterns('zz91app.myrc',
    #----生意管家
    (r'^myrc_index/$', 'myrc_index'),
    (r'^myrc_mycommunity/$', 'myrc_mycommunity'),
    (r'^myrc_mycommunitydel/$', 'myrc_mycommunitydel'),
    (r'^myrc_mypost/$', 'myrc_mypost'),
    (r'^myrc/myguanzhu.html$', 'myrc_myguanzhu'),
    (r'^myrc_mypostsave/$', '.myrc_mypostsave'),
    (r'^myrc_myreply/$', 'myrc_myreply'),
    (r'^myrc_myreplysave/$', 'myrc_myreplysave'),
    (r'^openmessages/$', 'openmessages'),
    (r'^myrc_backquestion/$', 'myrc_backquestion'),
    (r'^myrc_backquestionsave/$', 'myrc_backquestionsave'),
    (r'^products_refresh/$', 'products_refresh'),
    (r'^products_refreshall/$', 'products_refreshall'),
    (r'^products_stop/$', 'products_stop'),
    (r'^products_start/$', 'products_start'),
    (r'^products_update/$', 'products_update'),
    (r'^myrc/del_productpic.html$', 'del_productpic'),
    
    #----我的收藏(一期)
    (r'^myrc_collect/$', 'myrc_collect'),
    (r'^myrc_collectmain/$', 'myrc_collectmain'),
    (r'^myrc_collectprice/$', 'myrc_collectprice'),
    (r'^myrc_leavewords/$', 'myrc_leavewords'),
    (r'^myrc_favorite/$', 'myrc_favorite'),
    (r'^myrc_products/$', 'myrc_products'),
    (r'^myrc/favoritedel.html$', 'del_favorite'),
    #----定制页面
    (r'^order/$', 'orderindex'),
    (r'^order/business.html$', 'orderbusiness'),
    (r'^order/price.html$', 'orderprice'),
    (r'^order/save_collect.html$', 'save_collect'),
    
    #---新版app 定制
    (r'^order/myorderprice.html$', 'myorderprice'),
    (r'^order/myorderprice_save.html$', 'myorderprice_save'),
    (r'^order/myorderprice_del.html$', 'myorderprice_del'),
    (r'^order/myordertrade_save.html$', 'myordertrade_save'),
    (r'^order/myordertrade.html$', 'myordertrade'),
    
    (r'^myrc/my_addressbook.html$', 'my_addressbook'),
    (r'^myrc/join_addressbook.html$', 'join_addressbook'),
    (r'^myrc/del_addressbook.html$', 'del_addressbook'),
    (r'^myrc/savecreditfile.html$', 'savecreditfile'),
    (r'^myrc/infocreditfile.html$', 'infocreditfile'),
    (r'^myrc/delcreditfile.html$', 'delcreditfile'),
    
    (r'^myrc/companyprice.html$', 'myrc_companyprice'),
    (r'^myrc/companyprice_edit.html$', 'myrc_companyprice_edit'),
    (r'^myrc/companyprice_save.html$', 'myrc_companyprice_save'),
    
    (r'^myrc/mycard.html$', 'mycard'),
    
    
    
)

#----再生钱包和抢购栏目
urlpatterns += patterns('zz91app.qianbao',
    (r'^qianbao/$', 'index'),
    (r'^qianbao/zhangdan.html$', 'zhangdan'),
    (r'^qianbao/zhangdannore.html$', 'zhangdannore'),
    (r'^qianbao/chongzhi.html$', 'chongzhi'),
    (r'^qianbao/chongzhi_new.html$', 'chongzhi_new'),
    (r'^qianbao/intxt.html$', 'intxt'),
    (r'^qianbao/outtxt.html$', 'outtxt'),
    (r'^qianbao/simptxt.html$', 'simptxt'),
    (r'^qianbao/shop.html$', 'shop'),
    (r'^qianbao/oflist.html$', 'oflist'),
    (r'^qianbao/offmore.html$', 'offmore'),
    (r'^qianbao/chongzhisuc.html$', 'chongzhisuc'),
    (r'^qianbao/qiandao.html$', 'qiandao'),
    (r'^qianbao/qianbaobaoblance.html$', 'qianbaobaoblance'),
    (r'^sendfee.html$', 'sendfee'),
    (r'^payfee.html$', 'payfee'),
    #---支付宝支付
    (r'^zz91pay.html$', 'zz91pay'),
    (r'^zz91paysubmit.html$', 'zz91paysubmit'),
    (r'^zz91payrequery.html$', 'zz91payrequery'),
    #---抢购栏目
    (r'^qianbao/qianbaopay.html$', 'qianbaopay'),
    (r'^qianbao/openservice.html$', 'openservice'),
    (r'^qianbao/voucherused.html$', 'voucherused'),
    
    (r'^qianbao/qg.html$', 'qg'), #再生钱包抢购页
    (r'^qianbao/qg_tourl.html$', 'qg_tourl'), #广告跳转
    (r'^qianbao/myservice.html$', 'myservice'), #我的服务
    (r'^qianbao/youhuilist.html$', 'youhuilist'), #优惠活动
    (r'^qianbao/mydaijinquan.html$', 'mydaijinquan'), #我的代金券
    (r'^qianbao/mydaijinquanlist.html$', 'mydaijinquanlist'), #我的代金券
    
    
    (r'^qianbao/jingjia_info.html$', 'jingjia_info'),
    (r'^qianbao/jingjia_keywords_save.html$', 'jingjia_keywords_save'),
    (r'^qianbao/jingjia_index.html$', 'jingjia_index'),
    (r'^qianbao/jingjia_keywords_info.html$', 'jingjia_keywords_info'),
    (r'^qianbao/jingjia_keywords_onesave.html$', 'jingjia_keywords_onesave'),
    (r'^qianbao/jingjia_keywords_offline.html$', 'jingjia_keywords_offline'),
    (r'^qianbao/jingjia_keywords_paylist.html$', 'jingjia_keywords_paylist'),
    (r'^qianbao/jingjia_keywords_clicklist.html$', 'jingjia_keywords_clicklist'),
    (r'^qianbao/jingjia_click_save.html$', 'jingjia_click_save'),
    
    
)

#----采购频道
urlpatterns += patterns('zz91app.trust',
    (r'^trust/list.html$', 'listcaigou'),
    #免费发布
    (r'^trust/supplyPub.html$', 'supplyPub'),
    (r'^trust/supplyPubok.html$', 'supplyPubok'),
    #我要供货
    (r'^trust/supplyForm.html$', 'supplyForm'),
    (r'^trust/supplyFormok.html$', 'supplyFormok'),
    #我的采购
    (r'^trust/listmycaigou.html$', 'listmycaigou'),
    #我的供货
    (r'^trust/listmysupply.html$', 'listmysupply'),
                        
)
#---产业带
urlpatterns += patterns('zz91app.ye',
    (r'^ye/(?P<big_category>\d+)/$', 'ye_list'),
    (r'^ye/(?P<big_category>\d+)/(?P<small_category>\d+).html$', 'ye_list'),#列表页
    (r'^ye/pro(?P<id>\d+).html$', 'ye_prolist'),
    (r'^ye/comp(?P<id>\d+).html$', 'ye_complist'),
    (r'^ye/ye_detail/(?P<ye_pinyin>\w+).html$', 'ye_detail'),#详细页
    (r'^ye/list_other_ye.html$','list_other_ye'),#查看其他相关产业带  list_other_ye_more
    (r'^ye/list_other_ye_more/$','list_other_ye_more'),#查看其他相关产业带
    (r'^ye/join_ye.html$','join_ye'),#加入产业带
    (r'^ye/quit_ye.html$','quit_ye'),#退出产业带
)


#----来电宝
urlpatterns += patterns('zz91app.laidianbao',
    (r'^laidianbao/$', 'laidianbao'),
    (r'^laidianbao/list-(?P<page>\d+).html$', 'laidianbao'),
)
#----用户登录
urlpatterns += patterns('zz91app.useradmin',
    (r'^login/$', 'login'),
    (r'^login1/$', 'login1'),
    (r'^logininfo.html$', 'logininfo'),
    (r'^logininfo1.html$', 'logininfo1'),
    (r'^loginout/$', 'loginout'),
    (r'^loginof.html$', 'loginsave'),
    (r'^loginok/$', 'loginok'),
    (r'^reg.html$', 'reg'),
    (r'^regsave.html$', 'regsave'),
    (r'^forgetpasswd.html$', 'forgetpasswd'),
    (r'^forgetpasswdpage.html$', 'forgetpasswdpage'),
    (r'^info.html$', 'info'),
    (r'^infosave.html', 'infosave'),
    (r'^changeaccount.html$', 'changeaccount'),
    (r'^modpasswd.html$', 'modpasswd'),
    (r'^modpasswdsave.html$', 'modpasswdsave'),
    (r'^blank.html$', 'blank'),
    (r'^user/myinfo.html$', 'myinfo'),
    (r'^user/myinfosave.html$', 'myinfosave'),
    #账号绑定和解绑
    (r'^user/auth_yzmcode.html$', 'auth_yzmcode'),
    (r'^user/auth_unbundlingmobile.html$', 'auth_unbundlingmobile'),
    (r'^user/auth_bindingmobile.html$', 'auth_bindingmobile'),
    #修改密码
    (r'^user/resetpasswd.html$', 'resetpasswd'),
    (r'^user/qqlogin.html$', 'qqlogin'),
    
    (r'^user/tokeninfo.html$', 'tokeninfo'),
    (r'^user/get_token.html$', 'get_token'),
    
    
    
)
#----301跳转
urlpatterns += patterns('zz91app.views',
    (r'^priceList_t(?P<typeid>\w+)_metal.htm$', 'price301'),
    (r'^priceList_a(?P<assist_id>\w+)_metal.htm$', 'price301'),
    (r'^priceList_t40_a(?P<assist_id>\w+)_metal.htm$', 'price301'),
    (r'^moreList_p3_t(?P<typeid>\w+)_metal.htm$', 'price301'),
    (r'^moreList_p17_a(?P<assist_id>\w+)_metal.htm$', 'price301'),
    
    (r'^priceList_t(?P<typeid>\w+)_plastic.htm$', 'price301'),
    (r'^priceList_a(?P<assist_id>\w+)_plastic.htm$', 'price301'),
    (r'^priceList_t40_a(?P<typeid>\w+)_plastic.htm$', 'price301'),
    (r'^moreList_p(?P<typeid>\w+)_plastic.htm$', 'price301'),
    
    (r'^priceDetails_(?P<id>\w+)_plastic.htm$', 'price301'),
    (r'^priceDetails_(?P<id>\w+)_paper.htm$', 'price301'),
    (r'^priceDetails_(?P<id>\w+)_metal.htm$', 'price301'),
    (r'^priceDetails_(?P<id>\w+).htm$', 'price301'),
    
    (r'^priceList_t(?P<typeid>\w+)_paper.htm$', 'price301'),
    (r'^moreList_p(?P<typeid>\w+)_paper.htm$', 'price301'),
    #翻页
    (r'^priceList_t_p_a(?P<assist_id>\w+)_c_metal--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
    (r'^priceList_t_p_a(?P<assist_id>\w+)_c_plastic--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
    (r'^priceList_t_p_a(?P<assist_id>\w+)_c_paper--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
    
    (r'^priceList_t(?P<typeid>\w+)_p_a_c_metal--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
    (r'^priceList_t(?P<typeid>\w+)_p_a_c_plastic--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
    (r'^priceList_t(?P<typeid>\w+)_p_a_c_paper--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
)
#----js app
urlpatterns += patterns('zz91app.appjs',
    (r'^appjs/$', 'pricelist'),
    (r'^appjs/provincejson.html$', 'provincejson'),
    (r'^app/appversion.html$', 'appversion'),
    (r'^wxpay/wxpay.html$', 'wxpay'),
    (r'^keywords/savekeywords.html$', 'savekeywords'),
    (r'^keywords/getkeywords.html$', 'getkeywords'),
    (r'^keywords/searchtis.html$', 'searchtis'),
    (r'^app/ggopen.html$', 'ggopen'),
)
#荣云
urlpatterns += patterns('zz91app.rong_views',
    (r'^rong/gettoken.html$', 'gettoken'),
)
urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
