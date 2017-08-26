from django.conf.urls import patterns, include, url
from settings import STATIC_ROOT

#----首页
urlpatterns=patterns('zz91yinyong.main',
	(r'^log/getloginfo.html$', 'getloginfo'),
	(r'^log/saveloginfo.html$', 'saveloginfo'),
	(r'^ad/show.html$', 'adshow'),
	(r'^showppccomplist_float.html$', 'showppccomplist_float'),
)

urlpatterns += patterns('',
	#----记录客户浏览页面
	(r'^addrecordeddata/$', 'zz91yinyong.views.addrecordeddata'),
	
	(r'^ajaxTopprice/$', 'zz91yinyong.views.ajaxTopprice'),
	
	(r'^getzwpic/$', 'zz91yinyong.views.getzwpic'),
	(r'^getkl91baojia/$', 'zz91yinyong.views.getkl91baojia'),
	(r'^tradedetail_price/$', 'zz91yinyong.views.tradedetail_price'),
	(r'^province.html$', 'zz91yinyong.views.jsprovince'),
	(r'^provincejs.js$', 'zz91yinyong.views.provincejs'),
	(r'^areahtml/$', 'zz91yinyong.views.areahtml'),
	(r'^keywordsearch/$', 'zz91yinyong.views.keywordsearch'),
	
	#其他应用
	
	(r'^showadscript/$', 'zz91yinyong.views.showadscript'),
	(r'^showcommadscript/$', 'zz91yinyong.views.showcommadscript'),
	(r'^showcompanyadscript/$', 'zz91yinyong.views.showcompanyadscript'),
	(r'^showppctxtadscript/$', 'zz91yinyong.views.showppctxtadscript'),
	(r'^showppctxtadscript2/$', 'zz91yinyong.views.showppctxtadscript2'),
	(r'^showppccomplist/$', 'zz91yinyong.views.showppccomplist'),
	(r'^showppccomplist2/$', 'zz91yinyong.views.showppccomplist2'),
	(r'^showppccomplist_pic/$', 'zz91yinyong.views.showppccomplist_pic'),
	
	
	
	(r'^app/areyouknow.html$', 'zz91yinyong.views.areyouknow'),
	(r'^app/areyouknowmore.html$', 'zz91yinyong.views.areyouknowmore'),
	(r'^app/ppchit.html$', 'zz91yinyong.views.ppchit'),
	(r'^app/yangad.html$', 'zz91yinyong.yang.yangad'),
	(r'^app/yangad_long.html$', 'zz91yinyong.yang.yangad_long'),
	(r'^app/tzsad_long.html$', 'zz91yinyong.yang.tzsad_long'),
	
	#----改变图片大小
	(r'^app/changepic.html$', 'zz91yinyong.views.changepic'),
	#(r'^app/i/(?P<width>\d+)x(?P<height>\d+)/(?P<imgurl>\w+).jpg$', 'zz91yinyong.views.showimg'),
	(r'^img/(?P<width>\d+)x(?P<height>\d+)/(?P<path>.*)$', 'zz91yinyong.views.showimg'),
	
	#----二维码
	(r'^app/qrcodeimg.html$', 'zz91yinyong.views.qrcodeimg'),
	(r'^app/getzhidahtml.html$', 'zz91yinyong.views.getzhidahtml'),
	(r'^app/useragent.html$', 'zz91yinyong.views.useragent'),
	
	(r'^weixin/zz91weixin_yz.html$', 'zz91yinyong.weixin.zz91weixin_yz'),
	(r'^weixin/zz91weixin_yzsave.html$', 'zz91yinyong.weixin.zz91weixin_yzsave'),
	(r'^weixin/zz91weixin_yzfront.html$', 'zz91yinyong.weixin.zz91weixin_yzfront'),
	
	(r'^weixin/huanbaowxget.html$', 'zz91yinyong.weixin.huanbaowxget'),
	(r'^weixin/huanbaoweixin_yz.html$', 'zz91yinyong.weixin.huanbaoweixin_yz'),
	(r'^weixin/huanbaoweixin_yzsave.html$', 'zz91yinyong.weixin.huanbaoweixin_yzsave'),
	(r'^weixin/huanbaoweixin_yzfront.html$', 'zz91yinyong.weixin.huanbaoweixin_yzfront'),
	
	#----获得资讯列表
	(r'^news/javagetnewslist.html$', 'zz91yinyong.views.javagetnewslist'),
	(r'^news/javagetnewslist_json.html$', 'zz91yinyong.views.javagetnewslist_json'),
	#----调用企业报价json
	(r'^price/javagetcompanyprice_json.html$', 'zz91yinyong.views.javagetcompanyprice_json'),
	(r'^calllogin/$', 'zz91yinyong.views.calllogin'),
	(r'^companyindexnewproducts/$', 'zz91yinyong.views.companyindexnewproducts'),
	(r'^companyindexnewcomplist/$', 'zz91yinyong.views.companyindexnewcomplist'),
	(r'^showhuanbaoindexpic/$', 'zz91yinyong.views.showhuanbaoindexpic'),
	#二维码
	(r'^getdomainpic(?P<company_id>\d+).html$', 'zz91yinyong.views.getdomainpic'),
	(r'^getvcardpic(?P<company_id>\d+).html$', 'zz91yinyong.views.getvcardpic'),
	(r'^getqiyexiupic(?P<company_id>\d+).html$', 'zz91yinyong.views.getqiyexiupic'),
	(r'^getdomainhtml(?P<company_id>\d+).html$', 'zz91yinyong.views.getdomainhtml'),
	(r'^feifa.html$', 'zz91yinyong.views.feifa'),
	
	(r'^loginredirect.htm$', 'zz91yinyong.views.loginredirect'),
	(r'^webapp/$', 'zz91yinyong.webapp.index'),
	(r'^closefloatapp.html$', 'zz91yinyong.views.closefloatapp'),
	#抽奖获得2015
	(r'^choujiangstaus.html$', 'zz91yinyong.views.choujiangstaus'),
	(r'^choujiangcount.html$', 'zz91yinyong.views.choujiangcount'),
	#2016砸金蛋活动
	(r'^zajindanstaus.html$', 'zz91yinyong.views.zajindanstaus'),
	(r'^zajindancount.html$', 'zz91yinyong.views.zajindancount'),
	#2016刮刮乐活动
	(r'^guagualecount.html$', 'zz91yinyong.views.guagualecount'),
	(r'^guagualestaus.html$', 'zz91yinyong.views.guagualestaus'),
	
	#2016国庆抽奖
	(r'^guoqincount2016.html$', 'zz91yinyong.views.guoqincount2016'),
	(r'^guoqin2016staus.html$', 'zz91yinyong.views.guoqin2016staus'),
	
	(r'^updatelogininfo.html$', 'zz91yinyong.views.updatelogininfo'),
	
	(r'^subject/hongbao.html$', 'zz91yinyong.views.subject_hongbao'),

	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':STATIC_ROOT}),
	
)

handler404 = 'zz91yinyong.views.viewer_404'
handler500 = 'zz91yinyong.views.viewer_500'
