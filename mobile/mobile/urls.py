from django.conf.urls import patterns, include, url
from settings import STATIC_ROOT
#微信授权登录
urlpatterns=patterns('mobile.wechat',
    (r'^wechat/auth_login.html$', 'auth_login'),
    (r'^wechat/redirect_uri.html$', 'redirect_uri'),
    (r'^wechat/weixinshare.js', 'weixinsharejs'),
)

urlpatterns+=patterns('mobile.vote',
    (r'^vote/index.html$', 'index'),
    (r'^vote/jsindex.html$', 'jsindex'),
    (r'^vote/vote.html$', 'vote'),
    (r'^vote/voteranking.html$', 'voteranking'),
    (r'^vote/jsvoteranking.html$', 'jsvoteranking'),
    (r'^vote/ybp_redirect.html$', 'ybp_redirect'),
    (r'^vote/ybp_index.html$', 'ybp_index'),
    (r'^vote/ybp_vote_save.html$', 'ybp_vote_save'),
    (r'^vote/vote_check.html$', 'vote_check'),
    
    #2017 -621峰会
    (r'^vote/621/index.html$', 'v621_index'),
    (r'^vote/621/$', 'v621_index'),
    (r'^vote/621$', 'v621_index'),
    
    (r'^vote/621/gys.html$', 'v621_gys'),
    (r'^vote/621/gys-zxpm.html$', 'v621_gys_zxpm'),
    (r'^vote/621/gys-view(?P<vid>\d+).html$', 'v621_gys_view'),
    (r'^vote/621/cgs.html$', 'v621_cgs'),
    (r'^vote/621/cgs-zxpm.html$', 'v621_cgs_zxpm'),
    (r'^vote/621/cgs-view(?P<vid>\d+).html$', 'v621_cgs_view'),
    
    #公用模式
    (r'^vote/v(?P<votename>\w+)/list.html$', 'vote_comm_list'),
    (r'^vote/v(?P<votename>\w+)/sort.html$', 'vote_comm_sort'),
    (r'^vote/v(?P<votename>\w+)/view(?P<vid>\d+).html$', 'vote_comm_view'),
    
)
urlpatterns+=patterns('mobile.zsh',
    (r'^zsh/$', 'index'),
    (r'^zsh/index.html$', 'index'),
    (r'^zsh/qiandao_save.html$', 'qiandao_save'),
    (r'^zsh/qiandao_suc.html$', 'qiandao_suc'),
    (r'^zsh/qiandao_noreg.html$', 'qiandao_noreg'),
    (r'^zsh/qiandao_noreg_save.html$', 'qiandao_noreg_save'),
    (r'^zsh/choujiangqiandao.html$', 'choujiangqiandao'),
    #团购
    (r'^zsh/groupbuy/$', 'groupbuy_index'),
    (r'^zsh/groupbuy/index.html$', 'groupbuy_index'),
    (r'^zsh/groupbuy/detail.html$', 'groupbuy_detail'),
    (r'^zsh/groupbuy/detail_save.html$', 'groupbuy_detail_save'),
    (r'^zsh/groupbuy/success(?P<gid>\d+).html$', 'groupbuy_success'),
)
#业务工单
urlpatterns += patterns('mobile.gd',
    #---后台
    (r'^gd/list.html$','gd_list'),#所有工单
    (r'^gd/add.html$','gd_add'),#添加工单
    (r'^gd/reply.html$','gd_reply'),
    (r'^gd/replysave.html$','gd_replysave'),
    (r'^gd/save.html$','gd_save'),#添加工单
    (r'^gd/details.html$','gd_details'),#工单详情
    (r'^gd/station.html$','gd_station'),#工单状态
    (r'^gd/answer.html$','gd_answer'),#回复
)
#服务中心
urlpatterns += patterns('mobile.help',
    (r'^help/$','index'),#
    (r'^help/index.html$','index'),#
    (r'^help/list.html$','list'),#
    (r'^help/detail.html$','detail'),#
)
#----首页
urlpatterns+=patterns('mobile.main',
    (r'^$', 'index'),
    #----广告页
    (r'^guanggao.html$', 'guanggao'),
    (r'^loginstatus.html$', 'loginstatus'),
    
    (r'^app.html', 'app'),
    (r'^pay/index.html', 'pay'),
    (r'^invite/invite.html', 'invite'),
    (r'^invite/i(?P<mcode>\w+).html', 'invite'),
    (r'^invite/help.html', 'invitehelp'),
    (r'^invite/help(?P<code>\w+).html', 'invitehelp'),
    (r'^invite/s(?P<mcode>\w+).html', 'invitesee'),
    (r'^showppccomplist_float.html$', 'showppccomplist_float'),
    (r'^messages.html$', 'messages'),
    (r'^messages_save.html$', 'messages_save'),
    
    (r'^log/getloginfo.html$', 'getloginfo'),
    (r'^log/saveloginfo.html$', 'saveloginfo'),
    (r'^test.html$', 'test'),
    (r'^choujiang/index.html$', 'choujiang'),
    (r'^2016zadanplay/index.html$', 'zadanplay'),
    (r'^taizhou2016/index.html$', 'taizhou2016'),
    
    (r'^guaguale/index.html$', 'guaguale_index'),
    (r'^guaguale/play.html$', 'guaguale_play'),
    #帮你找
    (r'^need/put.html$', 'need_put'),
    (r'^need/category.html$', 'need_category'),
    (r'^need/province.html$', 'need_province'),
    #优惠券活动
    (r'^youhui/index.html$', 'youhui'),
    (r'^zhongqiu/index.html$', 'zhongqiu'),
    (r'^zhongqiu/ybindex.html$', 'ybzhongqiu'),
    (r'^zhongqiu/savecontent.html$', 'zhongqiu_savecontent'),
    
    
    (r'^yuanbaopu/help.html$', 'yuanbaopu_help'),
    (r'^yuanbaopu/about.html$', 'yuanbaopu_about'),
    
    #2016双11砍价
    (r'^kanjia/index.html$', 'kanjiaindex'),
    (r'^kanjia/baoming.html$', 'kanjiabaoming'),
    (r'^kanjia/cut(?P<baoming_id>\d+).html$', 'kanjiacut'),
    (r'^kanjia/cutsave.html$', 'kanjiacut_save'),
    (r'^kanjia/redirect_uri.html$', 'redirect_uri'),
    (r'^kanjia/appload.html$', 'kanjiaappload'),
    
    #元旦送祝福
    (r'^newyear/index.html$', 'newyearindex'),
    (r'^newyear/ybpindex.html$', 'newyearybpindex'),
    
    (r'^usr/getcontactinfo.html$', 'getcontactinfo'),
    (r'^usr/feedbacksave.html$', 'feedbacksave'),
    (r'^usr/seoregister.html$', 'seoregister'),
    
    (r'^ad/bdtuiguan.html$', 'bdtuiguan'),
    
    #红包送不停
    (r'^ad/hongbao/hongbao.html$', 'hongbao'),
    #专题
    (r'^subject/621/index.html$', 'subject_621'),
    
    (r'^kangzhuang/zhifu.html$', 'kangzhuang_zhifu'),
    
    
)
#----采购频道
urlpatterns += patterns('mobile.trust',
    (r'^trust/$', 'listcaigou'),
    (r'^trust/p(?P<page>\d+).html$', 'listcaigou'),
    (r'^trust/listcaigou2.html$', 'listcaigou'),
    #免费发布
    (r'^trust/supplyPub.html$', 'supplyPub'),
    (r'^trust/supplyPubok.html$', 'supplyPubok'),
    (r'^trust/supplyPubsuc.html$', 'supplyPubsuc'),
    
    #我要供货
    (r'^trust/supplyForm.html$', 'supplyForm'),
    (r'^trust/supplyFormok.html$', 'supplyFormok'),
    (r'^trust/supplyFormsuc.html$', 'supplyFormsuc'),
    #我的采购
    (r'^trust/listmycaigou.html$', 'listmycaigou'),
    #我的供货
    (r'^trust/listmysupply.html$', 'listmysupply'),
                        
)

