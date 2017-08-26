function compareVersion(ov, nv) {
	if (!ov || !nv || ov == "" || nv == "") {
		return false;
	}
	var b = false, ova = ov.split(".", 4), nva = nv.split(".", 4);
	for (var i = 0; i < ova.length && i < nva.length; i++) {
		var so = ova[i], no = parseInt(so), sn = nva[i], nn = parseInt(sn);
		if (nn > no || sn.length > so.length) {
			return true;
		} else if (nn < no) {
			return false;
		}
	}
	if (nva.length > ova.length && 0 == nv.indexOf(ov)) {
		return true;
	}
}
function openApp() {
    api.openApp({
        androidPkg : 'android.intent.action.VIEW',
        mimeType : 'text/html',
        uri : 'http://app.zz91.com/app/zz91.apk'
    }, function(ret, err) {
        var msg = JSON.stringify(ret);
        api.alert({
            title : '确定版本更新',
            msg : '',
            buttons : ['确定']
        });
    });
}
function oldappupdateverson(){
	if (api.systemType == "android"){
		var updateflag = compareVersion(api.appVersion, '1.4.52');
		if (updateflag){
			api.confirm({
				title : '软件更新',
				msg : '你当前的版本太低了，建议你更新最新版本',
				buttons : ['立即更新','取消'],
				
			}, function(ret, err) {
				if (ret.buttonIndex == 1) {
					openApp()
				}
			});
		}
	}
}
//融云
function rongcloudcontact() {
	oldappupdateverson()
	//融云
	//apppushself()
	receviedxg()
	api.setStatusBarStyle({
		style : 'dark',
		color:'#fff',
	});
	var rong = api.require('rongCloud2');
	if (rong) {
		rong.init(function(ret, err) {
			if (ret.status == 'error')
				api.toast({
					msg: err.code
				});
		});
		//getchoujiangnum()
		//获取token
		var data = {
				company_id: UserInfo.memberID(),
				usertoken: UserInfo.token(),
				appsystem: api.systemType,
				datatype: "json",
				userid: api.deviceId,
			}
			//zzalert(api.deviceId)
		zzappajax("get", hosturl + "rong/gettoken.html", data, function(ret) {
				if (ret) {
					var token = ret.token
					rong.connect({
							token: token
						},
						function(ret, err) {
							//api.toast({ msg: ret });
						})
				}
			}, function(errret) {
				//zzalert(JSON.stringify(errret))
			})
			//		rong.connect({
			//				token: '10p45ESwJetPSwArNU/s+0PbTqeKLP/CYlw+oPc8EhCbzCOJMYx2vcoMAY89nXSWfv1GqlaUE1JCF4GppQOW0NIxXgC0N/nHjf8EzI4J3So='
			//			},
			//			function(ret, err) {
			//				if (ret.status == 'success'){
			//					//alert(ret.result.userId)
			//					rong.sendTextMessage({
			//				        conversationType: 'PRIVATE',
			//				        targetId: ret.result.userId,
			//				        text: 'Hello world.',
			//				        extra: ''
			//				    }, function (ret, err) {
			//				    	//alert(JSON.stringify(ret))
			//				    	//alert(JSON.stringify(err))
			//				        if (ret.status == 'prepare')
			//				            //api.toast({ msg: JSON.stringify(ret.result.message) });
			//				        else if (ret.status == 'success')
			//				            //api.toast({ msg: ret.result.message.messageId });
			//				        else if (ret.status == 'error')
			//				            //api.toast({ msg: err.code });
			//				    }
			//				    );
			//				}
			//			});
			//设置连接状态变化的监听器
		rong.setConnectionStatusListener(function(ret, err) {
			//alert(ret.result.connectionStatus)
			//api.toast({ msg: ret.result.connectionStatus });
		});
		//设置接收消息的监听器
		rong.setOnReceiveMessageListener(function(ret, err) {
			//api.toast({ msg: JSON.stringify(ret.result.message.content) });
			showmsgstaus(ret.result.message)
				//alert(JSON.stringify(ret))
			//showlocalmsg()
				//api.toast({ msg: JSON.stringify(ret.result) });
				//api.toast({ msg: ret.result.message.left });

			//		    {
			//			    result:
			//			    {
			//			        message:
			//			        {
			//			            content: {
			//			                text: 'Hello world!',
			//			                extra: ''
			//			            }, // 消息内容
			//			            conversationType: 'PRIVATE', // 参见 会话类型 枚举
			//			            messageDirection: 'SEND', // 消息方向：SEND 或者 RECEIVE
			//			            targetId: '55', // 这里对应消息发送者的 userId
			//			            objectName: 'RC:TxtMsg', // 消息类型，参见 http://docs.rongcloud.cn/android_message.html#_内置内容类消息
			//			            sentStatus: 'SENDING', // 发送状态：SENDING, SENT 或 FAILED
			//			            senderUserId: '55', // 发送者 userId
			//			            messageId: 608, // 本地消息 Id
			//			            sentTime: 1418971531533, // 发送消息的时间戳，从 1970 年 1 月 1 日 0 点 0 分 0 秒开始到现在的毫秒数
			//			            receivedTime: 0 // 收到消息的时间戳，从 1970 年 1 月 1 日 0 点 0 分 0 秒开始到现在的毫秒数
			//			        },
			//			        left: 0 // 剩余未拉取的消息数目
			//			    }
			//			}
		})
	} else {
		api.toast({
			msg: "err"
		});
	}
	//打开广告
	//openwindows("noorder",hosturl+"app/html/ad/shuang11.html");
	var adloadflag = $api.getStorage("adload1");
	//adloadflag=1
	if (!adloadflag || adloadflag == 1) {
		//openwindows("noorder",hosturl+"app/html/ad/zhongqiu/gg.html");
	} else {
		
	}
	//打开双11砍价活动
	
	$api.setStorage("adload1", 0);
}

