//ASTO ITC.-----hetao138@gmail.com
//通用类方法  通过构造函数构建，每次使用前无需建立新对象调用（不需要new）直接调用便可
//NOTES注意:请严格按照JS书写代码格式，便于后期对JS进行压缩
// 使用方法示例 --Exp:hb.util.msg
//hb.util.msg.Error({m:"commonError"});

//非通用类方法原型prototype构建，每次使用前，请务必建立调用对象（使用new）
//NOTES注意:请严格按照JS书写代码格式，便于后期对JS进行压缩
// 使用方法示例 --Exp:hb.util.msg
//建立调用对象
//var s = new hb.index.slide();
//赋值参数 引用
//s.indexTopSlide(config={conter:"#hbslide",spd:500,intval:5000});

/******hb namespace register******/

hb={};//申明用于命名空间注册
hb.register= function(fname){
	var nArray = fname.split('.');//分置方法
	var tfn = '';
	var feval= '';
	
	for(var i= 0; i< nArray.length;i++){
		if(i!=0){tfn += '.';}
		tfn += nArray[i];
		feval += "if (typeof("+tfn+") == 'undefined'){" + tfn + "={};}";
	}
	//alert(feval);
	if(feval!=''){eval(feval)}
}

hb.register('hb.util');//huanbao通用方法
hb.util.context={}//上下文注册关系
hb.util.search={};//搜索方法
hb.util.validate={};//验证
hb.util.loadDynamic={};//外部文件动态加载
hb.util.topBar={};//topbar 动作封装
hb.util.header={};//头部动作封装

hb.util.commonCallback=null;


////通用错误消息列队
//hb.util.msg.Error=function(key){
//	var m={
//            "commonError":"发生了一点错误，请过一会再试!",
//            "connectError":"与服务器失去连接，请过一会再试!",
//            "default":"发生错误，请重新操作!"
//        };
//        if(typeof(m[key]) == "undefined" ){
//            alert(m["default"]);
//            return ;
//        }
//        alert(m[key]);
//        return ;
//};
//
////通用信息提醒消息列队
//hb.util.msg.Tips=function(key){
//	var m={
//            "failureInsert":"信息没有发布成功，可能是服务器出现了问题，请再试一次!",
//            "failureUpdate":"信息没有更新成功，可能是服务器出现了问题，请再试一次!",
//            "sessionTimeOut":"您是不是很长时间没有操作了，请重新登录后再操作!",
//            "memberAuthorFailure":"对不起，您现在的会员类型还不能这么做，\n您可以跟我们的客服联系，升级会员后再操作!",
//            "companyInfoBroken":"对不起，您查看的企业信息不完整!",
//            "contactInfoBroken":"对不起，您查看的联系人信息不完整!",
//            "overLimit":"对不起，您的操作已经超过了限制!",
//            "canNotVoteSelf":"对不起，您不能对自己评价!",
//            "default":"抱歉!你的操作有误,请与客服联系!"
//        };
//        if(typeof(m[key]) == "undefined" ){
//            alert(m["default"]);
//            return ;
//        }
//        alert(m[key]);
//        return ;
//};

//上下文路径
hb.util.context.path={
		www:'http:\/\/www.huanbao.com',
		trade:'http:\/\/www.huanbao.com\/trade',
		exhibit:'http:\/\/www.huanbao.com\/exhibit',
		news:'http:\/\/www.huanbao.com\/news',
		myesite:'http:\/\/www.huanbao.com\/myesite',
		esite:'http:\/\/www.huanbao.com\/esite'
}
//上下文信息
hb.util.context.msg={
	ipt_username:'请输入用户名',
	ipt_password:'请输入密码',
	ipt_email:'请输入邮箱',
	comm_loading:"正在加载...",
	//There was an error contacting the server. Please try again.
	comm_server_error:"连接服务器时发生错误.请再试一次.",
	comm_session_timeout:"登录超时.请重新登录."
}

