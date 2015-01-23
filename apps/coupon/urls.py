#-*- coding: UTF-8 -*- 
'''
Created on 2014年12月23日

@author: jin
'''
from django.conf.urls import patterns, url
urlpatterns=patterns('apps.coupon.views',
     #获取验证密码页面
     url(r'^verfy_info_page/', 'verfy_info_page'),
     #验证商家信息
     url(r'^verfy_business/', 'verfy_business'),
      #优惠券
     url(r'^get_coupon/([A-Za-z-0-9]*)/', 'get_coupon'),
     #呱呱卡页面
     url(r'^scratch_card_page/(.+)/', 'scratch_card_page'),
     #验证兑换码
     url(r'^verfy_code/', 'verfy_code'),
     #根据邮箱获取兑换码
     url(r'^get_coupons_by_email/', 'get_coupons_by_email'),
)
