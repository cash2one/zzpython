$(".prolist").on("click",".selectpro", function() {
	var pdt_id=$(this).attr("id");
	var proname=$(this).attr("proname");
	api.execScript({
		name : "servicejingjia",
		frameName:"servicejingjia_",
		script : "selectproducts('"+pdt_id+"','"+escape(proname)+"')"
	});
	closeselect();
})