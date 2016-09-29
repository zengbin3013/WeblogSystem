#coding:utf-8
import sys,base64,json,time
from datetime import datetime,date
from datetime import timedelta
from django.db.models import Sum,Count
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from WebLogSystem.apps.api.models import api
from WebLogSystem.apps.core.models import Log_by_hour,Log_by_ip,Site,User
from json import dump,dumps
from django.views.generic.base import TemplateView
from WebLogSystem.apps.core.views import WeblogBaseView,WeblogAjaxView

class LoginView(TemplateView):
    template_name="admin/login.html"
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if(self.request.session.get('login',None) != None):
            return HttpResponseRedirect('/admin/index')
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

class AjaxLoginView(View):
    def post(self,request,*args,**kwargs):
        ret={"errcode":0,"msg":"ok"}
        username=request.POST.get('username',None);
        passwd=request.POST.get('passwd',None);
        if(User.objects.filter(username=username,passwd=passwd).count()>0):
            request.session['login']={'username':username}
        else:
            ret={'errcode':-1,'msg':'用户名或者密码不正确!'}
        return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')

class IndexView(WeblogBaseView):
    template_name="admin/index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sitelist']=Site.objects.all().order_by('rank','name')
        default_site=Site.objects.order_by('rank','name')[:1][0]
        context['defaultsite']=default_site
        yestoday=(datetime.now()-timedelta(days=1)).date()
        vcnt_set=Log_by_hour.objects.filter(siteid=default_site.id).filter(udate=yestoday).values('udate','hour').annotate(code20x=Sum('code20x')).annotate(code30x=Sum('code30x')).annotate(code40x=Sum('code40x')).annotate(code50x=Sum('code50x')).order_by('udate','hour')
        visit_total=[]
        visit_20x=[]
        visit_30x=[]
        visit_40x=[]
        visit_50x=[]
        for q in vcnt_set:
            timestamp=time.mktime(time.strptime(date.strftime(q['udate'],'%Y-%m-%d')+' {:02d}'.format(q['hour'])+':00:00','%Y-%m-%d %H:%M:%S'))*1000
            visit_total_child=[timestamp,q['code20x']+q['code30x']+q['code40x']+q['code50x']]
            visit_20x_child=[timestamp,q['code20x']]
            visit_30x_child=[timestamp,q['code30x']]
            visit_40x_child=[timestamp,q['code40x']]
            visit_50x_child=[timestamp,q['code50x']]
            visit_total.append(visit_total_child)
            visit_20x.append(visit_20x_child)
            visit_30x.append(visit_30x_child)
            visit_40x.append(visit_40x_child)
            visit_50x.append(visit_50x_child)
        context['visit_total']=visit_total
        context['visit_20x']=visit_20x
        context['visit_30x']=visit_30x
        context['visit_40x']=visit_40x
        context['visit_50x']=visit_50x
        context['yestoday']=datetime.strftime(datetime.now()-timedelta(days=1),'%Y-%m-%d')
        return context

class GetcodedataView(WeblogAjaxView):
    def get_ajax_result(self,request,*args,**kwargs):
        print(request)
        ret={"errcode":0,"msg":"ok"}
        sitename=self.request.POST.get('sitename')
        sdate=self.request.POST.get('sdate')
        edate=self.request.POST.get('edate')
        deltat=datetime.strptime(edate,'%Y-%m-%d')-datetime.strptime(sdate,'%Y-%m-%d')
        site=Site.objects.get(name=sitename)
        
        print(deltat.total_seconds())
        if(deltat.total_seconds()<3600*24*7):
            vcnt_set=Log_by_hour.objects.filter(siteid=site.id).filter(udate__range=(datetime.strptime(sdate,'%Y-%m-%d'),datetime.strptime(edate,'%Y-%m-%d'))).values('udate','hour').annotate(code20x=Sum('code20x')).annotate(code30x=Sum('code30x')).annotate(code40x=Sum('code40x')).annotate(code50x=Sum('code50x')).order_by('udate','hour')
            visit_total=[]
            visit_20x=[]
            visit_30x=[]
            visit_40x=[]
            visit_50x=[]
            for q in vcnt_set:
                timestamp=time.mktime(time.strptime(date.strftime(q['udate'],'%Y-%m-%d')+' {:02d}'.format(q['hour'])+':00:00','%Y-%m-%d %H:%M:%S'))*1000
                visit_total_child=[timestamp,q['code20x']+q['code30x']+q['code40x']+q['code50x']]
                visit_20x_child=[timestamp,q['code20x']]
                visit_30x_child=[timestamp,q['code30x']]
                visit_40x_child=[timestamp,q['code40x']]
                visit_50x_child=[timestamp,q['code50x']]
                visit_total.append(visit_total_child)
                visit_20x.append(visit_20x_child)
                visit_30x.append(visit_30x_child)
                visit_40x.append(visit_40x_child)
                visit_50x.append(visit_50x_child)
            ret={'errcode':0,'msg':'ok','data':{'visit_total':visit_total,'visit_20x':visit_20x,'visit_30x':visit_30x,'visit_40x':visit_40x,'visit_50x':visit_50x}}
        else:
            vcnt_set=Log_by_hour.objects.filter(siteid=site.id).filter(udate__range=(datetime.strptime(sdate,'%Y-%m-%d'),datetime.strptime(edate,'%Y-%m-%d'))).values('udate').annotate(code20x=Sum('code20x')).annotate(code30x=Sum('code30x')).annotate(code40x=Sum('code40x')).annotate(code50x=Sum('code50x')).order_by('udate')
            visit_total=[]
            visit_20x=[]
            visit_30x=[]
            visit_40x=[]
            visit_50x=[]
            for q in vcnt_set:
                timestamp=time.mktime(time.strptime(date.strftime(q['udate'],'%Y-%m-%d')+' 00:00:00','%Y-%m-%d %H:%M:%S'))*1000
                visit_total_child=[timestamp,q['code20x']+q['code30x']+q['code40x']+q['code50x']]
                visit_20x_child=[timestamp,q['code20x']]
                visit_30x_child=[timestamp,q['code30x']]
                visit_40x_child=[timestamp,q['code40x']]
                visit_50x_child=[timestamp,q['code50x']]
                visit_total.append(visit_total_child)
                visit_20x.append(visit_20x_child)
                visit_30x.append(visit_30x_child)
                visit_40x.append(visit_40x_child)
                visit_50x.append(visit_50x_child)
            ret={'errcode':0,'msg':'ok','data':{'visit_total':visit_total,'visit_20x':visit_20x,'visit_30x':visit_30x,'visit_40x':visit_40x,'visit_50x':visit_50x}}
        return ret
        #return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')