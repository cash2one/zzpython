function ajaxInfo(){
	var forcompany_id = api.pageParam.forcompany_id;
	var company_id = UserInfo.memberID();
	api.showProgress({
		title : '加载中',
		modal : true
	});
	api.ajax({
		url : hosturl + 'msg/list.html?datatype=json&company_id='+UserInfo.memberID()+'&forcompany_id='+forcompany_id.toString()+'&appsystem='+api.systemType+"&t=" + (new Date()).getTime().toString()+"&page=" + currPage,
		method : 'get',
		timeout : 30,
		dataType : 'json',
		returnAll : false
	}, function(ret, err) {
		api.hideProgress();
		if(err){
			saveerrlog(err.body);
		}
		var pageHtml = "";
		$.each(ret, function(index, item) {
			if (item.company_id.toString()!=company_id.toString()){
				item['class']='aui-chat-receiver';
				item['classbg']='aui-chat-left-triangle';
				item['chatimg']='../../image/demo2.png';
			}else{
				item['class']='aui-chat-sender';
				item['classbg']='aui-chat-right-triangle';
				item['chatimg']='../../image/demo1.png';
				item['contact']='我'
			}
			var fcompanyid=item.company_id.toString();
			var getTpl = $api.html($api.byId("leavewords-list"));
			laytpl(getTpl).render(item, function(html) {
				pageHtml = html+pageHtml;
			});
		});
		//zzalert(JSON.stringify(ret.list))
		if (currPage == 1) {
			$(".chatlist").html(pageHtml);
			api.pageDown({
				'bottom':true        //是否滚动，为false时说明当前页面已经到达底部了
			});
		}else{
			$(".chatlist").prepend(pageHtml)
		}
		if (pageHtml != "") {
			currPage += 1;
		}else{
		}
		$(".aui-chat-receiver-cont").css({'background-color':'#ebebeb'})
		$(".aui-chat-receiver-avatar").css({'font-size':'12px','color':'#ccc','text-align':'center'});
		$(".aui-chat-left-triangle").css({'position':'absolute','top':'6px','border-color':'transparent #ebebeb transparent transparent'})
		api.refreshHeaderLoadDone();
		api.hideProgress();
		api.execScript({
			name : 'root',
			script : 'chatrefrush()'
		});
	});
	$("body").on("click",".aui-chat-receiver-avatar",function() {
		var company_id = $(this).find('img').attr("comid");
		if (!company_id){
			return;
		}
		var pageParam = {
            wintitle:"公司详情",
            type:"companyshop",
            showbottom : 1,
			forcompany_id : company_id,
            bounces:false
        };
        openWin("companyshop", "../company/shop.html", pageParam);
	})
}
