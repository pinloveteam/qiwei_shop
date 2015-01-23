# -*- coding: utf-8 -*-
'''
Created on 2015年1月21日

@author: jin
'''
from django import forms
class VerfyBusinessForm(forms.Form):
    email=forms.EmailField(label='邮箱')
    password=forms.CharField(label='密码')
    