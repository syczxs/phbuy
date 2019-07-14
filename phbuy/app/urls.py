from django.urls import path

from app.views import  register, index, register2, personal, shopping_cart, roots, commodity, \
    add_commoditys, pay_all, update_commodity_information, sousuo, Login

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name='register'),
    path('register2/', register2, name='register2'),
    path('index/', index, name='index'),
    path('personal/', personal, name='personal'),
    path('shopping_cart/', shopping_cart, name='shopping_cart'),
    path('roots/', roots, name='roots'),
    path('commodity/<str:ID>/', commodity, name='commodity'),
    path('add_commoditys/<str:commodity_id>/', add_commoditys, name='add_commoditys'),
    path('pay_all/<str:sum_all>/', pay_all, name='pay_all'),
    path('update_commodity_information/<str:commodity_id>/', update_commodity_information, name='update_commodity_information'),
    path('sousuo/', sousuo, name='sousuo'),

]