hb.util.search.slideSearchType=function(c){
	this.c = c||{};
    var srhType 		= $(c.hbSearchType).children()||$("#hbSearchType").children();
    var srhTypeValue	= $(c.hbsearchTypeValue)||$("#hbSearchTypeValue");
    var srhKeyWords 	= $(c.hbsearchKeyWords)||$("#hbSearchKeyWords");
    var srhLabel 		= $(c.hbSearchKeyLabel)||$("#hbSearchKeyLabel");
    
    srhType.parent().after('<span class="isSelectTip"></span>');
    
	srhType.click(function(){
		$(this).addClass("srhyes").siblings('li').removeClass('srhyes');
		$('.isSelectTip').animate({left:($(this).width()*($(this).index()+1)-8)},200)
		srhTypeValue.attr({value:$(this).index()});
	});
	srhKeyWords.focus(function(){
		srhLabel.fadeOut(200);
	});
	srhKeyWords.blur(function(){
		var thisValue=$(this).val();
		if($.trim(thisValue)==""){
			srhLabel.fadeIn(200);
		}
	});
    
};



//通用供应搜索
hb.util.search.WWWSearch=function(c){
	var wwwSearch=this;
	this.c = c||{};
	
    this.products=function(config){
        config=config||{};  
        var contextpath=config.contextpath||"";
        var target=config.target||"_blank"; 
        var searchOpt=config.searchOptions||[];
        var debug=config.debug||false;
        
        var ptype=searchOpt["ptype"]||"";  
        var province=searchOpt["province"]||""; 
        var posttime=searchOpt["posttime"]||"";
        var priceflag=searchOpt["priceflag"]||""; 
        var nopiclist=searchOpt["nopiclist"]||""; 
        var havepic=searchOpt["havepic"]||"";
        var page=searchOpt["page"]||"";
        var keywords=searchOpt["keywords"]||"";  //关键字
        
        if(keywords.length<=0){
            return false;
        }
        
        window.open("http://www.huanbao.com/trade/suply/?ptype="+ptype+"&keywords="+encodeURI(keywords));
        
//      var targetUrl="/offerlist";
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--a",ptype);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--b",province);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--c",posttime);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--d",priceflag);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--e",nopiclist);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--f",havepic);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--p",page);
//      targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--",encodeURI(keywords));
//      
//      targetUrl=targetUrl+".htm";
//      if(debug){
//          alert("the target url is: "+targetUrl);
//      }else{
//          if(target=="_self"){
//              location.href=contextpath+targetUrl;
//          }else{
//              window.open(contextpath+targetUrl);
//          }
//      }
        
    };
    
    this.price=function(config){
        config=config||{};
        var contextpath=config.contextpath||"";
        var target=config.target||"_blank";
        var searchOpt=config.searchOptions||[];
        var k=searchOpt["keywords"]||"";
        
        if(k.length<=0){
            return false;
        }
        
        var targetUrl="/priceSearch.htm?title="+encodeURI(k);
        
        if(target=="_self"){
            location.href=contextpath+targetUrl;
        }else{
            window.open(contextpath+targetUrl);
        }
    };
    
    this.company=function(config){
    };
    
    this.companyPrice=function(config){
        config=config||{};
        var contextpath=config.contextpath||"";
        var target=config.target||"_blank";
        var searchOpt=config.searchOptions||[];
        var k=searchOpt["keywords"]||"";  //关键字
        var pc=searchOpt["categoryCompanyPriceCode"]||"";  //企业报价类别
        var area=searchOpt["area"]||"";  //地区
        var interval=searchOpt["interval"]||"";  //产品刷新时间期限  距离现在，单位：天
        var priceRange=searchOpt["priceRange"]||"";  //报价区间
        var targetUrl="/companyprice/index--"+encodeURI(k);
        targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--pc",pc);
        targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--area",area);
        targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--int",interval);
        targetUrl=wwwSearch.buildProductSearchUrl(targetUrl,"--pr",priceRange);
        targetUrl=targetUrl+".htm";
        if(target=="_self"){
            location.href=contextpath+targetUrl;
        }else{
            window.open(contextpath+targetUrl);
        }
    };

    this.buildProductSearchUrl=function(targetUrl,prefix,v){
        if(v.length>0){
            return targetUrl+prefix+v;
        }else{
            return targetUrl+prefix;
        }
    };
    
    //initialization  search  effects
    this.initSearchSlide=function(slideObj,noSearchSelectClass,SearchSelectClass,getSearchType,searchFocus,searchLabel){
        var operateObj = zz91Util.getElem(slideObj).getElementsByTagName("li");
        getSearchType = zz91Util.getElem(getSearchType);
        searchLabel=zz91Util.getElem(searchLabel);
        searchFocus = zz91Util.getElem(searchFocus);
        //获取当前节点索引
        var getIndex = function(self, obj){
            for(var i=0;i<obj.length;i++){
                if(obj[i]== self){
                    return i;
                }
            }
        }
        for (var i = 0; i < operateObj.length; i++) {
            iNum = i
            operateObj[i].onmouseover = function(){
                //alert(i);
                //i = parseInt(i);
                for (var j = 0; j < operateObj.length; j++) {
                    operateObj[j].className = noSearchSelectClass;
                }
                this.className = SearchSelectClass;
                //确定搜索类型，并且设置搜索焦点
                //alert(getSearchType.value+"_" +getIndex(this,operateObj));
                getSearchType.value = parseInt(getIndex(this,operateObj)+1);
                searchLabel.style.display="none";
                searchFocus.focus();    
            }
            operateObj[i].onmouseout=function(){
                if (searchFocus.value == "" || searchFocus.value == null) {
                    setInterval(function(){
                        searchFocus.blur();
                        searchLabel.style.display = "";
                    }, 1000)
                }
            }
        }
        searchLabel.onclick=function(){
            searchLabel.style.display="none";
            searchFocus.focus();
        }
    };
};
	