#---产业带
urlpatterns += patterns('mobile.ye',
    (r'^ye/$', 'ye_index'),
    (r'^ye/index.html$', 'ye_index'),
    (r'^ye/ye_more/$', 'ye_more'),#首页加载更多
    (r'^ye/(?P<big_category>\d+)/$', 'ye_list'),
    (r'^ye/(?P<big_category>\d+)/(?P<small_category>\d+).html$', 'ye_list'),#列表页
    (r'^ye/pro(?P<id>\d+).html$', 'ye_prolist'),
    (r'^ye/comp(?P<id>\d+).html$', 'ye_complist'),
    (r'^ye_list_more/$', 'ye_list_more'),#产业带列表页加载更多
    (r'^ye/ye_detail/(?P<ye_pinyin>\w+).html$', 'ye_detail'),#详细页
    (r'^ye/ye_detail/ye_offerlist_more/$', 'ye_offerlist_more'),#详细页供求底部加载更多
    (r'^ye/ye_detail/ye_company_more/$', 'ye_company_more'),#详细页公司黄页底部加载更多
    (r'^ye/list_other_ye.html$','list_other_ye'),#查看其他相关产业带  list_other_ye_more
    (r'^ye/list_other_ye_more/$','list_other_ye_more'),#查看其他相关产业带
    (r'^ye/join_ye.html$','join_ye'),#加入产业带
    (r'^ye/quit_ye.html$','quit_ye'),#退出产业带
)
#----再生钱包
urlpatterns+=patterns('mobile.qianbao',
    (r'^qianbao/$', 'index'),
    (r'^qianbao/zhangdan.html$', 'zhangdan'),
    (r'^qianbao/zhangdannore.html$', 'zhangdannore'),
    (r'^qianbao/chongzhi.html$', 'chongzhi'),
    (r'^qb.h(?P<id>\w+)$', 'chongzhi'),
    (r'^qianbao/intxt.html$', 'intxt'),
    (r'^qianbao/outtxt.html$', 'outtxt'),
    (r'^qianbao/shop.html$', 'shop'),
    (r'^qianbao/simptxt.html$', 'simptxt'),
    (r'^qianbao/oflist.html$', 'oflist'),
    (r'^qianbao/offmore.html$', 'offmore'),
    (r'^qianbao/qianbaopay.html$', 'qianbaopay'),
    (r'^weixin/getqianbao.html$', 'getqianbao'),
    (r'^qianbao/qianbaobaoblance.html$', 'qianbaobaoblance'),
    (r'^qianbao/qiandao.html$', 'qiandao'),
    (r'^qianbao/myservice.html$', 'myservice'),
    
    
    #流量宝
    (r'^qianbao/llb_index.html$', 'llb_index'),
    (r'^qianbao/llb_add.html$', 'llb_add'),
    (r'^qianbao/llb_selectpro.html$', 'llb_selectpro'),
    (r'^qianbao/llb_category.html$', 'llb_category'),
    #
    (r'^qianbao/jingjia_info.html$', 'jingjia_info'),
    (r'^qianbao/jingjia_keywords_save.html$', 'jingjia_keywords_save'),
    (r'^qianbao/jingjia_index.html$', 'jingjia_index'),
    (r'^qianbao/jingjia_keywords_info.html$', 'jingjia_keywords_info'),
    (r'^qianbao/jingjia_keywords_onesave.html$', 'jingjia_keywords_onesave'),
    (r'^qianbao/jingjia_keywords_offline.html$', 'jingjia_keywords_offline'),
    (r'^qianbao/jingjia_keywords_paylist.html$', 'jingjia_keywords_paylist'),
    (r'^qianbao/jingjia_keywords_clicklist.html$', 'jingjia_keywords_clicklist'),
    (r'^qianbao/jingjia_click_save.html$', 'jingjia_click_save'),
    
    (r'^qianbao/minichongzhi.html$', 'minichongzhi'),
    
    #产品服务
    (r'^service/$', 'cp_index'),
     (r'^service/youhui.html$', 'cp_youhui'),
    (r'^service/index.html$', 'cp_index'),
    (r'^service/cp_autoreflush.html$', 'cp_autoreflush'),
    (r'^service/cp_book_buy.html$', 'cp_book_buy'),
    (r'^service/cp_book.html$', 'cp_book'),
    (r'^service/cp_createwebsite.html$', 'cp_createwebsite'),
    (r'^service/cp_createwebsite_buy.html$', 'cp_createwebsite_buy'),
    (r'^service/cp_ldb.html$', 'cp_ldb'),
    (r'^service/cp_listad.html$', 'cp_listad'),
    (r'^service/cp_listad_buy.html$', 'cp_listad_buy'),
    (r'^service/cp_indexad_buy.html$', 'cp_indexad_buy'),
    (r'^service/cp_huangjinad_buy.html$', 'cp_huangjinad_buy'),
    (r'^service/cp_lookcontact.html$', 'cp_lookcontact'),
    (r'^service/cp_producttop.html$', 'cp_producttop'),
    (r'^service/cp_producttop_buy.html$', 'cp_producttop_buy'),
    (r'^service/cp_producttop_select.html$', 'cp_producttop_select'),
    (r'^service/cp_qyx.html$', 'cp_qyx'),
    (r'^service/cp_qyx_buy.html$', 'cp_qyx_buy'),
    (r'^service/cp_seo.html$', 'cp_seo'),
    (r'^service/cp_seo_buy.html$', 'cp_seo_buy'),
    (r'^service/cp_showcontact.html$', 'cp_showcontact'),
    (r'^service/cp_zst.html$', 'cp_zst'),
    (r'^service/cp_qunfa.html$', 'cp_qunfa'),
    
    (r'^service/fuwu.html$', 'fuwu'),
    (r'^service/fuwu_zst.html$', 'fuwu_zst'),
    (r'^service/fuwu_baidu.html$', 'fuwu_baidu'),
    (r'^service/fuwu_jpppt.html$', 'fuwu_jpppt'),
    (r'^service/fuwu_ldb.html$', 'fuwu_ldb'),
    (r'^service/fuwu_ppai.html$', 'fuwu_ppai'),
    (r'^service/fuwu_zsppt.html$', 'fuwu_zsppt'),
    (r'^service/fuwu_zstct.html$', 'fuwu_zstct'),
    
    
    
)
#----生意管家
urlpatterns+=patterns('mobile.myrc',
    (r'^myrc/$', 'myrc_index'),
    (r'^myrc_index/$', 'oldmyrcindex'),
    (r'^myrc/index.html$', 'myrc_index'),
    (r'^myrc/products.html$', 'myrc_products'),
    (r'^myrc/refurbish.html$', 'products_refurbish'),
    (r'^myrc/refurbishall.html$', 'products_refurbishall'),
    (r'^myrc/prostop.html$', 'products_stop'),
    (r'^myrc/prostart.html$', 'products_start'),
    (r'^myrc/proupdate.html$', 'products_update'),
    
    (r'^myrc/info.html$', 'myrc_info'),
    (r'^myrc/share.html$', 'myrc_share'),
    (r'^myrc/card.html$', 'myrc_card'),
    (r'^myrc/addressbook.html$', 'myrc_addressbook'),
    (r'^myrc/addressbook_del.html$', 'myrc_addressbook_del'),
    (r'^myrc/addressbook_join.html$', 'myrc_addressbook_join'),
    (r'^myrc/favorite_save.html$', 'favorite_save'),
    (r'^myrc/info_save.html$', 'myrc_infosave'),
    (r'^myrc/bindweixin.html$', 'myrc_bindweixin'),
    (r'^myrc/password.html$', 'myrc_password'),
    (r'^myrc/forgetpassword.html$', 'forgetpassword'),
    (r'^myrc/auth_yzmcode.html$', 'auth_yzmcode'),
    (r'^myrc/resetpasswd.html$', 'resetpasswd'),
    (r'^myrc/mobile_login.html$', 'mobile_login'),
    (r'^myrc/mobile_loginof.html$', 'mobile_loginof'),
    (r'^myrc/mobile_bunding.html$', 'mobile_bunding'),
    (r'^myrc/mobile_unbunding.html$', 'mobile_unbunding'),
    (r'^myrc/auth_bindingmobile.html$', 'auth_bindingmobile'),
    (r'^myrc/auth_bindingmobile.html$', 'auth_bindingmobile'),
    (r'^myrc/auth_unbundlingmobile.html$', 'auth_unbundlingmobile'),
    (r'^myrc/xunpan.html$', 'myrc_xunpan'),
    (r'^myrc/xunpan_reply.html$', 'myrc_xunpan_reply'),
    (r'^myrc/xunpan_save.html$', 'myrc_xunpan_save'),
    (r'^myrc/favorite.html$', 'myrc_favorite'),
    (r'^myrc/favorite_del.html$', 'myrc_favorite_del'),
    (r'^myrc/community.html$', 'myrc_community'),
    (r'^myrc/mypost.html$', 'myrc_mypost'),
    (r'^myrc/viewreply.html$', 'myrc_viewreply'),
    (r'^myrc/myreply.html$', 'myrc_myreply'),
    (r'^myrc/myguanzhu.html$', 'myrc_myguanzhu'),
    (r'^myrc/products_propertylist.html$', 'products_propertylist'),
    (r'^myrc/products_picturelist.html$', 'products_picturelist'),
    (r'^myrc/products_delpicture.html$', 'products_delpicture'),
    
    
)
#----pingxx 支付
urlpatterns+=patterns('mobile.pingxx',
    (r'^pingxx/pay.html$', 'pay'),
    (r'^pingxx/pay_save.html$', 'pay_save'),
    (r'^wxpay/wx_pay.html$', 'wx_pay'),
    (r'^wxpay/wx_makepayment.html$', 'wx_makepayment'),
    (r'^pay/payupdate.html$', 'payupdate'),
)