function openadshowphone() {
	var pageParam = {
		wintitle: "显示联系方式",
		type: "serviceshow2",
		bounces: false,
	};
	openWin("serviceshow2", "../service/show2.html", pageParam);
}
//打开中秋分享
function zhongqiushare() {
	var pageParam = {
		wintitle: "中秋祝福！",
		type: "zhongqiu",
		bounces: false,
	};
	openWin("zhongqiu", hosturl + "app/html/ad/zhongqiu/index.html", pageParam);
}
//打开双11砍价活动
function shuang11kanjia() {
	var pageParam = {
		wintitle: "双11，呼朋唤友来砍价，“零”元价格到！",
		type: "shuang11k",
		bounces: false,
	};
	openWin("shuang11k", "http://m.zz91.com/kanjia/index.html", pageParam);
}
//打开双11充值活动
function shuang11show() {
	var pageParam = {
		wintitle: "2016双十一主会场_双11冲值_双十一返券",
		type: "shuang11c",
		bounces: false,
	};
	pageParam['company_id'] = UserInfo.memberID();
	pageParam['usertoken'] = UserInfo.token();
	pageParam['appsystem'] = api.systemType;
	openWin("shuang11c", hosturl + "app/html/ad/shuang11/index.html", pageParam);
}
//统一打开窗口
function openblankwin(title, name, url) {
	var pageParam = {
		wintitle: title,
		type: name,
		bounces: false
	};
	pageParam['company_id'] = UserInfo.memberID();
	pageParam['usertoken'] = UserInfo.token();
	pageParam['appsystem'] = api.systemType;
	openWin(name, url, pageParam);
}
//供求置顶2个月送企业秀
function openprotop() {
	if (!havelogin()) {
		return false;
	}
	var data = {
		paytype: '52',
		money: "900",
		datatype: 'json',
		t: (new Date()).getTime().toString()
	}
	api.confirm({
		title: '提示',
		msg: "确定要购买吗？",
		buttons: ['确定购买', '取消']
	}, function(ret, err) {
		if (ret.buttonIndex == 1) {
//			api.showProgress({
//				title: '加载中...',
//				modal: false
//			});
			zzappajax("get", hosturl + 'qianbao/qianbaopay.html', data, function(ret) {
				if (ret) {
					if (ret.err == 'false') {
						api.confirm({
							title: '提示',
							msg: ret.errtext,
							buttons: ['关闭', '查看我的服务']
						}, function(ret, err) {
							if (ret) {
								if (ret.buttonIndex == 2) {
									var pageParam = {
										wintitle: "我的服务",
										type: "myservice",
									};
									openWin("myservice", "../service/myservice.html", pageParam);
								} else {
									//api.closeWin();
								}
							} else {}
						});

					}
					if (ret.err == 'true' && ret.blanceflag == '0') {
						api.hideProgress();
						yuebuzuFun();
					}
					if (ret.err == 'true' && ret.blanceflag == '1') {
						zzalert(ret.errtext);
					}
					api.hideProgress();
				} else {
					api.hideProgress();
					if (err) {
						saveerrlog(err.body);
					}
				};
			}, function() {api.hideProgress();})
		}
	})
}
//购买显示联系方式+供求自动刷新 抢购服务
function openshowcontactandreflush() {
	if (!havelogin()) {
		return false;
	}
	var data = {
		paytype: '48',
		money: "350",
		datatype: 'json',
		t: (new Date()).getTime().toString()
	}
	api.confirm({
		title: '提示',
		msg: "确定要购买吗？",
		buttons: ['确定购买', '取消']
	}, function(ret, err) {
		if (ret.buttonIndex == 1) {
//			api.showProgress({
//				title: '加载中...',
//				modal: false
//			});
			zzappajax("get", hosturl + 'qianbao/qianbaopay.html', data, function(ret) {
				if (ret) {
					if (ret.err == 'false') {
						api.confirm({
							title: '提示',
							msg: ret.errtext,
							buttons: ['关闭', '查看我的服务']
						}, function(ret, err) {
							if (ret) {
								if (ret.buttonIndex == 2) {
									var pageParam = {
										wintitle: "我的服务",
										type: "myservice",
									};
									openWin("myservice", "../service/myservice.html", pageParam);
								} else {
									//api.closeWin();
								}
							} else {}
						});

					}
					if (ret.err == 'true' && ret.blanceflag == '0') {
						api.hideProgress();
						yuebuzuFun();
					}
					if (ret.err == 'true' && ret.blanceflag == '1') {
						zzalert(ret.errtext);
					}
					api.hideProgress();
				} else {
					api.hideProgress();
					if (err) {
						saveerrlog(err.body);
					}
				};
			}, function() {
				api.hideProgress();
			})
		}
	})

}
//购买双11砍价活动
function buyshuang11pro(paytype,money) {
	if (!havelogin()) {
		return false;
	}
	paytype1=0
	if (paytype==2){
		paytype1=11
	}
	if (paytype==1){
		paytype1=42
	}
	if (paytype==3){
		paytype1=9
	}
	var data = {
		paytype: paytype1,
		money: money,
		datatype: 'json',
		t: (new Date()).getTime().toString()
	}
	if (paytype==1){
		data['datevalue']=1
	}
	api.confirm({
		title: '提示',
		msg: "确定要购买吗？",
		buttons: ['确定购买', '取消']
	}, function(ret, err) {
		if (ret.buttonIndex == 1) {
//			api.showProgress({
//				title: '加载中...',
//				modal: false
//			});
			zzappajax("get", hosturl + 'qianbao/qianbaopay.html', data, function(ret) {
				if (ret) {
					if (ret.err == 'false') {
						api.confirm({
							title: '提示',
							msg: ret.errtext,
							buttons: ['关闭', '查看我的服务']
						}, function(ret, err) {
							if (ret) {
								if (ret.buttonIndex == 2) {
									var pageParam = {
										wintitle: "我的服务",
										type: "myservice",
									};
									openWin("myservice", "../service/myservice.html", pageParam);
								} else {
									//api.closeWin();
								}
							} else {}
						});

					}
					if (ret.err == 'true' && ret.blanceflag == '0') {
						api.hideProgress();
						yuebuzuFun();
					}
					if (ret.err == 'true' && ret.blanceflag == '1') {
						zzalert(ret.errtext);
					}
					api.hideProgress();
				} else {
					api.hideProgress();
					if (err) {
						saveerrlog(err.body);
					}
				};
			}, function() {
				api.hideProgress();
			})
		}
	})

}
//双11充值送券活动
function shuang11chongzhi(payflag,amount){
	if (!havelogin()){
		return false;
	}
	var subject = '再生钱包充值';
	var body = '再生钱包充值';
	if (amount=="添加" || amount==""){
		zzalert("请选择金额！");
		return;
	}
	var paytype="shuang11chongzhi"
	var tradeNO = new Date().getTime();
	var notifyURL = 'http://m.zz91.com';
	var paytypevalue;
	if (payflag==1){
		paytypevalue="在线-支付宝"
	}
	if (payflag==2){
		paytypevalue="在线-微信支付"
	}
	if (payflag==3){
		paytypevalue="在线-易宝支付"
	}
	//保存订单
	var data={
		company_id : UserInfo.memberID(),
		usertoken : UserInfo.token(),
		appsystem : api.systemType,
		datatype : "json",
		total_fee : amount,
		subject : subject,
		paytype : paytype,
		payflag : paytypevalue,
	}
	
	api.ajax({
	    url : hosturl + 'zz91pay.html',
	    method : 'get',
	    timeout : 30,
	    dataType : 'json',
	    returnAll : false,
	    data : {
			values : data
		}
	}, function(ret, err) {
		//zzalert(JSON.stringify(ret))
	    if (ret) {
	    	var yeepayurl=$.param(ret);
	    	//支付宝支付
			if (payflag==1){
				if (api.systemType == "ios") {
					api.appInstalled({
					    appBundle: "alipay"
					},function(ret, err){
					    if(ret.installed){
					        confirmzhifu();
					    }else{
					        //应用未安装
					        zzalert("您还未安装支付宝，请安装支付宝后再支付！")
					        return false;
					    }
					});
				}else{
					api.execScript({
						name : "shuang11c",
						frameName:"shuang11c_",
						script : "apploadingpay();"
					});
				}
				var obj = api.require('aliPay');
				obj.pay({
				    subject:subject,
				    body:body,
				    amount:amount,
				    tradeNO:ret.order_id
				},function(ret,err) {
					if (ret.code==9000){
						confirmzhifu();
						api.alert({
					        title: '提示',
					        msg: '支付成功',
					        buttons: ['确定']
					    });
						//api.closeWin();
				    }else{
				    	zzalert("支付异常！请重试或选择其他支付方式。");
				    }
				    api.hideProgress();
				    api.execScript({
						name : "shuang11c",
						frameName:"shuang11c_",
						script : "appclosepay();"
					});
				});
			}else{
				//api.hideProgress();
				api.execScript({
					name : "shuang11c",
					frameName:"shuang11c_",
					script : "appclosepay();"
				});
			}
			//微信支付
			if (payflag==2){
				if (api.systemType == "ios") {
					
					api.appInstalled({
					    appBundle: "weixin"
					},function(ret, err){
					    if(ret.installed){
					        confirmzhifu();
					    }else{
					        //应用未安装
					        zzalert("您还未安装微信，请安装微信后再支付！")
					        return false;
					    }
					});
				}else{
					api.execScript({
						name : "shuang11c",
						frameName:"shuang11c_",
						script : "apploadingpay();"
					});
				}
				//
				var out_trade_no=ret.order_id;
				//var wxdata={
				//	total_fee:amount*100,
				//	out_trade_no:out_trade_no,
				//}
				//wxpaypost(wxdata)
				
				
				var wxPay = api.require('wxPay');
				wxPay.config({
				     apiKey: 'wx6bb99d2f0581b5b0',
				     mchId: '1340905101',
				     partnerKey: 'OR3g3vtcNAdvm25ycHKfH5KWrLY9kAvd',
				     notifyUrl: 'http://m.zz91.com/zz91payverify_notify.html'
				}, function(ret, err){
				     if(ret.status){
				        //zzalert('配置商户支付参数成功');
				        $paySubmitWx();
				     }else{
				        //zzalert(err.code);
				        zzalert("支付异常！请重试或选择其他支付方式。");
				        api.hideProgress();
				        api.execScript({
							name : "shuang11c",
							frameName:"shuang11c_",
							script : "appclosepay();"
						});
				     }
				     //api.hideProgress();
				});
				
				//var wxPay = api.require('wxPay');
				
				$paySubmitWx=function(){
					wxPay.pay({
					     description: subject,
					     totalFee: amount*100,
					     tradeNo: out_trade_no,
					     spbillCreateIP: '196.168.1.1',
					     deviceInfo: api.deviceId,
					     detail: subject,
					     attach: body,
					     feeType: 'CNY',
					     //timeStart: '20091225091010',
					     //timeExpire: '20091227091010',
					     //goodsTag: 'WXG',
					     //productId: '12235413214070356458058',
					     //openId: 'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'
					},function(ret, err){
						 //zzalert(JSON.stringify(ret))
					     if(ret.status){
								var data={
									out_trade_no : out_trade_no,
									trade_no : out_trade_no,
									trade_status : "TRADE_SUCCESS",
								}
								api.showProgress({
									title : '充值中，请不要关闭窗口！',
									modal : true
								});
								api.ajax({
									url : 'http://m.zz91.com/zz91payverify_notify.html',
									method : "post",
									timeout : 30,
									dataType : 'html',
									returnAll : false,
									data : {
										values : data
									}
								}, function(ret, err) {
									confirmzhifu();
									api.alert({
								        title: '提示',
								        msg: '支付成功',
								        buttons: ['确定']
								    });
									
									api.hideProgress();
									api.execScript({
										name : "shuang11c",
										frameName:"shuang11c_",
										script : "appclosepay();"
									});
									//api.closeWin();
								});
								
								
					     }else{
					         //zzalert(err.body);
					         if (err.code=="-1"){
					         	zzalert("系统错误，或接口还未开通!");
					         }
					         api.hideProgress();
					         api.execScript({
								name : "shuang11c",
								frameName:"shuang11c_",
								script : "appclosepay();"
							});
					     }
					});
				}
				
				
			}
			//银行卡支付
			if (payflag==3){
				
				confirmzhifu();
				var payurl="http://phppay.zz91.com/pay/toMobilepay.php?"+yeepayurl;
				var pageParam = {
					wintitle : "在线充值",
					type : "backchongzhi",
					bounces : false
				};
				openWin("backchongzhi", payurl, pageParam);
				api.hideProgress();
				api.execScript({
					name : "shuang11c",
					frameName:"shuang11c_",
					script : "appclosepay();"
				});
				//zzalert("等待开通中!")
			}
			//
	    } else {
	    	if(err){
				saveerrlog(err.body);
			}
	    };
	    //api.hideProgress();
	});
}
//确认支付
function confirmzhifu(){
	api.execScript({
		name : 'shuang11c',
		frameName : 'shuang11c_',
		script : 'confirmzhifu()'
	});
}
function showmsgstaus(returnvalue) {
	//留言数量
	if (returnvalue.content.text == "question") {
		$(".mymessages").show();
		if (frame4 == 1) {
			var questionnum = returnvalue.content.extra
			if (frame4 == 1) {
				api.execScript({
					frameName: 'my-home',
					script: "showquestionnum('" + questionnum + "')"
				});
			}
		}
	}
	//聊天提醒
	if (returnvalue.content.text == "chat") {
		$(".chatmessages").show();
		if (frame3 == 1) {
			if (frame3 == 1) {
				api.execScript({
					name: 'root',
					frameName: 'quote',
					script: 'ajaxInfo(1)'
				});
			}
		}
	}
}
//自带推送
function apppushself() {
	//  绑定用户
	//	var push = api.require('push');
	//	push.bind({
	//	    userName:api.deviceId,
	//	    userId:"c" + api.deviceId
	//	},function(ret,err){
	//	    if(ret.status){
	//	        api.toast({msg:'绑定成功'});
	//	    }else{
	//	        api.toast({msg:err.msg});
	//	    }
	//	});
}