//通用登陆
//hb.util.login.LoginComm=function(config){
//        this.config=config||{};
//        
////      username,password,cookieMaxAge,url,randcode,randcodeKey,contextpath,fn
//        
//        var utils=this;
//        
//        var _username=config.username||"";
//        var _password=config.password||"";
//        var _cookieMaxAge=config.cookieMaxAge||"";
//        var _url=config.url||"";
//        var _randcode=config.randcode||"";
//        var _randcodeKey=config.randcodeKey||"";
//        var _contextpath=config.contextpath||hb.util.context.path.www;
//        var _success=config.success||function(response){
//            if(response.success){
//                window.location.href=response.data;
//            }else{
//                alert(response.data);
//            //  utils.showmsg(response.data);
//            }
//        };
//        
//        jQuery.ajax({
//            url:_contextpath+"/login.htm",
//            type:"POST",
//            cache:false,
//            dataType:"json",
//            data:{username:_username,password:_password,cookieMaxAge:_cookieMaxAge,url:_url,randCode:_randcode,randCodeKey:_randcodeKey},
//            success:_success,
//            error:function(e){
//                hb.util.msg.Error("accountValicateError");
//            }
//        });
//};

//网站通用登出
//hb.util.login.LoginOut=function(config){
//	if(config==null){
//            config={};
//        }
//        var utils=this;
//        var _url=config.url||"";
//        var _contextRoot = config.contextpath||"";
//        var _successFn=config.success||function(response){
//            if(response.success){
//                window.location.href=response.data;
//            }else{
//                alert(response.data);
//            }
//        };
//        jQuery.ajax({
//            url:_contextRoot+"/logout.htm",
//            type:"POST",
//            cache:false,
//            dataType:"json",
//            data:{url:_url},
//            success:_successFn
//        });
//};

//通用验证登陆
//hb.util.login.CheckLogin=function(username,password,cookieMaxAge,url,randcode,randcodeKey,contextpath,fn){
//    jQuery.ajax({
//        url:contextpath+"/dologin.htm",
//        type:"POST",
//        cache:false,
//        dataType:"json",
//        data:{username:username,password:password,cookieMaxAge:cookieMaxAge,url:url,randCode:randcode,randCodeKey:randcodeKey},
//        success:fn,
//        error:function(e){
//            alert("您的账号存在问题,请再试一次,如果仍然出现错误,请联系我们!" );
//        }
//    });
//};

//通用超时登出
//hb.util.login.LogOut=function(url,contextpath,fn){
//    jQuery.ajax({
//        url:contextpath+"/logout.htm",
//        type:"POST",
//        cache:false,
//        dataType:"json",
//        data:{url:url},
//        success:fn
//    });
//};


//网站通用动态加载js
hb.util.loadDynamic.LoadJs=function(file, callback){
	var script = document.createElement('script');
        script.type = 'text/javascript';
        if (callback) script.onload = script.onreadystatechange = function() {
            if (script.readyState && script.readyState != 'loaded' && script.readyState != 'complete') return;
            script.onreadystatechange = script.onload = null;
            callback();
        };
        script.src = url;
        document.getElementsByTagName('head')[0].appendChild(script);	
}

