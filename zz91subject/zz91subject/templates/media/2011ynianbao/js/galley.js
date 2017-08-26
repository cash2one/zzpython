// JavaScript Document
   function prepareGallery()
    {
       if(!document.getElementsByTagName || !document.getElementById){return false;}
       if(!document.getElementById("imagegallery")){return false;}
       var gallery = document.getElementById("imagegallery");
       var links = gallery.getElementsByTagName("a");
       for(var i=0;i<links.length;i++){
        links[i].onclick = function(){
            return showPic(this);
           }
       }
    }
      function showPic(whichpic)
      {
        var source = whichpic.getAttribute("href");
        var place = document.getElementById("place");
            place.setAttribute("src",source);
     
      }