//信鸽推送数据接收
function receviedxg() {
	var tencentPush = api.require('tencentPush');
	// 注册通知被点击的回调
	var resultCallback = function(ret, err) {
		var customContent = ret.customContent;
		if (customContent) {
			customContent = strToJson(customContent)
			if (customContent.hasOwnProperty("news")) {
				var pageParam = {
					wintitle: "资讯详情",
					type: "detail",
					bounces: false,
					infoid: customContent.news
				};
				openWin("detail" + customContent.news, "../news/detail.html", pageParam);
			}
			if (customContent.hasOwnProperty("huzhu")) {
				var pageParam = {
					wintitle: "互助详情",
					type: "double-heart",
					bounces: false, //窗口弹动
					infoid: customContent.huzhu
						// module:"回复"
				};
				openWin("cunity-detail", "../huzhu/cunity-detail.html", pageParam);
			}
			if (customContent.hasOwnProperty("url")) {
				var pageParam = {
					wintitle: "详细内容",
					type: "openother",
					bounces: false, //窗口弹动
				};
				openWin("openother", customContent.url, pageParam);
			}
			if (customContent.hasOwnProperty("orderprice")) {
				var pageParam = {
					wintitle: "我的行情定制",
					type: "offer-list",
					bounces: false, //窗口弹动
					orderflag: 1,
				};
				openWin("offer-list", "../price/offer-list.html", pageParam);
				randomSwitchBtn('', 'tabbar2', 1)
			}
		}
	}
	var params = {
		name: "notifactionClick"
	};
	tencentPush.setListener(params, resultCallback);
	//showlocalmsg()
}