//表单简单验证
hb.util.validate.SimpleValidate=function(){
	return {
            required:function(v){
                //对v做处理，去除空格等
                return v.length>0;
            },
            email:function(v){
                return /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i.test(v);
            },
            url:function(v){
                return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(v);
            },
            date:function(v){
                return !/Invalid|NaN/.test(new Date(v));
            },
            number: function(v) {
                return /^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(v);
            }
        }
};

/**
 * 通用地址联动加载
 * 示例：
 * var selector=new hb.util.Selector({
 * 		url:"/path/to/main/seletor/resources",
 * 		assistUrl:"/path/to/assist/selector/resources",
 * 		changeCallback:function(){
 * 			alert("alert while selector change")
 * 		},
 * 		field:{code:"code",label:"name"}
 * });
 * 
 * 初始化联动菜单
 * selector.init({
 * 		rootCode:"1000",
 * 		selectors:["#s1","#s2"],
 * 		assistSelects:["#assist"],
 * 		codeLength:4,
 * 		initCode:"100010001001",
 * 		initAssistCode:""
 * });
 * 
 * alert(selector.getValue());
 * 
 * */
hb.util.Selector=function(config){
	this.config = config||{};
    this.url=config.url||"/category/areaChild.htm";
    this.assistUrl=config.assistUrl||"/category/areaChild.htm";
    this.changCallback=config.changeCallback||function(){};
    this.field=config.field||{code:"code",label:"label"};
    this.selectors=config.selects||[];
    this.assistSelectors = config.assistSelects||[];
    
    var selinstance = this;
    
    this.init =function(cfg){
        cfg=cfg||{};
        var rootCode=cfg.rootCode||"";
        var codeLength=cfg.codeLength||4;
        var initCode=cfg.initCode||"";
        var initAssistCode=cfg.initAssistCode||"";
        
        var selectors=selinstance.selectors;
        var assistSelectors=selinstance.assistSelectors;
        
        //初始化辅助类别（如果有）
        if(assistSelectors.length>0 && initAssistCode!=""){
            selinstance.fillAssistOption(initCode, initAssistCode, assistSelectors[0]);
        }
        
        jQuery(selectors).each(function(idx,e){
            //初始化选择项    
            if(initCode.length>rootCode.length){
                if((rootCode.length+((idx+1)*codeLength))<=initCode.length){
                    var p=initCode.substring(0, rootCode.length+(idx*codeLength));
                    var c=initCode.substring(0, rootCode.length+(idx+1)*codeLength);
//                  alert(p+"   "+c)
                    selinstance.fillOption(p,c,e);
                }else{
                    if(initCode.length+codeLength == rootCode.length+((idx+1)*codeLength)){
                        selinstance.fillOption(initCode, "", e);
                    }
                }
            }else{
                if(idx==0){
                    selinstance.fillOption(rootCode,"",e);
                }
            }
            
            //为选择器绑定事件
            jQuery(e).change(function(obj){
                //如果选中值不为空，则将选中值放入指定隐藏域
                if(assistSelectors.length>0){
                    jQuery(assistSelectors[0]).val("");
                    var ahtml= jQuery(assistSelectors[0]).find('option:selected').html();
                    jQuery(assistSelectors[0]).empty();
                    jQuery(assistSelectors[0]).append("<option value=''>"+ahtml+"</option>");
                    if(jQuery(e).val()!="" && jQuery(e).val()!=null){
                        selinstance.fillAssistOption(jQuery(e).val(), "", assistSelectors[0]);
                    }
                }
                
                if(typeof(selectors[idx+1])!="undefined"){
	                //清除选择项后面的所有选择值
	                for(var ii=idx;ii<selectors.length;ii++){
	                    jQuery(selectors[ii+1]).val("");
	                    var html= jQuery(selectors[ii+1]).find('option:selected').html();
	                    jQuery(selectors[ii+1]).empty();
	                    jQuery(selectors[ii+1]).append("<option value=''>"+html+"</option>");
	                }
	                
	                //ajax获取子类别
	                if(jQuery(e).val()!="" && jQuery(e).val()!=null){
	                    selinstance.fillOption(jQuery(e).val(),"",selectors[idx+1]);
	                }
                }
                
                selinstance.changCallback(selinstance, idx);
            });
        });
    }
    
    this.fillOption = function(pc, currentCode, targetElement){
        jQuery.ajax({
            url:selinstance.url+"?parentCode="+pc,
            type:"get",
            cache:false,
            dataType:"json",
//            data:_data,
            success:function(req){
                jQuery(req).each(function(idx,e){
                    jQuery(targetElement).append("<option value='"+e[selinstance.field.code]+"'>"+e[selinstance.field.label]+"</option>");
                });
                jQuery(targetElement).val(currentCode);
            },
            error:function(e){
            }
        });
    }
    
    
    this.fillAssistOption = function(mainCode, currentCode, targetElement){
        jQuery.ajax({
            url:selinstance.assistUrl+"?mainCode="+mainCode,
            type:"POST",
            cache:false,
            dataType:"json",
//            data:{"mainCode":mainCode},
            success:function(req){
                jQuery(req).each(function(idx,e){
                    jQuery(targetElement).append("<option value='"+e[selinstance.field.code]+"'>"+e[selinstance.field.label]+"</option>");
                });
                jQuery(targetElement).val(currentCode);
            },
            error:function(e){
            }
        });
    }
    
    //得到联动菜单的最终选中值
    this.getValue=function(){
    	var v="";
    	jQuery(selinstance.selectors).each(function(idx,e){
    		if(jQuery(e).val()!=null && jQuery(e).val()!=""){
	    		v=jQuery(e).val();
    		}
    	});
    	return v;
    }
    
    //按顺利得到所有选中项的值
    this.getValues=function(){
    	var v=new Array();
    	jQuery(selinstance.selectors).each(function(idx,e){
    		if(jQuery(e).val()!=null && jQuery(e).val()!=""){
	    		v.push(jQuery(e).val());
    		}
    	});
    	return v;
    }
    
    //按顺序得到全部选中项的显示值
    this.getTexts=function(){
    	var v=new Array();
    	jQuery(selinstance.selectors).each(function(idx,e){
    		if(jQuery(e).val()!=null && jQuery(e).val()!=""){
	    		v.push(jQuery(e).find("option:selected").html());
    		}
    	});
    	return v;
    }
    
    //得到联动辅助菜单的选中值
    this.getAssistValue=function(){
    	if(assistSelectors.length>0){
    		return jQuery(assistSelectors[0]).val();
    	}
    }
    
    //TODO 未完成
    this.isLeaf=function(url,code, callback){
    	jQuery.ajax({
            url:selinstance.assistUrl+"?mainCode="+mainCode,
            type:"POST",
            cache:false,
            dataType:"json",
//            data:{"mainCode":mainCode},
            success:callback,
            error:function(e){
            }
        });
    }

};

