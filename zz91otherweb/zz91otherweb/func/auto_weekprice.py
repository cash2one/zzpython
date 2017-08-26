#-*- coding:utf-8 -*-

#str_time=time.strftime('%m-%d',time.localtime(time.time()))
#gmt_created=getToday()
#gmt_created2=datetime.datetime.now()

def getjinshuweekprice(type,gmt_created):
    if type=='废铜':
        content1=getpricecontent('江浙沪废铜',gmt_created)
        price1=getjinshuweekprice2(content1,'光亮铜(CU>99%',3,4)
        if not price1:
            price1=getjinshuweekprice2(content1,'光亮铜(Cu>99%',3,4)
#        return price1
        
        content2=getpricecontent('广东南海废铜',gmt_created)
        price2=getjinshuweekprice2(content2,'光亮铜(CU>99%',3,4)
        if not price2:
            price2=getjinshuweekprice2(content2,'光亮铜(Cu>99%',3,4)
        
        content3=getpricecontent('天津废铜',gmt_created)
        price3=getjinshuweekprice2(content3,'光亮铜(CU>99%',3,4)
        if not price3:
            price3=getjinshuweekprice2(content3,'光亮铜(Cu>99%',3,4)
        
        content4=getpricecontent('山东临沂废铜',gmt_created)
        price4=getjinshuweekprice2(content4,'#1铜(CU97%',3,4)
        if not price4:
            price4=getjinshuweekprice2(content4,'光亮铜(Cu>99%',3,4)
        
        content5=getpricecontent('河南长葛废铜',gmt_created)
        price5=getjinshuweekprice2(content5,'#1铜(CU97%',3,4)
        if not price5:
            price5=getjinshuweekprice2(content5,'光亮铜(Cu>99%',3,4)
        
        content6=getpricecontent('湖南汨罗废铜',gmt_created)
        price6=getjinshuweekprice2(content6,'#1铜(CU97%',3,4)
        if not price6:
            price6=getjinshuweekprice2(content6,'光亮铜(Cu>99%',3,4)
        
        content7=getpricecontent('清远废铜',gmt_created)
        price7=getjinshuweekprice2(content7,'1＃光亮铜',2,3)
        
        priceall='<table border=1 cellpadding="0" cellspacing="0"><tr><td>'+price1+'</td></tr><tr><td>'+price2+'</td></tr><tr><td>'+price3+'</td></tr><tr><td>'+price4+'</td></tr><tr><td>'+price5+'</td></tr><tr><td>'+price6+'</td></tr><tr><td>'+price7+'</td></tr></table>'
        return priceall
    if type=='废铝':
        content1=getpricecontent('江浙沪废铝',gmt_created)
        price1=getjinshuweekprice2(content1,'干净割胶铝线',3,4)
        
        content2=getpricecontent('广东南海废铝',gmt_created)
        price2=getjinshuweekprice2(content2,'干净割胶铝线',3,4)
        
        content3=getpricecontent('天津废铝',gmt_created)
        price3=getjinshuweekprice2(content3,'干净割胶铝线',3,4)
        
        content4=getpricecontent('山东临沂废铝',gmt_created)
        price4=getjinshuweekprice2(content4,'干净割胶铝线',3,4)
        
        content5=getpricecontent('河南长葛废铝',gmt_created)
        price5=getjinshuweekprice2(content5,'干净割胶铝线',3,4)
        
        content6=getpricecontent('清远废铝',gmt_created)
        price6=getjinshuweekprice2(content6,'干净机件生铝',2,3)
        
        priceall='<table border=1 cellpadding="0" cellspacing="0"><tr><td>'+price1+'</td></tr><tr><td>'+price2+'</td></tr><tr><td>'+price3+'</td></tr><tr><td>'+price4+'</td></tr><tr><td>'+price5+'</td></tr><tr><td>'+price6+'</td></tr></table>'
        return priceall
    if type=='废锌和铅':
        content1=getpricecontent('江浙沪废锌和铅',gmt_created)
        price1=getjinshuweekprice2(content1,'破碎锌',3,4)
        
        content2=getpricecontent('广东南海废锌和铅',gmt_created)
        price2=getjinshuweekprice2(content2,'破碎锌',3,4)
        
        content3=getpricecontent('江浙沪废锌和铅',gmt_created)
        price3=getjinshuweekprice2(content3,'软铅皮',3,4)
        
        content4=getpricecontent('广东南海废锌和铅',gmt_created)
        price4=getjinshuweekprice2(content4,'软铅皮',3,4)
        
        content5=getpricecontent('天津废锌和铅',gmt_created)
        price5=getjinshuweekprice2(content5,'软铅皮',3,4)
        
        priceall='<table border=1 cellpadding="0" cellspacing="0"><tr><td>'+price1+'</td></tr><tr><td>'+price2+'</td></tr><tr><td>'+price3+'</td></tr><tr><td>'+price4+'</td></tr><tr><td>'+price5+'</td></tr></table>'
        return priceall
    if type=='废不锈钢':
        content1=getpricecontent('江浙沪废不锈钢',gmt_created)
        price1=getjinshuweekprice2(content1,'304一级新料',3,4)
        
        content2=getpricecontent('广东南海废不锈钢',gmt_created)
        price2=getjinshuweekprice2(content2,'304一级新料',3,4)
        
        priceall='<table border=1 cellpadding="0" cellspacing="0"><tr><td>'+price1+'</td></tr><tr><td>'+price2+'</td></tr></table>'
        return priceall
    if type=='废钢':
        ljie='</td></tr><tr><td>'
        priceall='<table border=1 cellpadding="0" cellspacing="0"><tr><td>'
        content1=getpricecontent('江浙沪地区废钢',gmt_created)
        baojialist=re.findall('[\d]+',content1)
        listall=[]
        for baojia in baojialist:
            if len(baojia)>2:
                listall.append(baojia)
        
        zhongfei=listall[0]+'-'+listall[1]+ljie+listall[2]+'-'+listall[3]+ljie+listall[4]+'-'+listall[5]+ljie
        tongfei=listall[6]+'-'+listall[7]+ljie+listall[8]+'-'+listall[9]+ljie+listall[10]+'-'+listall[11]+ljie
        
        content2=getpricecontent('广东南海废钢',gmt_created)
        baojialist2=re.findall('[\d]+',content2)
        listall2=[]
        for baojia2 in baojialist2:
            if len(baojia2)>2:
                listall2.append(baojia2)
        zhongfei+=listall2[0]+'-'+listall2[1]+ljie
        tongfei+=listall2[2]+'-'+listall2[3]+ljie
        
        content3=getpricecontent('天津废钢',gmt_created)
        baojialist3=re.findall('[\d]+',content3)
        listall3=[]
        for baojia3 in baojialist3:
            if len(baojia3)>2:
                listall3.append(baojia3)
        zhongfei+=listall3[0]+'-'+listall3[1]+ljie
        tongfei+=listall3[2]+'-'+listall3[3]+ljie
        
        content4=getpricecontent('山东临沂废钢',gmt_created)
        baojialist4=re.findall('[\d]+',content4)
        listall4=[]
        for baojia4 in baojialist4:
            if len(baojia4)>2:
                listall4.append(baojia4)
        zhongfei+=listall4[0]+'-'+listall4[1]
        tongfei+=listall4[2]+'-'+listall4[3]
        
        priceall+=zhongfei+ljie+tongfei+'</td></tr></table>'
        return priceall

