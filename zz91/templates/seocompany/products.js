﻿document.write("<ul>{%for list in productslist.list%}<li><span class='img'><a href='http://{{pingyin}}.zz91.com/products{{list.pdt_id}}.htm' target=_blank><img src='{{list.pdt_images}}'></a></span><span><a href='http://{{pingyin}}.zz91.com/products{{list.pdt_id}}.htm' target=_blank>{{list.pdt_name|safe}}</a></span></li>{%endfor%}</ul>")