hb.util.topBar.HoverList = function(){
	var liHover= $('#hb_bar_navls>li')||{};
	var viewLsStatus = false;
	//hb.util.msg.Error({m:"commonError"});
	//alert(a);
	
	liHover
	.mouseover(function(){
		if(!viewLsStatus){
			$(this).attr({'class':'ishover'})
			$(this).find('#hb_bar_nav_block').slideDown(300);
			var viewLsStatus=true;
		}
	})
	.mouseleave(function(){
		if(!viewLsStatus){
			$(this).attr({'class':''})
			$(this).find('#hb_bar_nav_block').slideUp(100);
			var viewLsStatus=false;
		}
	});
};

hb.util.topBar.AddBookmark=function(tit,url){
	
	if(window.sidebar){//IE
		window.sidebar.addPanel(tit,url,'')
	}
	else if(document.all){//FireFox
		window.external.AddFavorite(url,tit);
	}
	else if(window.opera && window.print){//opera
		return true
	}
	//else if(window.MessageEvent && !document.getBoxObjectFor){//chrome
		//var desktop = google.gears.factory.create("beta.desktop"); 
    	//var description = tit; 
    	//var name = url;   //name不支持中文 
    	//var icons = {"32x32": "images/32.gif"}; 
    	//desktop.createShortcut(name, "index.htm", icons, description);
    	 
	//}
	else{//默认
		alert("浏览器不支持快捷方式添加收藏夹！请按Ctrl+D手动添加！")
	}
}