urlpatterns+=patterns('mobile.huzhu',
    (r'^huzhu/wenda.html$', 'huzhu_wenda'),
    (r'^huzhu/shequ.html$', 'huzhu_shequ'),
    (r'^huzhu/xueyuan.html$', 'huzhu_xueyuan'),
    (r'^huzhu/remen.html$', 'huzhu_remen'),
    (r'^huzhu/zuixin.html$', 'huzhu_zuixin'),
    (r'^huzhu/shangquan.html$', 'huzhu_shangquan'),
    (r'^huzhu/(?P<id>\d+).html$', 'huzhuview'),
    (r'^huzhu/recommend_add.html$', 'recommend_add'),
    #----互助
    (r'^huzhu/$', 'huzhu301'),
    (r'^huzhumore/$', 'huzhumore'),
    (r'^huzhupost/$', 'huzhupost'),
    (r'^huzhu_imgload/$', 'huzhu_imgload'),
    (r'^huzhu_upload/$', 'huzhu_upload'),
    (r'^huzhupostsave/$', 'huzhupostsave'),
    (r'^huzhuview/(?P<id>\d+).htm$', 'huzhuview301'),
    (r'^huzhuview/viewReply(?P<id>\d+).htm$', 'huzhuview301'),
    (r'^huzhureplymore/$', 'replymore'),
    (r'^huzhu_replay/$', 'huzhu_replay'),
    (r'^huzhu_replayshow/$', 'huzhu_replayshow'),
    (r'^reply_reply/$', 'reply_reply'),
    (r'^huzhucate/$', 'huzhucate'),
)
#----来电宝
urlpatterns+=patterns('mobile.ldb_weixin',
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
urlpatterns+=patterns('mobile.trade',
    (r'^trade/$', 'tradeindex'),
    (r'^trade/category(?P<code>\w+).html$', 'category'),
    (r'^trade/p(?P<page>\d+).html$', 'offerlist'),
    (r'^trade/gy.html$', 'offergongyin'),
    (r'^trade/qg.html$', 'offerqiugou'),
    (r'^trade/gy_p(?P<page>\d+).html$', 'offergongyin'),
    (r'^trade/qg_p(?P<page>\d+).html$', 'offerqiugou'),
    (r'^trade/(?P<pinyin>\w+)/$', 'offerlist'),
    (r'^trade/(?P<pinyin>\w+)/p(?P<page>\d+).html$', 'offerlist'),
    (r'^trade/(?P<pinyin>\w+)/gy.html$', 'offergongyin'),
    (r'^trade/(?P<pinyin>\w+)/gy_p(?P<page>\d+).html$', 'offergongyin'),
    (r'^trade/(?P<pinyin>\w+)/qg.html$', 'offerqiugou'),
    (r'^trade/(?P<pinyin>\w+)/qg_p(?P<page>\d+).html$', 'offerqiugou'),
    (r'^trade/pro_report.html$', 'pro_report'),
    (r'^trade/detail(?P<pid>\d+).html$', 'detail'),
    (r'^detail/$', 'detail301'),
    (r'^trade/pricelist.html$', 'pricelist'),
    (r'^trade/telclicklog.html$', 'telclicklog'),
    (r'^trade/hiturl.html$', 'hiturl'),
    (r'^trade/post_save.html$', 'post_save'),
    (r'^trade/post_success.html$', 'post_success'),
    (r'^trade/question_success.html$', 'question_success'),
    (r'^trade/viewcontact.html$', 'viewcontact'),
    
    
)
urlpatterns+=patterns('mobile.news',
    #----看资讯(一期)
    (r'^news/(?P<type>\w+)/$', 'index'),
    (r'^news/(?P<type>\w+)/p(?P<page>\d+).html$', 'index'),
    (r'^news/(?P<type>\w+)/(?P<type1>\w+)/$', 'index'),
    (r'^news/(?P<type>\w+)/(?P<type1>\w+)/p(?P<page>\d+).html$', 'index'),
    (r'^news/p(?P<page>\d+).html$', 'index'),
    ('^news/zh/list(?P<type>\w+).html$', 'zhlist'),
    ('^news/zh/list(?P<type>\w+)-p(?P<page>\d+).html$', 'zhlist'),
    ('^news/zh/detail(?P<zhid>\d+).html$', 'zhdetail'),
    #(r'^news/$', 'newsindex'),
    (r'^news/$', 'index'),
    (r'^news/list-(?P<typeid>\w+).html$', 'news_list301'),
    (r'^news/search.html$', 'news_list301'),
    (r'^news/search-(?P<page>\d+).html$', 'news_list301'),
    (r'^news/list-(?P<typeid>\w+)-(?P<page>\d+).html$', 'news_list301'),
    
    (r'^news/newsdetail(?P<newsid>\d+).htm$', 'newsdetail'),
    (r'^news/(?P<type>\w+)/(?P<newsid>\d+).html$', 'detail'),
)                    
urlpatterns+=patterns('mobile.price',
    
    (r'^jiage/$', 'index'),
    (r'^jiage$', 'index'),
    (r'^jiage/pricechartdata.html$', 'pricechartdata'),
    (r'^jiage/pricechart.html$', 'pricechart'),
    (r'^jiage/p(?P<page>\d+).html$', 'pricelist'),
    (r'^jiage/(?P<pinyin>\w+)/$', 'pricelist'),
    (r'^jiage/(?P<pinyin>\w+)$', 'pricelist'),
    (r'^jiage/order/$', 'pricelist'),
    (r'^jiage/(?P<pinyin>\w+)/p(?P<page>\d+).html$', 'pricelist'),
    (r'^jiage/(?P<pinyin>\w+)/(?P<apinyin>\w+)/$', 'pricelist'),
    (r'^jiage/(?P<pinyin>\w+)/(?P<apinyin>\w+)/p(?P<page>\d+).html$', 'pricelist'),
    (r'^jiage/detail(?P<id>\d+).html$', 'details'),
    
    (r'^jiage/cdetail(?P<id>\d+).html$', 'compdetails'),
    
    (r'^jiage/jinshuarea.html$', 'jinshuarea'),
    (r'^jiage/suliaoarea.html$', 'suliaoarea'),
    (r'^jiage/suliaoxinliao.html$', 'suliaoxinliao'),
    (r'^jiage/xinliaochuchangjia.html$', 'xinliaochuchangjia'),
    (r'^jiage/xinliaoshichangjia.html$', 'xinliaoshichangjia'),
    (r'^jiage/areasuliao.html$', 'areasuliao'),
    (r'^jiage/suliaoqihuo.html$', 'suliaoqihuo'),
    (r'^jiage/suliaozaishengliao.html$', 'suliaozaishengliao'),
    (r'^jiage/meiguosuliao.html$', 'meiguosuliao'),
    (r'^jiage/ouzhousuliao.html$', 'ouzhousuliao'),
    (r'^jiage/suliaozaishengliao.html$', 'suliaozaishengliao'),
    (r'^jiage/feizhidongtai.html$', 'feizhidongtai'),
    (r'^jiage/feizhiarea.html$', 'feizhiarea'),
    (r'^jiage/feizhiriping.html$', 'feizhiriping'),
    
    #----行情报价
    (r'^priceindex/$', 'index301'),
    (r'^price/$', 'pricelist301'),
    (r'^priceindex/(?P<category_id>\d+).html$', 'pricelist301'),
    (r'^priceindex/p(?P<assist_id>\d+).html$', 'pricelist301'),
    (r'^pricemore/(?P<category_id>\d+).html$', 'pricemore'),
    (r'^pricemore/p(?P<assist_id>\d+).html$', 'pricemore'),
    
    (r'^priceindex/(?P<pinyin>\w+)/$', 'priceindex301'),
    
    (r'^priceindex/jinshuarea/$', 'jinshuarea301'),
    (r'^priceindex/suliaoarea/$', 'suliaoarea301'),
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
    
    (r'^priceviews/$', 'details301'),
    #----企业报价最终页
    (r'^compriceviews/$', 'compdetails301'),
)
urlpatterns+=patterns('mobile.company',
    (r'^company/$', 'company'),
    (r'^company/p(?P<page>\d+).html$', 'company'),
    (r'^company/ldb/$', 'companyldb'),
    (r'^company/ldb/p(?P<page>\d+).html$', 'companyldb'),
    (r'^company/detail(?P<forcompany_id>\d+).html$', 'companyinfo'),
    (r'^company/products/(?P<company_id>\d+)/$', 'companyproducts'),
    (r'^company/products/(?P<company_id>\d+)/p(?P<page>\d+).html$', 'companyproducts'),
    
    (r'^companydetail/$', 'companydetail'),
    (r'^companyinfo/$', 'companyinfo301'),
    #----公司供求列表
    (r'^companyproducts/$', 'companyproducts301'),
    (r'^company/companyproductslist.html$', 'companyproductslist'),
    (r'^company/shop(?P<forcompany_id>\d+).html$', 'companyshop'),
    (r'^company/card(?P<forcompany_id>\d+).html$', 'companycard'),
    
    
)
#----price301跳转
urlpatterns += patterns('mobile.views',
#    (r'^(?P<typeid1>\w+)List_(?P<typeid>\w+)_(?P<typeid3>\w+).htm$', 'mobile.views.price301'),
#    (r'^(?P<typeid1>\w+)List(?P<typeid2>\w+)_(?P<typeid>\w+)_(?P<typeid3>\w+).htm$', 'mobile.views.price301'),
#    (r'^priceDetails_(?P<id>\w+).htm$', 'mobile.views.price301'),
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
)

urlpatterns += patterns('',
    (r'^goback/$', 'mobile.views.goback'),
    (r'^slider2/js/widget/$', 'mobile.views.default2'),
    (r'^index.html$', 'mobile.views.newdefault'),
    (r'^category/$', 'mobile.views.category'),
    (r'^offerlist/$', 'mobile.views.offerlist301'),
    (r'^register/$', 'mobile.views.register'),
    (r'^reg/reginfo.html$', 'mobile.views.reginfo'),
    (r'^user/regsecond.html$', 'mobile.views.regsecond'),
    (r'^user/regsecond_save.html$', 'mobile.views.regsecond_save'),
    (r'^user/province.html$', 'mobile.views.province'),
    (r'^user/regsuccess.html$', 'mobile.views.regsuccess'),
    
    (r'^registerSave/$', 'mobile.views.registerSave'),
    (r'^login/$', 'mobile.views.login'),
    (r'^loginout/$', 'mobile.views.loginout'),
    (r'^loginof/$', 'mobile.views.loginof'),
    (r'^serviceterms/$', 'mobile.views.serviceterms'),
    
    (r'^dataalter.html/$','mobile.views.dataalter'),#用户资料完善
    (r'^dataalter_ok/$','mobile.views.dataalter_ok'),#用户资料完善确认
    #----供求

    
    
    (r'^feedback/$', 'mobile.views.feedback'),
    (r'^feedbacksave/$', 'mobile.views.feedbacksave'),
    
    (r'^verifycode/$', 'mobile.views.verifycode'),
    (r'^upload/$', 'mobile.views.upload'),
    
    (r'^categoryinfo.html$', 'mobile.views.categoryinfo'),
    
    #---支付宝支付
    (r'^zz91pay.html$', 'mobile.views.zz91pay'),
    (r'^pay/callback_get.html$', 'mobile.views.callback_get'),
    (r'^pay/callback_post.html$', 'mobile.views.callback_post'),
    
    (r'^zz91payverify_notify.html$', 'mobile.views.zz91payverify_notify'),
    (r'^zz91payverify_notifyali.html$', 'mobile.views.zz91payverify_notifyali'),
    
    (r'^zz91paypingxx_notify.html$', 'mobile.views.zz91paypingxx_notify'),
    (r'^zz91payreturn_url.html$', 'mobile.views.zz91payreturn_url'),
    

    #----微信
    (r'^weixin/order.html$', 'mobile.weixin.order'),
    (r'^weixin/tradesearch.html$', 'mobile.weixin.tradesearch'),
    (r'^weixin/pricesearch.html$', 'mobile.weixin.pricesearch'),
    (r'^weixin/login.html$', 'mobile.weixin.login'),
    (r'^weixin/loginsave.html$', 'mobile.weixin.loginsave'),
    (r'^weixin/reg.html$', 'mobile.weixin.reg'),
    (r'^weixin/baoming.html$', 'mobile.weixin.baoming'),
    (r'^weixin/regsave.html$', 'mobile.weixin.regsave'),
    (r'^weixin/qqlogin.html$', 'mobile.weixin.qqlogin'),
    (r'^weixin/forgetpasswd.html$', 'mobile.weixin.forgetpassword'),
    (r'^weixin/doget.html$', 'mobile.weixin.doget'),
    (r'^weixin/ldbdoget.html$', 'mobile.weixin.ldbdoget'),
    (r'^weixin/priceday.html$', 'mobile.weixin.priceday'),
    (r'^weixin/weixintest.html$', 'mobile.weixin.weixintest'),
    (r'^weixin/getqrcode.html$', 'mobile.weixin.getqrcode'),
    (r'^weixin/getloginqrcode.html$', 'mobile.weixin.getloginqrcode'),
    (r'^weixin/weixinshare.html$', 'mobile.weixin.weixinshare'),
    
    (r'^weixin/getzsh.html$', 'mobile.weixin.getzsh'),
    
    
    
    
    (r'^weixin/zz91weixin_yz.html$', 'mobile.weixin.zz91weixin_yz'),
    (r'^weixin/zz91weixin_yzsave.html$', 'mobile.weixin.zz91weixin_yzsave'),
    (r'^weixin/zz91weixin_yzfront.html$', 'mobile.weixin.zz91weixin_yzfront'),
    
    (r'^weixin/huanbaowxget.html$', 'mobile.weixin.huanbaowxget'),
    (r'^weixin/huanbaoweixin_yz.html$', 'mobile.weixin.huanbaoweixin_yz'),
    (r'^weixin/huanbaoweixin_yzsave.html$', 'mobile.weixin.huanbaoweixin_yzsave'),
    (r'^weixin/huanbaoweixin_yzfront.html$', 'mobile.weixin.huanbaoweixin_yzfront'),
    
    #元宝铺微信
    (r'^weixin/yuanbaopuwxget.html$', 'mobile.weixin.yuanbaopuwxget'),
    #优质客户
    (r'^weixin/company/$', 'mobile.weixin.categoryindex'),
    (r'^weixin/company/(?P<code>\w+)/$', 'mobile.weixin.categorylist'),
    
    #----定制页面(一期)
    (r'^order/$', 'mobile.views.orderindex'),
    (r'^order/business.html$', 'mobile.views.orderbusiness'),
    (r'^order/price.html$', 'mobile.views.orderprice'),
    (r'^order/myorderprice_save.html$', 'mobile.views.myorderprice_save'),
    (r'^order/myorderprice_del.html$', 'mobile.views.myorderprice_del'),
    (r'^order/myordertrade_save.html$', 'mobile.views.myordertrade_save'),
    
    #----企业微站,来电宝(一期)
    (r'^smallsite/$', 'mobile.views.smallsite'),
    (r'^smallsite/list-(?P<page>\d+).html$', 'mobile.views.smallsite'),
        
    (r'^ajaxTopbbs/$', 'mobile.views.ajaxTopbbs'),
    (r'^ajaxTopprice/$', 'mobile.views.ajaxTopprice'),
    
    (r'^getzwpic/$', 'mobile.views.getzwpic'),
    (r'^searchfirst/$', 'mobile.views.searchfirst'),
    (r'^leavewords/$', 'mobile.views.leavewords'),
    (r'^leavewords_save/$', 'mobile.views.leavewords_save'),
    (r'^favorite/$', 'mobile.views.favorite'),
    (r'^openfavorite/$', 'mobile.views.openfavorite'),
    #(r'^service/$', 'mobile.views.service'),
    (r'^servicemore/$', 'mobile.views.servicemore'),
    (r'^about/$', 'mobile.views.about'),
    
    #(r'^myrc_mycommunity/$', 'mobile.views.myrc_mycommunity'),
    #(r'^myrc_mycommunitymore/$', 'mobile.views.myrc_mycommunitymore'),
    #(r'^myrc_mycommunitydel/$', 'mobile.views.myrc_mycommunitydel'),
    #(r'^myrc_mypost/$', 'mobile.views.myrc_mypost'),
    (r'^myrc_mypostsave/$', 'mobile.views.myrc_mypostsave'),
    (r'^myrc_mypostmore/$', 'mobile.views.myrc_mypostmore'),
    #(r'^myrc_myreply/$', 'mobile.views.myrc_myreply'),
    (r'^myrc_myreplysave/$', 'mobile.views.myrc_myreplysave'),
    #(r'^myrc_myreplymore/$', 'mobile.views.myrc_myreplymore'),
    #(r'^openmessages/$', 'mobile.views.openmessages'),
    #(r'^myrc_backquestion/$', 'mobile.views.myrc_backquestion'),
    #(r'^myrc_backquestionsave/$', 'mobile.views.myrc_backquestionsave'),
    #----供求发布保存修改
    (r'^products_publish/$', 'mobile.views.products_publish'),
    (r'^products_save/$', 'mobile.views.products_save'),
    #(r'^products_update/$', 'mobile.views.products_update'),
    (r'^products_updatesave/$', 'mobile.views.products_updatesave'),
    #(r'^products_refresh/$', 'mobile.views.products_refresh'),
    #----记录客户浏览页面
    (r'^addrecordeddata/$', 'mobile.views.addrecordeddata'),
    #标准版

    #----网站索引
    (r'^zz91index/$', 'mobile.views_sy.default'),
    (r'^zz91index/p(?P<id>\d+)-(?P<page>\d+).htm$', 'mobile.views_sy.plist'),
    (r'^zz91index/p-p(?P<pinyin>\w+)-(?P<page>\d+).htm$', 'mobile.views_sy.plist_pinyin'),
    (r'^zz91index/c(?P<id>\d+)-(?P<page>\d+).htm$', 'mobile.views_sy.clist'),
    (r'^zz91index/c-p(?P<pinyin>\w+)-(?P<page>\d+).htm$', 'mobile.views_sy.clist_pinyin'),
    (r'^zz91index/tags-(?P<page>\d+).htm$', 'mobile.views_sy.tagslist'),
    (r'^zz91index/tags-(?P<pinyin>\w+)-(?P<page>\d+).htm$', 'mobile.views_sy.tagslist_pinyin'),
    (r'^zz91index/p_date.htm$', 'mobile.views_sy.plist_date'),
    
    (r'^zz91register/$', 'mobile.views.zz91register'),
    (r'^zz91registerSucceed/$', 'mobile.views.zz91registerSucceed'),
    (r'^zz91registerSave/$', 'mobile.views.zz91registerSave'),
    (r'^zz91regGetemail/$', 'mobile.views.zz91regGetemail'),
    (r'^zz91regGetusername/$', 'mobile.views.zz91regGetusername'),
    (r'^zz91regGetmobile/$', 'mobile.views.zz91regGetmobile'),
    (r'^zz91verifycode/$', 'mobile.views.zz91verifycode'),
    (r'^getkl91baojia/$', 'mobile.views.getkl91baojia'),
#    (r'^kl91price/$', 'mobile.views.kl91price'),
#    (r'^kl91pricedetail/$', 'mobile.views.kl91pricedetail'),
    (r'^tradedetail_price/$', 'mobile.views.tradedetail_price'),
    (r'^province.html$', 'mobile.views.jsprovince'),
    (r'^provincejs.js$', 'mobile.views.provincejs'),
    (r'^areahtml/$', 'mobile.views.areahtml'),
    (r'^keywordsearch/$', 'mobile.views.keywordsearch'),
    
    #其他应用
    
    (r'^showadscript/$', 'mobile.views.showadscript'),
    (r'^showcommadscript/$', 'mobile.views.showcommadscript'),
    (r'^showcompanyadscript/$', 'mobile.views.showcompanyadscript'),
    (r'^showppctxtadscript/$', 'mobile.views.showppctxtadscript'),
    (r'^showppccomplist/$', 'mobile.views.showppccomplist'),
    (r'^showppccomplist_pic/$', 'mobile.views.showppccomplist_pic'),
    
    
    
    (r'^app/areyouknow.html$', 'mobile.views.areyouknow'),
    (r'^app/areyouknowmore.html$', 'mobile.views.areyouknowmore'),
    (r'^app/ppchit.html$', 'mobile.views.ppchit'),
    (r'^app/yangad.html$', 'mobile.yang.yangad'),
    (r'^app/yangad_long.html$', 'mobile.yang.yangad_long'),
    
    #----改变图片大小
    (r'^app/changepic.html$', 'mobile.views.changepic'),
    #(r'^app/i/(?P<width>\d+)x(?P<height>\d+)/(?P<imgurl>\w+).jpg$', 'mobile.views.showimg'),
    (r'^img/(?P<width>\d+)x(?P<height>\d+)/(?P<path>.*)$', 'mobile.views.showimg'),
    
    #----二维码
    (r'^app/qrcodeimg.html$', 'mobile.views.qrcodeimg'),
    (r'^app/getzhidahtml.html$', 'mobile.views.getzhidahtml'),
    (r'^app/useragent.html$', 'mobile.views.useragent'),
    
    
    #----获得资讯列表
    (r'^news/javagetnewslist.html$', 'mobile.views.javagetnewslist'),
    (r'^news/javagetnewslist_json.html$', 'mobile.views.javagetnewslist_json'),
    #----调用企业报价json
    (r'^price/javagetcompanyprice_json.html$', 'mobile.views.javagetcompanyprice_json'),
    (r'^calllogin/$', 'mobile.views.calllogin'),
    (r'^companyindexnewproducts/$', 'mobile.views.companyindexnewproducts'),
    (r'^companyindexnewcomplist/$', 'mobile.views.companyindexnewcomplist'),
    (r'^showhuanbaoindexpic/$', 'mobile.views.showhuanbaoindexpic'),
    (r'^getdomainpic(?P<company_id>\d+).html$', 'mobile.views.getdomainpic'),
    (r'^getdomainhtml(?P<company_id>\d+).html$', 'mobile.views.getdomainhtml'),
    
    (r'^loginredirect.htm$', 'mobile.views.loginredirect'),
    #----积分
    (r'^score/index.html$', 'mobile.views.weixin_qiandao'),
    (r'^score/helptxt.html$', 'mobile.views.weixin_helptxt'),
    (r'^score/scorelist.html$', 'mobile.views.weixin_scorelist'),
    (r'^score/scorelistmore.html$', 'mobile.views.weixin_scorelistmore'),
    (r'^score/savemoble.html$', 'mobile.views.weixin_savemoble'),
    (r'^score/prizelist.html$', 'mobile.views.weixin_prizelist'),
    (r'^score/prizelog.html$', 'mobile.views.weixin_prizelog'),
    (r'^score/saveprize.html$', 'mobile.views.weixin_saveprize'),
    
    #----tags手机站转化
    (r'^a/(?P<keywords>\w+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagsPriceList'),
    (r'^b/(?P<keywords>\w+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagsHuzhuList'),
    (r'^d/(?P<keywords>\w+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagsnewsList'),
    (r'^a/(?P<keywords>\w+)-(?P<page>\d+)$', 'mobile.tagsurl.tagsPriceList'),
    (r'^b/(?P<keywords>\w+)-(?P<page>\d+)$', 'mobile.tagsurl.tagsHuzhuList'),
    (r'^d/(?P<keywords>\w+)-(?P<page>\d+)$', 'mobile.tagsurl.tagsnewsList'),
    (r'^c/(?P<keywords>\w+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagsPriceCompanyList'),
    (r'^c/(?P<keywords>\w+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagsPriceCompanyList'),
    (r'^s/(?P<keywords>\w+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagssearchList_hex'),
    (r'^s/(?P<keywords>\w+)-(?P<page>\d+)$', 'mobile.tagsurl.tagssearchList_hex'),    
    (r'^s/(?P<keywords>\w+)-(?P<kind>\d+)-(?P<page>\d+)/$', 'mobile.tagsurl.tagsTradeList'),
    (r'^s/(?P<keywords>\w+)-(?P<kind>\d+)-(?P<page>\d+)$', 'mobile.tagsurl.tagsTradeList'),
    (r'^s/(?P<keywords>\w+)/$', 'mobile.tagsurl.tagsmain'),
    (r'^s/(?P<keywords>\w+)$', 'mobile.tagsurl.tagsmain'),
    
    (r'^webapp/$', 'mobile.webapp.index'),
    (r'^closefloatapp.html$', 'mobile.views.closefloatapp'),
    

    (r'^(?!admin!templates)(?P<path>.*)$','django.views.static.serve',{'document_root':STATIC_ROOT}),
    
)


handler404 = 'mobile.views.viewer_404'
handler500 = 'mobile.views.viewer_500'



