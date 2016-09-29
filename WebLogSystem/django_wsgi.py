#!/usr/bin/python3
# coding: utf-8
import os
import sys
import importlib
# ??ϵͳ?ı???????ΪUTF8
importlib.reload(sys)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebLogSystem.settings")
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()