//增加本地消息
function showlocalmsg() {
	// 添加本地通知
	var tencentPush = api.require('tencentPush');
	var params = {
		title: "消息", // 标题
		content: "全球钢市继续分化弱行走势", // 内容
		//date: "20150127", // 日期
		//hour: "15", // 时间
		//min: "15", // 分钟
		customContent: "{\"news\":\"1158007\"}", // 自定义key-value
		//activity: "", // 打开的activity
		//ring: 1, // 是否响铃
		//vibrate: 1 // 是否振动
	};
	var resultCallback = function(ret, err) {
		if (ret.status) {
			//zzalert("添加通知成功，通知id：" + ret.notiId);
		} else {
			//zzalert("添加本地通知失败，错误码：" + err.code + "，错误信息：" + err.msg);
		}
	};
	tencentPush.addlocalNotification(params, resultCallback);
}

function getchoujiangnum() {
	var ajaxurl = "http://pyapp.zz91.com/choujiangcount.html?company_id=" + UserInfo.memberID() + "&p" + (new Date()).getTime().toString();
	$.getScript(ajaxurl, function() {
		var ccount = _suggest_result_.count;
		if (parseInt(ccount) > 0) {
			api.confirm({
				title: '2016端午大抽奖',
				msg: '恭喜您在“2016端午抽奖”活动中获得' + ccount + '次抽奖机会，赶紧去试试运气吧？',
				buttons: ['取消', '立即抽奖']
			}, function(ret, err) {
				if (ret) {
					if (ret.buttonIndex == 2) {
						var pageParam = {
							wintitle: "2016端午抽奖",
							type: "2016daunwu",
							bounces: false
						};
						openWin("2016daunwu", "http://m.zz91.com/choujiang/index.html", pageParam);
					}
				} else {

				}
			});
		}
	});
}

