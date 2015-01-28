# -*-coding: utf-8 -*-
'''
Created on 2015年1月21日

@author: jin
'''
import hashlib
from apps.coupon.coupon_settings import BUSINESS_VERFY
from apps.coupon.models import Settings, CouponsUser, Coupons, WinCoupons
import random
import string
def md5_encrypt(s):
    hash = hashlib.md5()
    hash.update(s)
    return hash.hexdigest()
def verfy_business_password(password,verfypassword):
    if password==verfypassword:
        return True
    else:
        return False
    
    
def encrypt(s,key=15, ):   
    b = bytearray(str(s).encode("gbk"))   
    n = len(b) # 求出 b 的字节数   
    c = bytearray(n*2)   
    j = 0   
    for i in range(0, n):   
        b1 = b[i]   
        b2 = b1 ^ key # b1 = b2^ key   
        c1 = b2 % 16   
        c2 = b2 // 16 # b2 = c2*16 + c1   
        c1 = c1 + 65   
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码   
        c[j] = c1   
        c[j+1] = c2   
        j = j+2   
    return c.decode("gbk")  
 
def decrypt( s,key=15,):   
    c = bytearray(str(s).encode("gbk"))   
    n = len(c) # 计算 b 的字节数   
    if n % 2 != 0 :   
        return ""   
    n = n // 2   
    b = bytearray(n)   
    j = 0   
    for i in range(0, n):   
        c1 = c[j]   
        c2 = c[j+1]   
        j = j+2   
        c1 = c1 - 65   
        c2 = c2 - 65   
        b2 = c2*16 + c1   
        b1 = b2^ key   
        b[i]= b1   
    try:   
        return b.decode("gbk")   
    except:   
        return False  
    


'''
获得优惠券
'''
def get_coupons():
    price=1
    CouponsList=Coupons.objects.all()
    number=random.randint(1,100)
    if number<=40:
        price=CouponsList[0].price
    elif 40<number<=70:    
        price=CouponsList[1].price
    elif 70<number<=90:    
        price=CouponsList[2].price  
    elif 90<number<=100:    
        price=CouponsList[3].price
    return  price  

'''
生成二维码
'''
def build_code():
    while True:
        code=random_str()
        if not WinCoupons.objects.filter(verif_code=code).exists():
            return code
    
def random_str(randomlength=10):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

'''
发送邮件
'''
def send_email(email):
    email_message=u'由于您推荐的好友在本店消费，您获得了一次奇味香锅代金券的抽奖机会，具体使用方法请到店里用餐时咨询.' 
    try :
       from django.core.mail import send_mail
       from qiwei_shop.settings import DEFAULT_FROM_EMAIL
       send_mail(u'恭喜你获得奇味麻辣香锅抽奖机会', email_message,DEFAULT_FROM_EMAIL,[email,]) 
    except Exception as e:
        raise 