# -*-coding: utf-8 -*-
'''
Created on 2015年1月21日

@author: jin
'''
import logging
from django.shortcuts import render
from django.http.response import HttpResponse
from django.utils import simplejson
from apps.coupon.forms import VerfyBusinessForm
from apps.coupon.method import verfy_business_password, encrypt, md5_encrypt,\
    get_coupons
from apps.coupon.models import CouponsUser, Coupons, WinCoupons, Settings
import time
from random import randint
import random
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import datetime

'''
获取验证页面
'''
def verfy_info_page(request,template_name="index.html"):
    args={}
    try:
        return render(request,template_name,args)
    except Exception as e:
        logging.exception('获取验证页面错误')
        args={'result':'error','error_message':e.message}
        return render(request,'error.html',args)
    
'''
验证商户密码
@param email: 邮箱 
@param password:   密码
'''
@require_POST
@csrf_exempt
def verfy_business(request):
    args={}
    try:
        if request.is_ajax():
            verfyBusinessForm=VerfyBusinessForm(request.POST)
            if verfyBusinessForm.is_valid():
                couponSetings=Settings.objects.all()[0]
                if verfy_business_password(verfyBusinessForm.cleaned_data['password'],couponSetings.buiness_password):
                    email=verfyBusinessForm.cleaned_data['email']
                    if not CouponsUser.objects.filter(email=email).exists():
                        CouponsUser(email=email,number=0).save()
                    from apps.coupon.method import build_code
                    code=build_code()
                    time=datetime.datetime.now()
                    expire_time=time+datetime.timedelta(days=couponSetings.valid_time)
                    winCoupons=WinCoupons(email=email,verif_code=code,number=couponSetings.share_number,time=time,expire_time=expire_time)
                    winCoupons.save()
                    args={'result':'success','url':'%s%s%s'%('/coupon/get_coupon/',code,'/')}
                else:
                    args={'result':'error','error_message':{'password':u'密码错误!'}}
            else:
                errors=verfyBusinessForm.errors.items()
                error_message={}
                for error in errors:
                    error_message[error[0]]=error[1][0]
                args={'result':errors,'error_message':error_message}
        else:
            args={'result':'error','error_message':u'访问方式出错'}
        json=simplejson.dumps(args)
        return HttpResponse(json, mimetype='application/json')
    except Exception as e:
        logging.exception('验证商户密码错误')
        args={'result':'error','error_message':'验证商户密码错误:'+e.message}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    
'''
获取兑换码
'''    
def get_coupon(request,code,template_name="code.html"):  
    args={}
    try:
        winCoupons=WinCoupons.objects.get(verif_code=code)
        args={'code':code,'expire_time':winCoupons.expire_time.strftime('%Y年%m月%d日 %H时'),'start_time':winCoupons.time.strftime('%Y年%m月%d日 %H时')}
        return render(request,template_name,args)
    except Exception as e:
        logging.exception('获取兑换码页面错误')
        args={'result':'error','error_message':'获取兑换码页面错误:'+e.message}
        return render(request,'error.html',args)
    

'''
获取刮刮卡页面
'''    
def scratch_card_page(request,number,template_name="scratchcard.html"):
    args={}
    try:
        if number==u'1':
            args['type']='code'
        elif number==u'2':
            args['type']='email'
        else:
            args={'result':'error','error_message':'参数错误!'}
            template_name='error.html'
    except Exception as e:
        logging.exception('获取刮刮卡页面错误')
        args={'result':'error','error_message':e.message}
        template_name='error.html'
    return render(request,template_name,args)
 
'''
验证兑换码
@method: POST
@param code: 兑换码
@return: json
   result : less 没有次数
            error 错误
            success 成功
            
''' 
@require_POST
@csrf_exempt
def verfy_code(request):
    args={}
    try:
        if request.is_ajax():
            code=request.POST.get('code').rstrip()
            winCoupons=WinCoupons.objects.filter(verif_code=code)
            if len(winCoupons)>0:
                winCoupons=winCoupons[0]
            else:
                args={'result':'error','error_message':u'兑换码错误!'}
                json=simplejson.dumps(args)
                return HttpResponse(json)
            
            if winCoupons.expire_time.replace(tzinfo=None)<datetime.datetime.now():
                args={'result':'expire'}
                json=simplejson.dumps(args)
                return HttpResponse(json)
            elif winCoupons.number<=0:
                args={'result':'success','number':0}
                json=simplejson.dumps(args)
                return HttpResponse(json)
            else:
                winCoupons.number=winCoupons.number-1
            if  winCoupons.status:
                winCoupons.status=False
                couponsUser=CouponsUser.objects.get(email=winCoupons.email)
                couponsUser.number=couponsUser.number+1
                couponsUser.save()
                from apps.coupon.method import send_email
                send_email(winCoupons.email)
                #send_email()
            winCoupons.save() 
            price=get_coupons()
            args={'result':'success','number':1,'price':price}
        else:
            args={'result':'error','error_message':'请求方式错误!'}
    except Exception as e:
        logging.exception('验证兑换码错误')
        args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)


'''
获取优惠券根据邮箱
'''  
@require_POST
@csrf_exempt
def get_coupons_by_email(request):
    args={}
    try:
        if request.is_ajax():
            email=request.POST.get('email').rstrip()
            if CouponsUser.objects.filter(email=email).exists():
                couponsUser=CouponsUser.objects.get(email=email)
            else:
                args={'result':'error','error_message':'邮箱不存在!'}
                json=simplejson.dumps(args)
                return HttpResponse(json)
            number=couponsUser.number
            if number<=0:
                args={'result':'success','number':0}
            else:
                couponsUser.number=couponsUser.number-1
                couponsUser.save()
                price=get_coupons()
                args={'result':'success','number':number,'price':price}
        else:
            args={'result':'error','error_message':'请求方式错误!'}
    except Exception as e:
        logging.exception('获取刮刮卡页面错误')
        args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)









'''
查询优惠券
@param email: email
'''
def select_coupons(request,template_name='CouponList.html'):
    args={}
    try:
        email=request.POST.get('email');
        winCouponsList=WinCoupons.objects.filter(email=email)
        args['couponsList']=winCouponsList
    except Exception as e:
        logging.exception('获取刮刮卡页面错误')
        args={'result':'error','error_message':e.message}
        template_name='error.html'
    return render(request,template_name,args)
    
    
        