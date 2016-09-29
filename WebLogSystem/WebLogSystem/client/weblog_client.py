#coding:utf-8
import re,base64,sys,os,signal,re,fcntl,time,json
import urllib,http.cookiejar
from datetime import datetime,timedelta

#所需要上传日志的站点列表
SITE_LIST=('apk.hoios.com','apk.lqbzdym.com','cw.hoios.com','git.hoios.com','hwunlock.lqbzdym.com','newapi.hoios.com','newapi.lqbzdym.com','oa.hoios.com','report.lqbzdym.com','romrsync.hoios.com','wcf.hoios.com','wcf.huawei.lqbzdym.com','wcf.lqbzdym.com','wcf.ttroot.com','weblog.hoios.com','www.hoios.com','www.lqbzdym.com','www.ttroot.com','xb.hoios.com','xblock.lqbzdym.com','xb.lqbzdym.com')
#nginx运行日志路径
NGINXLOG_PATH='/usr/local/nginx/logs/'
#nginx的pid文件路径
NGINX_PIDPATH='/usr/local/nginx/logs/nginx.pid'
#过期日志文件路径
LOGFILE_PATH='/usr/local/nginx/logs/expirelogs/'
#日志文件保存格式
LOGFILENAME_FORMAT='{domainname}_{yyyymmdd}.log'
#连接服务器所需的密匙
API_KEY='9cndk438gn'
#日志上传地址
SERVER_ADDR='http://weblog.hoios.com'
#接口上传登录路径
LOGIN_PATH='/api/apilogin/'
#获取站点id路径
GET_SITEID_PATH='/api/getsiteid/'
#上传日志路径
UPLOAD_LOG_PATH='/api/uploadlog/'
#日志文件行正则表达式,groups()[0]表示ip地址,groups()[1]表示表示日，groups()[2]表示英文月，groups()[3]表示年，groups()[4]表示小时数，groups()[5]表示http访问路径，groups()[6]表示http返回代码，groups()[7]表示发送字节数
PATTERN=re.compile(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - .* \[([0-9]{1,2})\/([a-zA-Z]{3,4})\/([0-9]{4}):([0-9]{2}).*\] ".* (\/.*) .*" ([2,3,4,5][0-9]{2}) ([0-9]{1,}) (".*") (".*")')
#月份英文与数字互换字典
DICT_MONTH={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


#单实例运行
def ApplicationInstance():  
    global pidfile  
    pidfile = open(os.path.realpath(__file__), "r")  
    try:  
        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB) #创建一个排他锁,并且所被锁住其他进程不会阻塞  
    except:  
        print("another instance is running..." )
        sys.exit(1)

#程序日志处理
def writelog(content):
    logpath=sys.path[0]+'/error.log'
    f=open(logpath,'w+')
    f.write(content+'\n')
    f.close()

#分析日志文件函数，返回按年月日|时|路径|http code组成的每小时访问次数集合和以天为key的ip访问次数集合
#格式为:{'log_statistic_by_hour':{'年月日|时|路径|http code':{'vcount':123,'sendbytes':99999},},'log_statistic_by_ip':22222}
def deal_logfile(filepath):
    ret={}
    dict_by_hour={}
    dict_by_ip={}
    f=open(filepath)
    for line in f:
        m=PATTERN.match(line)
        #不匹配规则的日志行跳过
        if(not m or len(m.groups(0))!=10):
            continue
        log_ip=m.groups(0)[0]
        log_year=m.groups(0)[3]
        log_month=DICT_MONTH.get(m.groups(0)[2],'01')
        log_day=m.groups(0)[1]
        log_hour=m.groups(0)[4]
        log_path=m.groups(0)[5]
        log_code=m.groups(0)[6]
        log_send=m.groups(0)[7]
        
        key_hour=log_year+'-'+log_month+'-'+log_day+'|'+log_hour+'|'+log_path+'|'
        log_statistic_by_hour=dict_by_hour.get(key_hour,{"vcount":0,"sendbytes":0,"code20x":0,"code30x":0,"code40x":0,"code50x":0})
        log_statistic_by_hour['vcount']+=1
        log_statistic_by_hour["sendbytes"]+=int(log_send)
        if(int(log_code)>=200 and int(log_code)<=299):
            log_statistic_by_hour['code20x']+=1
        elif(int(log_code)>=300 and int(log_code)<=399):
            log_statistic_by_hour['code30x']+=1
        elif(int(log_code)>=400 and int(log_code)<=499):
            log_statistic_by_hour['code40x']+=1
        elif(int(log_code)>=500 and int(log_code)<=599):
            log_statistic_by_hour['code50x']+=1
        else:
            continue
        dict_by_hour[key_hour]=log_statistic_by_hour
        key_ip=log_year+'-'+log_month+'-'+log_day+'|'+log_ip
        ipcount=dict_by_ip.get(key_ip,0)
        ipcount+=1
        dict_by_ip[key_ip]=ipcount
    f.close()
    ret={'log_statistic_by_hour':dict_by_hour,'log_statistic_by_ip':dict_by_ip}
    return ret

#登录日志服务器
def api_login():
    ret=''
    return ret

#访问http服务器
def http_by_get(url,cookie):
    opener=urllib.request.build_opener(cookie)
    try:
        res=urllib.request.urlopen(url)
        ret=res.read().decode('utf-8')
        json_result=json.loads(ret)
        return json_result
    except Exception as e:
        return {'errcode':-1,'msg':e}

#访问http服务器
def http_by_post(url,data,cookie):
    opener=urllib.request.build_opener(cookie)
    data=urllib.parse.urlencode(data)
    req=urllib.request.Request(url,data.encode(encoding='utf-8',errors='ignore'),method='POST')
    try:
        res=urllib.request.urlopen(req)
        ret=res.read().decode('utf-8')
        json_result=json.loads(ret)
        return json_result
    except Exception as e:
        return {'errcode':-1,'msg':e}

#
def get_site_id(url,sitename,cookie):
    r=http_by_post(url,{'sitename':sitename},cookie)
    if(r['errcode']==0):
        return {'siteid':r['siteid'],'update_time':r['msg']}
    else:
        return None

#主函数
if __name__=='__main__':
    ApplicationInstance()
    now=None
    #处理运行参数
    if(len(sys.argv)>1):
        try:
            #参数+1天表示处理指定参数日期的日志
            now=datetime.strptime(sys.argv[1]+' 23:00:00','%Y-%m-%d %H:%M:%S')
            now=now+timedelta(days=1)
        except Exception as e:
            print('参数不合法')
            exit(-1)
    else:
        now=datetime.now()
    hour=now.hour
    minute=now.minute
    expire_date=datetime.strftime(now-timedelta(days=3),'%Y%m%d')
    str_yesterday=datetime.strftime(now-timedelta(days=1),'%Y%m%d')
    #每日0点分割nginx日志
    if(hour==0 or minute==0):
        for site in SITE_LIST:
            if(os.path.exists(LOGFILE_PATH+site+'_'+expire_date+'.log')):
                os.remove(LOGFILE_PATH+site+'_'+expire_date+'.log')
            else:
                logtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
                writelog("{0}\t移除文件,但未找到{1}".format(logtime,LOGFILE_PATH+site+'_'+expire_date+'.log'))
            if(os.path.exists(NGINXLOG_PATH+site+'.log')):
                os.rename(NGINXLOG_PATH+site+'.log',LOGFILE_PATH+site+'_'+str_yesterday+'.log')
            else:
                logtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
                writelog("{0}\t切割文件,但未找到{1}".format(logtime,NGINXLOG_PATH+site+'.log'))
        if(os.path.exists(NGINX_PIDPATH)):
            f=open('/usr/local/nginx/logs/nginx.pid')
            nginx_pid=int(f.read())
            os.kill(nginx_pid,signal.SIGUSR1)
    
    #处理给定列表站点的日志
    for site in SITE_LIST:
        cj=http.cookiejar.CookieJar()
        cookie=urllib.request.HTTPCookieProcessor(cj)
        if(not os.path.exists(LOGFILE_PATH+site+'_'+str_yesterday+'.log')):
            logtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            writelog("{0}\t处理日志文件,但未找到{1}".format(logtime,NGINXLOG_PATH+site+'.log'))
            continue
        result_siteid=get_site_id(SERVER_ADDR+GET_SITEID_PATH+'?apikey='+API_KEY,site,cookie)
        
        if(result_siteid==None):
            logtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            writelog("{0}\t未能获取到站点id".format(logtime))
            continue
        today=time.strptime(datetime.strftime(datetime.now(),'%Y-%m-%d 00:00:00'),'%Y-%m-%d %H:%M:%S')
        last_updatetime=time.strptime(result_siteid['update_time'],'%Y-%m-%d %H:%M:%S')
        if(len(sys.argv)<=1):
            if(last_updatetime>today):
                continue
        
        log=deal_logfile(LOGFILE_PATH+site+'_'+str_yesterday+'.log')
        data=json.dumps(log,ensure_ascii=False)
        data=data.encode('utf8')
        data=base64.b64encode(data)
        r=http_by_post(SERVER_ADDR+UPLOAD_LOG_PATH+'?apikey='+API_KEY,{'log':data,'siteid':result_siteid['siteid']},cookie)
        if(r['errcode']!=0):
            logtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            writelog("{0}\t处理站点{1}日志失败,原因:{2}".format(logtime,site,r['msg']))