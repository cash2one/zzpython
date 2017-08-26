$(".searchhistory").on("click",".searchname",function(){
	var keywords=$(this).text();
	opensearch(keywords,type);
})