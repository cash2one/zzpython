//����д��һ��������жϵĴ���
var UA = navigator.userAgent.toLowerCase();
var browerKernel = {
    isTrident : function(){
        if(/trident/i.test(UA)) return true;
        else return false;
    },
    isWebkit : function(){
        if(/webkit/i.test(UA)) return true;
        else return false;
    },
    isGecko : function(){
        if(/gecko/i.test(UA)) return true;
        else return false;
    },
    isPresto : function(){
        if(/presto/i.test(UA)) return true;
        else return false;
    },
    isIE : function(){
        if(/msie/i.test(UA) && !/opera/.test(UA)) return true;
        else return false;
    },
    isChrome : function(){
        if(/chrome/i.test(UA) && /webkit/i.test(UA) && /mozilla/i.test(UA)) return true;
        else return false;
    },
    isFireFox : function(){
        if(/firefox/i.test(UA)) return true;
        else return false;
    },
    isOpear : function(){
        if(/opera/i.test(UA)) return true;
        else return false;
    },
    isSafari : function(){
        if(/webkit/i.test(UA) &&!(/chrome/i.test(UA) && /webkit/i.test(UA) && /mozilla/i.test(UA))) return true;
        else return false;
    }
}

//���ض���
backTop = function (btnId){
    var btn=document.getElementById(btnId);
    if(browerKernel.isWebkit()){
        var d=document.body;
    }else{
        var d=document.documentElement;
    }
    window.onscroll=set;
    btn.onclick=function (){
        //��ʼ����ʾ
        btn.style.display="none";
        window.onscroll=null;
        this.timer=setInterval(function(){
            d.scrollTop-=Math.ceil(d.scrollTop*0.1);
            if(d.scrollTop==0) clearInterval(btn.timer,window.onscroll=set);
        },10);
        
        //����ƽ������
        var o = this;
        var ot = o.offsetTop;
        for(var t = 0; t < 20; t++){
            //���ó�ʱ
            setTimeout("scrollBy(0,-" + parseInt(ot / 20) + ")",t * 50 + 1);
        }
        return false;
    };
    function set(){
        //btn.style.display=d.scrollTop?"block":"none";
    }
};
//ִ�д���
backTop("top");

