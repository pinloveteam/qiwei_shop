# -*- coding: utf-8 -*-
'''
Created on  Jan 21, 2015

@author: jin liguang
'''
from django.db import models
import datetime
from ImImagePlugin import number
class CouponsUser(models.Model):
    email=models.EmailField(verbose_name=r'邮箱',unique=True)
    number=models.IntegerField(verbose_name=r'抽奖次数',default=0)
    class Meta:
        verbose_name = u'用户信息表' 
        verbose_name_plural = u'用户信息表'
        db_table = "coupons_user"
        
class Coupons(models.Model):
    price=models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        verbose_name = u'优惠券表' 
        verbose_name_plural = u'优惠券表'
        db_table = "coupons"
        
        
class WinCoupons(models.Model):
    email=models.EmailField(verbose_name=r'邮箱',null=True)
    verif_code=models.CharField(verbose_name=r'验证码',max_length=255)
    time=models.DateTimeField(verbose_name='时间')
    status=models.BooleanField(verbose_name='状态',default=True)
    number=models.IntegerField(verbose_name=r'可分享次数',default=0)
    def save(self):
        self.time=datetime.datetime.now()
        super(WinCoupons, self).save()
    class Meta:
        verbose_name = u'获得优惠券表' 
        verbose_name_plural = u'获得优惠券表'
        db_table = "win_coupons"
    
class Settings(models.Model):
    buiness_password=models.CharField(verbose_name=r'商户密码',max_length=255)
    share_number =models.IntegerField(verbose_name=r'分享次数',)
    class Meta:
        verbose_name = u'设置表' 
        verbose_name_plural = u'设置表'
        db_table = "settings"
    

