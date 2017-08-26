
$(function(){
	$(".nav_td").click(function(e){
		$(this).css("background", "#e6e6e6");
	});
});




$(function(){
	$('.i-txt').click(function(e){
		$('#reply_div_req').lightbox_me({
					overlaySpeed:0,
					lightboxSpeed:0,
            		centered: true, 
            		
        	});
		e.preventDefault();
	});
});


function dismiss(){
	$('#reply_div').trigger('close');
	$('#reply_div_').trigger('close');
	$('#reply_div_req').trigger('close');
	$('#reply_div_nick').trigger('close');
}


var selectRow=null;   
//单击时,改变样式;  
function onClickChangeStyle(obj){  
       //获取表格对象;  
       var tab = document.getElementById("tab1");  
         
         //获取当前行选择下标;  
         var currentRowIndex = obj.rowIndex;  
  
         //获取表格所有行数;  
       var tabtablRows = tab.rows.length;  
        
       //获取表格第一行,第一列的值;  
       //var firstCellValue = tab.rows[0].cells[0].innerHTML;  
         
       //获取表格的第一行，第一列的第一个元素的值;  
       //var firstChildValue = tab.rows[0].cells[0].firstChild.value;  
         
       //循环表格的所有行;并且选择的当前行，改变背景颜色；  
       for(var i = 1;i<tablRows;ii=i+1){  
           
       }      
}  
























