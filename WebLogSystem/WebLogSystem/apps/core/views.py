# Create your views here.
from json import dump,dumps
from django.views.generic.base import TemplateResponseMixin,ContextMixin,View
from django.http import HttpResponseRedirect,HttpResponse
from WebLogSystem.settings import LOGIN_URL

#用于检测模板类视图是否登录
def require_login(func):
    def login_check(view,request,*args,**kwargs):
        if(request.session.get('login',None) == None):
            return HttpResponseRedirect(LOGIN_URL)
        else:
            return func(view,request,*args,**kwargs)
    return login_check

#用于检测ajax类视图是否登录
def ajax_require_login(func):
    def login_check(view,request,*args,**kwargs):
        if(request.session.get('login',None) == None):
            ret={'errcode':-1,'msg':'尚未登录!'}
            return HttpResponse(dumps(ret,ensure_ascii=False),content_type='application/json')
        else:
            return func(view,request,*args,**kwargs)
    return login_check

class WeblogBaseView(TemplateResponseMixin, ContextMixin, View):
    @require_login
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class WeblogAjaxView(View):
    ajax_result={}

    def get_ajax_result(self,request, *args, **kwargs):
        pass

    @ajax_require_login
    def get(self, request, *args, **kwargs):
        ajax_result=self.get_ajax_result(self, request, *args, **kwargs)
        return HttpResponse(dumps(ajax_result,ensure_ascii=False),content_type='application/json')

    @ajax_require_login
    def post(self, request, *args, **kwargs):
        ajax_result=self.get_ajax_result(self, request, *args, **kwargs)
        return HttpResponse(dumps(ajax_result,ensure_ascii=False),content_type='application/json')