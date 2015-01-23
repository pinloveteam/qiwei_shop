import os
import sys
import django.core.handlers.wsgi

sys.path.append(r'E:/eclipse_64/code/qiwei_shop')
os.environ['DJANGO_SETTINGS_MODULE'] = 'qiwei_shop.settings'
application = django.core.handlers.wsgi.WSGIHandler()