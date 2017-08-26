# -*- coding: utf-8 -*-  
class zzgd:
    def __init__(self):
        self.db=db
#所有工单
    def getgdlist(self,frompageCount="",limitNum="",searchlist=""):
        sqls=""
        argument=[]
        question_kind=searchlist.get("question_kind")
        if question_kind:
            sqls+="and question_kind=%s"
            argument.append(question_kind)
        compelete=searchlist.get("compelete")
        if compelete:
            sqls+="and compelete=%s"
            argument.append(compelete)
        isviewflag=searchlist.get("isviewflag")
        if isviewflag:
            sqls+="and exists(select question_id from gd_answer where question_id=gd_question.id and isview=0)"
        index=searchlist.get("index")
        if index:
            index=index
        else:
            index=1
        company_id=searchlist.get("company_id")
        if company_id:#客户登陆
            sqls+="and company_id=%s"
            argument.append(company_id)
            sqlcount="select count(0) as count from gd_question where id>0 "+sqls+""
            count=db.fetchonedb(sqlcount,argument)['count']
            sqllist="select id,question,company_id,question_time,question_kind,compelete from gd_question where id>0 "+sqls+" order by id desc limit "+str(frompageCount)+","+str(limitNum)+""
            listall=db.fetchalldb(sqllist,argument)
            for list in listall:
                time=list['question_time']
                list['title']=subString(filter_tags(list['question']),200)
                list['question_time']=formattime(time,flag=2)
                sqlb="select count(0) as bcount from gd_answer where question_id=%s and isview=0"
                resultb=db.fetchonedb(sqlb,[list['id']])
                if resultb['bcount']>0:
                    list['noviewanwercount']=resultb['bcount']
            return {'count':count,'list':listall,'index':index}
    def getgddetail(self,id="",mycompany_id=''):
        if id:
            sql="select id,question,company_id,question_time,question_kind,compelete from gd_question where id=%s"
            result=db.fetchonedb(sql,[id])
            if result:
                question_time=result['question_time']
                result['question_time']=formattime(question_time,2)
                sqls="select id,company_id,answer,answer_time,isview from gd_answer where question_id=%s order by id desc"
                result_answer=db.fetchalldb(sqls,[result['id']])
                for list in result_answer:
                    list['answer_time']=formattime(list['answer_time'],2)
                    company_id=list['company_id']
                    if str(mycompany_id)==str(company_id):
                        list['postuser']='我'
                    else:
                        list['postuser']=None
                result['answerlist']=result_answer
            return result
