from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from .models import Product, User, Order, Chat, Messages, Profile, OrderProduct, Address, Basket
from .forms import LoginForm
from . import views
from .views import CheckoutView, HomeView, products, login, View, ProductDetailView,  PaymentView, swapper_profile, createOrder, updateOrder, deleteOrder, swapperPage, welcome, registerPage, profileSettings, logout, orderConfirmation, CheckoutView, add_product_in_basket
from django.utils import timezone
from django.urls import reverse_lazy

app_name= 'myswapapp'

urlpatterns = [
    
    path('', HomeView.as_view(), name = 'home'),
    path('products/', views.products, name= 'products'), 
    path('swapper_profile/', views.swapper_profile, name= 'swapper_profile'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('product_detail/<slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('order_summary/', CheckoutView.as_view(), name='order_summary'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('updateOrder/<str:pk>/', views.updateOrder, name='update_order'),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('swapper_homepage/', views.swapperPage, name='swapper_homepage'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.registerPage, name='register'),
    path('profile/', views.profileSettings, name='profile'),
    path('order_confirmation/', views.orderConfirmation, name='order_confirmation'),
    #path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('add_product_in_basket/', views.add_product_in_basket, name='add_product_in_basket')


    

    
]
