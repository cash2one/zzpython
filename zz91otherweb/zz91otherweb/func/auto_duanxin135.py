#-*- coding:utf-8 -*-

def getgedihq(name,type):
    re_alist='¥.*?</span>'
    urlone='http://jiage.1688.com/price/new_list.html?cname='+name+'&fname_2109='+type
    html_area=get_url_content(urlone)
#    print html_area
    html_alist=re.findall('<span class="price">.*?</span>',html_area)
    html_alist2=re.findall('<td class="td5">.*?</td>',html_area)
#    html_alist=get_content(re_alist,html_area)
    if html_alist:
        numb=''
        if '全国' in html_alist2[1]:
            numb=0
        elif '全国' in html_alist2[2]:
            numb=1
        
        price=html_alist[numb].replace(' ','')[-12:-7]
        duanxin_price='品名'+name + ' 牌号' +type + ' 价格 ' +price
        return duanxin_price
    else:
        duanxin_price='品名'+name + ' 牌号' +type+ ' 价格: 无'
        return duanxin_price

def getduanxin135():
    listall=[]
    data1=getgedihq('ABS','PA-707K')
    data2=getgedihq('GPPS','123p')
    data3=getgedihq('GPPS','PG-33')
    data4=getgedihq('PP','FC801M')
    data5=getgedihq('PP','EPS30RA')
    data6=getgedihq('HIPS','514P')
    data7=getgedihq('HIPS','622')
    listall.append(data1)
    listall.append(data2)
    listall.append(data3)
    listall.append(data4)
    listall.append(data5)
    listall.append(data6)
    listall.append(data7)
    return listall


def gettablelist1(content):
    content=content.lower()
    content=content.replace("<th","<td")
    content=content.replace("</th>","</td>")
    content=content.replace("TR","tr")
    content=content.replace("TD","td")
    content=content.replace("TABLE","table")
    arrtable=content.split("<table")
    listall=[]
    tablestr=""
    for table in arrtable:
        tablestr+="<table border=1>"
        arrtr=table.split("<tr")
        i=1
        trow=[]
        for row in arrtr[1:]:
            tablestr+="<tr>"
            arrtd=row.split("<td")
            j=1
            for tr in arrtd[1:]:
                tr="<td "+tr
                trsss=tr.split("</td>")
                tr=trsss[0]+"</td>"
                trs=tr
                tr = BeautifulSoup(tr)
                textname=tr.text.encode("utf-8")
                textname=filter_tags(textname.replace(" ","")).strip('\n')

                
                if ("rowspan" in trs):
                    aatr=trs.split("rowspan")
                    rowspan=aatr[1][1:2]
                    #rowspan=tr.td['rowspan']
                    #trow.append([i,j])
                    for a in range(i+1,int(rowspan)+i):
                        trow.append([a,j,textname])
                else:
                    rowspan=1
                #print rowspan
                
                if ("colspan" in trs):
                    colspan=tr.td['colspan']
                else:
                    colspan=1
                        
                tablestr+="<td >"
                tablestr+=textname
                tablestr+="</td>"
                if int(colspan)>1:
                    for r in range(1,int(colspan)):
                        tablestr+="<td>"
                        tablestr+=textname
                        tablestr+="</td>"
                j+=1
            tablestr+="</tr>"
            i+=1
        tablestr+="</table>"

    return {'content':tablestr,'trow':trow}
def getpricetable2(content,trow):
    soup = BeautifulSoup(content)
    tablestr=""
    for table in soup.findAll('table'):
        tablestr+="<table border=1>"
        i=1
        for row in table.findAll('tr'):
            tablestr+="<tr>"
            j=1
            for tr in row.findAll('td'):
                textname=tr.text.encode("utf-8")
                for l in trow:
                    if l[0]==i and l[1]==j:
                        tablestr+="<td >"
                        tablestr+=l[2]
                        tablestr+="</td>"
                tablestr+="<td >"
                tablestr+=textname
                tablestr+="</td>"
                j+=1
            i+=1
    return tablestr
def getpricetable3(content,type):
    soup = BeautifulSoup(content)
    tablestr=""
    for table in soup.findAll('table'):
        tablestr+="<table border=1>"
        i=1
        for row in table.findAll('tr'):
            tablestr+="<tr>"
            j=1
            for tr in row.findAll('td'):
                textname=tr.text.encode("utf-8")
                if type in ['PC','PA']:
                    if j>3 and j<6:
                        tablestr+="<td >"
                        tablestr+=textname
                        tablestr+="</td>"
                else: 
                    if j>3 and j<8:
                        tablestr+="<td >"
                        tablestr+=textname
                        tablestr+="</td>"
                j+=1
            i+=1
    return tablestr

def gettpye(title):
    typelist=[
              'PMMA',
              'PET',
              'LDPE',
              'HDPE',
              'PP',
              'PVC',
              'PS',
              'ABS',
              'PA',
              'PC',
              ]
    for type in typelist:
        if type in title:
            return type
    