/**
 * 系统消息提示工具
 * 示例：
 * 显示消息
 * hb.util.Message.show({
 * 		msg:"message text",
 * 		msgType:hb.util.Message.ERROR,
 * 		bar:[{text:hb.util.Message.BAR_CLOSE,handler:function(){
 * 			hb.util.Message.clear();
 * 		}}],
 * 		target:"#targetid",
 * 		autoClose:3000
 * });
 * 
 * 配置：
 * msg:要显示的消息，必填
 * msgType:显示消息的类型，有三种INFO,WARN,ERROR, error会显示成红色文字
 * bar:消息后面的工具按钮，默认有关闭按钮，设置成[]则无任何按钮
 * target:将显示到指定element
 * autoClose:自动关闭时间，不设置则不自动关闭，单位毫秒
 * 
 * 清除消息
 * hb.util.Message.clear(time);
 * time:不设置或设置成0则立即清除消息
 * 
 * */


hb.util.Message=new function(){
	this.BAR_CLOSE="关闭";
	this.BAR_RETRY="重试";
	this.BAR_UNDO="撤消";
	this.BAR_REFRESH="刷新";
	
	this.INFO="black";
	this.WARN="black";
	this.ERROR="red";
	
	var message=this;
	this.msg="";
	this.isCompleteClear=false;
	
	this.msgBody=null;
	
	this.show=function(cfg){
		cfg=cfg||{};
		var top=cfg.top||"0px";
		var left=cfg.left||"";
		var target=cfg.target||"body";
		
		var msg=cfg.msg||"";
		var msgType=cfg.msgType||message.INFO;
		
		var bar=cfg.bar||[{text:message.BAR_CLOSE,handler:function(){
			message.clear();
		}}];
		
		message.msg=msg;
		message.isCompleteClear=cfg.isCompleteClear||false;
		
		//自动关闭选项，默认0，不自动关闭
		var autoClose=cfg.autoClose||0;
		
		message.buildMsg(msg, top, left, target, msgType, bar);
		
		if(autoClose>0){
			message.clear(autoClose);
		}
	}
	
	this.buildMsg=function(msg, t, l, target, mt, bar){
		if(message.msgBody!=null){
			message.msgBody.remove();
			message.msgBody=null;
		}
		
		message.msgBody=jQuery("<div class='notice_box'></div>");
		message.msgBody.addClass("notice_box");
		
		if(l==""){
			l=(($(document).width()/2 )-msg.length*6)+'px';
		}
		
		message.msgBody.css({
			"margin-top":t,
			"margin-left":l,
			"color":mt,
			"font-size":"12px"
		});
		
		jQuery("<b>"+msg+"</b>").appendTo(message.msgBody);
		
		jQuery(bar).each(function(idx,obj){
			var b=message.buildBar(obj);
			if(b != null){
				b.appendTo(message.msgBody);
			}
		});

//		message.msgBody.appendTo(jQuery(target))
//		jQuery(target).append("<div style='clear:both;'></div>");
//		jQuery(target).append(message.msgBody);
		jQuery(target).prepend(message.msgBody);
	}
	
	//创建单个工具栏
	this.buildBar=function(cfg){
		cfg=cfg||{};
		var text=cfg.text||"";
		if(text==""){
			return null;
		}
		var handler=cfg.handler||function(){};
		
		var obj=jQuery("<a href='javascript:void(0);' >"+text+"</a> ");
		obj.css({
			"font-size":"12px",
			"font-weight":"bold",
			"margin-left":"10px",
			"cursor":"pointer",
			"color":"blue"
		});
		obj.click(handler);
		
		return obj;
	}
	
	//清除消息框,不带时间则立即清除,时间单位：毫秒
	this.clear=function(time){
		time=time||0;
		if(time>0){
			setTimeout(function(){
				if(message.msgBody!=null){
					message.msgBody.remove();
				}
			},time);
		}else{
			if(message.msgBody!=null){
				message.msgBody.remove();
			}
		}
	}
	
}

/**
 * 	var pop=new hb.util.PopupBox({
		height:"300px",
		width:"400px",
		top:"80px",
		url:"http://www.baidu.com"
	});
	pop.show();
 * */