def getpricecontent(type,gmt_created):
    gmt_created2=getnextdate(gmt_created)
    sql='select title,content from price where gmt_created>=%s and gmt_created<%s'
    resultlist=zzcomp.fetchalldb(sql,[gmt_created,gmt_created2])
    for result in resultlist:
        title=result[0]
        if type in title:
            content=result[1]
            content=re.sub('<a.*?>','',content)
            content=re.sub('</a>','',content)
            content=re.sub('<u>','',content)
            content=re.sub('</u>','',content)
            return title+content

def getjinshuweekprice2(content,type,num1,num2):
    if not content:
        return '0'
    arg1=getjinshuweekprice3(content,type)
#    return arg1
    listall=''
    if arg1:
        soup = BeautifulSoup(content)
        for table in soup.findAll('table'):
            i=1
            for row in table.findAll('tr'):
                j=1
                for tr in row.findAll('td'):
                    if i==arg1:
                        if j==num1 or j==num2:
                            textname=tr.text.encode("utf-8")
                            listall+=textname+'-'
                    j+=1
                i+=1
    return listall[:-1]

def getjinshuweekprice3(content,types):
    type1=''
    type2=''
    typelist=types.split('(')
    if len(typelist)==2:
        type1=typelist[0]
        type2=typelist[1]
