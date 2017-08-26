function selectOption(menuname, value) {
	var menu = document.getElementById(menuname);
	if(menu) {
		for(var i = 0; i <= menu.options.length; i++) {
			if(menu.options[i].value == value) {
				menu.options[i].selected = true;
				break;
			}
		}
	}
}

function selectOptionHy(menuname, value, hyID) {
	var menu = document.getElementById(menuname);
	var hyIDvalue = document.getElementById(hyID);
	if(menu && hyIDvalue) {
		for(var i = 0; i < menu.options.length; i++) {
			//alert(menu.options[i].text)
			if(menu.options[i].className != "" && hyIDvalue.value != "") {
				if(hyIDvalue.value != menu.options[i].className) {
					menu.options.remove(i);
					i = 0;
				}
			}
		}
	}
}

function getprovincevalue() {
	if(selectname1 != "") {
		change_sort1("" + selectname1 + "", "" + selectname2 + "", "" + selectname3 + "", Fstyle);
		selectOption("" + selectname1 + "", "" + Fvalue1 + "");
	}
	if(selectname2 != "") {
		change_sort2("" + selectname1 + "", "" + selectname2 + "", "" + selectname3 + "", "" + Fvalue1 + "", Fstyle);
		selectOption("" + selectname2 + "", "" + Fvalue2 + "");
	}
	if(selectname3 != "") {
		change_sort4("" + selectname1 + "", "" + selectname2 + "", "" + selectname3 + "", "" + Fvalue2 + "", Fstyle);
		selectOption("" + selectname3 + "", "" + Fvalue3 + "");
	}

}
//第二级菜单内容
function change_sort2(Fname, Fname1, Fname2, sindustry, Fstyle) {
	switch(sindustry) {
		case '10':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1001'>北京</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '13':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1301'>重庆</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '14':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1401'>保定</option>";
			temp += "<option value='1402'>沧州</option>";
			temp += "<option value='1403'>承德</option>";
			temp += "<option value='1404'>邯郸</option>";
			temp += "<option value='1405'>衡水</option>";
			temp += "<option value='1406'>廊坊</option>";
			temp += "<option value='1407'>秦皇岛</option>";
			temp += "<option value='1408'>石家庄</option>";
			temp += "<option value='1409'>唐山</option>";
			temp += "<option value='1410'>邢台</option>";
			temp += "<option value='1411'>张家口</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '16':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1601'>长治</option>";
			temp += "<option value='1602'>大同</option>";
			temp += "<option value='1603'>晋城</option>";
			temp += "<option value='1604'>晋中</option>";
			temp += "<option value='1605'>临汾</option>";
			temp += "<option value='1606'>吕梁</option>";
			temp += "<option value='1607'>朔州</option>";
			temp += "<option value='1608'>太原</option>";
			temp += "<option value='1609'>忻州</option>";
			temp += "<option value='1610'>阳泉</option>";
			temp += "<option value='1611'>运城</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '17':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1701'>阿拉善盟</option>";
			temp += "<option value='1702'>巴彦淖尔盟</option>";
			temp += "<option value='1703'>包头</option>";
			temp += "<option value='1704'>赤峰</option>";
			temp += "<option value='1705'>鄂尔多斯</option>";
			temp += "<option value='1706'>呼和浩特</option>";
			temp += "<option value='1707'>呼伦贝尔</option>";
			temp += "<option value='1708'>通辽</option>";
			temp += "<option value='1709'>乌海</option>";
			temp += "<option value='1710'>乌兰察布</option>";
			temp += "<option value='1711'>锡林郭勒盟</option>";
			temp += "<option value='1712'>兴安盟</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '18':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1801'>鞍山</option>";
			temp += "<option value='1802'>本溪</option>";
			temp += "<option value='1803'>朝阳</option>";
			temp += "<option value='1804'>大连</option>";
			temp += "<option value='1805'>沈阳</option>";
			temp += "<option value='1806'>丹东</option>";
			temp += "<option value='1807'>抚顺</option>";
			temp += "<option value='1808'>阜新</option>";
			temp += "<option value='1809'>葫芦岛</option>";
			temp += "<option value='1810'>锦州</option>";
			temp += "<option value='1811'>辽阳</option>";
			temp += "<option value='1812'>盘锦</option>";
			temp += "<option value='1813'>铁岭</option>";
			temp += "<option value='1814'>营口</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '19':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1901'>白城</option>";
			temp += "<option value='1902'>白山</option>";
			temp += "<option value='1903'>长春</option>";
			temp += "<option value='1904'>吉林</option>";
			temp += "<option value='1905'>辽源</option>";
			temp += "<option value='1906'>四平</option>";
			temp += "<option value='1907'>松原</option>";
			temp += "<option value='1908'>通化</option>";
			temp += "<option value='1909'>延边朝鲜族自治州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '20':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2001'>大庆</option>";
			temp += "<option value='2002'>大兴安岭</option>";
			temp += "<option value='2003'>哈尔滨</option>";
			temp += "<option value='2004'>鹤岗</option>";
			temp += "<option value='2005'>黑河</option>";
			temp += "<option value='2006'>鸡西</option>";
			temp += "<option value='2007'>佳木斯</option>";
			temp += "<option value='2008'>牡丹江</option>";
			temp += "<option value='2009'>七台河</option>";
			temp += "<option value='2010'>齐齐哈尔</option>";
			temp += "<option value='2011'>双鸭山</option>";
			temp += "<option value='2012'>绥化</option>";
			temp += "<option value='2013'>伊春</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '22':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2201'>安庆</option>";
			temp += "<option value='2202'>蚌埠</option>";
			temp += "<option value='2203'>巢湖</option>";
			temp += "<option value='2204'>池州</option>";
			temp += "<option value='2205'>滁州</option>";
			temp += "<option value='2206'>阜阳</option>";
			temp += "<option value='2207'>合肥</option>";
			temp += "<option value='2208'>淮北</option>";
			temp += "<option value='2209'>淮南</option>";
			temp += "<option value='2210'>黄山</option>";
			temp += "<option value='2211'>六安</option>";
			temp += "<option value='2212'>马鞍山</option>";
			temp += "<option value='2213'>宿州</option>";
			temp += "<option value='2214'>铜陵</option>";
			temp += "<option value='2215'>芜湖</option>";
			temp += "<option value='2216'>宣城</option>";
			temp += "<option value='2217'>亳州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '23':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2301'>福州</option>";
			temp += "<option value='2302'>龙岩</option>";
			temp += "<option value='2303'>南平</option>";
			temp += "<option value='2304'>宁德</option>";
			temp += "<option value='2305'>莆田</option>";
			temp += "<option value='2306'>泉州</option>";
			temp += "<option value='2307'>三明</option>";
			temp += "<option value='2308'>厦门</option>";
			temp += "<option value='2309'>漳州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '24':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2401'>白银</option>";
			temp += "<option value='2402'>定西</option>";
			temp += "<option value='2403'>甘南藏族自治州</option>";
			temp += "<option value='2404'>嘉峪关</option>";
			temp += "<option value='2405'>金昌</option>";
			temp += "<option value='2406'>酒泉</option>";
			temp += "<option value='2407'>兰州</option>";
			temp += "<option value='2408'>临夏回族自治州</option>";
			temp += "<option value='2409'>陇南</option>";
			temp += "<option value='2410'>平凉</option>";
			temp += "<option value='2411'>庆阳</option>";
			temp += "<option value='2412'>天水</option>";
			temp += "<option value='2413'>武威</option>";
			temp += "<option value='2414'>张掖</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '25':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2501'>阿克苏</option>";
			temp += "<option value='2502'>阿拉尔</option>";
			temp += "<option value='2503'>巴音郭楞蒙古自治州</option>";
			temp += "<option value='2504'>博尔塔拉蒙古自治州</option>";
			temp += "<option value='2505'>昌吉回族自治州</option>";
			temp += "<option value='2506'>哈密</option>";
			temp += "<option value='2507'>和田</option>";
			temp += "<option value='2508'>喀什</option>";
			temp += "<option value='2509'>克拉玛依</option>";
			temp += "<option value='2510'>克孜勒苏柯尔克孜自治州</option>";
			temp += "<option value='2511'>石河子</option>";
			temp += "<option value='2512'>图木舒克</option>";
			temp += "<option value='2513'>吐鲁番</option>";
			temp += "<option value='2514'>乌鲁木齐</option>";
			temp += "<option value='2515'>五家渠</option>";
			temp += "<option value='2516'>伊犁哈萨克自治州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '26':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2601'>抚州</option>";
			temp += "<option value='2602'>赣州</option>";
			temp += "<option value='2603'>吉安</option>";
			temp += "<option value='2604'>景德镇</option>";
			temp += "<option value='2605'>九江</option>";
			temp += "<option value='2606'>南昌</option>";
			temp += "<option value='2607'>萍乡</option>";
			temp += "<option value='2608'>上饶</option>";
			temp += "<option value='2609'>新余</option>";
			temp += "<option value='2610'>宜春</option>";
			temp += "<option value='2611'>鹰潭</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '28':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2801'>安阳</option>";
			temp += "<option value='2802'>鹤壁</option>";
			temp += "<option value='2803'>济源</option>";
			temp += "<option value='2804'>焦作</option>";
			temp += "<option value='2805'>开封</option>";
			temp += "<option value='2806'>洛阳</option>";
			temp += "<option value='2807'>南阳</option>";
			temp += "<option value='2808'>平顶山</option>";
			temp += "<option value='2809'>三门峡</option>";
			temp += "<option value='2810'>商丘</option>";
			temp += "<option value='2811'>新乡</option>";
			temp += "<option value='2812'>信阳</option>";
			temp += "<option value='2813'>许昌</option>";
			temp += "<option value='2814'>郑州</option>";
			temp += "<option value='2815'>周口</option>";
			temp += "<option value='2816'>驻马店</option>";
			temp += "<option value='2817'>漯河</option>";
			temp += "<option value='2818'>濮阳</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '29':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2901'>鄂州</option>";
			temp += "<option value='2902'>恩施土家族苗族自治州</option>";
			temp += "<option value='2903'>黄冈</option>";
			temp += "<option value='2904'>黄石</option>";
			temp += "<option value='2905'>荆门</option>";
			temp += "<option value='2906'>荆州</option>";
			temp += "<option value='2907'>潜江</option>";
			temp += "<option value='2908'>神农架林区</option>";
			temp += "<option value='2909'>十堰</option>";
			temp += "<option value='2910'>随州</option>";
			temp += "<option value='2911'>天门</option>";
			temp += "<option value='2912'>武汉</option>";
			temp += "<option value='2913'>仙桃</option>";
			temp += "<option value='2914'>咸宁</option>";
			temp += "<option value='2915'>襄樊</option>";
			temp += "<option value='2916'>孝感</option>";
			temp += "<option value='2917'>宜昌</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '30':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3001'>常德</option>";
			temp += "<option value='3002'>长沙</option>";
			temp += "<option value='3003'>郴州</option>";
			temp += "<option value='3004'>衡阳</option>";
			temp += "<option value='3005'>怀化</option>";
			temp += "<option value='3006'>娄底</option>";
			temp += "<option value='3007'>邵阳</option>";
			temp += "<option value='3008'>湘潭</option>";
			temp += "<option value='3009'>湘西土家族苗族自治州</option>";
			temp += "<option value='3010'>益阳</option>";
			temp += "<option value='3011'>永州</option>";
			temp += "<option value='3012'>岳阳</option>";
			temp += "<option value='3013'>张家界</option>";
			temp += "<option value='3014'>株洲</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '32':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3201'>百色</option>";
			temp += "<option value='3202'>北海</option>";
			temp += "<option value='3203'>崇左</option>";
			temp += "<option value='3204'>防城港</option>";
			temp += "<option value='3205'>桂林</option>";
			temp += "<option value='3206'>贵港</option>";
			temp += "<option value='3207'>河池</option>";
			temp += "<option value='3208'>贺州</option>";
			temp += "<option value='3209'>来宾</option>";
			temp += "<option value='3210'>柳州</option>";
			temp += "<option value='3211'>南宁</option>";
			temp += "<option value='3212'>钦州</option>";
			temp += "<option value='3213'>梧州</option>";
			temp += "<option value='3214'>玉林</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '33':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3301'>白沙黎族自治县</option>";
			temp += "<option value='3302'>保亭黎族苗族自治县</option>";
			temp += "<option value='3303'>昌江黎族自治县</option>";
			temp += "<option value='3304'>澄迈县</option>";
			temp += "<option value='3305'>定安县</option>";
			temp += "<option value='3306'>东方</option>";
			temp += "<option value='3307'>海口</option>";
			temp += "<option value='3308'>乐东黎族自治县</option>";
			temp += "<option value='3309'>临高县</option>";
			temp += "<option value='3310'>陵水黎族自治县</option>";
			temp += "<option value='3311'>琼海</option>";
			temp += "<option value='3312'>琼中黎族苗族自治县</option>";
			temp += "<option value='3313'>三亚</option>";
			temp += "<option value='3314'>屯昌县</option>";
			temp += "<option value='3315'>万宁</option>";
			temp += "<option value='3316'>文昌</option>";
			temp += "<option value='3317'>五指山</option>";
			temp += "<option value='3318'>儋州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '34':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3401'>阿坝藏族羌族自治州</option>";
			temp += "<option value='3402'>巴中</option>";
			temp += "<option value='3403'>成都</option>";
			temp += "<option value='3404'>达州</option>";
			temp += "<option value='3405'>德阳</option>";
			temp += "<option value='3406'>甘孜藏族自治州</option>";
			temp += "<option value='3407'>广安</option>";
			temp += "<option value='3408'>广元</option>";
			temp += "<option value='3409'>乐山</option>";
			temp += "<option value='3410'>凉山彝族自治州</option>";
			temp += "<option value='3411'>眉山</option>";
			temp += "<option value='3412'>绵阳</option>";
			temp += "<option value='3413'>南充</option>";
			temp += "<option value='3414'>内江</option>";
			temp += "<option value='3415'>攀枝花</option>";
			temp += "<option value='3416'>遂宁</option>";
			temp += "<option value='3417'>雅安</option>";
			temp += "<option value='3418'>宜宾</option>";
			temp += "<option value='3419'>资阳</option>";
			temp += "<option value='3420'>自贡</option>";
			temp += "<option value='3421'>泸州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '35':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3501'>安顺</option>";
			temp += "<option value='3502'>毕节</option>";
			temp += "<option value='3503'>贵阳</option>";
			temp += "<option value='3504'>六盘水</option>";
			temp += "<option value='3505'>黔东南苗族侗族自治州</option>";
			temp += "<option value='3506'>黔南布依族苗族自治州</option>";
			temp += "<option value='3507'>黔西南布依族苗族自治州</option>";
			temp += "<option value='3508'>铜仁</option>";
			temp += "<option value='3509'>遵义</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '36':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3601'>保山</option>";
			temp += "<option value='3602'>楚雄彝族自治州</option>";
			temp += "<option value='3603'>大理白族自治州</option>";
			temp += "<option value='3604'>德宏傣族景颇族自治州</option>";
			temp += "<option value='3605'>迪庆藏族自治州</option>";
			temp += "<option value='3606'>红河哈尼族彝族自治州</option>";
			temp += "<option value='3607'>昆明</option>";
			temp += "<option value='3608'>丽江</option>";
			temp += "<option value='3609'>临沧</option>";
			temp += "<option value='3610'>怒江傈傈族自治州</option>";
			temp += "<option value='3611'>曲靖</option>";
			temp += "<option value='3612'>思茅</option>";
			temp += "<option value='3613'>文山壮族苗族自治州</option>";
			temp += "<option value='3614'>西双版纳傣族自治州</option>";
			temp += "<option value='3615'>玉溪</option>";
			temp += "<option value='3616'>昭通</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '37':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3701'>安康</option>";
			temp += "<option value='3702'>宝鸡</option>";
			temp += "<option value='3703'>汉中</option>";
			temp += "<option value='3704'>商洛</option>";
			temp += "<option value='3705'>铜川</option>";
			temp += "<option value='3706'>渭南</option>";
			temp += "<option value='3707'>西安</option>";
			temp += "<option value='3708'>咸阳</option>";
			temp += "<option value='3709'>延安</option>";
			temp += "<option value='3710'>榆林</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '38':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3801'>阿里</option>";
			temp += "<option value='3802'>昌都</option>";
			temp += "<option value='3803'>拉萨</option>";
			temp += "<option value='3804'>林芝</option>";
			temp += "<option value='3805'>那曲</option>";
			temp += "<option value='3806'>日喀则</option>";
			temp += "<option value='3807'>山南</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '39':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3901'>果洛藏族自治州</option>";
			temp += "<option value='3902'>海北藏族自治州</option>";
			temp += "<option value='3903'>海东</option>";
			temp += "<option value='3904'>海南藏族自治州</option>";
			temp += "<option value='3905'>海西蒙古族藏族自治州</option>";
			temp += "<option value='3906'>黄南藏族自治州</option>";
			temp += "<option value='3907'>西宁</option>";
			temp += "<option value='3908'>玉树藏族自治州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '40':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='4001'>固原</option>";
			temp += "<option value='4002'>石嘴山</option>";
			temp += "<option value='4003'>吴忠</option>";
			temp += "<option value='4004'>中卫</option>";
			temp += "<option value='4005'>银川</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '45':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='4501'>澳门</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '11':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1101'>上海</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '12':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1201'>天津</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '27':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2701'>滨州</option>";
			temp += "<option value='2702'>德州</option>";
			temp += "<option value='2703'>东营</option>";
			temp += "<option value='2704'>菏泽</option>";
			temp += "<option value='2705'>济南</option>";
			temp += "<option value='2706'>济宁</option>";
			temp += "<option value='2707'>莱芜</option>";
			temp += "<option value='2708'>聊城</option>";
			temp += "<option value='2709'>临沂</option>";
			temp += "<option value='2710'>青岛</option>";
			temp += "<option value='2711'>日照</option>";
			temp += "<option value='2712'>泰安</option>";
			temp += "<option value='2713'>威海</option>";
			temp += "<option value='2714'>潍坊</option>";
			temp += "<option value='2715'>烟台</option>";
			temp += "<option value='2716'>枣庄</option>";
			temp += "<option value='2717'>淄博</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '31':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='3101'>潮州</option>";
			temp += "<option value='3102'>东莞</option>";
			temp += "<option value='3103'>佛山</option>";
			temp += "<option value='3104'>广州</option>";
			temp += "<option value='3105'>河源</option>";
			temp += "<option value='3106'>惠州</option>";
			temp += "<option value='3107'>江门</option>";
			temp += "<option value='3108'>揭阳</option>";
			temp += "<option value='3109'>茂名</option>";
			temp += "<option value='3110'>梅州</option>";
			temp += "<option value='3111'>清远</option>";
			temp += "<option value='3112'>汕头</option>";
			temp += "<option value='3113'>汕尾</option>";
			temp += "<option value='3114'>韶关</option>";
			temp += "<option value='3115'>深圳</option>";
			temp += "<option value='3116'>阳江</option>";
			temp += "<option value='3117'>云浮</option>";
			temp += "<option value='3118'>湛江</option>";
			temp += "<option value='3119'>肇庆</option>";
			temp += "<option value='3120'>中山</option>";
			temp += "<option value='3121'>珠海</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '15':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='1501'>杭州</option>";
			temp += "<option value='1502'>湖州</option>";
			temp += "<option value='1503'>嘉兴</option>";
			temp += "<option value='1504'>金华</option>";
			temp += "<option value='1505'>丽水</option>";
			temp += "<option value='1506'>宁波</option>";
			temp += "<option value='1507'>绍兴</option>";
			temp += "<option value='1508'>台州</option>";
			temp += "<option value='1509'>温州</option>";
			temp += "<option value='1510'>舟山</option>";
			temp += "<option value='1511'>衢州</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '21':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='2101'>常州</option>";
			temp += "<option value='2102'>淮安</option>";
			temp += "<option value='2103'>连云港</option>";
			temp += "<option value='2104'>南京</option>";
			temp += "<option value='2105'>南通</option>";
			temp += "<option value='2106'>苏州</option>";
			temp += "<option value='2107'>宿迁</option>";
			temp += "<option value='2108'>泰州</option>";
			temp += "<option value='2109'>无锡</option>";
			temp += "<option value='2110'>徐州</option>";
			temp += "<option value='2111'>盐城</option>";
			temp += "<option value='2112'>扬州</option>";
			temp += "<option value='2113'>镇江</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '44':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '43':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='4301'>台北</option>";
			temp += "<option value='4302'>高雄</option>";
			temp += "<option value='4303'>台中</option>";
			temp += "<option value='4304'>台南</option>";
			temp += "<option value='4305'>基隆</option>";
			temp += "<option value='4306'>新竹</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		case '41':
			var temp;
			temp = "<select name='" + Fname1 + "' id='" + Fname1 + "' style='" + Fstyle + "' onChange=change_sort4('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='4101'>香港</option>";
			temp += "<option value='4102'>九龙</option>";
			temp += "<option value='4103'>新界</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
		default:
			var temp;
			temp = "<select style=" + Fstyle + " name='" + Fname1 + "' id='" + Fname1 + "'>";
			temp += "<option value=''>请选择...</option>";
			temp += "</select>";
			if(Fname1 != '') {
				document.getElementById("main" + Fname1 + "").innerHTML = "" + temp + "";
				change_sort3(Fname1, Fname2, sindustry, Fstyle);
			}
			break;
	}
	if(Fname2 != '') {
		change_sort3(Fname1, Fname2, sindustry, Fstyle);
	}
}
//第三级菜单内容
function change_sort3(Fname1, Fname2, sindustry, Fstyle) {
	switch(sindustry) {
		case '14':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='11' title=1406 class=2>文安尹村市场</option>";
			temp += "<option value='18' title=1406 class=2>霸州废塑料集散地</option>";
			temp += "<option value='17' title=1406 class=2>文安废塑料集散地</option>";
			temp += "<option value='12' title=1401 class=2>定州大吴村市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '18':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='35' title=1814 class=1>大石桥废金属集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '22':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='31' title=2202 class=2>五河废塑料集散地</option>";
			temp += "<option value='54' title=2206 class=1>界首田营金属园区</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '23':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='50' title=2309 class=1>全通金属园区</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '28':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='28' title=2801 class=2>安阳废塑料集散地</option>";
			temp += "<option value='29' title=2813 class=2>长葛废塑料集散地</option>";
			temp += "<option value='39' title=2813 class=1>长葛废金属集散地</option>";
			temp += "<option value='52' title=2813 class=1>长葛废旧金属回收市场</option>";
			temp += "<option value='30' title=2817 class=2>漯河废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '30':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='43' title=3012 class=1>汨罗废金属集散地</option>";
			temp += "<option value='51' title=3003 class=1>郴州产业园(废金属)</option>";
			temp += "<option value='55' title=3012 class=1>汨罗工业园(废金属)</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '34':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='58' title=3403 class=1>再生资源市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '11':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='37' title=1101 class=1>上海废金属集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '12':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='36' title=1201 class=1>静海废金属集散地</option>";
			temp += "<option value='53' title=1201 class=1>子牙产业园(废金属)</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '27':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='44' title=2709 class=1>临沂废金属集散地</option>";
			temp += "<option value='48' title=2708 class=1>聊城有色金属城</option>";
			temp += "<option value='49' title=2709 class=1>华东交易城</option>";
			temp += "<option value='57' title=2709 class=2>临沂再生塑料园区</option>";
			temp += "<option value='10' title=2702 class=2>莱州路旺塑料市场</option>";
			temp += "<option value='27' title=2715 class=2>莱州废塑料集散地</option>";
			temp += "<option value='26' title=2709 class=2>临沂废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '31':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='32' title=3103 class=2>顺德废塑料集散地</option>";
			temp += "<option value='33' title=3112 class=2>汕头废塑料集散地</option>";
			temp += "<option value='34' title=3103 class=2>南海废塑料集散地</option>";
			temp += "<option value='45' title=3103 class=1>南海废金属集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '15':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='40' title=1504 class=1>永康废金属集散地</option>";
			temp += "<option value='41' title=1508 class=1>台州废金属集散地</option>";
			temp += "<option value='42' title=1506 class=1>宁波废金属集散地</option>";
			temp += "<option value='46' title=1506 class=1>镇海金属园区</option>";
			temp += "<option value='47' title=1508 class=1>峰江金属园区</option>";
			temp += "<option value='19' title=1508 class=2>台州废塑料集散地</option>";
			temp += "<option value='20' title=1504 class=2>东阳废塑料集散地</option>";
			temp += "<option value='13' title=1506 class=2>桥头废塑料市场</option>";
			temp += "<option value='21' title=1506 class=2>慈溪废塑料集散地</option>";
			temp += "<option value='59' title=1506 class=2>余姚塑料城</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '21':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "'  onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='38' title=2106 class=1>太仓废金属集散地</option>";
			temp += "<option value='56' title=2108 class=2>兴化资源再生园</option>";
			temp += "<option value='14' title=2112 class=1>扬州物资市场</option>";
			temp += "<option value='15' title=2108 class=1>戴南不锈钢市场</option>";
			temp += "<option value='22' title=2110 class=2>徐州废塑料集散地</option>";
			temp += "<option value='23' title=2108 class=2>兴化废塑料集散地</option>";
			temp += "<option value='24' title=2106 class=2>太仓废塑料集散地</option>";
			temp += "<option value='25' title=2107 class=2>宿迁废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		default:
			document.getElementById("main" + Fname2 + "").innerHTML = "无";
			break;
	}
	selectOptionHy(Fname2, '', hyID);
}
//第四级菜单内容
function change_sort4(Fname, Fname1, Fname2, sindustry, Fstyle) {
	switch(sindustry) {
		case '3103':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='32' title=3103 class=2>顺德废塑料集散地</option>";
			temp += "<option value='34' title=3103 class=2>南海废塑料集散地</option>";
			temp += "<option value='45' title=3103 class=1>南海废金属集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '3112':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='33' title=3112 class=2>汕头废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2309':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='50' title=2309 class=1>全通金属园区</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '3003':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='51' title=3003 class=1>郴州产业园(废金属)</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '3012':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='43' title=3012 class=1>汨罗废金属集散地</option>";
			temp += "<option value='55' title=3012 class=1>汨罗工业园(废金属)</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1201':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='36' title=1201 class=1>静海废金属集散地</option>";
			temp += "<option value='53' title=1201 class=1>子牙产业园(废金属)</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2801':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='28' title=2801 class=2>安阳废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2813':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='29' title=2813 class=2>长葛废塑料集散地</option>";
			temp += "<option value='39' title=2813 class=1>长葛废金属集散地</option>";
			temp += "<option value='52' title=2813 class=1>长葛废旧金属回收市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2817':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='30' title=2817 class=2>漯河废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1401':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='12' title=1401 class=2>定州大吴村市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1406':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='11' title=1406 class=2>文安尹村市场</option>";
			temp += "<option value='18' title=1406 class=2>霸州废塑料集散地</option>";
			temp += "<option value='17' title=1406 class=2>文安废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2702':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='10' title=2702 class=2>莱州路旺塑料市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2708':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='48' title=2708 class=1>聊城有色金属城</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2709':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='44' title=2709 class=1>临沂废金属集散地</option>";
			temp += "<option value='49' title=2709 class=1>华东交易城</option>";
			temp += "<option value='57' title=2709 class=2>临沂再生塑料园区</option>";
			temp += "<option value='26' title=2709 class=2>临沂废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2715':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='27' title=2715 class=2>莱州废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1814':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='35' title=1814 class=1>大石桥废金属集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1101':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='37' title=1101 class=1>上海废金属集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '3403':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='58' title=3403 class=1>再生资源市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2202':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='31' title=2202 class=2>五河废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2206':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='54' title=2206 class=1>界首田营金属园区</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2106':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='38' title=2106 class=1>太仓废金属集散地</option>";
			temp += "<option value='24' title=2106 class=2>太仓废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2107':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='25' title=2107 class=2>宿迁废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2108':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='56' title=2108 class=2>兴化资源再生园</option>";
			temp += "<option value='15' title=2108 class=1>戴南不锈钢市场</option>";
			temp += "<option value='23' title=2108 class=2>兴化废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2110':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='22' title=2110 class=2>徐州废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '2112':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='14' title=2112 class=1>扬州物资市场</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1504':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='40' title=1504 class=1>永康废金属集散地</option>";
			temp += "<option value='20' title=1504 class=2>东阳废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1506':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='42' title=1506 class=1>宁波废金属集散地</option>";
			temp += "<option value='46' title=1506 class=1>镇海金属园区</option>";
			temp += "<option value='13' title=1506 class=2>桥头废塑料市场</option>";
			temp += "<option value='21' title=1506 class=2>慈溪废塑料集散地</option>";
			temp += "<option value='59' title=1506 class=2>余姚塑料城</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '1508':
			var temp;
			temp = "<select name='" + Fname2 + "' id='" + Fname2 + "' style='" + Fstyle + "' onChange=selectOption('" + Fname1 + "',this.options[this.selectedIndex].title)>";
			temp += "<option value=''>请选择...</option>";
			temp += "<option value='41' title=1508 class=1>台州废金属集散地</option>";
			temp += "<option value='47' title=1508 class=1>峰江金属园区</option>";
			temp += "<option value='19' title=1508 class=2>台州废塑料集散地</option>";
			temp += "</select>";
			document.getElementById("main" + Fname2 + "").innerHTML = "" + temp + "";
			break;
		case '':
			change_sort3(Fname1, Fname2, document.getElementById(Fname).value, Fstyle);
			break;
		default:
			document.getElementById("main" + Fname2 + "").innerHTML = "无";
			break;
	}
	selectOptionHy(Fname2, '', hyID);
}
//第一级菜单内容
function change_sort1(Fname, Fname1, Fname2, Fstyle) {
	var temp;
	temp = "<select style='" + Fstyle + "' name='" + Fname + "' id='" + Fname + "' onChange=javascript:change_sort2('" + Fname + "','" + Fname1 + "','" + Fname2 + "',this.options[this.selectedIndex].value,'" + Fstyle + "')>";
	temp += "<option value=''>请选择...</option>";
	temp += "<option value='10'>北京</option>";
	temp += "<option value='11'>上海</option>";
	temp += "<option value='12'>天津</option>";
	temp += "<option value='13'>重庆</option>";
	temp += "<option value='14'>河北</option>";
	temp += "<option value='15'>浙江</option>";
	temp += "<option value='16'>山西</option>";
	temp += "<option value='17'>内蒙古</option>";
	temp += "<option value='18'>辽宁</option>";
	temp += "<option value='19'>吉林</option>";
	temp += "<option value='20'>黑龙江</option>";
	temp += "<option value='21'>江苏</option>";
	temp += "<option value='22'>安徽</option>";
	temp += "<option value='23'>福建</option>";
	temp += "<option value='24'>甘肃</option>";
	temp += "<option value='25'>新疆</option>";
	temp += "<option value='26'>江西</option>";
	temp += "<option value='27'>山东</option>";
	temp += "<option value='28'>河南</option>";
	temp += "<option value='29'>湖北</option>";
	temp += "<option value='30'>湖南</option>";
	temp += "<option value='31'>广东</option>";
	temp += "<option value='32'>广西</option>";
	temp += "<option value='33'>海南</option>";
	temp += "<option value='34'>四川</option>";
	temp += "<option value='35'>贵州</option>";
	temp += "<option value='36'>云南</option>";
	temp += "<option value='37'>陕西</option>";
	temp += "<option value='38'>西藏</option>";
	temp += "<option value='39'>青海</option>";
	temp += "<option value='40'>宁夏</option>";
	temp += "<option value='41'>香港</option>";
	temp += "<option value='43'>台湾</option>";
	temp += "<option value='44'>国外</option>";
	temp += "<option value='45'>澳门</option>";
	temp += "</select>";
	document.getElementById("main" + Fname + "").innerHTML = "" + temp + "";
}