hb.util.PopupBox=function(cfg){
	cfg=cfg||{};
	
	this.id=cfg.id||null;
	this.modal=cfg.modal;
	
	if(this.modal==null || typeof(this.modal)=="undefined"){
		this.modal=true;
	}
		
	this.closeAction=cfg.closeAction||"close";
	
	this.width = cfg.width ||"140px";
	this.height = cfg.height||"200px";
	this.top=cfg.top||"60px";
	
	this.url=cfg.url||null;
	this.html=cfg.html||null;
	
	this.bc=null;
	this.box=null;
	
	this.closeText=cfg.closeText||"";
	
	var popup=this;
	
	this.show=function(){
		
		if(popup.box!=null){
			popup.close();
			popup.box=null;
			popup.bc=null;
		}
		
		popup.buildBody();
		
		jQuery("body").append(popup.bc);
		jQuery("body").append(popup.box);
	}
	
	this.buildBody=function(){
		//build modal
		if(popup.modal){
			popup.bc=jQuery("<div></div>");
			popup.bc.addClass("popup_box_bc");
			popup.bc.css({height:$(document).height()+'px',width:$(document).width()+'px'})
		}
		
		//build box
		popup.box=jQuery("<div></div>");
		popup.box.addClass("popup_box");
		popup.box.css({
			"width":popup.width,
			"height":popup.height,
			"margin-top":popup.top
		});
		popup.box.css({
			left:(($(document).width()/2 )-(popup.box.width()/2))+'px'
		})
		
		//build close button
		var closebtn=jQuery("<div class='popup_close' href='#close'>"+popup.closeText+"</div>");
		closebtn.click(function(){
			popup.close();
		});
		closebtn.css({
//			left:(($(document).width()/2 )-(popup.box.width()/2))+'px',
//			left:(popup.box.width() - 50)+"px",
			width:popup.width,
			top:-25
		});
		
		popup.box.append(closebtn);
		
		if(popup.url!=null){
			popup.box.append("<iframe id='popupiframe' frameborder = 'no' scrolling = 'auto' style = 'width:100%;height:100%' src ='"+popup.url+"' />");  //
		}
		
		if(popup.html!=null){
			popup.box.append(popup.html);
		}
	}
	
	this.close=function(){
		if(popup.bc!=null){
			popup.remove(popup.bc);
		}
		if(popup.box!=null){
			popup.remove(popup.box);
		}
	}
	
	this.remove=function(obj){
		if(popup.closeAction=="hide"){
			obj.hide();
		}else{
			obj.remove();
		}
	}
	
	
}

hb.util.MiniLogin=new function(){
	
	this.loginUrl=hb.util.context.path.myesite+"/loginMini.htm";
	this.destUrl=hb.util.context.path.myesite+"/callback/login.htm";
	
	this.popup=null;
	
	var login=this;
	
	this.show=function(cfg){
		cfg=cfg||{};
		
		if(login.popup!=null){
			login.popup.close();
			login.popup=null;
		}
		
		var url=cfg.url||hb.util.context.path.myesite+"/loginMini.htm";
		var destUrl=cfg.destUrl||null;
		
		if(destUrl!=null){
			if(url.indexOf("?")>=0){
				url=url+"&destUrl="+destUrl;
			}else{
				url=url+"?destUrl="+destUrl;
			}
		}
		
		login.popup=new hb.util.PopupBox({
			id:"loginwin",
			height:"300px",
			width:"400px",
			top:"120px",
			modal:false,
			url:url
		});
		
		login.popup.show();
	}
	
	this.close=function(){
		login.popup.close();
	}
}

//session检测
//hb.util.gloabAjaxEvent=function(){
jQuery(document).ready(function(){
	jQuery(document).ajaxSend(function(e,XHR,options){
		hb.util.Message.show({
			msg:hb.util.context.msg.comm_loading,
			isCompleteClear:true,
			bar:[]
		});
		
	}).ajaxError(function(e,XHR,settings,thrownError){
		hb.util.Message.show({
			autoClose:10000,
			msg:XHR.status+":"+hb.util.context.msg.comm_server_error
		});
	}).ajaxComplete(function(e, XHR, options){
		var str=XHR.getAllResponseHeaders();
		if(str.indexOf("sessionstatus")>=0){
			//提示消息
			hb.util.Message.show({
				msg:hb.util.context.msg.comm_session_timeout,
				autoClose:3000
			});

			hb.util.commonCallback=function(success,data){
				hb.util.MiniLogin.close();
			}

			hb.util.MiniLogin.show({
				url:hb.util.MiniLogin.loginUrl,
				destUrl:hb.util.MiniLogin.destUrl
			});
			
		}else{
			if(XHR.status==200 && hb.util.Message.isCompleteClear){
				hb.util.Message.clear();
			}
		}
	});
});