#        return type2
    soup = BeautifulSoup(content)
    for table in soup.findAll('table'):
        i=1
        for row in table.findAll('tr'):
            j=1
            for tr in row.findAll('td'):
                textname=tr.text.encode("utf-8")
                if type1 and type2:
                    if type1 in textname and type2 in textname:
                        return i
                else:
                    if types in textname:
                        return i
                j+=1
            i+=1

    
def getweektable1(content):
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
def getweektable2(content,trow):
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
def getweektable3(content,type):
    listarg=['-','/']
    soup = BeautifulSoup(content)
    tablestr=""
#    listall=[]
    listall2='<table border=1>'
    for table in soup.findAll('table'):
        tablestr+="<table border=1>"
        i=1
        for row in table.findAll('tr'):
            tablestr+="<tr>"
            j=1
            for tr in row.findAll('td'):
                textname=tr.text.encode("utf-8")
                if (j>3 and j<6) or j==7:
                    if type=='PP':
                        if i<3 or i==25:
#                            tablestr+="<td >"
#                            tablestr+=textname
#                            tablestr+="</td>"
    #                        listall.append(textname)
                            if '-' in textname:
                                textnames=textname.split('-')
                                textnames1=textnames[0]
                                textnames2=textnames[1]
                                textname=str((int(textnames1)+int(textnames2))/2)
                            listall2=listall2+'<tr><td>'+textname+'</td></tr>'
                    elif type=='LDPE':
                        if i<2 or i==16:
                            if '-' in textname:
                                textnames=textname.split('-')
                                textnames1=textnames[0]
                                textnames2=textnames[1]
                                textname=str((int(textnames1)+int(textnames2))/2)
                            listall2=listall2+'<tr><td>'+textname+'</td></tr>'
                    elif type=='ABS':
                        if i<2 or i==7 or i==11:
                            if '-' in textname:
                                textnames=textname.split('-')
                                textnames1=textnames[0]
                                textnames2=textnames[1]
                                textname=str((int(textnames1)+int(textnames2))/2)
                            listall2=listall2+'<tr><td>'+textname+'</td></tr>'
                    elif type=='PMMA':
                        if i<3 or i==9:
                            if '-' in textname:
                                textnames=textname.split('-')
                                textnames1=textnames[0]
                                textnames2=textnames[1]
                                textname=str((int(textnames1)+int(textnames2))/2)
                            listall2=listall2+'<tr><td>'+textname+'</td></tr>'
                    elif type=='PS':
                        if i<2 or i==15:
                            if '-' in textname:
                                textnames=textname.split('-')
                                textnames1=textnames[0]
                                textnames2=textnames[1]
                                textname=str((int(textnames1)+int(textnames2))/2)
                            listall2=listall2+'<tr><td>'+textname+'</td></tr>'
                        
                j+=1
            i+=1
    listall2=listall2+'</table>'
    return listall2

