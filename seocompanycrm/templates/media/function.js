function send1()
{
document.form.action="/assigntoseo/"
document.form.submit()
}
function send2()
{
document.form.action="/choicedelete/"
document.form.submit()
}
function send3()
{
document.form.action="/choicereduction/"
document.form.submit()
}
function send4()
{
document.form.action="/choicelostcomp/"
document.form.submit()
}
function send5()
{
document.form.action="/choicereductioncomp/"
document.form.submit()
}
function send6()
{
document.form.action="/assigntoseocomp/"
document.form.submit()
}
function send7()
{
document.form.action="/choicelost/"
document.form.submit()
}
function send8()
{
document.form.action="/choicereductionlost/"
document.form.submit()
}
function send9()
{
document.form.action="/assigntosales/"
document.form.submit()
}
function send10()
{
document.form.action="/addcompanyok/"
document.form.submit()
}

function changeSelect()
{
var select = document.getElementById("select").value;
document.getElementById('seo_id').value=select;
}


//选中全选按钮，下面的checkbox全部选中 
var selAll = document.getElementById("selAll"); 
function selectAll() 
{ 
  var obj = document.getElementsByName("checkAll"); 
  if(document.getElementById("selAll").checked == false) 
  { 
  for(var i=0; i<obj.length; i++) 
  { 
    obj[i].checked=false; 
  } 
  }else 
  { 
  for(var i=0; i<obj.length; i++) 
  {	  
    obj[i].checked=true; 
  }	
  } 
  
} 
//当选中所有的时候，全选按钮会勾上 
function setSelectAll() 
{ 
var obj=document.getElementsByName("checkAll"); 
var count = obj.length; 
var selectCount = 0; 

for(var i = 0; i < count; i++) 
{ 
if(obj[i].checked == true) 
{ 
selectCount++;	
} 
} 
if(count == selectCount) 
{	
document.all.selAll.checked = true; 
} 
else 
{ 
document.all.selAll.checked = false; 
} 
} 

//反选按钮 
function inverse() { 
var checkboxs=document.getElementsByName("checkAll"); 
for (var i=0;i<checkboxs.length;i++) { 
  var e=checkboxs[i]; 
  e.checked=!e.checked; 
  setSelectAll(); 
} 
} 