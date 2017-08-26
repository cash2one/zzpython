import settings,sys,os
from django.shortcuts import render_to_response
from django.http import HttpResponse
reload(sys)
sys.setdefaultencoding('UTF-8')
def default(request,path):
    #return HttpResponse(locals())
    #os.path.join(os.path.dirname(__file__), 'templates')
    if ".html" not in path:
        path=path+"/index.html"
    return render_to_response(path,locals())