def getweektable4(content,type):
    soup = BeautifulSoup(content)
    tablestr=""
    for table in soup.findAll('table'):
        tablestr+="<table border=1>"
        i=1
        for row in table.findAll('tr')[::-1]:
            tablestr+="<tr>"
            j=1
            for tr in row.findAll('td'):
                textname=tr.text.encode("utf-8")
                if j==6:
                    tablestr+="<td >"
                    tablestr+=textname
                    tablestr+="</td>"
                j+=1
            j=1
            for tr in row.findAll('td'):
                textname=tr.text.encode("utf-8")
                if j==2:
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
    
def getweekprice(type,gmt_created,page):
    re_alist='<div class="l_newsmaindetails">(.*?)<div>'
    re_list=r'<li>(.*?)</li>'
    urlone='http://baojia.feijiu.net/price-p'+page+'-cid-bjcid2.29-dqid-.html'
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
#        savetime=time.strftime('%m-%d',time.localtime(time.time()))
#        savetime='06-12'
        savetime=gmt_created
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
            if type in title.decode('utf-8'):
                if 'HDPE' in title:
                    htmls=get_url_content(a_url)
                    baojialist=re.findall('[\d]+',htmls)
                    listall=[]
                    continue_list=[]
                    passa=0
                    if 'HDPE' in title:
                        continue_list=[52,53,54,55,58,59,272,273,274,275,278,279]
#                        continue_list=[60,61,70,71,80,81,90,91,100,101,110,111,120,121,130,131,140,141,150,151,160,161,170,171,180,181,190,191,200,201,210,211,220,221,230,231,240,241,250,251,260,261,270,271,280,281,290,291]
                    if baojialist:
                        for baojia in baojialist:
                            if len(baojia)>3:
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
                    allnumb=[]
                    for list in listall:
                        js=js+1
                        if 'HDPE' in title:
                            if js>51 and js<282:
                                if js in continue_list:
#                                    continue
                                    allnumb.append(int(list))
                    numb1=str((allnumb[0]+allnumb[1])/2)
                    numb2=str((allnumb[2]+allnumb[3])/2)
                    numb3=str((allnumb[4]+allnumb[5])/2)
                    numb4=str((allnumb[6]+allnumb[7])/2)
                    numb5=str((allnumb[8]+allnumb[9])/2)
                    numb6=str((allnumb[10]+allnumb[11])/2)
                    
                    listall3='<table border=1>'+'<tr><td>'+'广东'+'</td></tr>'+'<tr><td>'+'浙江'+'</td></tr>'+'<tr><td>'+'山东'+'</td></tr>'+'<tr><td>'+numb4+'</td></tr>'+'<tr><td>'+numb5+'</td></tr>'+'<tr><td>'+numb6+'</td></tr>'+'<tr><td>'+numb1+'</td></tr>'+'<tr><td>'+numb2+'</td></tr>'+'<tr><td>'+numb3+'</td></tr>'+'</table>'
                    return listall3
                else:
                    html_area=get_url_content(a_url)
                    html_alist=get_content('<p class="l_newscon1">(.*?)</p>',html_area)
#                    list=getweektable1(html_area)
#                    content=getweektable2(list['content'],list['trow'])
                    content=getweektable3(html_alist,type)
                    return content

def getchart(type,page):
    re_alist='<table width="100%" border="0" align="center" cellpadding="1" cellspacing="1" bgcolor="#DEE0E8">(.*?)</table>'
    urlone='http://www.l-zzz.com/shiyou/sy_list.jsp?nID='+type+'&pageNum='+page
    html_area=get_url_content(urlone)
    html_alist=get_content(re_alist,html_area)
    
    list=getweektable1(html_alist)
    content=getweektable2(list['content'],list['trow'])
    content=getweektable4(content,type)
#    content=getweektable3(html_alist,type)
    return content