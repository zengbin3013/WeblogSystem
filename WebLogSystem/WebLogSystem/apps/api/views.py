# Create your views here.
import sys,base64,json
from datetime import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from WebLogSystem.apps.api.models import api
from WebLogSystem.apps.core.models import Log_by_hour,Log_by_ip,Site
from json import dump,dumps

#用于检测api是否登录
def decorator_apilogin_view(func):
    def login_check(view,request,*args,**kwargs):
        if(request.session.get('apilogin',0)==1):
            return func(view,request,*args,**kwargs)
        request_key=request.GET.get('apikey','')
        if(api.objects.filter(key=request_key)):
            request.session['apilogin']=1
            return func(view,request,*args,**kwargs)
        else:
            ret={'errcode':-1,'msg':'登录信息不正确'}
            return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')
    return login_check

class Index(View):
    def get(self,request,*args,**kwargs):
        a=''
        while(True):
            a+='a'*1024*1024
            print(sys.getsizeof(a)/1024/1024)
        myapi=api()
        myapi.name='zengbin'
        myapi.key='abc'
        myapi.save()
        return HttpResponse('hello,world')

#返回apilogin登录结果
class ApiLogin(View):
    @decorator_apilogin_view
    def get(self,request,*args,**kwargs):
        ret={'errcode':0,'msg':'ok'}
        return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')

#获取站点id
class GetSiteId(View):
    
    @decorator_apilogin_view
    def post(self,request,*args,**kwargs):
        try:
            site_name=request.POST.get('sitename')
            site=None
            try:
                site=Site.objects.get(name=site_name)
            except Exception as e:
                pass
            if(site == None):
                site=Site(name=site_name);
                site.token=site_name.replace('.',' ')+' '+site_name
                site.save()
            ret={'errcode':0,'msg':datetime.strftime(site.utime,'%Y-%m-%d %H:%M:%S'),'siteid':site.id}
        except Exception as e:
            ret={'errcode':-1,'msg':e}
        return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')

#上传日志
class UploadLog(View):
    @decorator_apilogin_view
    def post(self,request,*args,**kwargs):
        try:
            data=request.POST.get('log')
            siteid=request.POST.get('siteid')
            data=base64.b64decode(data).decode()
            log=json.loads(data)
            log_by_hour=log['log_statistic_by_hour']
            log_by_ip=log['log_statistic_by_ip']
            queryset_log_by_hour=[]
            for k in log_by_hour:
                arr_s=k.split('|')
                udate=arr_s[0]
                hour=arr_s[1]
                path=arr_s[2]
                vcount=log_by_hour[k]['vcount']
                sendbytes=log_by_hour[k]['sendbytes']
                code20x=log_by_hour[k]['code20x']
                code30x=log_by_hour[k]['code30x']
                code40x=log_by_hour[k]['code40x']
                code50x=log_by_hour[k]['code50x']
                queryset_log_by_hour.append(Log_by_hour(siteid=siteid,vcount=vcount,path=path,sendbytes=sendbytes,code20x=code20x,code30x=code30x,code40x=code40x,code50x=code50x,udate=datetime.strptime(udate,'%Y-%m-%d').date(),hour=hour))
                if(len(queryset_log_by_hour)>=50):
                    Log_by_hour.objects.bulk_create(queryset_log_by_hour)
                    queryset_log_by_hour=[]
            Log_by_hour.objects.bulk_create(queryset_log_by_hour)
            queryset_log_by_ip=[]
            for k in log_by_ip:
                arr_s=k.split('|')
                udate=arr_s[0]
                ipaddr=arr_s[1]
                vcount=log_by_ip[k]
                queryset_log_by_ip.append(Log_by_ip(siteid=siteid,vcount=vcount,ipaddr=ipaddr,udate=udate))
                if(len(queryset_log_by_ip)>=50):
                    Log_by_ip.objects.bulk_create(queryset_log_by_ip)
                    queryset_log_by_ip=[]
            Log_by_ip.objects.bulk_create(queryset_log_by_ip)
            site=Site.objects.get(id=siteid)
            site.utime=datetime.now()
            site.save()
            ret={'errcode':0,'msg':'ok'}
        except Exception as e:
            ret={'errcode':-1,'msg':str(e)}
        return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')