def getduanxin430(type):
    re_alist='<div class="l_newsmaindetails">(.*?)<div>'
    re_list=r'<li>(.*?)</li>'
    urlone='http://baojia.feijiu.net/price-p-cid-bjcid2.29-dqid-.html'
    html_area=get_url_content(urlone)
#    print html_alist
    html_alist=get_content(re_alist,html_area)
#    print html_alist
    urls_pat=re.compile(re_list,re.DOTALL)
    alist=re.findall(urls_pat,html_alist)
    newtime=''
    for als in alist:
        newtimes=''
        newtime=als.replace(' ','')
        if 'feijiu.net' in urlone:
            newtimes=newtime[11:16]
        savetime=time.strftime('%m-%d',time.localtime(time.time()))
#        savetime='06-13'
        if newtimes==savetime:
            title=get_inner_a(als)
            a_url=get_a_url(als)
            if 'feijiu.net' in urlone:
                a_url=re.findall('.*?\.html',a_url)[0]
#            type=gettpye(title)

#            print type
#            print title
#            print a_url
#            return title
            if u'国内'+type in title.decode('utf-8'):
                if 'HDPE' in title:
                    htmls=get_url_content(a_url)
                    baojialist=re.findall('[\d]+',htmls)
                    listall=[]
                    continue_list=[]
                    passa=0
                    if 'HDPE' in title:
                        continue_list=[59,60,69,70,79,80,89,90,99,100,109,110,119,120,129,130,139,140,149,150,159,160,169,170,179,180,189,190,199,200,209,210,219,220,229,230,239,240,249,250,259,260,269,270,279,280,289,290]
                    if 'PMMA' in title:
                        continue_list=[52,53,62,63,72,73,82,83,92,93,102,103,112,113,122,123,132,133,142,143,152,153,162,163,173]
                    if 'PET' in title:
                        continue_list=[49,50,59,60,69,70,79,80,89,90,99,100,109,110,119,120,129,130,139,140,149,150,159,160,169,170,179,180,189,190,199,200,209,210,219,220,229,230,239,240,249,250,259,260,269,270]
                    if 'LDPE' in title:
                        continue_list=[52,53,62,63,72,73,82,83,92,93,102,103,112,113,122,123,132,133,142,143,152,153,162,163,173]
                    if baojialist:
                        for baojia in baojialist:
                            if len(baojia)>3:
                                if baojia=='000000':
                                    continue
                                if len(baojia)==8:
                                    listall.append(baojia[:4])
                                    listall.append(baojia[4:])
                                elif len(baojia)==10:
                                    listall.append(baojia[:5])
                                    listall.append(baojia[5:])
                                else:
                                    listall.append(baojia)
        #                print listall

                    js=0
                    listall2=[]
                    for list in listall:
                        js=js+1
                        if 'HDPE' in title:
                            if js>50 and js<281:
                                if js in continue_list:
                                    continue
    #                            print list
                                listall2.append(list)
                        if 'PMMA' in title:
                            if js>44 and js<174:
                                if js in continue_list:
                                    continue
    #                            print list
                                listall2.append(list)
                        if 'PET' in title:
                            if js>40 and js<261:
                                if js in continue_list:
                                    continue
    #                            print list
                                listall2.append(list)
                        if 'LDPE' in title:
                            if js>40 and js<261:
    #                            if js in continue_list:
    #                                continue
                                print list
                                listall2.append(list)
                        
                    js2=0
                    listall3=[]
                    for list2 in listall2:
                        js2=js2+1
                        if js2%2==0:
                            list2=str(list2)+','
                        else:
                            list2=str(list2)
                        listall3.append(list2)
                    listall4='-'.join(listall3)
                    listall5=listall4.split(',')
                    js5=0
                    listall6=[]
                    for list5 in listall5:
                        js5=js5+1
                        if '-'==list5[:1]:
                            list5=list5[1:]
                        if js5%4==0:
                            list5=str(list5)+','
                        else:
                            list5=str(list5)
                        listall6.append(list5)
                    
                    listall7='|'.join(listall6)[:-2]
                    listall8=listall7.split(',')
                    
                    listall9=[]
                    
                    alltable=type+' <table border=1>'
                    js8=0
                    for list8 in listall8:
                        js8=js8+1
                        if '|'==list8[:1]:
                            list8=list8[1:]
                        
                        if 'HDPE' in title and js8==3:
                            list8=list8.replace('|','</td><td rowspan="2">')    
                            list8='<tr><td rowspan="2">'+list8+'</td></tr><tr></tr>'
                        else:
                            list8='<tr><td>'+list8+'</td></tr>'
                            list8=list8.replace('|','</td><td>')    
                        alltable=alltable+list8
                    alltable=alltable+'</table>'
                    return alltable
                else:
                    html_area=get_url_content(a_url)
                    list=gettablelist1(html_area)
                    content=getpricetable2(list['content'],list['trow'])
                    content=getpricetable3(content,type)
                    return content