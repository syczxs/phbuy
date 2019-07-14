import datetime
import json
import os
import time

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.

from django.views import View

from app.commodity_sql import add_commodity, all_commodity_all, commodity_all, update_commodity_number, \
    add_commodity_number, set_commodity_discount, add_buy_history, select_buy_history, add_look_history, \
    select_look_history, name_commodity_massage
from app.redis_sql import append_shopping_cart, get_user_shaopping_cart, delete_shopping_cart
from app.usersql import input_user, check_pwd, create_user_look_record, create_user_collection, create_user_buy_history, \
    perfecting_personal_date, get_pwd, select_all_user_by_username


def auth(request):
    data_cookie = request.COOKIES.get('cookie')
    if not data_cookie:
        data_cookies = {'name': 0, 'ID': 0}
        return data_cookies
    else:
        data_cookie = request.COOKIES.get('cookie')
        data_cookies = json.loads(data_cookie)
        print(data_cookies)
        return data_cookies

class Login(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        user_name = request.POST.get('name')
        pwd = request.POST.get('password')
        ID = select_all_user_by_username('syc')['user_id']
        try:
            if get_pwd(user_name) == pwd:
                response = redirect(index)
                dict_cookie = {'name': user_name, 'ID': ID}
                response.set_cookie('cookie', json.dumps(dict_cookie), max_age=60 * 60)
                return response
            else:
                return render(request, 'login.html', {'date': '用户名不存在或密码错误'})
        except:
            return render(request, 'login.html', {'date': '登陆失败，请输入正确的用户名，密码'})



def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        user_name = request.POST.get('name')
        pwd = request.POST.get('password')
        pwd2 = request.POST.get('password2')
        user_pic = '/static/head/moren.jpg'
        ID = str(time.time()) + user_name
        try:
            if pwd == pwd2:
                if check_pwd(user_name) == True:
                    input_user(ID, user_name, pwd, user_pic)
                    create_user_look_record(user_name)
                    create_user_collection(user_name)
                    create_user_buy_history(user_name)
                    return render(request, 'register2.html')
                if check_pwd(user_name) == False:
                    return render(request, 'register.html', {'date': '用户名已被注册'})
            else:
                return render(request, 'register.html', {'date': '两次输入密码不同'})
        except:
            return render(request, 'register.html', {'date': '注册失败，请输入正确的用户名，密码'})


def register2(request):
    if request.method == 'GET':
        return render(request, 'register2.html')
    else:
        user_name = request.POST.get('name')
        alipay = request.POST.get('alipay')
        pay_number = request.POST.get('pay_number')
        user_address = request.POST.get('user_address')
        up_file = request.FILES.get('pic')
        if user_name and alipay and pay_number and user_address:
            if up_file:
                user_pic_name = up_file.name
                file_path = os.path.join('static/book_pic', user_pic_name)
                f = open(file_path, 'wb+')
                for chunk in up_file.chunks():
                    f.write(chunk)
                f.close()
                user_pic = '/static/book_pic/' + user_pic_name
                perfecting_personal_date(alipay, pay_number, user_pic, user_address, user_name)
                return HttpResponseRedirect("/app/index")
            else:
                user_pic = '/static/head/moren.jpg'
                perfecting_personal_date(alipay, pay_number, user_pic, user_address, user_name)
                return HttpResponseRedirect("/app/index")
        else:
            date = '输入有误'
            return render(request, 'register2.html', {'date': date})


def index(request):
    all_commodity = all_commodity_all()
    return render(request, 'index.html', {'all_commodity': all_commodity})


def roots(request):
    all_commodity=all_commodity_all()
    if request.method == 'GET':
        return render(request, 'roots.html',{'all_commodity':all_commodity})
    else:
        commodity_name = request.POST.get('name')
        commodity_price = request.POST.get('price')
        commodity_introduce = request.POST.get('introduce')
        head_file = request.FILES.get('head_pic')
        commodity_type = request.POST.get('type')
        commodity_number = str(request.POST.get('number'))
        commodity_id = str(time.time()) + commodity_name
        if commodity_name and commodity_price and commodity_introduce and commodity_price and commodity_type:
            if head_file:
                head_pic_commodity = head_file.name
                file_path = os.path.join('static/commodity_head', head_pic_commodity)
                f = open(file_path, 'wb+')
                for chunk in head_file.chunks():
                    f.write(chunk)
                f.close()
                head_pic = '/static/commodity_head/' + head_pic_commodity
                add_commodity(commodity_id, commodity_name, commodity_price, commodity_type, commodity_introduce,
                              head_pic, commodity_number)
                return HttpResponseRedirect("/app/index")
            else:
                head_pic = '/static/cpmmodity_head/weijiazai.jpg'
                add_commodity(commodity_id, commodity_name, commodity_price, commodity_type, commodity_introduce,
                              head_pic, commodity_number)
                return HttpResponseRedirect("/app/index")
        else:
            date = '输入有误'
            return render(request, 'roots.html', {'date': date,'all_commodity':all_commodity})


def personal(request):
    data_cookies = auth(request)
    user_name = data_cookies['name']
    all_user_by_username = select_all_user_by_username(user_name)
    user_buy_history=select_buy_history(user_name)
    user_look_history=select_look_history(user_name)[0:4]
    return render(request, 'personal.html', {'all_user_by_username': all_user_by_username,'user_buy_history':user_buy_history,'user_look_history':user_look_history,'data_cookies':data_cookies})


def commodity(request, ID):
    data_cookies = auth(request)
    user_name = data_cookies['name']
    user_id = data_cookies['ID']
    commodity_information = commodity_all(ID)
    now = datetime.datetime.now()
    add_look_history(user_id,user_name,now,commodity_information['commodity_name'])
    if request.method == 'GET':
        return render(request, 'commodity.html', {'commodity_information': commodity_information})


def add_commoditys(request, commodity_id):
    data_cookies = auth(request)
    user_name = data_cookies['name']
    user_id = data_cookies['ID']
    commodity_number = request.POST.get('number')
    append_shopping_cart(user_id, commodity_id, commodity_number)
    return HttpResponseRedirect("/app/shopping_cart")


def shopping_cart(request):
    data_cookies = auth(request)
    user_id = data_cookies['ID']
    user_cart = get_user_shaopping_cart(user_id)
    commodity_list = []
    sum_all=0

    for i in user_cart:
        commodity_massage = commodity_all(i.decode(encoding='utf-8'))
        if commodity_massage['commodity_discount']==None:
            discount=1
        else:
            discount=float(commodity_massage['commodity_discount'])
        commodity_sum=int(user_cart[i].decode(encoding='utf-8'))*commodity_massage['commodiy_price']*discount
        sum_all=sum_all+commodity_sum
        c = {'commodity_number': user_cart[i].decode(encoding='utf-8'),
             'commodity_name': commodity_massage['commodity_name'],
             'commodity_pic': commodity_massage['commodity_head_pic'],
             'commodity_discount': commodity_massage['commodity_discount']
            , 'commodity_id': commodity_massage['commodity_id']
             , 'commodity_price': commodity_massage['commodiy_price'],
             'commodity_sum': commodity_sum}
        commodity_list.append(c)
    str_sum_all=str(sum_all)
    print(str_sum_all)
    return render(request, 'shopping_cart.html', {'commodity_list': commodity_list,'str_sum_all':str_sum_all})


def pay_all(request,sum_all):
    print(sum_all)
    data_cookies = auth(request)
    user_name=data_cookies['name']
    user_id = data_cookies['ID']
    user_cart = get_user_shaopping_cart(user_id)
    date_all=[]
    for i in user_cart:
        commodity_massage = commodity_all(i.decode(encoding='utf-8'))
        if int(user_cart[i].decode(encoding='utf-8'))>int(commodity_massage['commodity_number']):
            date=commodity_massage['commodity_name']+''
            date_all.append(date)
        else:
            new_commodity_number=int(commodity_massage['commodity_number'])-int(user_cart[i].decode(encoding='utf-8'))
            update_commodity_number(commodity_massage['commodity_id'], str(new_commodity_number))
            delete_shopping_cart(user_id)
            ID=int(time.time())
            now = datetime.datetime.now()
            add_buy_history(ID, user_name, now,commodity_massage['commodity_name'] , '未发货')
    if date_all==[]:
        warning='货物充足'
    else:
        warning=str(date_all)+'货物不足'
    return render(request,'pay_all.html',{'sum':sum_all,'warning':warning})


def update_commodity_information(request,commodity_id):
    commodity_discout = request.POST.get('discount')

    commodity_number = request.POST.get('number')
    if commodity_discout:
        commodity_discout = int(commodity_discout) / 10
        set_commodity_discount(commodity_id, commodity_discout)
    if commodity_number:
         add_commodity_number(commodity_id, commodity_number)
    return HttpResponseRedirect("/app/roots")

def sousuo(request):
    select = request.POST.get('select')
    massage=name_commodity_massage(select)
    print(massage)
    return render(request, 'sousuo.html', {'massage': massage})