function tokeninfo() {
	var data = {
		pwd_hash: UserInfo.password(),
		username: UserInfo.username(),
		clientid : api.deviceId,
	}
	var datainfo = {
		company_id: UserInfo.memberID(),
		usertoken: UserInfo.token(),
	}
	var login_sn = UserInfo.has_login();
	if (login_sn) {
		zzappajax("post", hosturl + "user/tokeninfo.html", datainfo, function(ret) {
			//zzalert(JSON.stringify(ret))
			if (ret.err == "true") {
				//如果token过期，重新获得
				zzappajax("post", hosturl + "user/get_token.html", data, function(ret) {
					//zzalert(JSON.stringify(ret))
					if (ret.err == "false") {
						var token = ret.result
							//保存信息到本地
						UserInfo.token(token);
					} else {
						UserInfo.clear();
						//havelogin();
					}
				}, function(errret) {
					//zzalert(JSON.stringify(errret))
				})
			}
		}, '')
	}
}

function opengonggao(){
	//不打开认证提醒
	return false;
	if (zzonline==0){
		return false;
	}
	api.openFrame({
	    name: 'gonggao',
	    url: hosturl+"app/html/ad/gonggao.html",
	    rect:{
	        x:0,
	        y:0,
	        w:'auto',
	        h:api.winHeight-$("footer").height()
	    },
	    bounces: false,
	});
	api.bringFrameToFront({
	    from: 'post-add',
	});
}