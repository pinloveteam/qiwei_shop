#-*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
 
from django.contrib import admin
from apps.coupon.models import Coupons, WinCoupons, Settings, CouponsUser
class CouponsAdmin(admin.ModelAdmin):
    list_display = [
        "price", 
    ]
    search_fields = ["price",]
 
admin.site.register(Coupons,CouponsAdmin)

class WinCouponsAdmin(admin.ModelAdmin):
    list_display = [
        "email",'verif_code' ,'time','status','number'
    ]
    search_fields = ["email",'verif_code']
 
admin.site.register(WinCoupons,WinCouponsAdmin)

class SettingsAdmin(admin.ModelAdmin):
    list_display = [
        "buiness_password", 'share_number'
    ]
 
admin.site.register(Settings,SettingsAdmin)

class CouponsUserAdmin(admin.ModelAdmin):
    list_display = [
        "email", 
    ]
    search_fields = ["email",]
 
admin.site.register(CouponsUser,CouponsUserAdmin)



# from django.conf.urls import patterns
# from django.contrib import admin
# from django.http import HttpResponse
# 
# def my_view(request):
#     return HttpResponse("Hello!")

# def get_admin_urls(urls):
#     def get_urls():
#         my_urls = patterns('',
#             (r'^my_view/$', admin.site.admin_view(my_view))
#         )
#         return my_urls + urls
#     return get_urls
# 
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls


