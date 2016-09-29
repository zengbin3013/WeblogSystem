from datetime import datetime
from django.db import models

# Create your models here.
class Site(models.Model):
    name=models.CharField(max_length=50)
    token=models.CharField(max_length=50,default='')
    utime=models.DateTimeField(default=datetime.strptime('1972-01-01 00:00:00','%Y-%m-%d %H:%M:%S'))
    rank=models.IntegerField(default=9999)

class Log_by_hour(models.Model):
    siteid=models.IntegerField()
    vcount=models.IntegerField()
    path=models.CharField(max_length=255)
    sendbytes=models.IntegerField()
    code20x=models.IntegerField()
    code30x=models.IntegerField()
    code40x=models.IntegerField()
    code50x=models.IntegerField()
    udate=models.DateField(auto_now=False)
    hour=models.IntegerField()

class Log_by_ip(models.Model):
    siteid=models.IntegerField()
    vcount=models.IntegerField()
    ipaddr=models.CharField(max_length=32)
    udate=models.DateField(auto_now=False)

class User(models.Model):
    username=models.CharField(max_length=50)
    passwd=models.CharField(max_length=50)
